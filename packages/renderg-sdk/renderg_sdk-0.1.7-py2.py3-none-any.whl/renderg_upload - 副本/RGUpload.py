import os
import subprocess
import time

from renderg_api.constants import JobStatus
from renderg_upload.AssetsPathHelper import AssetsPathHelper

import renderg_utils


class RenderGUpload:

    def __init__(self, api, job_id, info_path, line, spend, workspace=None):
        self.api = api
        self.transfer_config = api.transfer.get_transfer_config(job_id)
        self.transfer_lines = api.transfer.get_transfer_line(line)
        self.info_path = info_path
        self.job_id = job_id
        if spend is not None:
            self.spend = spend
        else:
            self.spend = 1000
        self.workspace = os.path.join(renderg_utils.get_workspace(workspace), str(self.job_id))
        if not os.path.isdir(self.workspace):
            os.makedirs(self.workspace)
        self.log_path = os.path.join(renderg_utils.get_workspace(workspace), 'log')
        if not os.path.isdir(self.log_path):
            os.makedirs(self.log_path)

    def upload(self):
        self.api.job.update_job_status(self.job_id, JobStatus.STATUS_UPLOAD)
        source_paths, dest_paths = AssetsPathHelper.get_file_list_for_info_cfg(self.info_path, self.job_id)

        host, port = self.transfer_lines
        username = self.transfer_config.get("username")
        password = self.transfer_config.get("password")

        root_dir = AssetsPathHelper.get_root_dir()
        ascp_dir = "{root_dir}/ascp/bin/ascp.exe".format(root_dir=root_dir)
        timestamp = time.time()

        formatted_time = time.strftime('%Y%m%d%H%M%S', time.localtime(timestamp))
        file_pair_list_path = os.path.join(
            self.workspace,
            '{job_id}_{formatted_time}.txt'.format(
                job_id=self.job_id,
                formatted_time=formatted_time
            )
        )

        with open(file_pair_list_path, 'w') as f:
            for index, source in enumerate(source_paths, 0):
                dest = dest_paths[index]
                print("source:", source)
                print("dest:", dest)
                f.write("{source}\n".format(source=source))
                f.write("{dest}\n".format(dest=dest))

        cmd_pass = "set ASPERA_SCP_PASS={password}".format(password=password)
        cmd = '{cmd_pass}&& ' \
              '{ascp_dir} -P {port} -O {port} -T -l{spend}m ' \
              '--mode=send -k2 --overwrite=diff --user={username} -d ' \
              '--host={host} -L {log_path} --file-pair-list={file_pair_list_path} .' \
              ''.format(
                cmd_pass=cmd_pass,
                ascp_dir=ascp_dir,
                host=host,
                port=port,
                spend=self.spend,
                username=username,
                log_path=self.log_path,
                file_pair_list_path=file_pair_list_path)
        print(cmd)
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                print(line.decode('gbk').strip())
        except Exception as e:
            print('Error:', e)
