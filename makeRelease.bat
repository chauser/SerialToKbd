pyinstaller -F SerialToKbd.py
copy /Y dist\SerialToKbd.exe .
del /Q SerialToKbd.zip
zip SerialToKbd.zip SerialToKeybd.py keyboardlayout.py LICENSE README.md SerialToKbd.exe
powershell Compress-Archive -Path SerialToKbd.py,keyboardlayout.py,LICENSE,README.md,SerialToKbd.exe,makeRelease.bat -DestinationPath SerialToKbd.zip 

