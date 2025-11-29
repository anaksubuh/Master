
@echo off
chcp 65001 >nul
echo Membuat requirements.txt...
pip freeze > requirements.txt
echo requirements.txt berhasil dibuat!
dir requirements.txt
pause