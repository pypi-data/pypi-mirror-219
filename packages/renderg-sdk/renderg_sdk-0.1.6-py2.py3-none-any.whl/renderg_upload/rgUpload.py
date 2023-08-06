import os
import subprocess
import time

from renderg_api.constants import JobStatus
from renderg_upload.assetsPathHelper import AssetsPathHelper


class RendergUpload:

    def __init__(self,api,job_id,info_path,line,spend):
        self.api = api
        self.transfer_config = api.transfer.get_transfer_config(job_id)
        self.transfer_lines = api.transfer.get_transfer_line(line)
        self.info_path = info_path
        self.job_id = job_id
        if spend is not None:
            self.spend = spend
        else:
            self.spend = 1000

    def upload(self):
        self.api.job.update_job_status(self.job_id, JobStatus.STATUS_UPLOAD)
        source_paths,dest_paths = AssetsPathHelper.get_file_list_for_info_cfg(self.info_path,self.job_id)

        host, port = self.transfer_lines
        username = self.transfer_config.get("username")
        password = self.transfer_config.get("password")

        root_dir = AssetsPathHelper.get_root_dir()
        ascp_dir = f"{root_dir}/ascp/bin/ascp.exe".replace('\\', '/')
        timestamp = time.time()

        formatted_time = time.strftime('%Y%m%d%H%M%S', time.localtime(timestamp))
        workspace = self.info_path.replace('info.cfg', '')
        filepairlist_dir = os.path.join(workspace, f'{self.job_id}_{formatted_time}.txt')
        print(filepairlist_dir)

        with open(filepairlist_dir, 'w') as f:
            for index, source in enumerate(source_paths, 0):
                dest = dest_paths[index]
                print("source:", source)
                print("dest:", dest)
                f.write(f"{source}\n")
                f.write(f"{dest}\n")

        cmd_pass = f"set ASPERA_SCP_PASS={password}"
        cmd = f'{cmd_pass}&& {ascp_dir} -P {port} -O {port} -T -l{self.spend}m --mode=send -k2 --overwrite=diff --user={username} -d --host={host} -L {workspace} --file-pair-list={filepairlist_dir} .'

        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                print(line.decode('gbk').strip())
        except Exception as e:
            print('Error:',e)