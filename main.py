from flask import Flask, render_template, request
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, SSLError, ProxyError
import re


app = Flask(__name__)


def edit_page(response) -> bytearray:
    """
    Read response, modify (add ™ after ich word from six letters
    and modify links for navigate to other pages)
    and encode UTF-8 for return
    :param response: object from url
    :return: html page UTF-8
    """
    data = response.content
    if response.headers['content-type'].split(";")[0] == "text/html":
        data = re.sub(r"<a href=\"https*://", "<a href=\"http://127.0.0.1:8000/", response.text)

        def replicate(match):
            return match.group(0) + "™"
        pattern = re.compile(r"(\b|\s)([a-zA-Z]{6})(\b|\s)")
        data = re.sub(pattern, replicate, data)
        data.encode(encoding="utf-8")
    return data


def get_data(url: str, params: dict) -> render_template:
    """
    Pull data from url, handling exceptions, call edit page or return error page
    :param url: with http:// or https://
    :param params: use for add params to url
    :return: modify url page or error page
    """
    headers = request.headers
    try:
        response = requests.get(url, headers=headers, params=params)
        return edit_page(response)
    except ConnectionError or HTTPError or Timeout or SSLError or ProxyError as e:
        return render_template("error.html", url=url, error=e)


@app.route("/<path:url>", methods=["GET", "POST"])
def proxy(url: str):
    """
    If url not start from http:// or https://, first time add to url http://
    params - calling from flask request, and get dict of user input url params
    :param url: any url
    :return: modify page with ™ and other links
    """
    params = request.args
    if url[:7] not in ["https:/", "http://"]:
        url = "http://" + url
    return get_data(url, params)


@app.route("/", methods=["GET", "POST"])
def index() -> render_template:
    """
    Its render of main page
    :return: main page index.html
    """
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=8000, debug=True, host="0.0.0.0")
