# Standard Library

# Third Party
from pytest_httpserver import HTTPServer

# First Party
from seotool.crawl import Crawler


def test_external(httpserver: HTTPServer):
    img = "http://example.com/external1.png"
    httpserver.expect_request("/page1").respond_with_data(
        f'<img src="{img}" />',
        content_type="text/html",
    )
    httpserver.expect_request("/page2").respond_with_data(
        f'<img src="{img}" />',
        content_type="text/html",
    )
    httpserver.expect_request("/").respond_with_data(
        f"""
        <img src="internal.png" />
        <a href="{httpserver.url_for("/page1")}">page1</a>
        <a href="{httpserver.url_for("/page2")}">page2</a>
        """,
        content_type="text/html",
    )

    crawler = Crawler(httpserver.url_for("/"), verbose=False, plugins=["ExternalImagesByURL"])
    (res,) = crawler.asyncio_crawl(save=False)

    expected_data = [{"image": img, "urls": sorted([httpserver.url_for("/page1"), httpserver.url_for("/page2")])}]

    assert res.data == expected_data


def test_not_external(httpserver: HTTPServer):
    httpserver.expect_request("/page1").respond_with_data(
        '<img src="internal.png" />',
        content_type="text/html",
    )
    httpserver.expect_request("/page2").respond_with_data(
        '<img src="internal.png" />',
        content_type="text/html",
    )
    httpserver.expect_request("/").respond_with_data(
        f"""
        <img src="internal.png" />
        <a href="{httpserver.url_for("/page1")}">page1</a>
        <a href="{httpserver.url_for("/page2")}">page2</a>
        """,
        content_type="text/html",
    )

    crawler = Crawler(httpserver.url_for("/"), verbose=False, plugins=["ExternalImagesByURL"])
    (res,) = crawler.asyncio_crawl(save=False)

    assert res.data == []
