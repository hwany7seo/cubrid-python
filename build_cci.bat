@echo off
if "%VS2017COMNTOOLS%x" == "x" echo "Please add 'VS2017COMNTOOLS' in the environment variable"

echo arg is :%1%
cd cci-src\win\cas_cci

call "%VS2017COMNTOOLS%VsDevCmd.bat"
if "%1%"=="x86" (
devenv cas_cci_v141_lib.vcxproj /build "release|x86"
) else ( 
devenv cas_cci_v141_lib.vcxproj /build "release|x64"
)
cd ..\..\..
