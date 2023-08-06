import os
import json
import re


class AsperaTransferHelper:

    @staticmethod
    def is_unc_path(path):
        upc_match = re.search(r'/?/?'
                              r'(((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3})'  # ip
                              r'|'
                              r'([a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?)'  # 域名
                              r'/.+', path)
        if upc_match:
            return True
        return False

    @staticmethod
    def read_json(file_path):
        encoding_list = ['utf-8-sig', 'utf-8', 'None', 'gb2312']
        for encoding in encoding_list:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    info_json = json.loads(f.read())
                return info_json
            except BaseException as e:
                print(e)
        return {}

    @staticmethod
    def handing_local_paths(paths):
        """

        Args:
            path: 本地文件路径

        Returns:
            规范路径后的本地文件路径
        """
        if isinstance(paths, list):
            for path in paths:
                norma_path = os.path.normpath(path)
                norma_path.replace('\\', '/')
            return paths
        else:
            norma_path = os.path.normpath(paths)
            return norma_path.replace('\\', '/')