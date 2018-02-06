# flaskblog

debian8

系统如果存在python2可能会有问题
apt install nginx python3 python3-pip python3-dev libmysqlclient-dev

pip3 install virtualenv

virtualenv -p python3 .env

source .env/bin/activate

pip install -r 'requirements.txt'

python app.py

deactivate  # 停用 virtualenv 你的命令提示符会恢复原样

前台:bootstrap3 blog

模块: flask_admin

uwsgi --socket 0.0.0.0:80 --protocol=http -w wsgi:app
uwsgi --socket 0.0.0.0:80 --protocol=http -w run:app  --thunder-lock  --enable-threads
uwsgi --ini uwsgi.ini