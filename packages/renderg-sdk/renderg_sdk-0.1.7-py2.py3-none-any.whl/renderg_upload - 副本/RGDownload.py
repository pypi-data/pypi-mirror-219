import json
import os
import subprocess
import time

from renderg_upload.AssetsPathHelper import AssetsPathHelper
import renderg_utils
from renderg_upload.mqttSubscriber import MqttClient


class RenderGDownload:

    def __init__(self,api,job_id,download_path,line,cluster_id,spend,workspace=None):
        self.api = api
        if job_id is not None:
            self.transfer_config = api.transfer.get_transfer_config(job_id)
            self.user_id = self.transfer_config.get('username').split('_')[2]
        else:
            self.transfer_config = api.transfer.get_transfer_cluster(cluster_id)[0]
            self.user_id = self.transfer_config.get('username').split('_')[2]
        print(self.user_id)
        self.transfer_lines = api.transfer.get_transfer_line(line)
        self.download_path = download_path
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
        auth_key = self.api.mqConnect.get_key()
        self.mqtt_client = MqttClient(f'{self.user_id}_sdk', auth_key)
        self.jobEnd_list = []

    def mq_callback(self,result):
        print("Received message: " + result)
        payload = json.loads(result)
        if payload.get('type_id') == '030003':
            data = payload.get('data')
            job_id = data.get('job_id')
            self.jobEnd_list.append(str(job_id))

    def download(self):
        job_info = self.api.job.get_jobs_info(self.job_id)
        status = job_info.get('Status')
        status = 1111
        if 'Completed' != status:
            # 任务未完成，监听mqtt状态，等待完成
            self.mqtt_client.subscribe(f'mqtt/front/user/{self.user_id}/{self.job_id}', self.mq_callback)
            while True:
                print(f"监听任务{self.job_id}")
                if str(self.job_id) in self.jobEnd_list:
                    print("MQTT:渲染完成")
                    self.mqtt_client.unsubscribe(f'mqtt/front/user/{self.user_id}/{self.job_id}')
                    break
                time.sleep(3)

        host, port = self.transfer_lines
        username = self.transfer_config.get("output_username")
        password = self.transfer_config.get("password")

        root_dir = AssetsPathHelper.get_root_dir()
        ascp_dir = f"{root_dir}/ascp/bin/ascp.exe".replace('\\', '/')
        timestamp = time.time()

        formatted_time = time.strftime('%Y%m%d%H%M%S', time.localtime(timestamp))
        filepairlist_dir = os.path.join(self.workspace, f'{self.job_id}_{formatted_time}.txt')

        # 下载：
        cmd_pass = f"set ASPERA_SCP_PASS={password}"
        files_source_path = f'./{self.job_id}/'
        files_dest_path = self.download_path
        cmd = f'{cmd_pass}&& {ascp_dir} -P {port} -O {port} -T -l{self.spend}m --mode=recv -k2 --overwrite=diff --user={username} -d --host={host} -L {self.log_path} {files_source_path} {files_dest_path}'
        RendergDownload.process_cmd(cmd)
        return "success"

    @staticmethod
    def process_cmd(cmd):
        try:
            print(cmd)
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                print(line.decode('gbk').strip())
        except Exception as e:
            print('Error:',e)

    def custom_download(self,server_path):
        host, port = self.transfer_lines
        username = self.transfer_config.get("output_username")
        password = self.transfer_config.get("password")

        job_ids = [path.split("/")[1] for path in server_path] # 取出所有任务号
        for job_id in job_ids:
            job_info = self.api.job.get_jobs_info(job_id)
            status = job_info.get('Status')
            if 'Completed' != status:
                # 任务未完成，监听mqtt状态，等待完成
                self.mqtt_client.subscribe(f'mqtt/front/user/{self.user_id}/{job_id}', self.mq_callback)
            else:
                self.jobEnd_list.append(str(job_id))
        while True:
            print(f"监听任务{job_ids}")
            if set(job_ids) == set(self.jobEnd_list):
                print("MQTT:渲染完成")
                for job_id in job_ids:
                    self.mqtt_client.unsubscribe(f'mqtt/front/user/{self.user_id}/{job_id}')
                break
            time.sleep(3)

        root_dir = AssetsPathHelper.get_root_dir()
        ascp_dir = f"{root_dir}/ascp/bin/ascp.exe".replace('\\', '/')
        timestamp = time.time()
        formatted_time = time.strftime('%Y%m%d%H%M%S', time.localtime(timestamp))
        filepairlist_dir = os.path.join(self.workspace, f'custom_{formatted_time}.txt')

        with open(filepairlist_dir, 'w') as f:
            for source in server_path:
                dest = f'{self.download_path}/{source}'
                print("source:", source)
                print("dest:", dest)
                f.write(f"{source}\n")
                f.write(f"{dest}\n")

        # 下载：
        cmd_pass = f"set ASPERA_SCP_PASS={password}"
        cmd = f'{cmd_pass}&& {ascp_dir} -P {port} -O {port} -T -l{self.spend}m --mode=recv -k2 --overwrite=diff --user={username} -d --host={host} -L {self.log_path} --file-pair-list={filepairlist_dir} .'
        RendergDownload.process_cmd(cmd)