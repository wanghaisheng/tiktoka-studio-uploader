pip3 uninstall -y tsup
pip3 install -i https://pypi.mirrors.ustc.edu.cn/simple/ -r requirements.txt
python -m playwright install

python3 setup.py install
python3 -m playwright install

#auto save cookie file without manually export
# python examples/save-youtube-Cookie.py
# test exported cookie file before actually use
# python examples/test-youtube-Cookie.py
#upload one file to youtube in different publish policy
PWDEBUG=0 HOME=/root python3 examples/onefile-example_youtube_windows.py
