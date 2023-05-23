# URLS
invalidCharacters = ['<', '>']

YoutubeUploadURL = 'https://www.youtube.com/upload?persist_gl=1&gl=US&persist_hl=1&hl=en'
YoutubeHomePageURL = 'https://www.youtube.com/?persist_gl=1&gl=US&persist_hl=1&hl=en'

TIKTOK_URL= f"https://www.tiktok.com/upload?lang=en"

DOUYIN_URL = "https://creator.douyin.com/creator-micro/home"
DOUYIN_STUDIO_URL = "https://creator.douyin.com/creator-micro/home"
DOUYIN_UPLOAD_URL = "https://creator.douyin.com/creator-micro/content/upload"

DOUYIN_INPUT_FILE_VIDEO='.upload-btn--9eZLd'
DOUYIN_TEXTBOX  ='.notranslate'
DOUYIN_TITLE_COUNTER=500
DOUYIN_INPUT_FILE_THUMBNAIL_EDIT='.mycard-info-text-span--1vcFz'

DOUYIN_INPUT_FILE_THUMBNAIL_OPTION_UPLOAD='.header--3-YMH > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)'
DOUYIN_INPUT_FILE_THUMBNAIL='.upload-btn--9eZLd'
DOUYIN_INPUT_FILE_THUMBNAIL_UPLOAD_TRIM_CONFIRM='button.primary--1AMXd:nth-child(2)'
DOUYIN_INPUT_FILE_THUMBNAIL_UPLOAD_CONFIRM='.submit--3Qt1n'
DOUYIN_LOCATION='.select--148Qe > div:nth-child(1) > div:nth-child(1)'
DOUYIN_LOCATION_RESULT='div.semi-select-option:nth-child(1) > div:nth-child(2) > div:nth-child(1)'
DOUYIN_MINI_SELECT='.select--2uNK1'
DOUYIN_MINI_SELECT_OPTION='.select--2uNK1 > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)'
DOUYIN_MINI='.semi-input'
DOUYIN_MINI_RESULT=''

DOUYIN_HOT_TOPIC='div.semi-select-filterable:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)'
DOUYIN_HOT_TOPIC_RESULT='//html/body/div[7]/div/div/div/div/div/div/div[1]/div[2]/div[1]/div'

DOUYIN_HEJI_SELECT_OPTION='.sel-area--2hBSM > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)'
DOUYIN_HEJI_SELECT_OPTION_VALUE='.sel-area--2hBSM > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > div:nth-child(1)'
DOUYIN_UP2='.semi-switch-native-control'




WEIXIN_URL="https://channels.weixin.qq.com/post/create"
YOUTUBE_URL = "https://www.youtube.com"
YOUTUBE_STUDIO_URL = "https://studio.youtube.com"
YOUTUBE_UPLOAD_URL = "https://www.youtube.com/upload"
USER_WAITING_TIME = 1

# CONTAINERS
avatarButtonSelector='button#avatar-btn'
langMenuItemSelector='yt-multi-page-menu-section-renderer.style-scope:nth-child(3) > div:nth-child(2) > ytd-compact-link-renderer:nth-child(2) > a'
selector_en_path = "ytd-compact-link-renderer.style-scope:nth-child(13) > a:nth-child(1) > tp-yt-paper-item:nth-child(1) > div:nth-child(2) > yt-formatted-string:nth-child(1)"

CONFIRM_CONTAINER='#confirmation-dialog'
youtubeDescriptiontextBoxes = '//*[@id="textbox"]'

TAGS_CONTAINER = '//*[@id="tags-container"]'
ERROR_CONTAINER = '//*[@id="error-message"]'
STATUS_CONTAINER = "//html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[1]/ytcp-video-upload-progress/span"
VIDEO_URL_CONTAINER = "//span[@class='video-url-fadeable style-scope ytcp-video-info']"

TITLE_CONTAINER = "#title-textarea"

DESCRIPTION_CONTAINER = "//*[@id='description-wrapper']"
MORE_OPTIONS_CONTAINER = "#toggle-button > div:nth-child(2)"
TIME_BETWEEN_POSTS = 3600
# COUNTERS
TAGS_COUNTER = 500
TITLE_COUNTER = 100
DESCRIPTION_COUNTER = 5000

# OTHER
HREF = "href"
UPLOADED = "Uploading"
TEXT_INPUT = "#text-input"
NOT_MADE_FOR_KIDS_RADIO_LABEL = "tp-yt-paper-radio-button.ytkc-made-for-kids-select:nth-child(2) > div:nth-child(2) > ytcp-ve:nth-child(1)"
DONE_BUTTON = "//*[@id='done-button']"
NEXT_BUTTON = "//*[@id='next-button']"
PUBLIC_RADIO_LABEL ="tp-yt-paper-radio-button.style-scope:nth-child(19)"
PRIVATE_RADIO_LABEL ="#private-radio-button > div:nth-child(1)"


PUBLIC_BUTTON = "PUBLIC"
PRIVATE_BUTTON = "PRIVATE"
SCHEDULE_BUTTON="#schedule-radio-button"
SCHEDULE_PUBLISH_DATE="//html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[3]/ytcp-visibility-scheduler/div[1]/ytcp-datetime-picker/div/div[1]/ytcp-text-dropdown-trigger/ytcp-dropdown-trigger/div"

RADIO_CONTAINER = "//*[@id='radioContainer']"
INPUT_FILE_VIDEO = "//input[@type='file']"
VIDEO_URL_ELEMENT = "//a[@class='style-scope ytcp-video-info']"
UPLOAD_DIALOG_MODAL = "#dialog.ytcp-uploads-dialog"
INPUT_FILE_THUMBNAIL = "//input[@accept='image/jpeg,image/png']"
VIDEO_NOT_FOUND_ERROR = "Could not find video_id"
NOT_MADE_FOR_KIDS_LABEL = ".made-for-kids-rating-container"
ERROR_SHORT_SELECTOR = '#dialog > div > ytcp-animatable.button-area.metadata-fade-in-section.style-scope.ytcp-uploads-dialog > div > div.left-button-area.style-scope.ytcp-uploads-dialog > div > div.error-short.style-scope.ytcp-uploads-dialog'
ERROR_SHORT_XPATH = '//*[@id="dialog"]/div/ytcp-animatable[2]/div/div[1]/div/div[1]'
UPLOADING_PROGRESS_SELECTOR = '#dialog > div > ytcp-animatable.button-area.metadata-fade-in-section.style-scope.ytcp-uploads-dialog > div > div.left-button-area.style-scope.ytcp-uploads-dialog > ytcp-video-upload-progress > span'
