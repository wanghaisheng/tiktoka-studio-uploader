import json
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
import random


class YoutubeUpload:
    def __init__(
        self,
        root_profile_directory: str,
        proxy_option: str = "",
        timeout: int = 200 * 1000,
        watcheveryuploadstep: bool = True,
        debug: bool = True,
        username:str ="",
        password:str ="",
        recoveryemail:str="",
        browserType:str="firefox",
        # 'chromium', 'firefox', or 'webkit'
        CHANNEL_COOKIES: str = "",
        closewhen100percent:int =2,
        # 0-uploading done
        # 1-Processing done
        # 2-Checking done

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
        self._playwright=''
        self.browserType=browserType
        self.context=''
        self.page=''
        self.closewhen100percent=closewhen100percent
        self.recordvideo=recordvideo
        # self.setup()

    def send(self, element, text: str) -> None:
        element.clear()
        sleep(self.timeout)
        element.send_keys(text)
        sleep(self.timeout)

    async def click_next(self, page) -> None:
        await page.locator(NEXT_BUTTON).click()
        sleep(random(5*1000,self.timeout))

    async def not_uploaded(self, page) -> bool:
        s=await page.locator(STATUS_CONTAINER).text_content()
        return s.find(UPLOADED) != -1

    async def upload(
        self,
        videopath: str="",
        title: str = "",
        description: str = "",
        thumbnail: str = "",
        publishpolicy: int = 0,
        date_to_publish: datetime = datetime(
            date.today().year,  date.today().month,  date.today().day),
        hour_to_publish: str="10:15",
        playlist:str="",
        isAgeRestriction:bool=False,
        isNotForKid:bool=True,
        isPaidpromotion:bool=True,
        isAutomaticchapters:bool=True,
        Language:int=0,
        # input language str and get index in the availableLanguages list
        CaptionsCertification:int=0,

# 0-        None
# 1-This content has never aired on television in the U.S.
# 2-This content has only aired on television in the U.S. without captions
# 3-This content has not aired on U.S. television with captions since September 30, 2012.
# 4-This content does not fall within a category of online programming that requires captions under FCC regulations (47 C.F.R. § 79).
# 5-The FCC and/or U.S. Congress has granted an exemption from captioning requirements for this content.

        # parse from video metadata  using ffmpeg
        VideoRecordingdate:str='',
        VideoRecordinglocation:str='',
        LicenceType:str='Standard YouTube License',
        ShortsremixingType:int=0,
        # 0-  Allow video and audio remixing
        # 1-    Allow only audio remixing
        # 2-   Don’t allow remixing 
        Category:str=0,
        # 0-Autos & Vehicles
        # 1-Comedy
        # 2-Education
        # 3-Entertainment
        # 4-Film & Animation
        # 5-Gaming
        # 6-Howto & Style
        # 7-Music
        # 8-News & Politics
        # 9-Nonprofits & Activism
        # 10-People & Blogs
        # 11-Pets & Animals
        # 12-Science & Technology
        # 13-Sports
        # 14-Travel & Events
        CommentsRatingsPolicy:int =0,
            # 0-Allow all comments
            # 1-Hold potentially inappropriate comments for review
            # 2-Increase strictness
            # 3-Hold all comments for review
            # 4-Disable comments 
        CopyrightCheckswait:bool=True,
        tags: list = [],
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
        self.log.debug(f'whether run in view mode:{headless}')
        if self.proxy_option == "":
            self.log.debug(f'start web page without proxy:{self.proxy_option}')

            browserLaunchOptionDict = {
                "headless": headless,
                # "executable_path": executable_path,
                "timeout": self.timeout
            }

            if not self.root_profile_directory:

                self.browser = await self._start_browser(self.browserType, **browserLaunchOptionDict)
                if self.recordvideo:
                    self.context = await self.browser.new_context(record_video_dir=os.getcwd()+os.sep+"screen-recording")
                else:
                    self.context = await self.browser.new_context()
            else:
                self.context = await self._start_persistent_browser(
                    self.browserType, user_data_dir=self.root_profile_directory, **browserLaunchOptionDict
                )

        else:
            self.log.debug('start web page with proxy')

            browserLaunchOptionDict = {
                "headless": headless,
                "proxy": {
                    "server": self.proxy_option,
                },

                # timeout <float> Maximum time in milliseconds to wait for the browser instance to start. Defaults to 30000 (30 seconds). Pass 0 to disable timeout.#
                "timeout": self.timeout
            }


            if not self.root_profile_directory:

                self.browser = await self._start_browser(self.browserType, **browserLaunchOptionDict)
                if self.recordvideo:
                    self.context = await self.browser.new_context(record_video_dir=os.getcwd()+os.sep+"screen-recording")
                else:
                    self.context = await self.browser.new_context()
            else:
                self.context = await self._start_persistent_browser(
                    self.browserType, user_data_dir=self.root_profile_directory, **browserLaunchOptionDict
                )

        self.log.debug("Firefox is now running")
        if not videopath:
            raise FileNotFoundError(f'Could not find file with path: "{videopath}"')

        try:

            if self.CHANNEL_COOKIES and not self.CHANNEL_COOKIES == '' and os.path.exists(self.CHANNEL_COOKIES) and os.path.getsize(self.CHANNEL_COOKIES)>0:
                self.log.debug(f'cookies existing:{self.CHANNEL_COOKIES}')

                await self.context.clear_cookies()

                await self.context.add_cookies(
                    json.load(open(self.CHANNEL_COOKIES, 'r'))['cookies']
                )            

                print('11111111111111111')
                self.page = await self.context.new_page()
                print('111111111111111112')

        except:
            print('your should provide a valid cookie file')


            # login_using_cookie_file(self,self.CHANNEL_COOKIES,page)         
        await self.page.goto(YoutubeHomePageURL,timeout= self.timeout)

        page=self.page
        islogin = confirm_logged_in(self)
        self.log.debug(f'checking login status:{islogin}')

        if not islogin:
            self.log.debug('you can mannually sign in to save credentials for later auto login')
            passwordlogin(self,page)
            await page.goto(YoutubeHomePageURL,timeout=self.timeout)
            self.log.debug('start to check login status')

            islogin = confirm_logged_in(self)

            # https://github.com/xtekky/google-login-bypass/blob/main/login.py


        self.log.debug('check whether  home page is English') 
        await set_channel_language_english(self,page)
        self.log.debug('go to youtube studio home page') 
        await page.goto(YOUTUBE_STUDIO_URL,timeout=self.timeout)

        self.log.debug('double check youtube studio home page display language') 

        if not await page.locator('.page-title').text_content()=='Channel content':
            self.log.debug('It seems studio home page is not English,start change locale to english again')
            await set_channel_language_english(self,page)
            self.log.debug('finish change locale to english')

        await page.goto(YOUTUBE_UPLOAD_URL,timeout=self.timeout) 
        self.log.debug("Found YouTube upload Dialog Modal")



        self.log.debug(f'Trying to upload "{videopath}" to YouTube...')
        if os.path.exists(get_path(videopath)):
            page.locator(
                INPUT_FILE_VIDEO)
            await page.set_input_files(INPUT_FILE_VIDEO, get_path(videopath))
            self.log.debug(f'Trying to upload "{get_path(videopath)}" to YouTube...')

        else:
            if os.path.exists(videopath.encode('utf-8')):
                self.log.debug(f'file found: {videopath}')
                page.locator(
                    INPUT_FILE_VIDEO)
                await page.set_input_files(INPUT_FILE_VIDEO, videopath.encode('utf-8'))
            self.log.debug(f'Trying to upload "{videopath.encode("utf-8")}" to YouTube...')

    #     <h1 slot="primary-header" id="dialog-title" class="style-scope ytcp-confirmation-dialog">
    #   Verify it's you
    # </h1>

        await VerifyDialog(self,page)


        try:
            self.log.debug(f'Trying to detect daily upload limit...')
            hint=await page.locator('#error-short style-scope ytcp-uploads-dialog').waitfor().text_content()
            if 'Daily upload limit reached' in hint:
                self.log.debug(f'you have reached daily upload limit pls try tomorrow')

                self.close()

            else:
                pass
        except:
            self.log.debug(f'Finishing detect daily upload limit...')


       # random case of you are currently sign out ,please sigin
       # to be fixed     

        # detect video id during uploading done in the title description page
        #.row

        self.log.debug(f'Trying to set "{title}" as title...')

        await VerifyDialog(self,page)

        if len(title) > TITLE_COUNTER:
            self.log.debug(f"Title was not set due to exceeding the maximum allowed characters ({len(title)}/{TITLE_COUNTER})")
            title=title[:TITLE_COUNTER-1]

                # TITLE
        self.log.debug('find  title field element to input')
        # titlecontainer= page.locator(TITLE_CONTAINER)
        await page.get_by_label("Add a title that describes your video (type @ to mention a channel)").fill(title)
        # await titlecontainer.click()
        # self.log.debug('clear existing title')
        # await page.keyboard.press("Backspace")
        # await page.keyboard.press("Control+KeyA")
        # await page.keyboard.press("Delete")
        # self.log.debug('filling new  title')

        # await page.keyboard.type(title)

        self.log.debug(f'Trying to set "{description}" as description...')

        if description:
            if len(description) > DESCRIPTION_COUNTER:
                self.log.debug(
                    f"Description was not set due to exceeding the maximum allowed characters ({len(description)}/{DESCRIPTION_COUNTER})"
                )
                description=description[:4888]

            self.log.debug('click description container to input')
            # print('1',await page.get_by_label("Tell viewers about your video (type @ to mention a channel)").is_visible())
            # print('2',await page.locator("html body#html-body ytcp-uploads-dialog tp-yt-paper-dialog#dialog.style-scope.ytcp-uploads-dialog div.dialog-content.style-scope.ytcp-uploads-dialog ytcp-animatable#scrollable-content.metadata-fade-in-section.style-scope.ytcp-uploads-dialog ytcp-ve.style-scope.ytcp-uploads-dialog ytcp-video-metadata-editor#details.style-scope.ytcp-uploads-dialog div.left-col.style-scope.ytcp-video-metadata-editor ytcp-video-metadata-editor-basics#basics.style-scope.ytcp-video-metadata-editor div#description-container.input-container.description.style-scope.ytcp-video-metadata-editor-basics ytcp-video-description#description-wrapper.style-scope.ytcp-video-metadata-editor-basics div#description-container.input-container.description.style-scope.ytcp-video-description ytcp-social-suggestions-textbox#description-textarea.style-scope.ytcp-video-description ytcp-form-input-container#container.fill-height.style-scope.ytcp-social-suggestions-textbox div#outer.style-scope.ytcp-form-input-container div#child-input.style-scope.ytcp-form-input-container div#container-content.style-scope.ytcp-social-suggestions-textbox ytcp-social-suggestion-input#input.fill-height.style-scope.ytcp-social-suggestions-textbox div#textbox.style-scope.ytcp-social-suggestions-textbox").is_visible())

            await page.locator(DESCRIPTION_CONTAINER).is_visible()
            # await page.get_by_label("Tell viewers about your video (type @ to mention a channel)").click().fill(description)

            await page.locator(DESCRIPTION_CONTAINER).click()

            self.log.debug('clear existing description')
            await page.keyboard.press("Backspace")
            await page.keyboard.press("Control+KeyA")
            await page.keyboard.press("Delete")
            await page.keyboard.type(description)
            self.log.debug('filling new  description')
        await VerifyDialog(self,page)

        if self.closewhen100percent in [0,1,2]:

            self.log.debug('start to check whether upload is finished')
            while await self.not_uploaded(page):
                self.log.debug("Still uploading...")
                sleep(1)
        if self.closewhen100percent ==0:
            self.log.debug('we choose not to wait progress and check tasks done')
        elif self.closewhen100percent ==1:
            self.log.debug('we choose not to wait check progress  task done')
        else:
            self.log.debug('waiting copyright check task done')

            await wait_for_processing(page,process=self.closewhen100percent)
            self.log.debug('check task and copyright check progress done')



        if thumbnail:
            self.log.debug(f'Trying to set "{thumbnail}" as thumbnail...')
            if os.path.exists(get_path(thumbnail)):
                await page.locator(
                    INPUT_FILE_THUMBNAIL).set_input_files(get_path(thumbnail))
            else:
                if os.path.exists(thumbnail.encode('utf-8')):
                    self.log.debug('thumbnail found', thumbnail)
                    await page.locator(INPUT_FILE_THUMBNAIL).set_input_files(
                        thumbnail.encode('utf-8'))
        await VerifyDialog(self,page)
        self.log.debug('Trying to set video to "Not made for kids"...')

        try:
            
            if await page.locator(NOT_MADE_FOR_KIDS_LABEL).is_visible():
                await page.locator(NOT_MADE_FOR_KIDS_RADIO_LABEL).click()
                self.log.debug('not made for kids task done')
        except:
            self.log.debug('failed to set not made for kids')
        self.log.debug('click show more button')
        print('show more button check',await page.get_by_text('Show more').is_visible())
        print('show more button check',await page.locator(MORE_OPTIONS_CONTAINER).is_visible())

        await page.locator(MORE_OPTIONS_CONTAINER).click()            
        if tags is None or tags =="" or len(tags)==0:
            pass
        else:
            self.log.debug(f'tags you give:{tags}')
            if type(tags) == list:
                tags=",".join(str(tag) for tag in tags)
                tags=tags[:500]
            else:
                tags=tags
            self.log.debug('overwrite prefined channel tags')
            if len(tags) > TAGS_COUNTER:
                self.log.debug(f"Tags were not set due to exceeding the maximum allowed characters ({len(tags)}/{TAGS_COUNTER})")
                tags=tags[:TAGS_COUNTER]


         # show more to set Paid promotion,Automatic chapters,Featured places,Language and captions certification,
        #  Recording date and location,License, Shorts remixing ,Comments and ratings,Category
            self.log.debug(f'Trying to set "{tags}" as tags...')
            await page.locator(TAGS_CONTAINER).locator(TEXT_INPUT).click()
            
            await page.get_by_label("Tags").click()

            self.log.debug('clear existing tags')
            await page.keyboard.press("Backspace")
            await page.keyboard.press("Control+KeyA")
            await page.keyboard.press("Delete")
            await page.get_by_label("Tags").fill(tags)
            self.log.debug('filling new  tags')

# Language and captions certification
# Recording date and location
# Shorts sampling
# Category
# there are 4 steps:uploading,Upload complete ... Processing will begin shortly,处理中，画质最高可为标清 ... 还剩 8 分钟,Checks complete. No issues found.
# after uploding,there is a video link
#after check, there is a text shows Checks complete. No issues found. and the progress bar of check is selected

        # sometimes you have 4 tabs instead of 3
        # this handles both cases
        for _ in range(3):
            try:
                await self.click_next(page)
                self.log.debug('next next!')
            except:
                pass

        # if there is issue in Copyright check, mandate publishpolicy to 0

        if not int(publishpolicy) in [0, 1, 2]:
            publishpolicy=0
        if int(publishpolicy) == 0:
            self.log.debug("Trying to set video visibility to private...")

            await page.locator(PRIVATE_RADIO_LABEL).click()
        elif int(publishpolicy) == 1:
            self.log.debug("Trying to set video visibility to public...")
            await page.locator("#first-container > tp-yt-paper-radio-button:nth-child(1)").is_visible()
            await page.locator("#first-container > tp-yt-paper-radio-button:nth-child(1)").click()

            publish='public'
            try:
                if publish == 'private':
                    await page.locator('#privacy-radios > tp-yt-paper-radio-button:nth-child(2)').click()
                    await page.locator('#privacy-radios > tp-yt-paper-radio-button.style-scope.ytcp-video-visibility-select.iron-selected').click()
                elif publish == 'unlisted':
                    await page.locator('#privacy-radios > tp-yt-paper-radio-button.style-scope.ytcp-video-visibility-select.iron-selected').click()

                    await page.locator('#privacy-radios > tp-yt-paper-radio-button:nth-child(11)').click()
                elif publish == 'public':
                    print('switch case to public')
                    if await page.get_by_text('Public').is_visible():
                        await page.get_by_text('Public').click()
                    else:
                        await page.locator('#privacy-radios > tp-yt-paper-radio-button:nth-child(15)').click()
                        await page.locator('#privacy-radios > tp-yt-paper-radio-button:nth-child(16)').click()
                    
                elif publish == 'public&premiere':
                    await page.click('#privacy-radios > tp-yt-paper-radio-button:nth-child(15)')
            except:
                pass

            try:
                print(f'detect public button visible{PUBLIC_BUTTON}:',await page.locator(PUBLIC_BUTTON).is_visible())
                print(f'detect public button visible:{PUBLIC_RADIO_LABEL}',await page.locator(PUBLIC_RADIO_LABEL).is_visible())

                await page.locator(PUBLIC_BUTTON).click()
            except:
                self.log.debug("we could not find the public buttton...")

        else:

            if date_to_publish is None:
                date_to_publish =datetime(
                    date.today().year,  date.today().month,  date.today().day)
            else:
                date_to_publish = date_to_publish

            if hour_to_publish and hour_to_publish in availableScheduleTimes:
                hour_to_publish=datetime.strptime(hour_to_publish, "%H:%M")
                hour_to_publish=hour_to_publish.strftime("%I:%M %p")     
            else:

                self.log.debug(
                f"your specified schedule time is not supported by youtube yet{hour_to_publish}")                
                hour_to_publish="10:15"
                hour_to_publish=hour_to_publish.strftime("%I:%M %p")     

            self.log.debug(
                f"Trying to set video schedule time...{date_to_publish}...{hour_to_publish}")

            await setscheduletime(page,date_to_publish,hour_to_publish)
        self.log.debug('publish setting task done')
        video_id=await self.get_video_id(page)

        try:
            done_button=page.locator(DONE_BUTTON)

            if await done_button.get_attribute("aria-disabled") == "true":
                error_message= await page.locator(
                    ERROR_CONTAINER).text_content()
                return False, error_message

            await done_button.click()
        except:
            self.log.debug('Failed to locate done button')
        self.log.debug('upload process is done')


   
 

        sleep(5)
        logging.info("Upload is complete")

        # upload multi-language subtitles and title description
        # https://studio.youtube.com/video/_aaNTRwoJco/translations
        YoutubeSubtitleURL='https://studio.youtube.com/video/'+video_id+'/translations'

        await self.close()
        # page.locator("#close-icon-button > tp-yt-iron-icon:nth-child(1)").click()
        # self.log.debug(page.expect_popup().locator("#html-body > ytcp-uploads-still-processing-dialog:nth-child(39)"))
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