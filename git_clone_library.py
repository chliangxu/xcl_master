# 拉库自动编辑编辑器
# 批处理
# @echo off
# set Aclient_branch=Develop
# set AEngine_branch=Develop
# set Content_branch=Develop
#
# set ACLIENT_DIR=%~dp0\AClient
# set ENGINE_DIR=%~dp0\AEngine
#
# rem 拉库
# git clone git@git.code.oa.com:AGame/AClient.git -b %Aclient_branch%
# git clone git@git.code.oa.com:AGame/AEngine.git -b %AEngine_branch%
#
# cd /d %ACLIENT_DIR%\trunk\AClient
# git clone git@git.code.oa.com:AGame/AClient_Content.git Content -b %Content_branch%
#
# rem 编译编辑器
# cd /d %ENGINE_DIR%
# call .\Engine\Binaries\DotNET\GitDependencies.exe
# start /wait Engine\Extras\Redist\en-us\UE4PrereqSetup_x64.exe /quiet
# call .\Engine\Binaries\Win64\UnrealVersionSelector-Win64-Shipping.exe /register /unattended
# call .\GenerateProjectFiles.bat
#
# cd /d %ENGINE_DIR%\Engine\Build\BatchFiles
# call .\RunUAT.bat
# call .\Build.bat ShaderCompileWorker Win64 Development
# call .\Build.bat UnrealHeaderTool Win64 Development
# call .\Build.bat UnrealPak Win64 Development
#
# cd /d %ENGINE_DIR%
# call .\GenerateProjectFiles.bat
#
# cd /d %ENGINE_DIR%\Engine\Binaries\DotNET
# call .\UnrealBuildTool.exe -projectfiles -project=%ACLIENT_DIR%\trunk\AClient\AClient.uproject -game -engine -progress -Region=ROW
#
# cd /d %ENGINE_DIR%\Engine\Build\BatchFiles
# call .\Build.bat UE4Editor Win64 Development
#
# cd /d %ENGINE_DIR%\Engine\Binaries\DotNET
# call .\UnrealBuildTool.exe AClientEditor Win64 Development -DEPLOY %ACLIENT_DIR%\trunk\AClient\AClient.uproject -NoNextBuild -Region=ROW
#
#
#
# pause