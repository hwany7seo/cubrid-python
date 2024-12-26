import os
import sys
import subprocess

major_start_date='2017-06-27'

if os.name == 'nt':
    from distutils import msvc9compiler
    msvc9compiler.VERSION = 14.0 #Visual studio 2015

if sys.version > '3':
    setup_file = "setup_3.py"
else:
    setup_file = "setup_2.py"

with open('VERSION', 'r') as file:
    version = file.readline().strip()

command = "git rev-list --after={} --count HEAD | awk '{{ printf \"%04d\", $1 }}'".format(major_start_date)
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
if process.returncode == 0:
    serial_number = stdout.decode().strip()

python_version = version + "." + str(serial_number)

#os.system(setup_file)
setup_fh = open(setup_file)
setup_content = setup_fh.read()
setup_fh.close()
exec(setup_content, {'python_version':python_version})
