# opplast
[![Version](https://img.shields.io/pypi/v/opplast.svg)](https://pypi.org/project/opplast)
[![License](https://img.shields.io/github/license/offish/opplast.svg)](https://github.com/offish/opplast/blob/master/LICENSE)
[![Stars](https://img.shields.io/github/stars/offish/opplast.svg)](https://github.com/offish/opplast/stargazers)
[![Issues](https://img.shields.io/github/issues/offish/opplast.svg)](https://github.com/offish/opplast/issues)
[![Size](https://img.shields.io/github/repo-size/offish/opplast.svg)](https://github.com/offish/opplast)
[![Discord](https://img.shields.io/discord/467040686982692865?color=7289da&label=Discord&logo=discord)](https://discord.gg/t8nHSvA)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Donate Steam](https://img.shields.io/badge/donate-steam-green.svg)](https://steamcommunity.com/tradeoffer/new/?partner=293059984&token=0-l_idZR)
[![Donate PayPal](https://img.shields.io/badge/donate-paypal-blue.svg)](https://www.paypal.me/0ffish)

Upload videos to YouTube using geckodriver, Firefox profiles and Selenium. Easy to setup and use. Inspired by [youtube_uploader_selenium](https://github.com/linouk23/youtube_uploader_selenium).

"Opplast" is norwegian for "upload".

## Installing
Install and update using pip:

```
pip install --upgrade opplast
```

## geckodriver
Download [geckodriver](https://github.com/mozilla/geckodriver/releases) and place it inside `C:\Users\USERNAME\AppData\Local\Programs\Python\Python37`. If you are using another version of Python, you place it inside there. This only works if Python is added to PATH and it is the correct version.

You can check if geckodriver has been added to PATH by running `geckodriver --version` in the terminal. If this gives you an error or you are running into:
### selenium.common.exceptions.WebDriverException: Message: 'geckodriver' executable needs to be in PATH.
Specify `executable_path` in the [Configuration](https://github.com/offish/opplast#configuration) part.

## Configuration
Open Firefox, and go to `about:profiles`. Click "Create a New profile" and name it "Selenium" or whatever. Copy the "Root Directory" path of the new profile. This is your `root_profile_directory`. Now you can "Launch profile in new browser", go to [YouTube](https://youtube.com), and login to the account you want to upload with.

It's highly recommended that you clear your standard upload settings on YouTube.

```python
Upload(root_profile_directory: str, executable_path: str = "geckodriver", timeout: int = 3, headless: bool = True, debug: bool = True) -> None
```
`root_profile_directory: str` -  path to Firefox profile where you're logged into YouTube.

`executable_path: str` - full path to override which geckodriver binary to use for Firefox 47.0.1 and greater, which defaults to picking up the binary from the system path. Example: `r"C:/Users/USERNAME/Desktop/geckodriver"` (if geckodriver.exe is located in Desktop folder) Default: `geckodriver`.

`timeout: int` - seconds Selenium should wait, when getting pages and inserting data. Default: `3`.

`headless: bool` - whether or not you want to see the browser GUI. Default: `True` (hidden).

`debug: bool` - whether or not you want to see the debug info. Default: `True` (shown).


## Usage
```python
from opplast import Upload


upload = Upload(
    # use r"" for paths, this will not give formatting errors e.g. "\n"
    r"C:/Users/USERNAME/AppData/Roaming/Mozilla/Firefox/Profiles/r4Nd0m.selenium",
)

was_uploaded, video_id = upload.upload(
    r"C:/path/to/video.mp4",
    title="My YouTube Title",
    description="My YouTube Description",
    thumbnail=r"C:/path/to/thumbnail.jpg",
    tags=["these", "are", "my", "tags"],
)

if was_uploaded:
    print(f"{video_id} has been uploaded to YouTube")

upload.close()
```

## License
MIT License

Copyright (c) 2021 [offish](https://offi.sh)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
