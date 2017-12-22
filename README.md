# flaskblog

virtualenv -p python3 .env_py3

source .env_py3/bin/activate

pip install -r 'requirements.txt'

python app.py

deactivate  # 停用 virtualenv 你的命令提示符会恢复原样