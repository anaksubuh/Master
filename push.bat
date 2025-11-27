set tanggal=%DATE:~0,2%-%DATE:~3,2%-%DATE:~6,4%
set jam=%TIME: =0%
set jam=%jam::=_% 

git init
git add .
git commit -m "UPDATE %tanggal% %jam%"
git branch -M main
git remote add origin https://github.com/anaksubuh/Master.git
git push -u origin main
