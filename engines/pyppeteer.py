# Third Party
from pyppeteer import launch

# First Party
from engines import engine, response


class pyppeteer(engine):
    browser = None

    async def get(self, url: str, **kwargs) -> response:
        page = await self.browser.newPage()
        result = await page.goto(url, {"waitUntil": "domcontentloaded"})

        responseObj = response(
            headers=result.headers,
            status_code=result.status,
            url=result.url,
            body=await page.content(),
        )

        await page.close()

        return responseObj

    async def __aenter__(self):
        if self.browser is None:
            self.browser = await launch()

        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.browser is not None:
            await self.browser.close()
            self.browser = None
