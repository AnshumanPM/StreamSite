from urllib.parse import quote_plus, unquote_plus, unquote

from fastapi import FastAPI, Form, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from database import collection, new_collection
from helper import (
    decode_string,
    decrypt_string,
    gen_video_link,
    hashids,
    hide_name,
    is_valid_url,
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
templates.env.filters["quote_plus"] = lambda u: quote_plus(u)


@app.post("/short/v4")
async def short_api_v4(
    url_id: str = Form(...), dl_url: str = Form(...), metadata: str = Form(...)
):
    try:
        new_collection.insert_one(
            {"url_id": url_id, "dl_url": dl_url, "metadata": metadata}
        )
        short_url = f"https://stream.anshbotzone.com/view/{url_id}"
        return JSONResponse(
            content={
                "status": 200,
                "url_id": url_id,
                "short_url": short_url,
            }
        )
    except Exception:
        return JSONResponse(
            content={
                "status": 400,
                "url_id": 0,
                "short_url": "https://stream.anshbotzone.com/",
            },
            status_code=400,
        )


@app.post("/short/v5")
async def short_api_v5(
    url_id: str = Form(...), dl_url: str = Form(...), metadata: str = Form(...)
):
    try:
        new_collection.insert_one(
            {"url_id": url_id, "dl_url": dl_url, "metadata": metadata}
        )
        short_url = f"https://stream.anshbotzone.com/play/{url_id}"
        return JSONResponse(
            content={
                "status": 200,
                "url_id": url_id,
                "short_url": short_url,
            }
        )
    except Exception:
        return JSONResponse(
            content={
                "status": 400,
                "url_id": 0,
                "short_url": "https://stream.anshbotzone.com/",
            },
            status_code=400,
        )


@app.get("/tg/stream", response_class=HTMLResponse)
async def tg_stream(
    request: Request,
    url: str = Query(..., alias="url"),
    meta: str = Query(..., alias="meta"),
):
    video_url = await gen_video_link(url)
    if not video_url or not meta:
        return templates.TemplateResponse(
            "homepage.html",
            {"request": request, "error_msg": "Link Expired or Invalid Link"},
        )

    try:
        decoded_meta = await decode_string(unquote_plus(meta))
        data = decoded_meta.split("|")
        f_name = await hide_name(data[0])
        f_size = data[1]
        f_owner = await hide_name(data[2])
        f_time = data[3]
        tg_file_url = (
            data[4] if len(data) > 4 else "https://telegram.me/AnshumanFileBot"
        )

        return templates.TemplateResponse(
            "tg-stream.html",
            {
                "request": request,
                "video_url": video_url,
                "f_name": f_name,
                "f_size": f_size,
                "f_owner": f_owner,
                "f_time": f_time,
                "tg_file_url": tg_file_url,
            },
        )
    except Exception as e:
        return templates.TemplateResponse(
            "homepage.html",
            {
                "request": request,
                "error_msg": f"Link Expired or Invalid Link \n\nError {e}",
            },
        )


@app.get("/tg/play", response_class=HTMLResponse)
async def tg_stream_2(
    request: Request,
    url: str = Query(..., alias="url"),
    meta: str = Query(..., alias="meta"),
):
    try:
        video_url = await decrypt_string(unquote(url))
        video_url = await gen_video_link(video_url)
        if not video_url or not meta:
            return templates.TemplateResponse(
                "homepage.html",
                {"request": request, "error_msg": "Link Expired or Invalid Link"},
            )

        decoded_meta = await decrypt_string(unquote(meta))
        data = decoded_meta.split("|")
        f_name = await hide_name(data[0])
        f_size = data[1]
        f_owner = await hide_name(data[2])
        f_time = data[3]
        tg_file_url = (
            data[4] if len(data) > 4 else "https://telegram.me/AnshumanFileBot"
        )

        return templates.TemplateResponse(
            "tg-stream.html",
            {
                "request": request,
                "video_url": video_url,
                "f_name": f_name,
                "f_size": f_size,
                "f_owner": f_owner,
                "f_time": f_time,
                "tg_file_url": tg_file_url,
            },
        )
    except Exception as e:
        return templates.TemplateResponse(
            "homepage.html",
            {
                "request": request,
                "error_msg": f"Link Expired or Invalid Link \n\nError {e}",
            },
        )


@app.get("/tg/{id}")
async def tg(id: str):
    try:
        url_id = hashids.decode(id)[0]
        original_url = collection.find_one({"url_id": url_id})["long_url"]
        return RedirectResponse(url=original_url)
    except Exception:
        return templates.TemplateResponse(
            "homepage.html", {"request": Request, "error_msg": "Invalid Video Link"}
        )


@app.get("/view/{url_id}", response_class=HTMLResponse)
async def view(request: Request, url_id: str = Path(...)):
    try:
        obj = new_collection.find_one({"url_id": url_id})
        if not obj:
            raise ValueError("Document not found")

        video_url = await gen_video_link(obj["dl_url"])
        if not video_url:
            raise ValueError("Invalid video URL")

        decoded_meta = await decode_string(unquote_plus(obj["metadata"]))
        data = decoded_meta.split("|")
        f_name = await hide_name(data[0])
        f_size = data[1]
        f_owner = await hide_name(data[2])
        f_time = data[3]
        tg_file_url = (
            data[4] if len(data) > 4 else "https://telegram.me/AnshumanFileBot"
        )

        return templates.TemplateResponse(
            "tg-stream.html",
            {
                "request": request,
                "video_url": video_url,
                "f_name": f_name,
                "f_size": f_size,
                "f_owner": f_owner,
                "f_time": f_time,
                "tg_file_url": tg_file_url,
            },
        )
    except Exception as e:
        return templates.TemplateResponse(
            "homepage.html",
            {
                "request": request,
                "error_msg": f"Link Expired or Invalid Link \n\nError {e}",
            },
        )


@app.get("/play/{url_id}", response_class=HTMLResponse)
async def view(request: Request, url_id: str = Path(...)):
    try:
        obj = new_collection.find_one({"url_id": url_id})
        if not obj:
            raise ValueError("Document not found")

        video_url = await decrypt_string(obj["dl_url"])
        video_url = await gen_video_link(video_url)
        if not video_url:
            raise ValueError("Invalid video URL")

        decoded_meta = await decrypt_string(obj["metadata"])
        data = decoded_meta.split("|")
        f_name = await hide_name(data[0])
        f_size = data[1]
        f_owner = await hide_name(data[2])
        f_time = data[3]
        tg_file_url = (
            data[4] if len(data) > 4 else "https://telegram.me/AnshumanFileBot"
        )

        return templates.TemplateResponse(
            "tg-stream.html",
            {
                "request": request,
                "video_url": video_url,
                "f_name": f_name,
                "f_size": f_size,
                "f_owner": f_owner,
                "f_time": f_time,
                "tg_file_url": tg_file_url,
            },
        )
    except Exception as e:
        return templates.TemplateResponse(
            "homepage.html",
            {
                "request": request,
                "error_msg": f"Link Expired or Invalid Link \n\nError {e}",
            },
        )


@app.get("/stream", response_class=HTMLResponse)
async def stream(request: Request, url: str = Query(...)):
    return templates.TemplateResponse(
        "stream.html", {"request": request, "video_url": url}
    )


@app.api_route("/", methods=["GET", "POST"], response_class=HTMLResponse)
async def home_page(request: Request):
    if request.method == "POST":
        form_data = await request.form()
        video_url = form_data.get("url")

        if await is_valid_url(video_url):
            processed_url = await gen_video_link(video_url)
            return templates.TemplateResponse(
                "stream.html", {"request": request, "video_url": processed_url}
            )
        return templates.TemplateResponse(
            "homepage.html",
            {
                "request": request,
                "input_value": video_url,
                "error_msg": "Invalid Video Link",
            },
        )

    # GET request
    return templates.TemplateResponse("homepage.html", {"request": request})


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return templates.TemplateResponse(
        "homepage.html", {"request": request, "error_msg": str(exc)}, status_code=500
    )
