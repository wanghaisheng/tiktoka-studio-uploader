class YOUTUBE_CONSTANT:
    """A class for storing constants for YoutubeUploader class"""
    YOUTUBE_URL = 'https://www.youtube.com'
    YOUTUBE_STUDIO_URL = 'https://studio.youtube.com'
    YOUTUBE_UPLOAD_URL = 'https://www.youtube.com/upload'

    # 时间相关
    USER_WAITING_TIME = 3
    CONFIRM_TIME = 5
    LOAD_TIME = 10
    SHORT_WAIT_TIME = 20
    LONG_WAIT_TIME = 60
    LONG_UPLOAD_TIME = 600

    # xpath相关
    VIDEO_TITLE = 'title'
    VIDEO_DESCRIPTION = 'description'
    VIDEO_TAGS = 'tags'
    DESCRIPTION_CONTAINER = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/' \
                            'ytcp-uploads-details/div/ytcp-uploads-basics/ytcp-mention-textbox[2]'

    PICTURE_BUTTON = 'file-loader'

    TEXTBOX = 'textbox'
    TEXT_INPUT = 'text-input'
    RADIO_LABEL = 'radioLabel'

    STATUS_CONTAINER = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/' \
                       'div/div[1]/ytcp-video-upload-progress/span'
    NOT_MADE_FOR_KIDS_LABEL = 'radioLabel'

    # Thanks to romka777
    MORE_BUTTON = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-video-metadata-editor/div/div/ytcp-button/div'
    TAGS_INPUT_CONTAINER = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[3]/ytcp-form-input-container/div[1]/div[2]/ytcp-free-text-chip-bar/ytcp-chip-bar/div'

    TAGS_INPUT = 'text-input'
    TOOGLE_BUTN = "toggle-button"
    NEXT_BUTTON = 'next-button'
    PUBLIC_BUTTON = 'PUBLIC'
    VIDEO_URL_CONTAINER = "//span[@class='video-url-fadeable style-scope ytcp-video-info']"
    VIDEO_URL_ELEMENT = "//a[@class='style-scope ytcp-video-info']"
    HREF = 'href'
    UPLOADED = 'Uploading'
    ERROR_CONTAINER = '//*[@id="error-message"]'
    VIDEO_NOT_FOUND_ERROR = 'Could not find video_id'
    DONE_BUTTON = 'done-button'
    INPUT_FILE_VIDEO = "//input[@type='file']"
    INPUT_FILE_THUMBNAIL = "//input[@id='file-loader']"

class TIKTOK_CONSTANT:
    TIKTOK_URL = 'https://www.tiktok.com'
    TIKTOK_UPLOAD_URL = 'https://www.tiktok.com/upload/?lang=en'
    USER_WAITING_TIME = 2
    CHECK_TIME = 15
    POST_TIME = 15
    WAIT_TIME = 10
    LOAD_TIME = 5

    Caption = "//*[contains(@class, 'notranslate public-DraftEditor-content')]"
    IFRAME = '//*[@id="main"]/div[2]/div/iframe'
    INPUT_FILE_VIDEO = '//*[@id="root"]/div/div/div/div/div[2]/div[1]/div/input'

    ALLOW_CHECK = "tiktok-switch__switch-wrapper"

    POST_BUTTON = '//*[@id="root"]/div/div/div/div/div[2]/div[2]/div[7]/div[2]/button'
    PREVIEW = '/html/body/div[1]/div/div/div/div/div[2]/div[1]'


