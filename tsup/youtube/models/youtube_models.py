from __future__ import annotations

from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class YoutubeID(BaseModel):
    """
    Model for a YouTube ID:
    -----------------------
    videoId : str videoid of the youtube video
    category : str category [video, song, artist, playlist ...]
    resultType : str result type [video, song, artist, playlist ...]
    thumbnail : Optional[List[dict]] thumbnail url / link
    """
    title: Optional[str] = None
    videoId: Optional[str] = None
    category: Optional[str] = None
    resultType: Optional[str] = None
    thumbnail: Optional[List[Dict]] = None

##############
####basic
###############
        info = {
            'id': video_id,
            'title': video_title,
            'formats': formats,
            'thumbnails': thumbnails,
            # The best thumbnail that we are sure exists. Prevents unnecessary
            # URL checking if user don't care about getting the best possible thumbnail
            'thumbnail': traverse_obj(original_thumbnails, (-1, 'url')),
            'description': video_description,
            'channel_id': channel_id,
            'channel_url': format_field(channel_id, None, 'https://www.youtube.com/channel/%s', default=None),
            'duration': duration,
            'view_count': int_or_none(
                get_first((video_details, microformats), (..., 'viewCount'))
                or search_meta('interactionCount')),
            'average_rating': float_or_none(get_first(video_details, 'averageRating')),
            'age_limit': 18 if (
                get_first(microformats, 'isFamilySafe') is False
                or search_meta('isFamilyFriendly') == 'false'
                or search_meta('og:restrictions:age') == '18+') else 0,
            'webpage_url': webpage_url,
            'categories': [category] if category else None,
            'tags': keywords,
            'playable_in_embed': get_first(playability_statuses, 'playableInEmbed'),
            'live_status': live_status,
            'release_timestamp': live_start_time,
            '_format_sort_fields': (  # source_preference is lower for throttled/potentially damaged formats
                'quality', 'res', 'fps', 'hdr:12', 'source', 'vcodec:vp9.2', 'channels', 'acodec', 'lang', 'proto')
        }

###########        subtitles = {}
# 
# sub_name
# sub-langs
# sub-format "srt" or "ass/srt/best"
# sub_content    
############ music



The available fields are:

    id (string): Video identifier
    title (string): Video title
    fulltitle (string): Video title ignoring live timestamp and generic title
    ext (string): Video filename extension
    alt_title (string): A secondary title of the video
    description (string): The description of the video
    display_id (string): An alternative identifier for the video
    uploader (string): Full name of the video uploader
    license (string): License name the video is licensed under
    creator (string): The creator of the video
    timestamp (numeric): UNIX timestamp of the moment the video became available
    upload_date (string): Video upload date in UTC (YYYYMMDD)
    release_timestamp (numeric): UNIX timestamp of the moment the video was released
    release_date (string): The date (YYYYMMDD) when the video was released in UTC
    modified_timestamp (numeric): UNIX timestamp of the moment the video was last modified
    modified_date (string): The date (YYYYMMDD) when the video was last modified in UTC
    uploader_id (string): Nickname or id of the video uploader
    channel (string): Full name of the channel the video is uploaded on
    channel_id (string): Id of the channel
    channel_follower_count (numeric): Number of followers of the channel
    channel_is_verified (boolean): Whether the channel is verified on the platform
    location (string): Physical location where the video was filmed
    duration (numeric): Length of the video in seconds
    duration_string (string): Length of the video (HH:mm:ss)
    view_count (numeric): How many users have watched the video on the platform
    concurrent_view_count (numeric): How many users are currently watching the video on the platform.
    like_count (numeric): Number of positive ratings of the video
    dislike_count (numeric): Number of negative ratings of the video
    repost_count (numeric): Number of reposts of the video
    average_rating (numeric): Average rating give by users, the scale used depends on the webpage
    comment_count (numeric): Number of comments on the video (For some extractors, comments are only downloaded at the end, and so this field cannot be used)
    age_limit (numeric): Age restriction for the video (years)
    live_status (string): One of "not_live", "is_live", "is_upcoming", "was_live", "post_live" (was live, but VOD is not yet processed)
    is_live (boolean): Whether this video is a live stream or a fixed-length video
    was_live (boolean): Whether this video was originally a live stream
    playable_in_embed (string): Whether this video is allowed to play in embedded players on other sites
    availability (string): Whether the video is "private", "premium_only", "subscriber_only", "needs_auth", "unlisted" or "public"
    start_time (numeric): Time in seconds where the reproduction should start, as specified in the URL
    end_time (numeric): Time in seconds where the reproduction should end, as specified in the URL
    extractor (string): Name of the extractor
    extractor_key (string): Key name of the extractor
    epoch (numeric): Unix epoch of when the information extraction was completed
    autonumber (numeric): Number that will be increased with each download, starting at --autonumber-start, padded with leading zeros to 5 digits
    video_autonumber (numeric): Number that will be increased with each video
    n_entries (numeric): Total number of extracted items in the playlist
    playlist_id (string): Identifier of the playlist that contains the video
    playlist_title (string): Name of the playlist that contains the video
    playlist (string): playlist_id or playlist_title
    playlist_count (numeric): Total number of items in the playlist. May not be known if entire playlist is not extracted
    playlist_index (numeric): Index of the video in the playlist padded with leading zeros according the final index
    playlist_autonumber (numeric): Position of the video in the playlist download queue padded with leading zeros according to the total length of the playlist
    playlist_uploader (string): Full name of the playlist uploader
    playlist_uploader_id (string): Nickname or id of the playlist uploader
    webpage_url (string): A URL to the video webpage which if given to yt-dlp should allow to get the same result again
    webpage_url_basename (string): The basename of the webpage URL
    webpage_url_domain (string): The domain of the webpage URL
    original_url (string): The URL given by the user (or same as webpage_url for playlist entries)

All the fields in Filtering Formats can also be used

Available for the video that belongs to some logical chapter or section:

    chapter (string): Name or title of the chapter the video belongs to
    chapter_number (numeric): Number of the chapter the video belongs to
    chapter_id (string): Id of the chapter the video belongs to

Available for the video that is an episode of some series or programme:

    series (string): Title of the series or programme the video episode belongs to
    season (string): Title of the season the video episode belongs to
    season_number (numeric): Number of the season the video episode belongs to
    season_id (string): Id of the season the video episode belongs to
    episode (string): Title of the video episode
    episode_number (numeric): Number of the video episode within a season
    episode_id (string): Id of the video episode

Available for the media that is a track or a part of a music album:

    track (string): Title of the track
    track_number (numeric): Number of the track within an album or a disc
    track_id (string): Id of the track
    artist (string): Artist(s) of the track
    genre (string): Genre(s) of the track
    album (string): Title of the album the track belongs to
    album_type (string): Type of the album
    album_artist (string): List of all artists appeared on the album
    disc_number (numeric): Number of the disc or other physical medium the track belongs to
    release_year (numeric): Year (YYYY) when the album was released

Available only when using --download-sections and for chapter: prefix when using --split-chapters for videos with internal chapters:

    section_title (string): Title of the chapter
    section_number (numeric): Number of the chapter within the file
    section_start (numeric): Start time of the chapter in seconds
    section_end (numeric): End time of the chapter in seconds


### video file meta



    filesize: The number of bytes, if known in advance
    filesize_approx: An estimate for the number of bytes
    width: Width of the video, if known
    height: Height of the video, if known
    aspect_ratio: Aspect ratio of the video, if known
    tbr: Average bitrate of audio and video in KBit/s
    abr: Average audio bitrate in KBit/s
    vbr: Average video bitrate in KBit/s
    asr: Audio sampling rate in Hertz
    fps: Frame rate
    audio_channels: The number of audio channels
    stretched_ratio: width:height of the video's pixels, if not square

    url: Video URL
    ext: File extension
    acodec: Name of the audio codec in use
    vcodec: Name of the video codec in use
    container: Name of the container format
    protocol: The protocol that will be used for the actual download, lower-case (http, https, rtsp, rtmp, rtmpe, mms, f4m, ism, http_dash_segments, m3u8, or m3u8_native)
    language: Language code
    dynamic_range: The dynamic range of the video
    format_id: A short description of the format
    format: A human-readable description of the format
    format_note: Additional info about the format
    resolution: Textual description of width and height



class TopResultSearch(BaseModel):
    """
    Model for a top result search:
    --------------------------------
    artist : Optional[List[dict]] artist of the youtube video
    duration : Optional[str] duration of the youtube video
    """
    id: Optional[YoutubeID] = None
    artist: Union[List[Dict], str] = None
    duration: Optional[str] = None


class VideoResultSearch(BaseModel):
    """
    Model for Category: video
    ----------------------------
    artist : Optional[List[dict, str]] artist of the youtube video
    """
    id: Optional[YoutubeID] = None
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
    id: Optional[YoutubeID] = None
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
    id: Optional[YoutubeID] = None
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
    id: Optional[YoutubeID] = None
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

    id: Optional[YoutubeID] = None
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
