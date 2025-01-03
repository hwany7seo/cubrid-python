import os
import sys
import subprocess

major_start_date='2017-06-27'

if os.name == 'nt':
    from distutils.core import setup
    vs2017_path = os.environ.get('VS2017COMNTOOLS',
                            (r"C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\Common7\Tools"))
    os.environ['VS2017COMNTOOLS'] = vs2017_path
    os.environ['DISTUTILS_USE_SDK'] = '1'
    os.environ['MSSdk'] = '1'
    vs_link_path = r"C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.16.27023\bin\Hostx64\x64"
    os.environ['PATH'] = vs_link_path + os.pathsep + os.environ['PATH']
    include_path = r"C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\ucrt"
    os.environ['INCLUDE'] = include_path + os.pathsep + os.environ.get('INCLUDE', '')

if sys.version > '3':
    setup_file = "setup_3.py"
else:
    setup_file = "setup_2.py"

with open('VERSION', 'r') as file:
    version = file.readline().strip()

command = "git rev-list --after={0} --count HEAD | awk '{{ printf \"%04d\", $1 }}'".format(major_start_date)
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
if process.returncode == 0:
    serial_number = stdout.decode().strip()

python_version = version + "." + str(serial_number)

#os.system(setup_file)
setup_fh = open(setup_file)
setup_content = setup_fh.read()
setup_fh.close()
exec(setup_content, {'python_version':python_version, 'argv': sys.argv + ['arg1']})
