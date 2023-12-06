pip uninstall -y upgenius
pip install -r requirements.txt
python setup.py install
playwright install  firefox

PWDEBUG=0 HOME=/root python examples/onefile-example_tiktok_sessionid.py
