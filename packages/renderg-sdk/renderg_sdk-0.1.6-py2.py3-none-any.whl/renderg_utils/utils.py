import codecs
import json
import os
import subprocess
import sys

PY_VERSION = sys.version_info[0]


def get_workspace(workspace):
    if workspace and os.path.isabs(workspace):
        return workspace
    else:
        return os.path.join(os.getenv("USERPROFILE"), "RenderG_WorkSpace")


def read_json(json_path, encoding='utf-8'):
    if os.path.exists(json_path):
        with codecs.open(json_path, 'r', encoding=encoding) as f:
            data = json.load(f)
        return data


def write_json(file_path, data, encoding="utf-8", ensure_ascii=True):
    with codecs.open(file_path, 'w', encoding=encoding) as f:
        if PY_VERSION == 3:
            json.dump(data, f, ensure_ascii=ensure_ascii, indent=4)
        else:
            f.write(str(json.dumps(data, ensure_ascii=ensure_ascii, indent=4)))


def run_cmd(cmd, shell=False):
    if PY_VERSION == 2:
        cmd = str(cmd).encode(sys.getfilesystemencoding())

    popen = subprocess.Popen(cmd, stderr=subprocess.PIPE, shell=shell)
    popen.wait()

    return popen.returncode


def get_dcc_file_version(file_path, regex):
    version = ''

    with open(file_path, 'rb') as read_obj:
        while True:
            line = read_obj.readline()
            if not line:
                break
            try:
                line = line.decode('utf-8', 'ignore')
            except BaseException as err:
                # print(err)
                pass

            res = regex.search(line)
            if res:
                ver = res.groupdict()
                version = ver.get('version').strip()
                break
    return version


class SceneType:
    max = '3dsmax'
    maya = 'maya'
    houdini = 'houdini'
    clarisse = 'clarisse'
    c4d = 'c4d'
    katana = 'katana'
    blender = 'blender'

    @staticmethod
    def get_scene_file_type(scene_name):
        try:
            scene_type = os.path.splitext(scene_name.lower())[1]
            if scene_type in ['.ma', '.mb']:
                return SceneType.maya
            elif scene_type in ['.hip']:
                return SceneType.houdini
            elif scene_type in ['.project']:
                return SceneType.clarisse
            elif scene_type in ['.max']:
                return SceneType.max
            elif scene_type in ['.c4d']:
                return SceneType.c4d
            elif scene_type in ['.katana']:
                return SceneType.katana
            elif scene_type in ['.blend']:
                return SceneType.blender
        except Exception as e:
            print(e)
        return ''
