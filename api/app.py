from urllib.parse import unquote_plus

import validators
from flask import Flask, render_template, request
from hashids import Hashids

app = Flask(__name__)

hashids = Hashids(salt="only you and me")


def decode_string(encoded):
    decoded = "".join([chr(i) for i in hashids.decode(encoded)])
    return decoded


def is_valid_url(url):
    return validators.url(url)


@app.route("/stream", methods=["GET", "POST"])
def stream():
    if request.method == "POST":
        video_url = request.form["url"]
        if video_url != "" and is_valid_url(video_url):
            return render_template("stream.html", video_url=video_url)
        else:
            return render_template(
                "homepage.html", input_value=video_url, invalid_link=True
            )
    else:
        video_url = request.args.get("url")
        if video_url != "":
            return render_template("stream.html", video_url=video_url)
        return "Invalid URL!"


@app.route("/tg/stream")
def tg_stream():
    video_url = request.args.get("url")
    metadata = request.args.get("meta")
    if video_url != "" and metadata != "":
        try:
            data = decode_string(unquote_plus(metadata)).split("|")
            f_name = data[0]
            f_size = data[1]
            f_owner = data[2]
            f_time = data[3]
            return render_template(
                "tg-stream.html",
                video_url=video_url,
                f_name=f_name,
                f_size=f_size,
                f_owner=f_owner,
                f_time=f_time,
            )
        except BaseException:
            return "Invalid Input!"
    return "Invalid URL!"


@app.route("/")
def home_page():
    return render_template("homepage.html")
