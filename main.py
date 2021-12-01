import ctypes
import glob
import os
import subprocess


def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0


if not is_admin():
    raise Exception("Permissões elevadas obrigatórias para execução")

root = os.environ['SystemRoot']
arr = glob.glob("{}\\servicing\\Packages\\Microsoft-Windows-GroupPolicy-ClientExtensions-Package~3*.mum".format(root))
arr.extend(glob.glob("{}\\servicing\\Packages\\Microsoft-Windows-GroupPolicy-ClientTools-Package~3*.mum".format(root)))

for file in arr:
    try:
        proc = subprocess.check_call("dism /online /norestart /add-package:\"{}\"".format(file))
    except subprocess.CalledProcessError as e:
        raise Exception("Erro executando processo de ativação.", e)
