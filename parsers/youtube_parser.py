# -*- coding: utf-8 -*-
from urllib.parse import urlparse, parse_qs

# returns youtube video id
def get_yt_video_id(url):
    if url.startswith(("youtu", "www")):
        url = "http://" + url

    query = urlparse(url)

    if "youtube" in query.hostname:
        if query.path == "/watch":
            return parse_qs(query.query)["v"][0]
        elif query.path.startswith(("/embed/", "/v/")):
            return query.path.split("/")[2]
    elif "youtu.be" in query.hostname:
        return query.path[1:]
    else:
        raise ValueError
