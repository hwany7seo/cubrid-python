@echo off

echo "Execute VsDevCmd.bat"
set "VSDEV_CMD=C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\Common7\Tools\VsDevCmd.bat"
call "%VSDEV_CMD%"

echo "Execute vcvarsall.bat x64"
set "VCVARSALL_PATH=C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvarsall.bat"
call "%VCVARSALL_PATH%" x64

