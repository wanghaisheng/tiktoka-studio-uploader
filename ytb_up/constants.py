# URLS
invalidCharacters = ['<', '>']
closewhen100percentOptions=[0,1,2]
# 0 go next after uploading success,
# 1 go next after processing success,
# 2 go next after copyright check success,
# there are 4 steps:uploading,Upload complete ... Processing will begin shortly,处理中，画质最高可为标清 ... 还剩 8 分钟,Checks complete. No issues found.
# after uploding,there is a video link
#after check, there is a text shows Checks complete. No issues found. and the progress bar of check is selected

availableScheduleTimes=["0:00","0:15","0:30","0:45","1:00","1:15","1:30","1:45","2:00","2:15","2:30","2:45","3:00","3:15","3:30","3:45","4:00","4:15","4:30","4:45","5:00","5:15","5:30","5:45","6:00","6:15","6:30","6:45","7:00","7:15","7:30","7:45","8:00","8:15","8:30","8:45","9:00","9:15","9:30","9:45","10:00","10:15","10:30","10:45","11:00","11:15","11:30","11:45","12:00","12:15","12:30","12:45","13:00","13:15","13:30","13:45","14:00","14:15","14:30","14:45","15:00","15:15","15:30","15:45","16:00","16:15","16:30","16:45","17:00","17:15","17:30","17:45","18:00","18:15","18:30","18:45","19:00","19:15","19:30","19:45","20:00","20:15","20:30","20:45","21:00","21:15","21:30","21:45","22:00","22:15","22:30","22:45","23:00","23:15","23:30","23:45"]
PublishpolicyOptions=[0,1,2]
# 0 -private
# 1-publish
# 2-schedule
VideoLanguageOptions=["Not applicable","Abkhazian","Afar","Afrikaans","Akan","Akkadian","Albanian","American Sign Language","Amharic","Arabic","Aramaic","Armenian","Assamese","Aymara","Azerbaijani","Bambara","Bangla","Bashkir","Basque","Belarusian","Bhojpuri","Bislama","Bodo","Bosnian","Breton","Bulgarian","Burmese","Cantonese","Cantonese (Hong Kong)","Catalan","Cherokee","Chinese","Chinese (China)","Chinese (Hong Kong)","Chinese (Simplified)","Chinese (Singapore)","Chinese (Taiwan)","Chinese (Traditional)","Choctaw","Coptic","Corsican","Cree","Croatian","Czech","Danish","Dogri","Dutch","Dutch (Belgium)","Dutch (Netherlands)","Dzongkha","English","English (Canada)","English (India)","English (Ireland)","English (United Kingdom)","English (United States)","Esperanto","Estonian","Ewe","Faroese","Fijian","Filipino","Finnish","French","French (Belgium)","French (Canada)","French (France)","French (Switzerland)","Fula","Galician","Ganda","Georgian","German","German (Austria)","German (Germany)","German (Switzerland)","Greek","Guarani","Gujarati","Gusii","Haitian Creole","Hakka Chinese","Hakka Chinese (Taiwan)","Haryanvi","Hausa","Hawaiian","Hebrew","Hindi","Hindi (Latin)","Hiri Motu","Hungarian","Icelandic","Igbo","Indonesian","Interlingua","Interlingue","Inuktitut","Inupiaq","Irish","Italian","Japanese","Javanese","Kalaallisut","Kalenjin","Kamba","Kannada","Kashmiri","Kazakh","Khmer","Kikuyu","Kinyarwanda","Klingon","Konkani","Korean","Kurdish","Kyrgyz","Ladino","Lao","Latin","Latvian","Lingala","Lithuanian","Luba-Katanga","Luo","Luxembourgish","Luyia","Macedonian","Maithili","Malagasy","Malay","Malayalam","Maltese","Manipuri","Māori","Marathi","Masai","Meru","Min Nan Chinese","Min Nan Chinese (Taiwan)","Mixe","Mizo","Mongolian","Mongolian (Mongolian)","Nauru","Navajo","Nepali","Nigerian Pidgin","North Ndebele","Northern Sotho","Norwegian","Occitan","Odia","Oromo","Papiamento","Pashto","Persian","Persian (Afghanistan)","Persian (Iran)","Polish","Portuguese","Portuguese (Brazil)","Portuguese (Portugal)","Punjabi","Quechua","Romanian","Romanian (Moldova)","Romansh","Rundi","Russian","Russian (Latin)","Samoan","Sango","Sanskrit","Santali","Sardinian","Scottish Gaelic","Serbian","Serbian (Cyrillic)","Serbian (Latin)","Serbo-Croatian","Sherdukpen","Shona","Sicilian","Sindhi","Sinhala","Slovak","Slovenian","Somali","South Ndebele","Southern Sotho","Spanish","Spanish (Latin America)","Spanish (Mexico)","Spanish (Spain)","Spanish (United States)","Sundanese","Swahili","Swati","Swedish","Tagalog","Tajik","Tamil","Tatar","Telugu","Thai","Tibetan","Tigrinya","Tok Pisin","Toki Pona","Tongan","Tsonga","Tswana","Turkish","Turkmen","Twi","Ukrainian","Urdu","Uyghur","Uzbek","Venda","Vietnamese","Volapük","Võro","Welsh","Western Frisian","Wolaytta","Wolof","Xhosa","Yiddish","Yoruba","Zulu"]
CaptionsCertificationOptions=[0,1,2,3,4,5]

# 0-        None
# 1-This content has never aired on television in the U.S.
# 2-This content has only aired on television in the U.S. without captions
# 3-This content has not aired on U.S. television with captions since September 30, 2012.
# 4-This content does not fall within a category of online programming that requires captions under FCC regulations (47 C.F.R. § 79).
# 5-The FCC and/or U.S. Congress has granted an exemption from captioning requirements for this content.
LicenceTypeOptions=[0,1]
# 0-'Standard YouTube License',
# 1-Creative Commons - Attribution
ShortsremixingTypeOptions=[0,1,2]

# 0-  Allow video and audio remixing
# 1-    Allow only audio remixing
# 2-   Don’t allow remixing 
CategoryOptions=[
    "Autos & Vehicles",
    "Comedy",
    "Education",
    "Entertainment",
    "Film & Animation",
    "Gaming",
    "Howto & Style",
    "Music",
    "News & Politics",
    "Nonprofits & Activism",
    "People & Blogs",
    "Pets & Animals",
    "Science & Technology",
    "Sports",
    "Travel & Events",
]
CommentsRatingsPolicyOptions=[0,1,2,3,4]        
            # 0-Allow all comments
            # 1-Hold potentially inappropriate comments for review
            # 2-Increase strictness
            # 3-Hold all comments for review
            # 4-Disable comments 


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
YOUTUBE_URL = "https://www.youtube.com/?persist_gl=1&gl=US&persist_hl=1&hl=en"
YOUTUBE_STUDIO_URL = "https://studio.youtube.com/?persist_gl=1&gl=US&persist_hl=1&hl=en"
YOUTUBE_UPLOAD_URL = "https://www.youtube.com/upload?persist_gl=1&gl=US&persist_hl=1&hl=en"
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
PROCESSED = "Processing"
CHECKED = "Checking"

TEXT_INPUT = "#text-input"
NOT_MADE_FOR_KIDS_RADIO_LABEL = "tp-yt-paper-radio-button.ytkc-made-for-kids-select:nth-child(2) > div:nth-child(2) > ytcp-ve:nth-child(1)"
DONE_BUTTON = "//*[@id='done-button']"
NEXT_BUTTON = "//*[@id='next-button']"
PUBLIC_RADIO_LABEL ="//*[@id='radioContainer']"
PRIVATE_RADIO_LABEL ="#private-radio-button > div:nth-child(1)"


PUBLIC_BUTTON = "PUBLIC"
PRIVATE_BUTTON = "PRIVATE"
SCHEDULE_BUTTON="#schedule-radio-button"
SCHEDULE_PUBLISH_DATE="//html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[3]/ytcp-visibility-scheduler/div[1]/ytcp-datetime-picker/div/div[1]/ytcp-text-dropdown-trigger/ytcp-dropdown-trigger/div"
SCHEDULE_TIME = "//html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[3]/ytcp-visibility-scheduler/div[1]/ytcp-datetime-picker/div/div[2]/form/ytcp-form-input-container/div[1]/div/tp-yt-paper-input/tp-yt-paper-input-container/div[2]/div/iron-input/input"
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
