import json
from tkinter import EXCEPTION
from .constants import *
from .logging import Log
from .exceptions import *
from .utils import *
import os
from .login import *
from time import sleep
from datetime import datetime, date,timedelta
import logging
from playwright.async_api import async_playwright



class YoutubeUpload:
    def __init__(
        self,
        root_profile_directory: str,
        proxy_option: str = "",
        timeout: int = 3,
        watcheveryuploadstep: bool = True,
        debug: bool = True,
        username:str ="",
        password:str ="",
        CHANNEL_COOKIES: str = "",
        ytb_cookies:str="",
        tiktok_cookies:str="",
        recordvideo:bool=False

    ) -> None:
        self.timeout = timeout
        self.log = Log(debug)
        self.username=username
        self.password=password
        self.CHANNEL_COOKIES = CHANNEL_COOKIES    
        self.root_profile_directory=root_profile_directory
        self.proxy_option=proxy_option
        self.watcheveryuploadstep=watcheveryuploadstep
        self.ytb_cookies=ytb_cookies
        self.tiktok_cookies=tiktok_cookies
        self._playwright=''
        self.browser=None
        self.context=''
        self.page=''
        self.recordvideo=recordvideo
        # self.setup()

    def send(self, element, text: str) -> None:
        element.clear()
        sleep(self.timeout)
        element.send_keys(text)
        sleep(self.timeout)

    async def click_next(self, page) -> None:
        await page.locator(NEXT_BUTTON).click()
        sleep(self.timeout)

    async def not_uploaded(self, page) -> bool:
        s=await page.locator(STATUS_CONTAINER).text_content()
        return s.find(UPLOADED) != -1

    async def upload(
        self,
        videopath: str="",
        title: str = "",
        description: str = "",
        thumbnail: str = "",
        publishpolicy: str = 0,
        # mode a:release_offset exist,publish_data exist will take date value as a starting date to schedule videos
        # mode b:release_offset not exist, publishdate exist , schedule to this specific date
        # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
        # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow
        release_offset: str = '0-1',
        publish_date: datetime = datetime(
            date.today().year,  date.today().month,  date.today().day, 10, 15),
        tags: list = [],
        closewhen100percentupload:bool =True
    ) -> Tuple[bool, Optional[str]]:
        """Uploads a video to YouTube.
        Returns if the video was uploaded and the video id.
        """
        self._playwright = await self._start_playwright()
            #     browser = p.chromium.launch()

        # proxy_option = "socks5://127.0.0.1:1080"

        headless=True
        if self.watcheveryuploadstep:
            headless=False
        print('whether run in view mode',headless)
        if self.proxy_option == "":
            print('start web page without proxy')

            browserLaunchOptionDict = {
                "headless": headless,
                # "executable_path": executable_path,
                "timeout": 300000
            }

            if not self.root_profile_directory:

                self.browser = await self._start_browser("firefox", **browserLaunchOptionDict)
                if self.recordvideo:
                    self.context = await self.browser.new_context(record_video_dir=os.getcwd()+os.sep+"screen-recording")
                else:
                    self.context = await self.browser.new_context()
            else:
                self.context = await self._start_persistent_browser(
                    "firefox", user_data_dir=self.root_profile_directory, **browserLaunchOptionDict
                )

        else:
            print('start web page with proxy')

            browserLaunchOptionDict = {
                "headless": headless,
                "proxy": {
                    "server": self.proxy_option,
                },

                # timeout <float> Maximum time in milliseconds to wait for the browser instance to start. Defaults to 30000 (30 seconds). Pass 0 to disable timeout.#
                "timeout": 300000
            }


            if not self.root_profile_directory:

                self.browser = await self._start_browser("firefox", **browserLaunchOptionDict)
                if self.recordvideo:
                    self.context = await self.browser.new_context(record_video_dir=os.getcwd()+os.sep+"screen-recording")
                else:
                    self.context = await self.browser.new_context()
            else:
                self.context = await self._start_persistent_browser(
                    "firefox", user_data_dir=self.root_profile_directory, **browserLaunchOptionDict
                )

        self.log.debug("Firefox is now running")
        page = await self.context.new_page()
        print('============tags',tags)
        if not videopath:
            raise FileNotFoundError(f'Could not find file with path: "{videopath}"')


        if self.CHANNEL_COOKIES and not self.CHANNEL_COOKIES == '':
            print('cookies existing', self.CHANNEL_COOKIES)

            await self.context.clear_cookies()

            await self.context.add_cookies(
                json.load(
                    open(
                        self.CHANNEL_COOKIES, 
                        'r'
                    )
                )
            )            
            # login_using_cookie_file(self,self.CHANNEL_COOKIES,page)         
            await page.goto(YOUTUBE_URL,timeout=300000)

            await page.reload()
        else:
            self.log.info('Please sign in and then press enter')
            # input()

            await page.goto(YOUTUBE_URL,timeout=300000)
            # Interact with login form
            await self.context.clear_cookies()
            # page.click('text=Login')
            # page.fill('input[name="login"]', USERNAME)
            # page.fill('input[name="password"]', PASSWORD)
            # page.click('text=Submit')
            sleep(USER_WAITING_TIME)
            storage = await self.context.storage_state(path=self.CHANNEL_COOKIES)

        islogin = confirm_logged_in(page)
        print('checking login status', islogin)

        if not islogin:
            print('try to load cookie files')
            await self.context.clear_cookies()

            await self.context.add_cookies(
                json.load(
                    open(
                        self.CHANNEL_COOKIES, 
                        'r'
                    )
                )
            )            

            print('success load cookie files')
            await page.goto(YOUTUBE_URL,timeout=30000)
            print('start to check login status')

            islogin = confirm_logged_in(page)

            # https://github.com/xtekky/google-login-bypass/blob/main/login.py

        print('start change locale to english')

        await set_channel_language_english(page)
        print('finish change locale to english')
        await page.goto(YOUTUBE_UPLOAD_URL,timeout=300000)
        # sleep(self.timeout)
        self.log.debug("Found YouTube upload Dialog Modal")

        self.log.debug(f'Trying to upload "{videopath}" to YouTube...')
        if os.path.exists(get_path(videopath)):
            page.locator(
                INPUT_FILE_VIDEO)
            await page.set_input_files(INPUT_FILE_VIDEO, get_path(videopath))
        else:
            if os.path.exists(videopath.encode('utf-8')):
                print('file found', videopath)
                page.locator(
                    INPUT_FILE_VIDEO)
                await page.set_input_files(INPUT_FILE_VIDEO, videopath.encode('utf-8'))
        sleep(self.timeout)
        textbox=page.locator(TEXTBOX)
    #     <h1 slot="primary-header" id="dialog-title" class="style-scope ytcp-confirmation-dialog">
    #   Verify it's you
    # </h1>
        try:
            self.log.debug(f'Trying to detect verify...')
           
            hint=await page.locator('#dialog-title').text_content()
            if "Verify it's you" in hint:

    # fix google account verify
                print('verify its you')
                # await page.click('text=Login')
                # time.sleep(60)
                # await page.locator('#confirm-button > div:nth-child(2)').click()
                await page.goto('https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26next%3Dhttps%253A%252F%252Fstudio.youtube.com%252Freauth%26feature%3Dreauth%26authuser%3D3%26pageid%3D106691143538188646876%26skip_identity_prompt%3Dtrue&hl=en&authuser=3&rart=ANgoxcd6AUvx_ynaUmq5M6nROFwTagKglTZqT8c97xb1AEzoDasGeJ14cNlvYfH1_mJsl7us_sFLNGJskNrJyjMaIE2KklrO7Q&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
                page.locator('#identifierId')
                print('input username or email')

                # <div class="rFrNMe N3Hzgf jjwyfe QBQrY zKHdkd sdJrJc Tyc9J" jscontroller="pxq3x" jsaction="clickonly:KjsqPd; focus:Jt1EX; blur:fpfTEe; input:Lg5SV" jsshadow="" jsname="Vsb5Ub"><div class="aCsJod oJeWuf"><div class="aXBtI Wic03c"><div class="Xb9hP"><input type="email" class="whsOnd zHQkBf" jsname="YPqjbf" autocomplete="username" spellcheck="false" tabindex="0" aria-label="Email or phone" name="identifier" autocapitalize="none" id="identifierId" dir="ltr" data-initial-dir="ltr" data-initial-value=""><div jsname="YRMmle" class="AxOyFc snByac" aria-hidden="true">Email or phone</div></div><div class="i9lrp mIZh1c"></div><div jsname="XmnwAc" class="OabDMe cXrdqd Y2Zypf"></div></div></div><div class="LXRPh"><div jsname="ty6ygf" class="ovnfwe Is7Fhb"></div><div jsname="B34EJ" class="dEOOab RxsGPe" aria-atomic="true" aria-live="assertive"></div></div></div>

                await page.fill('input[name="identifier"]', self.username)

                await page.locator('.VfPpkd-LgbsSe-OWXEXe-k8QpJ > span:nth-child(4)').click()
                time.sleep(10)

                await page.fill('input[name="password"]', self.password)
                time.sleep(10)

                await page.locator('.VfPpkd-LgbsSe-OWXEXe-k8QpJ > span:nth-child(4)').click()
                # await page.click('text=Submit')

                Stephint=await page.locator('.bCAAsb > form:nth-child(1) > span:nth-child(1) > section:nth-child(1) > header:nth-child(1) > div:nth-child(1)').text_content()
                print(Stephint)
                if "2-Step Verification" in Stephint:            
    # <div class="L9iFZc" role="presentation" jsname="NjaE2c"><h2 class="kV95Wc TrZEUc"><span jsslot="" jsname="Ud7fr">2-Step Verification</span></h2><div class="yMb59d" jsname="HSrbLb" aria-hidden="true"></div></div>            
                # <span jsslot="" jsname="Ud7fr">2-Step Verification</span>
                    print('you need google auth and sms very code')
                    time.sleep(60)
                # await page.locator('#confirm-button > div:nth-child(2)').click()
                    await page.goto(YOUTUBE_UPLOAD_URL)
        except:
            print('there is no verification at all')
        #confirm-button > div:nth-child(2)
        # # Catch max uploads/day limit errors
        # if page.get_attribute(NEXT_BUTTON, 'hidden') == 'true':
        #     error_short_by_xpath=page.locator(ERROR_SHORT_XPATH)
        #     # print(f"ERROR: {error_short_by_xpath.text} {self.cookie_working_dir}")
        #     return False

        # await page.waitForXPath('//*[contains(text(),"Daily upload limit reached")]', { timeout: 15000 }).then(() => {
        #     console.log("Daily upload limit reached.");
        #     browser.close();
        # }).catch(() => {});


        hint=await page.locator('#error-short style-scope ytcp-uploads-dialog').text_content()
        if 'Daily upload limit reached' in hint:
        # try:
# <div class="error-short style-scope ytcp-uploads-dialog">Daily upload limit reached</div>

            # daylimit=await self.page.is_visible(ERROR_SHORT_XPATH)
            self.close()
                
            print('catch daily limit,pls try tomorrow')
            # if daylimit:
                # self.close()
        else:
            pass



        self.log.debug(f'Trying to set "{title}" as title...')


        # get file name (default) title
        # title=title if title else page.locator(TEXTBOX).text_content()
        # print(title)
        sleep(self.timeout)
        if len(title) > TITLE_COUNTER:
            print(f"Title was not set due to exceeding the maximum allowed characters ({len(title)}/{TITLE_COUNTER})")
            title=title[:TITLE_COUNTER-1]

                # TITLE
        print('click title field to input')
        titlecontainer= page.locator(TEXTBOX)
        await titlecontainer.click()
        print('clear existing title')
        await page.keyboard.press("Backspace")
        await page.keyboard.press("Control+KeyA")
        await page.keyboard.press("Delete")
        print('filling new  title')

        await page.keyboard.type(title)

        self.log.debug(f'Trying to set "{title}" as description...')

        if description:
            if len(description) > DESCRIPTION_COUNTER:
                print(
                    f"Description was not set due to exceeding the maximum allowed characters ({len(description)}/{DESCRIPTION_COUNTER})"
                )
                description=description[:4888]

            self.log.debug(f'Trying to set "{description}" as description...')
            print('click description field to input')
            await page.locator(DESCRIPTION_CONTAINER).click()
            print('clear existing description')
            await page.keyboard.press("Backspace")
            await page.keyboard.press("Control+KeyA")
            await page.keyboard.press("Delete")
            print('filling new  description')

            await page.keyboard.type(description)


        if thumbnail:
            self.log.debug(f'Trying to set "{thumbnail}" as thumbnail...')
            if os.path.exists(get_path(thumbnail)):
                await page.locator(
                    INPUT_FILE_THUMBNAIL).set_input_files(get_path(thumbnail))
            else:
                if os.path.exists(thumbnail.encode('utf-8')):
                    print('thumbnail found', thumbnail)
                    await page.locator(INPUT_FILE_THUMBNAIL).set_input_files(
                        thumbnail.encode('utf-8'))
            sleep(self.timeout)
        try:
            self.log.debug('Trying to set video to "Not made for kids"...')
            
            kids_section=page.locator(NOT_MADE_FOR_KIDS_LABEL)
            await page.locator(NOT_MADE_FOR_KIDS_RADIO_LABEL).click()
            sleep(self.timeout)
            print('not made for kids task done')
        except:
            print('failed to set not made for kids')
        if tags is None or tags =="" or len(tags)==0:
            pass
        else:
            print('tags you give',tags)
            if type(tags) == list:
                tags=",".join(str(tag) for tag in tags)
                tags=tags[:500]
            else:
                tags=tags
            print('overwrite prefined channel tags',tags)
            if len(tags) > TAGS_COUNTER:
                print(f"Tags were not set due to exceeding the maximum allowed characters ({len(tags)}/{TAGS_COUNTER})")
                tags=tags[:TAGS_COUNTER]
            print('click show more button')
            sleep(self.timeout)
            await page.locator(MORE_OPTIONS_CONTAINER).click()

            self.log.debug(f'Trying to set "{tags}" as tags...')
            await page.locator(TAGS_CONTAINER).locator(TEXT_INPUT).click()
            print('clear existing tags')
            await page.keyboard.press("Backspace")
            await page.keyboard.press("Control+KeyA")
            await page.keyboard.press("Delete")
            print('filling new  tags')
            await page.keyboard.type(tags)

# Language and captions certification
# Recording date and location
# Shorts sampling
# Category
        if closewhen100percentupload==False:
            pass
        else:
            await wait_for_processing(page,process=False)
            print('uploading progress check task done')
        # if "complete" in page.locator(".progress-label").text_content():

        # sometimes you have 4 tabs instead of 3
        # this handles both cases
        for _ in range(3):
            try:
                await self.click_next(page)
                print('next next!')
            except:
                pass
        if not int(publishpolicy) in [0, 1, 2]:
            publishpolicy=0
        if int(publishpolicy) == 0:
            self.log.debug("Trying to set video visibility to private...")

            public_main_button=page.locator(PRIVATE_BUTTON)
            await page.locator(PRIVATE_RADIO_LABEL).click()
        elif int(publishpolicy) == 1:
            self.log.debug("Trying to set video visibility to public...")

            public_main_button=page.locator(PUBLIC_BUTTON)
            await page.locator(PUBLIC_RADIO_LABEL).click()
        else:
        # mode a:release_offset exist,publish_data exist will take date value as a starting date to schedule videos
        # mode b:release_offset not exist, publishdate exist , schedule to this specific date
        # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
        # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow            
            print('date',type(publish_date),publish_date)
            if type(publish_date)==str:
                publish_date=datetime.fromisoformat(publish_date)
            if release_offset and not release_offset == "0-1":
                    print('mode a sta',release_offset)
                    if not int(release_offset.split('-')[0]) == 0:
                        offset = timedelta(months=int(release_offset.split(
                            '-')[0]), days=int(release_offset.split('-')[-1]))
                    else:
                        offset = timedelta(days=1)
                    if publish_date is None:
                        publish_date =datetime(
                            date.today().year,  date.today().month,  date.today().day, 10, 15)
                    else:
                        publish_date += offset
                
            else:
                if publish_date is None:
                    publish_date =datetime(
                        date.today().year,  date.today().month,  date.today().day, 10, 15)
                    offset = timedelta(days=1)  
                else:
                    publish_date = publish_date
                # dailycount=4

                # release_offset=str(int(start_index/30))+'-'+str(int(start_index)/int(setting['dailycount']))
                
            self.log.debug(
                f"Trying to set video schedule time...{publish_date}")

            await setscheduletime(page,publish_date)
            # set_time_cssSelector(page,publish_date)
        print('publish setting task done')
        video_id=await self.get_video_id(page)
        # option 1 to check final upload status
        if closewhen100percentupload==True:

            print('start to check whether upload is finished')
            while await self.not_uploaded(page):
                self.log.debug("Still uploading...")
                sleep(1)
        try:
            done_button=page.locator(DONE_BUTTON)

            if await done_button.get_attribute("aria-disabled") == "true":
                error_message= await page.locator(
                    ERROR_CONTAINER).text_content()
                return False, error_message

            await done_button.click()
        except:
            print('=======done buttone ')
        print('upload process is done')


   
 

        sleep(5)
        logging.info("Upload is complete")
        await self.close()
        # page.locator("#close-icon-button > tp-yt-iron-icon:nth-child(1)").click()
        # print(page.expect_popup().locator("#html-body > ytcp-uploads-still-processing-dialog:nth-child(39)"))
        # page.wait_for_selector("ytcp-dialog.ytcp-uploads-still-processing-dialog > tp-yt-paper-dialog:nth-child(1)")
        # page.locator("ytcp-button.ytcp-uploads-still-processing-dialog > div:nth-child(2)").click()
        return True, video_id

    async def get_video_id(self, page) -> Optional[str]:
        video_id=None
        try:
            video_url_container=page.locator(
                VIDEO_URL_CONTAINER)
            video_url_element=video_url_container.locator(
                VIDEO_URL_ELEMENT
            )

            video_id=await video_url_element.get_attribute(HREF)
            video_id=video_id.split("/")[-1]
        except:
            raise VideoIDError("Could not get video ID")

        return video_id

    # @staticmethod
    async  def _start_playwright(self):
        #  sync_playwright().start()
        return await  async_playwright().start()
    async def _start_browser(self, browsertype: str, **kwargs):
        if browsertype == "chromium":
            return await self._playwright.chromium.launch(**kwargs)

        if browsertype == "firefox":
            return await self._playwright.firefox.launch(**kwargs)
            # if self.recordvideo:
            #     return await self._playwright.firefox.launch(record_video_dir=os.path.abspath('')+os.sep+"screen-recording", **kwargs)
            # else:
            #     return await self._playwright.firefox.launch( **kwargs)



        if browsertype == "webkit":
            return await self._playwright.webkit.launch(**kwargs)

        raise RuntimeError(
            "You have to select either 'chromium', 'firefox', or 'webkit' as browser."
        )

    async def _start_persistent_browser(
        self, browser: str, user_data_dir: Optional[Union[str, Path]], **kwargs
    ):
        if browser == "chromium":

            return await self._playwright.chromium.launch_persistent_context(
                user_data_dir, **kwargs
            )
        if browser == "firefox":
            self.browser=await self._playwright.firefox.launch(**kwargs)

            if self.recordvideo:
                return await self._playwright.firefox.launch_persistent_context(user_data_dir,record_video_dir=os.path.abspath('')+os.sep+"screen-recording", **kwargs)
            else:
                return await self._playwright.firefox.launch_persistent_context(user_data_dir, **kwargs)

        if browser == "webkit":
            return await self._playwright.webkit.launch_persistent_context(
                user_data_dir, **kwargs
            )

        raise RuntimeError(
            "You have to select either 'chromium', 'firefox' or 'webkit' as browser."
        )
    async def close(self):
        await self.browser.close()
        await self._playwright.stop()