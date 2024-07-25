import re
from urllib.parse import parse_qs, urlparse, urlunparse

import validators
from hashids import Hashids
from pytubefix import YouTube

from config import HASH_SALT, NEW_DL_BASE_URL, OLD_DL_BASE_URL

hashids = Hashids(salt=HASH_SALT)


def hide_name(name):
    words = name.split()
    hidden_words = []
    for word in words:
        if len(word) > 4:
            hidden_word = word[:2] + "***" + word[-2:]
        else:
            hidden_word = word
        hidden_words.append(hidden_word)
    return " ".join(hidden_words)


def decode_string(encoded):
    decoded = "".join([chr(i) for i in hashids.decode(encoded)])
    return decoded


def is_valid_url(url):
    return validators.url(url)


def extract_gdrive_id(gdrive_link):
    match = re.match(
        r"^https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)/?.*$",
        gdrive_link)
    if match:
        return match.group(1)
    query_params = parse_qs(urlparse(gdrive_link).query)
    if "id" in query_params:
        return query_params["id"][0]
    return None

def gen_video_link(video_url):
    parsed_url = urlparse(url)
    if parsed_url.netloc in ["youtube.com", "youtu.be"]:
        yt = YouTube(video_url)
        video_streams = yt.streams.filter(progressive=True)
        return video_streams.get_highest_resolution().url
    elif parsed_url.netloc in ["drive.google.com"]:
        gid = extract_gdrive_id(video_url)
        return f"https://gdl.anshumanpm.eu.org/direct.aspx?id={gid}"
    # For Stream Bot
    elif parsed_url.netloc in OLD_DL_BASE_URL:
        return urlunparse(
        (parsed_url.scheme, NEW_DL_BASE_URL, parsed_url.path,
         parsed_url.params, parsed_url.query, parsed_url.fragment))
    else:
        return video_url
