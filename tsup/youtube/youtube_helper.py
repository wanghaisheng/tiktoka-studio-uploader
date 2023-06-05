import time
import re
import logging
from time import sleep
from datetime import datetime
from playwright.async_api import *
from tsup.utils.constants import *
from pathlib import Path
import os
from typing import Tuple, Optional, Union, Literal


def get_path(file_path: str) -> str:
    # no clue why, but this character gets added for me when running
    # return str(os.path(file_path)).replace("\u202a", "")
    # return file_path.replace("\u202a", "")
    return str(Path(file_path)).replace("\u202a", "")


def close_browser(self):
    self.browser.close()
    self._playwright.stop()


async def VerifyDialog(self, page):
    try:
        self.log.debug(f"Trying to detect verify...")

        # verifyvisible =await self.page.get_by_text("Verify it's you").is_visible()
        verifyvisible = await page.locator("#confirmation-dialog").is_visible()
        # verifyvisible1 =await page.locator("ytcp-dialog.ytcp-confirmation-dialog > tp-yt-paper-dialog:nth-child(1) > div:nth-child(1)").is_visible()
        # verifyvisible =await page.locator("#dialog-title").is_visible()
        if verifyvisible:
            # fix google account verify
            self.log.debug("verify its you")
            # await page.click('text=Login')
            # time.sleep(60)
            # await page.locator('#confirm-button > div:nth-child(2)').click()
            await page.goto(
                "https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26next%3Dhttps%253A%252F%252Fstudio.youtube.com%252Freauth%26feature%3Dreauth%26authuser%3D3%26pageid%3D106691143538188646876%26skip_identity_prompt%3Dtrue&hl=en&authuser=3&rart=ANgoxcd6AUvx_ynaUmq5M6nROFwTagKglTZqT8c97xb1AEzoDasGeJ14cNlvYfH1_mJsl7us_sFLNGJskNrJyjMaIE2KklrO7Q&flowName=GlifWebSignIn&flowEntry=ServiceLogin"
            )
            page.locator("#identifierId")
            self.log.debug("input username or email")

            # <div class="rFrNMe N3Hzgf jjwyfe QBQrY zKHdkd sdJrJc Tyc9J" jscontroller="pxq3x" jsaction="clickonly:KjsqPd; focus:Jt1EX; blur:fpfTEe; input:Lg5SV" jsshadow="" jsname="Vsb5Ub"><div class="aCsJod oJeWuf"><div class="aXBtI Wic03c"><div class="Xb9hP"><input type="email" class="whsOnd zHQkBf" jsname="YPqjbf" autocomplete="username" spellcheck="false" tabindex="0" aria-label="Email or phone" name="identifier" autocapitalize="none" id="identifierId" dir="ltr" data-initial-dir="ltr" data-initial-value=""><div jsname="YRMmle" class="AxOyFc snByac" aria-hidden="true">Email or phone</div></div><div class="i9lrp mIZh1c"></div><div jsname="XmnwAc" class="OabDMe cXrdqd Y2Zypf"></div></div></div><div class="LXRPh"><div jsname="ty6ygf" class="ovnfwe Is7Fhb"></div><div jsname="B34EJ" class="dEOOab RxsGPe" aria-atomic="true" aria-live="assertive"></div></div></div>

            await page.fill('input[name="identifier"]', self.username)

            await page.locator(
                ".VfPpkd-LgbsSe-OWXEXe-k8QpJ > span:nth-child(4)"
            ).click()
            time.sleep(10)

            await page.fill('input[name="password"]', self.password)
            time.sleep(10)

            await page.locator(
                ".VfPpkd-LgbsSe-OWXEXe-k8QpJ > span:nth-child(4)"
            ).click()
            # await page.click('text=Submit')

            Stephint = await page.locator(
                ".bCAAsb > form:nth-child(1) > span:nth-child(1) > section:nth-child(1) > header:nth-child(1) > div:nth-child(1)"
            ).text_content()
            self.log.debug(Stephint)
            if "2-Step Verification" in Stephint:
                # <div class="L9iFZc" role="presentation" jsname="NjaE2c"><h2 class="kV95Wc TrZEUc"><span jsslot="" jsname="Ud7fr">2-Step Verification</span></h2><div class="yMb59d" jsname="HSrbLb" aria-hidden="true"></div></div>
                # <span jsslot="" jsname="Ud7fr">2-Step Verification</span>
                self.log.debug("you need google auth and sms very code")
                time.sleep(60)
            # await page.locator('#confirm-button > div:nth-child(2)').click()

    except:
        self.log.debug("there is no verification at all")
    self.log.debug(f"Finishing detect verification...")


async def changeHomePageLangIfNeeded(self, localPage):
    await localPage.goto(YoutubeHomePageURL, timeout=self.timeout)
    try:
        if await localPage.get_by_label("Account").is_visible():
            await localPage.get_by_label("Account").click()

        else:
            if await localPage.locator(avatarButtonSelector).is_visible():
                await localPage.locator(avatarButtonSelector).click()

    except Exception:
        print("Avatar/Profile picture button not found : ")
        # print('detect avartar',await localPage.locator(avatarButtonSelector).is_visible())

        # await localPage.locator(avatarButtonSelector).click()
    truelangMenuItemSelector = ""
    try:
        if await localPage.locator(langMenuItemSelector).is_visible():
            await localPage.locator(langMenuItemSelector).click()
            truelangMenuItemSelector = langMenuItemSelector
        else:
            langMenuItemSelector2 = "yt-multi-page-menu-section-renderer.style-scope:nth-child(3) > div:nth-child(2) > ytd-compact-link-renderer:nth-child(2)"
            if await localPage.locator(langMenuItemSelector2).is_visible():
                await localPage.locator(langMenuItemSelector2).click()
                truelangMenuItemSelector = langMenuItemSelector2

    except:
        print('Language menu item selector/button(">") not found : ')

    selectedLang = await localPage.evaluate(
        f"document.querySelector({truelangMenuItemSelector}).innerText"
    )
    print(f"home page language setting is {selectedLang}")

    if not selectedLang:
        print("Failed to find selected language : Empty text")

    if "English" in selectedLang:
        print("there is no need to change youtube homepage language")

        return
    await localPage.click(langMenuItemSelector)

    englishItemXPath = "//*[normalize-space(text())='English']"

    try:
        await localPage.locator(englishItemXPath).wait_for()
    except:
        print("English item selector not found : ")
    # await localPage.wait_for_timeout(3000)

    await localPage.evaluate(
        "(englishItemXPath: any) => {let element: HTMLElement = document?.evaluate(englishItemXPath,document,null,XPathResult.FIRST_ORDERED_NODE_TYPE,null).singleNodeValue as HTMLElement;element.click()}",
        englishItemXPath,
    )
    # Recursive language change, if YouTube, for some reason, did not change the language the first time, although the English (UK) button was pressed, the exit from the recursion occurs when the selectedLang selector is tested for the set language
    await changeHomePageLangIfNeeded(localPage)

    return


async def set_channel_language_english(self, localPage):
    try:
        await localPage.goto(YoutubeHomePageURL, timeout=self.timeout)
    except:
        self.log.debug(
            "failed to youtube studio home page due to network issue,pls check your speed"
        )

    try:
        print("detect your account profile icon .")

        if await localPage.get_by_label("Account").is_visible():
            await localPage.get_by_label("Account").click()

        else:
            if await localPage.locator(avatarButtonSelector).is_visible():
                await localPage.locator(avatarButtonSelector).click()

    except Exception:
        print("Avatar/Profile picture button not found : ")
    truelangMenuItemSelector = ""

    try:
        print("detect language setting .")

        if await localPage.locator(langMenuItemSelector).is_visible():
            await localPage.locator(langMenuItemSelector).click()
            truelangMenuItemSelector = langMenuItemSelector
        else:
            langMenuItemSelector2 = "yt-multi-page-menu-section-renderer.style-scope:nth-child(3) > div:nth-child(2) > ytd-compact-link-renderer:nth-child(2)"
            if await localPage.locator(langMenuItemSelector2).is_visible():
                await localPage.locator(langMenuItemSelector2).click()
                truelangMenuItemSelector = langMenuItemSelector2

    except:
        print('Language menu item selector/button(">") not found : ')

        if (
            not "English"
            in await localPage.locator(truelangMenuItemSelector).text_content()
        ):
            print("choose the language or location you like to use.")
            if await localPage.locator(selector_en_path):
                await localPage.locator(selector_en_path).click()
        else:
            print("your youtube homepage language setting is already in English")


# fix google account verifys


async def verify(self, page):
    try:
        while True:
            await page.locator("#confirm-button > div:nth-child(2)").click()
            await page.goto(
                "https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26next%3Dhttps%253A%252F%252Fstudio.youtube.com%252Freauth%26feature%3Dreauth%26authuser%3D2%26skip_identity_prompt%3Dtrue&hl=en&authuser=2&rart=ANgoxcfF1TrrQp5lP5ySTmlJmdnwuMbSDi81WlN2aDXRgvpTnD1cv0nXHlRcMz6yv6hnqfERyjXMCgJqa8thKIAqVqatu9kTtA&flowName=GlifWebSignIn&flowEntry=ServiceLogin"
            )
            await page.locator("#identifierId").click()
            await page.fill("#identifierId", self.username)
            await page.locator(
                ".VfPpkd-LgbsSe-OWXEXe-k8QpJ > span:nth-child(4)"
            ).click()
            time.sleep(3)
            await page.fill(
                "#password > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)",
                self.password,
            )
            await page.locator(
                ".VfPpkd-LgbsSe-OWXEXe-k8QpJ > span:nth-child(4)"
            ).click()
            time.sleep(60)

    except:
        time.sleep(1)
    # x_path = '//*[@id="textbox"]'
    # if page.wait_for_selector(x_path):
    # break


async def wait_for_processing(page, process):
    if process:
        # Wait for processing to complete
        progress_label = page.locator("span.progress-label")
        pattern = re.compile(r"(finished processing)|(processing up to.*)|(check.*)")
        afterprocessingpattern = re.compile(r"(finished processing)|(processing hd.*)")
        afteruploadpattern = re.compile(r"(finished uploading)|(uploading 99.*)")
        # if process==2:
        #     pattern=aftercheckpattern
        # elif process==1:
        #     pattern=afterprocessingpattern
        # elif process==0:
        #     pattern=afteruploadpattern

        current_progress = await progress_label.all_text_contents()
        current_progress = "".join(current_progress)
        last_progress = None
        print(
            f"current_progress is : {current_progress}\n{not pattern.match(current_progress.lower())}"
        )
        while not pattern.match(current_progress.lower()):
            if last_progress != current_progress:
                logging.info(f"Current progress: {current_progress}")
            last_progress = current_progress
            sleep(5)
            current_progress = await progress_label.all_text_contents()
            current_progress = "".join(current_progress).lower()

            if process == 2:
                if "Checks complete. No issues found" in current_progress:
                    print(
                        f"current_progress is : {current_progress}\n{not pattern.match(current_progress.lower())}"
                    )

                    print("Finished Copyright checks!")
                    break
            elif process == 1:
                if "finished processing" in current_progress:
                    print(
                        f"current_progress is : {current_progress}\n{not pattern.match(current_progress.lower())}"
                    )

                    print("Finished Processing!")
                    break
            elif process == 0:
                if "Upload complete" in current_progress:
                    print(
                        f"current_progress is : {current_progress}\n{not pattern.match(current_progress.lower())}"
                    )

                    print("Finished Uploading!")
                    break
        print("==========", last_progress)
    else:
        while True:
            x_path = (
                "//span[@class='progress-label style-scope ytcp-video-upload-progress']"
            )
            # TypeError: 'WebElement' object  is not subscriptable
            upload_progress = await page.locator(
                '[class="progress-label style-scope ytcp-video-upload-progress"]'
            ).all_text_contents()

            # innerhtml = page.locator(x_path).get_attribute('innerHTML')
            # if re.match(r"\D \.\.\. \D", innerhtml) or re.match(r"^[^\.]+$", innerhtml):
            #     break
            upload_progress = " ".join(upload_progress)
            print("video status", upload_progress.lower())

            if not "%" in upload_progress.lower():
                break
            elif "checks complete. no issues found" in upload_progress.lower():
                break


async def setscheduletime_douyin(page, publish_date: datetime):
    hour_to_post, date_to_post, publish_date_hour = hour_and_date_douyin(publish_date)

    # Clicking in schedule video
    print("click schedule")
    await page.locator("label.one-line--2rHu9:nth-child(2)").click()

    sleep(1)
    # Writing date
    date_to_post = publish_date.strftime("%Y-%m-%d")
    hour_xpath = get_hour_xpath(hour_to_post)
    print("click date", str(publish_date_hour), type(publish_date_hour))
    # 2022-05-15 09:24
    # await page.locator('.semi-input').click()

    sleep(1)

    await page.keyboard.press("Control+KeyA")
    await page.keyboard.type(str(publish_date_hour))
    await page.keyboard.press("Enter")

    sleep(1)

    sleep(1)


async def setscheduletime(page, date_to_publish, hour_to_publish):
    # hour_xpath=get_hour_xpath(hour_to_publish)
    # Clicking in schedule video
    print("choose  schedule publish")
    try:
        if await page.locator(SCHEDULE_BUTTON).is_visible():
            await page.locator(SCHEDULE_BUTTON).click()
    except:
        if await page.get_by_text("Schedule").is_visible():
            await page.get_by_text("Schedule").click()
        else:
            print("we could not find the schedule button")
    # Writing date
    print("click date")
    await page.locator(
        "#datepicker-trigger > ytcp-dropdown-trigger:nth-child(1) > div:nth-child(2) > div:nth-child(4)"
    ).click()
    # #datepicker-trigger > ytcp-dropdown-trigger:nth-child(1) > div:nth-child(2) > div:nth-child(4) > span:nth-child(2)
    # page.locator(
    # '//html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[2]/ytcp-visibility-scheduler/div[1]/ytcp-datetime-picker/div/ytcp-text-dropdown-trigger[1]/ytcp-dropdown-trigger/div/div[3]').click()
    sleep(1)
    page.locator('//*[@id="input-4"]')

    # page.locator(
    # '//html/body/ytcp-date-picker/tp-yt-paper-dialog/div/form/tp-yt-paper-input/tp-yt-paper-input-container/div[2]/div/iron-input/input').click()
    await page.keyboard.press("Control+KeyA")
    print("before convert", date_to_publish)
    date_to_publish = date_to_publish.strftime("%b %d, %Y")
    print("after convert", date_to_publish)

    await page.keyboard.type(date_to_publish)
    await page.keyboard.press("Enter")

    sleep(1)
    print("start to Open time_picker", hour_to_publish)
    # Open time_picker
    # await page.locator("input.tp-yt-paper-input").fill(hour_to_publish)

    await page.locator(
        # "#time-of-day-trigger > ytcp-dropdown-trigger:nth-child(1) > div:nth-child(2)"
        # input-1 > input:nth-child(1)
        # '#time-of-day-container'
        # input.tp-yt-paper-input
        "#html-body ytcp-uploads-dialog tp-yt-paper-dialog#dialog.style-scope.ytcp-uploads-dialog div.dialog-content.style-scope.ytcp-uploads-dialog ytcp-animatable#scrollable-content.metadata-fade-in-section.style-scope.ytcp-uploads-dialog ytcp-uploads-review.style-scope.ytcp-uploads-dialog div.left-col.style-scope.ytcp-uploads-review div#visibility-container.style-scope.ytcp-uploads-review ytcp-video-visibility-select.style-scope.ytcp-uploads-review div#second-container.style-scope.ytcp-video-visibility-select ytcp-visibility-scheduler.scheduler.style-scope.ytcp-video-visibility-select div.scheduled-info-container.style-scope.ytcp-visibility-scheduler ytcp-datetime-picker.style-scope.ytcp-visibility-scheduler div.scheduled-info-container.style-scope.ytcp-datetime-picker div.style-scope.ytcp-datetime-picker form#form.style-scope.ytcp-datetime-picker ytcp-form-input-container#time-of-day-container.style-scope.ytcp-datetime-picker div#outer.style-scope.ytcp-form-input-container"
        # SCHEDULE_TIME
    ).click()

    print("clear existing timesetting")
    await page.keyboard.press("Backspace")
    await page.keyboard.press("Control+KeyA")
    await page.keyboard.press("Delete")
    await page.keyboard.type(hour_to_publish)
    # 很可能就是这个没有确认输入，导致悬浮窗口，无法获取提交按钮
    await page.keyboard.press("Enter")

    await page.locator("h1.style-scope:nth-child(2)").click()
    sleep(1)


def hour_and_date_douyin(now_date_hour):
    # now_date_hour += datetime.timedelta(seconds=TIME_BETWEEN_POSTS)
    hour_to_post = now_date_hour.strftime("%H:%M")
    hour, minutes = hour_to_post.split(":")[0], int(hour_to_post.split(":")[1])
    setting_minutes = minutes // 15
    minutes = setting_minutes * 15
    if minutes == 0:
        minutes = "00"
    hour_to_post = f"{hour}:{minutes}"
    # 2022-05-15 09:24
    print("now_date_hour", now_date_hour)
    date_to_post = now_date_hour.strftime("%d/%m/%Y")
    return hour_to_post, date_to_post, now_date_hour


def hour_and_date(now_date_hour):
    # now_date_hour += datetime.timedelta(seconds=TIME_BETWEEN_POSTS)
    hour_to_post = now_date_hour.strftime("%H:%M")
    hour, minutes = hour_to_post.split(":")[0], int(hour_to_post.split(":")[1])
    setting_minutes = minutes // 15
    minutes = setting_minutes * 15
    if minutes == 0:
        minutes = "00"
    hour_to_post = f"{hour}:{minutes}"
    date_to_post = now_date_hour.strftime("%d/%m/%Y")
    return hour_to_post, date_to_post, now_date_hour


def get_hour_xpath(input_hour):
    hour_xpath = dict()
    xpath_time = 0
    for hour in range(24):
        if hour < 10 and hour >= 0:
            hour = f"0{hour}"
        for minute in range(0, 46, 15):
            if minute == 0:
                minute = "00"
            xpath_time += 1
            hour_xpath.update(
                {
                    f"{hour}:{minute}": f"//html/body/ytcp-time-of-day-picker/tp-yt-paper-dialog/tp-yt-paper-listbox/tp-yt-paper-item[{xpath_time}]"
                }
            )
    return hour_xpath[input_hour]


def _set_time_cssSelector(page, publish_date: datetime):
    # Start time scheduling
    page.locator("SCHEDULE").click()

    # Open date_picker
    page.locator("#datepicker-trigger > ytcp-dropdown-trigger:nth-child(1)").click()

    date_input = page.locator("input.tp-yt-paper-input").click()
    date_input.clear()
    # Transform date into required format: Mar 19, 2021
    page.keyboard.press("Control+KeyA")
    page.keyboard.type(publish_date.strftime("%b %d, %Y"))
    page.keyboard.press("KeyReturn")
    # Open time_picker
    page.locator(
        "#time-of-day-trigger > ytcp-dropdown-trigger:nth-child(1) > div:nth-child(2)"
    ).click()

    time_list = page.locator("tp-yt-paper-item.tp-yt-paper-item")
    # Transform time into required format: 8:15 PM
    time_str = publish_date.strftime("%I:%M %p").strip("0")

    time = [time for time in time_list[2:] if time.text == time_str][0]
    time.click()


def _set_advanced_settings(page, game_title: str, made_for_kids: bool):
    # Open advanced options
    page = page

    page.wait_for_selector("#toggle-button").click()
    if game_title:
        game_title_input = page.wait_for_selector(
            ".ytcp-form-gaming > "
            "ytcp-dropdown-trigger:nth-child(1) > "
            ":nth-child(2) > div:nth-child(3) > input:nth-child(3)"
        )
        game_title_input.send_keys(game_title)

        # Select first item in game drop down
        page.wait_for_selector("#text-item-2").click()

    # WebDriverWait(page, 20).until(EC.element_to_be_clickable(
    # ("VIDEO_MADE_FOR_KIDS_MFK" if made_for_kids else "VIDEO_MADE_FOR_KIDS_NOT_MFK")
    # )).click()


def _set_endcard(self):
    page = page

    # Add endscreen
    page.wait_for_selector("#endscreens-button").click()
    sleep(5)

    for i in range(1, 11):
        try:
            # Select endcard type from last video or first suggestion if no prev. video
            page.wait_for_selector("div.card:nth-child(1)").click()
            break
        except:
            logging.warning(f"Couldn't find endcard button. Retry in 5s! ({i}/10)")
            sleep(5)

    page.is_visible("save-button").click()


# def close(self):
#    page.close()
#    page.quit()

#     self.log.debug("Closed Firefox")


def remove_unwatched_videos(self, page, remove_copyrighted, remove_unwatched_views):
    try:
        page.goto(YOUTUBE_URL)
        sleep(USER_WAITING_TIME)

        # set english as language
        self.__set_channel_language_english()

        page.get("https://studio.youtube.com/")
        sleep(USER_WAITING_TIME)
        page.wait_for_selector("menu-paper-icon-item-1").click()
        sleep(USER_WAITING_TIME)

        if self.__is_videos_available():
            return True

        page.wait_for_selector("#page-size .ytcp-text-dropdown-trigger").click()
        sleep(USER_WAITING_TIME)
        # clock 50 items per page
        pagination_sizes = page.wait_for_selector(
            "#select-menu-for-page-size #dialog .paper-item"
        )
        pagination_sizes[2].click()
        sleep(USER_WAITING_TIME)

        # filter to delete only copyrighted videos
        if remove_copyrighted:
            page.wait_for_selector("filter-icon").click()
            sleep(USER_WAITING_TIME)
            page.wait_for_selector(
                "ytcp-text-menu#menu tp-yt-paper-dialog tp-yt-paper-listbox paper-item#text-item-1 ytcp-ve div"
            ).click()
            sleep(USER_WAITING_TIME)

        # filter to delete videos with views lower than 100
        if remove_unwatched_views:
            views_no = "100000"
            page.wait_for_selector("filter-icon").click()
            sleep(USER_WAITING_TIME)
            page.wait_for_selector(
                "ytcp-text-menu#menu tp-yt-paper-dialog tp-yt-paper-listbox paper-item#text-item-5 ytcp-ve div"
            ).click()
            sleep(USER_WAITING_TIME)
            page.wait_for_selector("//iron-input[@id='input-2']/input").click()
            sleep(USER_WAITING_TIME)
            page.wait_for_selector("//iron-input[@id='input-2']/input").clear()
            sleep(USER_WAITING_TIME)
            page.wait_for_selector("//iron-input[@id='input-2']/input").send_keys(
                views_no
            )
            sleep(USER_WAITING_TIME)
            page.wait_for_selector("//input[@type='text']").click()
            sleep(USER_WAITING_TIME)
            page.wait_for_selector(
                "//tp-yt-paper-listbox[@id='operator-list']/paper-item[2]"
            ).click()
            sleep(USER_WAITING_TIME)
            page.wait_for_selector("//ytcp-button[@id='apply-button']/div").click()
            sleep(USER_WAITING_TIME)

        return self.__remove_unwatched_videos()
    except Exception as e:
        print(e)
        return False


def __is_videos_available(self, page):
    # if there are no videos to be deleted, this element should be visible
    # if not visible throw error, and proceed to delete more videos
    try:
        page.wait_for_selector(
            "//ytcp-video-section-content[@id='video-list']/div/div[2]/div"
        )
        # return True, there are no more video to be deleted
        return True
    except:
        return False


def waitforUplodingdone(page):
    # wait until video uploads
    # uploading progress text contains ": " - Timp ramas/Remaining time: 3 minutes.
    # we wait until ': ' is removed, so we know the text has changed and video has entered processing stage
    uploading_progress_text = page.locator(UPLOADING_PROGRESS_SELECTOR).text_content()
    while ": " in uploading_progress_text:
        sleep(5)
        page.locator(UPLOADING_PROGRESS_SELECTOR).text_content()


def uploadTikTok(username, tiktok, deletionStatus, file):
    regex = re.compile("[0-9]{17}")
    regexA = re.compile("[0-9]{18}")
    regexB = re.compile("[0-9]{19}")
    regexC = re.compile("[0-9]{8}")
    regexD = re.compile("[0-9]{9}")
    if os.path.isdir(tiktok):
        if (
            regex.match(str(tiktok))
            or (regexA.match(str(tiktok)))
            or (regexB.match(str(tiktok)))
            or (regexC.match(str(tiktok)))
            or (regexD.match(str(tiktok)))
        ):  # TODO: use or regex with "|" instead of this
            item = get_item("tiktok-" + tiktok)
            if username is None:
                if file is not None:
                    file.write(str(tiktok))
                    file.write("\n")
                return None
            item.upload(
                "./" + tiktok + "/",
                verbose=True,
                checksum=True,
                delete=deletionStatus,
                metadata=dict(
                    collection="opensource_media",
                    subject="tiktok",
                    creator=username,
                    title="TikTok Video by " + username,
                    originalurl="https://www.tiktok.com/@"
                    + username
                    + "/video/"
                    + tiktok,
                    scanner="TikUp " + getVersion(),
                ),
                retries=9001,
                retries_sleep=60,
            )
            if deletionStatus:
                os.rmdir(tiktok)
            print()
            print("Uploaded to https://archive.org/details/tiktok-" + tiktok)
            print()
            if file is not None:
                file.write(str(tiktok))
                file.write("\n")
