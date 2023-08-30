from __future__ import annotations
from datetime import datetime

from typing import Dict, List, Optional, Union

from pydantic import BaseModel
from tsup.youtube.models.youtube_enum import availableScheduleTimeSlotType,CategoryType, CommentsRatingsPolicyType, LicenceType, ShortsremixingType, VideoLanguageType, VideoType,PublishpolicyType,CaptionsCertificationType




class VideoFileMeta(BaseModel):

### video file meta
    id:int

    video_filesize: Optional[str] = None
    video_filesize_approx: Optional[str] = None
    video_width: Optional[str] = None
    video_height: Optional[str] = None
    video_aspect_ratio: Optional[str] = None
    video_tbr: Optional[str] = None
    video_abr: Optional[str] = None
    video_vbr: Optional[str] = None
    video_asr: Optional[str] = None
    video_fps: Optional[str] = None
    video_audio_channels: Optional[str] = None
    video_stretched_ratio: Optional[str] = None

    # video_ext (string): Video filename extension

    # filesize: The number of bytes, if known in advance
    # filesize_approx: An estimate for the number of bytes
    # width: Width of the video, if known
    # height: Height of the video, if known
    # aspect_ratio: Aspect ratio of the video, if known
    # tbr: Average bitrate of audio and video in KBit/s
    # abr: Average audio bitrate in KBit/s
    # vbr: Average video bitrate in KBit/s
    # asr: Audio sampling rate in Hertz
    # fps: Frame rate
    # audio_channels: The number of audio channels
    # stretched_ratio: width:height of the video's pixels, if not square
    video_acodec: Optional[str] = None
    video_vcodec: Optional[str] = None    
    video_container: Optional[str] = None
    video_language: Optional[str] = None
    video_dynamic_range: Optional[str] = None
    video_format_id: Optional[str] = None
    video_format: Optional[str] = None
    video_format_note: Optional[str] = None
    video_resolution: Optional[str] = None
    video_stretched_ratio: Optional[str] = None
    video_stretched_ratio: Optional[str] = None
    video_stretched_ratio: Optional[str] = None
    video_stretched_ratio: Optional[str] = None

    # url: Video URL
    # ext: File extension
    # acodec: Name of the audio codec in use
    # vcodec: Name of the video codec in use
    # container: Name of the container format
    # protocol: The protocol that will be used for the actual download, lower-case (http, https, rtsp, rtmp, rtmpe, mms, f4m, ism, http_dash_segments, m3u8, or m3u8_native)
    # language: Language code
    # dynamic_range: The dynamic range of the video
    # format_id: A short description of the format
    # format: A human-readable description of the format
    # format_note: Additional info about the format
    # resolution: Textual description of width and height
class Account(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    recoveryemail: Optional[str] = None

    cookie: Optional[str] = None
    channels: Optional[Channel] = None


    
class Uploader(BaseModel):
    uploader_id: Optional[str] = None
    uploader_name: Optional[str] = None
class Channel(BaseModel):
    channel_name: Optional[str] = None
    channel_id: Optional[str] = None
    channel_follower_count: Optional[str] = None
    channel_is_verified: Optional[str] = None
    channel_is_monitized: Optional[str] = None
    channel_url: Optional[str] = None

    uploader_id: Optional[str] = None
    uploader_name: Optional[str] = None
    uploader_url: Optional[str] = None
                # 'uploader_name': 'Philipp Hagemeister',
                # 'uploader_url': 'https://www.youtube.com/@PhilippHagemeister',
                # 'uploader_id': '@PhilippHagemeister',
                #     'channel_name': 'Philipp Hagemeister',
                # 'channel_id': 'UCLqxVugv74EIW3VWh2NOa3Q',
                # 'channel_url': r're:https?://(?:www\.)?youtube\.com/channel/UCLqxVugv74EIW3VWh2NOa3Q',                'channel': 'Philipp Hagemeister',
                # 'channel_id': 'UCLqxVugv74EIW3VWh2NOa3Q',
                # 'channel_url': r're:https?://(?:www\.)?youtube\.com/channel/UCLqxVugv74EIW3VWh2NOa3Q',

    # uploader_id (string): Nickname or id of the video uploader
    # channel (string): Full name of the channel the video is uploaded on
    # channel_id (string): Id of the channel
    # channel_follower_count (numeric): Number of followers of the channel
    # channel_is_verified (boolean): Whether the channel is verified on the platform    
class altMeta(BaseModel):
    lang: Optional[str] = None
    title: Optional[str] = None
    video_description: Optional[str] = None
    subtitle_name: Optional[str] = None
    subtitle_format: Optional[str] = None
    subtitle_contents: Optional[str] = None
class LiveMeta(BaseModel):
    playlist_id: Optional[str] = None
    live_status: Optional[str] = None
    is_live: Optional[str] = None
    was_live: Optional[bool] = None

    # live_status (string): One of "not_live", "is_live", "is_upcoming", "was_live", "post_live" (was live, but VOD is not yet processed)
    # is_live (boolean): Whether this video is a live stream or a fixed-length video
    # was_live (boolean): Whether this video was originally a live stream


class PlaylistMeta(BaseModel):
    playlist_id: Optional[str] = None
    n_entries: Optional[str] = None
    playlist_title: Optional[str] = None
    playlist_count: Optional[str] = None
    playlist_index: Optional[str] = None
    playlist_autonumber: Optional[str] = None
    playlist_uploader: Optional[Uploader] = None

    # n_entries (numeric): Total number of extracted items in the playlist
    # playlist_id (string): Identifier of the playlist that contains the video
    # playlist_title (string): Name of the playlist that contains the video
    # playlist_count (numeric): Total number of items in the playlist. May not be known if entire playlist is not extracted
    # playlist_index (numeric): Index of the video in the playlist padded with leading zeros according the final index
    # playlist_autonumber (numeric): Position of the video in the playlist download queue padded with leading zeros according to the total length of the playlist
    # playlist_uploader (string): Full name of the playlist uploader
    # playlist_uploader_id (string): Nickname or id of the playlist uploader




class logicalChapterMeta(BaseModel):
    chapter_name: Optional[str] = None
    chapter_title: Optional[str] = None
    chapter_number: Optional[int] = None
    chapter_id: Optional[str] = None


# Available for the video that belongs to some logical chapter or section:

#     chapter (string): Name or title of the chapter the video belongs to
#     chapter_number (numeric): Number of the chapter the video belongs to
#     chapter_id (string): Id of the chapter the video belongs to
class SeriesProgrammeMeta(BaseModel):
    series_title: Optional[str] = None
    programme_title: Optional[str] = None
    season_title: Optional[str] = None
    season_number: Optional[int] = None
    season_id: Optional[str] = None
    episode: Optional[str] = None
    episode_number: Optional[str] = None
    episode_id: Optional[str] = None


# Available for the video that is an episode of some series or programme:

#     series (string): Title of the series or programme the video episode belongs to
#     season (string): Title of the season the video episode belongs to
#     season_number (numeric): Number of the season the video episode belongs to
#     season_id (string): Id of the season the video episode belongs to
#     episode (string): Title of the video episode
#     episode_number (numeric): Number of the video episode within a season
#     episode_id (string): Id of the video episode
class MusicAlbumMeta(BaseModel):
    track_title: Optional[str] = None
    track_number: Optional[str] = None
    track_id: Optional[str] = None
    track_artist: Optional[str] = None
    album_title: Optional[str] = None
    album_type: Optional[str] = None
    album_artist: Optional[str] = None
    disc_number: Optional[str] = None
    release_year: Optional[str] = None

# Available for the media that is a track or a part of a music album:

#     track (string): Title of the track
#     track_number (numeric): Number of the track within an album or a disc
#     track_id (string): Id of the track
#     artist (string): Artist(s) of the track
#     genre (string): Genre(s) of the track
#     album (string): Title of the album the track belongs to
#     album_type (string): Type of the album
#     album_artist (string): List of all artists appeared on the album
#     disc_number (numeric): Number of the disc or other physical medium the track belongs to
#     release_year (numeric): Year (YYYY) when the album was released


class SectionMeta(BaseModel):
    section_title: Optional[str] = None
    section_number: Optional[str] = None
    section_start: Optional[str] = None
    section_end: Optional[str] = None    

# Available only when using --download-sections and for chapter: prefix when using --split-chapters for videos with internal chapters:

#     section_title (string): Title of the chapter
#     section_number (numeric): Number of the chapter within the file
#     section_start (numeric): Start time of the chapter in seconds
#     section_end (numeric): End time of the chapter in seconds




class YoutubeVideo(BaseModel):
    """
    Model for a YouTube video:
    -----------------------
    id: int serial id for internal managment

    video_id : str public videoid of the youtube video
    video_type : str category [video, song, artist, playlist ...]
    thumbnail : Optional[List[dict]] thumbnail url / link
    """
    id: int
    video_title: Optional[str] = None
    video_id: Optional[str] = None
    video_type: Optional[VideoType] = None
    video_local_path: str
    video_ext: str
    video_filename: str    
    thumbnail_url: Optional[str] = None
    thumbnail_locapath: Optional[str] = None
    video_description: Optional[str] = None
    channel_id: Optional[str] = None
    channel_url: Optional[str] = None
    duration: Optional[str] = None
    is_age_restriction: Optional[bool] = None
    is_not_for_kid: Optional[bool] = None
    is_paid_promotion: Optional[bool] = None
    is_automatic_chapters: Optional[bool] = None
    is_featured_place: Optional[bool] = None
    video_language: Optional[VideoLanguageType] = None
    captions_certification: Optional[CaptionsCertificationType] = None
    is_automatic_chapters: Optional[str] = None
    shorts_remixing_type: Optional[ShortsremixingType] = None
    comments_ratings_policy: Optional[CommentsRatingsPolicyType] = None
    is_show_howmany_likes: Optional[str] = None
    is_automatic_chapters: Optional[str] = None
    is_allow_embedding: Optional[bool] = None
    is_publish_to_subscriptions_feed_notify: Optional[bool] = None


    first_comment: Optional[str] = None
    subtitles:Optional[altMeta]=None


    # isAgeRestriction: Optional[bool] = False,
    # isNotForKid: Optional[bool] = False,
    # isPaidpromotion: Optional[bool] = False,
    # isAutomaticChapters: Optional[bool] = True,
    # isFeaturedPlace: Optional[bool] = True,
    # VideoLanguage: Optional[str] = None,
    # # input language str and get index in the availableLanguages list
    # CaptionsCertification: Optional[int] = 0,
    # # parse from video metadata  using ffmpeg
    # VideoRecordingdate: Optional[str] = None,
    # VideoRecordinglocation: Optional[str] = None,
    # LicenceType: Optional[int] = 0,
    # isAllowEmbedding: Optional[bool] = True,
    # isPublishToSubscriptionsFeedNotify: Optional[bool] = True,
    # ShortsremixingType: Optional[int] = 0,
    # Category: Optional[str] = None,
    # CommentsRatingsPolicy: Optional[int] = 1,
    # isShowHowManyLikes: Optional[bool] = True,


    # id (string): Video identifier
    # title (string): Video title
    # fulltitle (string): Video title ignoring live timestamp and generic title
    # ext (string): Video filename extension
    # alt_title (string): A secondary title of the video
    # description (string): The description of the video
    # display_id (string): An alternative identifier for the video
    # uploader (string): Full name of the video uploader
    # license (string): License name the video is licensed under
    # creator (string): The creator of the video
    # playable_in_embed (string): Whether this video is allowed to play in embedded players on other sites
            # return {
            # '_type': 'url',
            # 'ie_key': YoutubeIE.ie_key(),
            # 'id': video_id,
            # 'url': url,
            # 'title': title,
            # 'description': description,
            # 'duration': duration,
            # 'channel_id': channel_id,
            # 'channel': channel,
            # 'channel_url': f'https://www.youtube.com/channel/{channel_id}' if channel_id else None,
            # 'uploader': channel,
            # 'uploader_id': channel_handle,
            # 'uploader_url': format_field(channel_handle, None, 'https://www.youtube.com/%s', default=None),
            # 'thumbnails': self._extract_thumbnails(renderer, 'thumbnail'),
            # 'timestamp': (self._parse_time_text(time_text)
            #               if self._configuration_arg('approximate_date', ie_key=YoutubeTabIE)
            #               else None),
            # 'release_timestamp': scheduled_timestamp,
            # 'availability':
            #     'public' if self._has_badge(badges, BadgeType.AVAILABILITY_PUBLIC)
            #     else self._availability(
            #         is_private=self._has_badge(badges, BadgeType.AVAILABILITY_PRIVATE) or None,
            #         needs_premium=self._has_badge(badges, BadgeType.AVAILABILITY_PREMIUM) or None,
            #         needs_subscription=self._has_badge(badges, BadgeType.AVAILABILITY_SUBSCRIPTION) or None,
            #         is_unlisted=self._has_badge(badges, BadgeType.AVAILABILITY_UNLISTED) or None),
            # view_count_field: view_count,
            # 'live_status': live_status,
            # 'channel_is_verified': True if self._has_badge(owner_badges, BadgeType.VERIFIED) else None
    
    
    is_video_monitized: Optional[str] = None

    webpage_url: Optional[str] = None
    categories: Optional[CategoryType] = None
    playable_in_embed: Optional[str] = None
    tags: list[str] = ['tiktoka studio']
    license_type: Optional[LicenceType] = 0
    video_film_date: Optional[datetime] = None
    video_film_date_string: Optional[str] = None
    
    video_film_location: Optional[str] = None
    video_duration: Optional[int] = None
    video_duration_string: Optional[str] = None
    # location (string): Physical location where the video was filmed
    # duration (numeric): Length of the video in seconds
    # duration_string (string): Length of the video (HH:mm:ss)

    publish_policy: Optional[PublishpolicyType] = None
    # availability (string): Whether the video is "private", "premium_only", "subscriber_only", "needs_auth", "unlisted" or "public"

    timestamp: Optional[int] = None
    upload_date: Optional[datetime] = None
    upload_date_string: Optional[str] = None

    release_timestamp: Optional[int] = None
    release_date: Optional[datetime] = None
    release_date_string: Optional[str] = None
    release_date_hour: Optional[availableScheduleTimeSlotType] = None

    modified_timestamp: Optional[int] = None
    modified_date: Optional[datetime] = None
    modified_date_string: Optional[str] = None

    # timestamp (numeric): UNIX timestamp of the moment the video became available
    # upload_date (string): Video upload date in UTC (YYYYMMDD)
    # release_timestamp (numeric): UNIX timestamp of the moment the video was released
    # release_date (string): The date (YYYYMMDD) when the video was released in UTC
    # modified_timestamp (numeric): UNIX timestamp of the moment the video was last modified
    # modified_date (string): The date (YYYYMMDD) when the video was last modified in UTC
    view_count: Optional[int] = None
    concurrent_view_count: Optional[int] = None
    like_count: Optional[int] = None
    dislike_count: Optional[int] = None
    repost_count: Optional[int] = None
    average_rating: Optional[int] = None
    comment_count: Optional[int] = None

    # view_count (numeric): How many users have watched the video on the platform
    # concurrent_view_count (numeric): How many users are currently watching the video on the platform.
    # like_count (numeric): Number of positive ratings of the video
    # dislike_count (numeric): Number of negative ratings of the video
    # repost_count (numeric): Number of reposts of the video
    # average_rating (numeric): Average rating give by users, the scale used depends on the webpage
    # comment_count (numeric): Number of comments on the video (For some extractors, comments are only downloaded at the end, and so this field cannot be used)
    
    video_file_meta:Optional[VideoFileMeta]=None

    live_meta:Optional[LiveMeta]=None
    music_meta:Optional[MusicAlbumMeta]=None
    playlist_meta:Optional[PlaylistMeta]=None
    series_programme_meta:Optional[SeriesProgrammeMeta]=None
    logical_chapter_meta:Optional[logicalChapterMeta]=None

    
############ music
class UploadSetting(BaseModel):
    id:int
    proxy_option: Optional[int] = None
    headless: bool = False
    debug: bool = True
    use_stealth_js: bool = False
    recordvideo: bool = True
    root_profile_directory: Optional[int] = None
    CHANNEL_COOKIES: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    browserType: str = "firefox",
    closewhen100percent: str ="go next after copyright check success"
class UploadSession(BaseModel):
    id:int
    video:YoutubeVideo
    status:Optional[int]=0
    timestamp: Optional[int] = None
    upload_date: Optional[datetime] = None
    upload_date_string: Optional[str] = None    

class TopResultSearch(BaseModel):
    """
    Model for a top result search:
    --------------------------------
    artist : Optional[List[dict]] artist of the youtube video
    duration : Optional[str] duration of the youtube video
    """
    id: Optional[YoutubeVideo] = None
    artist: Union[List[Dict], str] = None
    duration: Optional[str] = None


class VideoResultSearch(BaseModel):
    """
    Model for Category: video
    ----------------------------
    artist : Optional[List[dict, str]] artist of the youtube video
    """
    id: Optional[YoutubeVideo] = None
    artist: Union[List[Dict], str] = None


class SongresultSearch(BaseModel):
    """
    Model for Category: song
    ----------------------------
    artist : Optional[List[dict, str]] artist of the youtube video
    album : Optional[List[dict, str]] album of the youtube video
    duration : Optional[str] duration of the youtube video
    isExplicit : Optional[bool] is explicit
    """
    id: Optional[YoutubeVideo] = None
    duration: Optional[str] = None
    artist: Union[List[Dict], str] = None
    album: Union[List[Dict], str, Dict] = None
    isExplicit: Optional[bool] = None


class Al1bumsSearchResult(BaseModel):
    """
    Model for Category: album
    ----------------------------
    browserID : str browser id of the youtube video
    type : str album type
    artist : Optional[List[dict, str]] artist of the youtube video
    isExplicit : Optional[bool] is explicit
    """
    id: Optional[YoutubeVideo] = None
    browseId: Optional[str] = None
    type: Optional[str] = None
    artist: Union[List[Dict], str] = None
    isExplicit: Optional[bool] = None


class PlaylistSearchResult(BaseModel):
    """
    Model for Category: playlist
    ----------------------------
    browserID : str browser id of the youtube video
    type : str playlist type
    """
    id: Optional[YoutubeVideo] = None
    author: Optional[str] = None
    itemCount: Optional[int] = None
    browseId: Optional[str] = None
    type: Optional[str] = None


class ArtistsSearchResult(BaseModel):
    """
    Model for Category: artist
    ----------------------------
    browserID : str browser id of the youtube video
    artist : Optional[List[dict, str]] artist of the youtube video
    shuffle : Optional[bool] is shuffle
    radioId : Optional[str] radio id
    """

    id: Optional[YoutubeVideo] = None
    browseId: Optional[str] = None
    artist: Union[List[Dict], str] = None
    shuffle: Optional[str] = None
    radioID: Optional[str] = None


class YoutubeSearchItems(BaseModel):
    """
    Model for a youtube search items:
    --------------------------------
    items : Dict[str, List] list of youtube search items
    """
    items: Dict[str, List] = None
