pip uninstall -y upgenius
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/Scripts/activate
py -m pip install -r requirements.txt
python setup.py install

PWDEBUG=0 HOME=/root python examples/onefile-example_tiktok_selenium.py
