pip uninstall -y upgenius
pip install -i https://pypi.mirrors.ustc.edu.cn/simple/ -r requirements.txt
python setup.py install
playwright install  firefox

PWDEBUG=0 HOME=/root python examples/onefile-example_tiktok_sessionid_proxy.py
