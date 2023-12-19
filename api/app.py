import json
import os
from urllib.parse import unquote_plus

import requests
from flask import (
    Flask,
    Response,
    make_response,
    redirect,
    render_template,
    render_template_string,
    request,
)
from hashids import Hashids
from pymongo import MongoClient

from helper import auto_increment_id, decode_string, extract_gdrive_id, is_valid_url

app = Flask(__name__)

hash_salt = os.environ.get("HASH_SALT")
hashids = Hashids(salt=hash_salt)

# db setup
db_url = os.environ.get("MONGO_URL")
client = MongoClient(db_url)
db = client["mydb"]
collection = db["links"]

# Dl Urls
OLD_DL_BASE_URL = os.environ.get("OLD_DL_BASE_URL")
NEW_DL_BASE_URL = os.environ.get("NEW_DL_BASE_URL")


@app.route("/short/v3", methods=["POST"])
def short_api_v3():
    try:
        org_url = request.form["url"]
        url_id = auto_increment_id()
        collection.insert_one({"url_id": url_id, "long_url": org_url})
        hashid = hashids.encode(url_id)
        short_url = f"{request.host_url}tg/{hashid}"
        response_data = {
            "org_url": org_url,
            "short_url": short_url,
        }
        json_data = json.dumps(response_data, indent=4)
        return Response(json_data, content_type="application/json")
    except BaseException:
        response_data = {
            "org_url": url,
            "short_url": "https://www.anshumanpm.eu.org",
        }
        json_data = json.dumps(response_data, indent=4)
        return Response(json_data, content_type="application/json")


@app.route("/tg/stream")
def tg_stream():
    old_video_url = request.args.get("url")
    metadata = request.args.get("meta")
    video_url = old_video_url.replace(OLD_DL_BASE_URL, NEW_DL_BASE_URL)
    if video_url != "" and metadata != "":
        try:
            data = decode_string(unquote_plus(metadata)).split("|")
            f_name = data[0]
            f_size = data[1]
            f_owner = data[2]
            f_time = data[3]
            ads_link = (
                "https://outrightsham.com/rrnx759f?key=d682ebbe96219cb8de23f4109a7b11c8"
            )
            try:
                tg_file_url = data[4]
            except BaseException:
                tg_file_url = "https://telegram.me/AnshumanFileBot"
            return render_template(
                "tg-stream.html",
                video_url=video_url,
                f_name=f_name,
                f_size=f_size,
                f_owner=f_owner,
                f_time=f_time,
                tg_file_url=tg_file_url,
                ads_link=ads_link,
            )
        except BaseException:
            return "Invalid Input!"
    return "Invalid URL!"


@app.route("/tg/<id>")
def tg(id):
    try:
        url_id = hashids.decode(id)[0]
        original_url = collection.find_one({"url_id": url_id})["long_url"]
        html = requests.get(original_url).content.decode("utf-8")
        return render_template_string(html)
    except BaseException:
        return render_template("homepage.html", invalid_link=True)


@app.route("/stream")
def stream():
    video_url = request.args.get("url")
    if is_valid_url(video_url):
        return render_template("stream.html", video_url=video_url)
    else:
        return render_template(
            "homepage.html", input_value=video_url, invalid_link=True
        )


@app.route("/", methods=["GET", "POST"])
def home_page():
    if request.method == "POST":
        video_url = request.form["url"]
        if is_valid_url(video_url):
            if extract_gdrive_id(video_url):
                video_url = f"https://gdl.anshumanpm.eu.org/direct.aspx?id={extract_gdrive_id(video_url)}"
            return render_template("stream.html", video_url=video_url)
        else:
            return render_template(
                "homepage.html", input_value=video_url, invalid_link=True
            )
    return render_template("homepage.html")


@app.errorhandler(Exception)
def page_not_found(e):
    return render_template("error.html")
