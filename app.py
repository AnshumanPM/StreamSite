import json
from urllib.parse import quote_plus, unquote_plus

from flask import Flask, Response, redirect, render_template, request

from config import NEW_DL_BASE_URL, OLD_DL_BASE_URL_1, OLD_DL_BASE_URL_2
from database import collection, new_collection
from helper import decode_string, extract_gdrive_id, hashids, is_valid_url

app = Flask(__name__)
app.jinja_env.filters["quote_plus"] = lambda u: quote_plus(u)


@app.route("/short/v4", methods=["POST"])
def short_api_v4():
    try:
        url_id = request.form["url_id"]
        dl_url = request.form["dl_url"]
        metadata = request.form["metadata"]
        new_collection.insert_one(
            {"url_id": url_id, "dl_url": dl_url, "metadata": metadata}
        )
        short_url = f"https://stream.anshbotzone.tech/view/{url_id}"
        response_data = {
            "status": 200,
            "url_id": url_id,
            "short_url": short_url,
        }
        json_data = json.dumps(response_data, indent=4)
        return Response(json_data, content_type="application/json")
    except BaseException:
        response_data = {
            "status": 400,
            "url_id": 0,
            "short_url": "https://stream.anshbotzone.tech/",
        }
        json_data = json.dumps(response_data, indent=4)
        return Response(json_data, content_type="application/json")


@app.route("/tg/stream")
def tg_stream():
    old_video_url = request.args.get("url")
    metadata = request.args.get("meta")
    video_url = old_video_url.replace(OLD_DL_BASE_URL_1, NEW_DL_BASE_URL).replace(
        OLD_DL_BASE_URL_2, NEW_DL_BASE_URL
    )
    if video_url != "" and metadata != "":
        try:
            data = decode_string(unquote_plus(metadata)).split("|")
            f_name = data[0]
            f_size = data[1]
            f_owner = data[2]
            f_time = data[3]
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
            )
        except BaseException:
            return render_template(
                "homepage.html", error_msg="Link Expired or Invalid Link"
            )
    return render_template("homepage.html", error_msg="Link Expired or Invalid Link")


# Again Added For Old Link
@app.route("/tg/<id>")
def tg(id):
    try:
        url_id = hashids.decode(id)[0]
        original_url = collection.find_one({"url_id": url_id})["long_url"]
        return redirect(original_url)
    except BaseException:
        return render_template("homepage.html", error_msg="Invalid Video Link")


@app.route("/view/<url_id>")
def view(url_id):
    try:
        obj = new_collection.find_one({"url_id": url_id})
        old_video_url = obj["dl_url"]
        metadata = obj["metadata"]
        video_url = old_video_url.replace(OLD_DL_BASE_URL_1, NEW_DL_BASE_URL).replace(
            OLD_DL_BASE_URL_2, NEW_DL_BASE_URL
        )
        data = decode_string(unquote_plus(metadata)).split("|")
        f_name = data[0]
        f_size = data[1]
        f_owner = data[2]
        f_time = data[3]
        tg_file_url = data[4]
        return render_template(
            "tg-stream.html",
            video_url=video_url,
            f_name=f_name,
            f_size=f_size,
            f_owner=f_owner,
            f_time=f_time,
            tg_file_url=tg_file_url,
        )
    except BaseException:
        return render_template(
            "homepage.html", error_msg="Link Expired or Invalid Link"
        )


@app.route("/stream")
def stream():
    video_url = request.args.get("url")
    return render_template("stream.html", video_url=video_url)


# For A Ads Verification


@app.route("/ads")
def ads_view():
    return render_template("ads.html")


@app.route("/", methods=["GET", "POST"])
def home_page():
    if request.method == "POST":
        video_url = request.form["url"]
        if is_valid_url(video_url):
            if gid := extract_gdrive_id(video_url):
                video_url = f"https://gdl.anshumanpm.eu.org/direct.aspx?id={gid}"
            return render_template("stream.html", video_url=video_url)
        else:
            return render_template(
                "homepage.html", input_value=video_url, error_msg="Invalid Video Link"
            )
    return render_template("homepage.html")


@app.errorhandler(Exception)
def page_not_found(e):
    return render_template("error.html")
