pip uninstall -y tsup
pip install -i https://pypi.mirrors.ustc.edu.cn/simple/ -r requirements.txt
python3 setup.py install
PWDEBUG=0 HOME=/root python3 examples/onefile-example_youtube.py
