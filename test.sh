pip uninstall -y tsup
python setup.py install
PWDEBUG=1 python examples/botcheck.py
