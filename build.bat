::setlocal

REM #打包工具路径
set PYINSTALLER_DIR=D:/Application/pyinstaller
REM #源文件
set SOURCE_FILES=D:/pythonspace/SuperMarket/src/untitled-1.py 
REM #文件名称
set FILE_NAME=%1
REM #图标文件名称
set ICON_FILE=D:/pythonspace/SuperMarket/Cashier_128px.ico
REM #输出路径
set DIR_EXE=D:/yhbak/cashier1

REM #执行转换并输出日志
cd /D %PYINSTALLER_DIR%
python pyinstaller.py -F %SOURCE_FILES% -o %DIR_EXE% --icon=%ICON_FILE%
:: # pyinstaller -F -w mainPage.py creatDetailTable.py creatTable.py databaseOpetation.py dataManager.py dataManager.py
::Pan.bat /norep -file=%DIR_JOB%/%FILE_NAME%.ktr -level:Basic > %DIR_LOGS%/%FILE_NAME%-%date:~0,4%%date:~5,2%%date:~8,2%.log

::echo. & pause