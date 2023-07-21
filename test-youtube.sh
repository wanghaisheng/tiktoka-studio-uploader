pip uninstall -y tsup
pip install -i https://pypi.mirrors.ustc.edu.cn/simple/ -r requirements.txt
python setup.py install
PWDEBUG=0 HOME=/root python examples/onefile-example_youtube.py
