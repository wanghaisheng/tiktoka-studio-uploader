from os.path import dirname, join
from sys import version_info

import setuptools

if version_info < (3, 6, 0):
    raise SystemExit("Sorry! tsup requires python 3.6.0 or later.")

with open(join(dirname(__file__), "tsup/VERSION"), "rb") as fh:
    version = fh.read().decode("ascii").strip()

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

packages = setuptools.find_packages()
packages.extend(["tsup"])


requires = [
    "better-exceptions>=0.2.2",
    "DBUtils>=2.0",
    "parsel>=1.5.2",
    "PyMySQL>=0.9.3",
    "redis>=2.10.6,<4.0.0",
    "requests>=2.22.0",
    "bs4>=0.0.1",
    "ipython>=7.14.0",
    "redis-py-cluster>=2.1.0",
    "cryptography>=3.3.2",
    "selenium>=3.141.0",
    "pymongo>=3.10.1",
    "urllib3>=1.25.8",
    "loguru>=0.5.3",
    "influxdb>=5.3.1",
    "pyperclip>=1.8.2",
    "webdriver-manager>=3.5.3",
    "terminal-layout>=2.1.3",
    "playwright",
]
setuptools.setup(
    name="tsup",
    version=version,
    author="wanghaisheng",
    author_email="admin@tiktokastudio.com",
    description="using playwright and selenium to upload and schedule publish video on social media platform like youtube,tiktok,douyin etc.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/wanghaisheng/tiktoka-studio-uploader",
    download_url="https://github.com/wanghaisheng/tiktoka-studio-uploader/tarball/version",
    # packages=["tsup", "tsup.utils", "tsup.tiktok", "tsup.db", "tsup.network"],
    packages=packages,
    # so we emit to hard code the package/sub-folder name
    include_package_data=True,
    # if not true, js folder wont included
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["playwright"],
    python_requires=">=3.6",
)
