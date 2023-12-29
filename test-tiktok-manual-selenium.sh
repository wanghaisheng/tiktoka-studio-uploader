pip uninstall -y upgenius
pip install -r requirements.txt
python setup.py install

PWDEBUG=0 HOME=/root python examples/onefile-example_tiktok_selenium.py
