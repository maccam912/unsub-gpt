import structlog
from playwright.async_api import Page, Playwright, async_playwright

log = structlog.get_logger()


class Browser:
    playwright: Playwright
    page: Page

    def __init__(self) -> None:
        pass

    async def start(self) -> None:
        self.playwright = await async_playwright().start()
        firefox = self.playwright.firefox  # or "firefox" or "webkit".
        browser = await firefox.launch()
        page = await browser.new_page()
        await page.set_viewport_size({"width": 1920, "height": 1080})
        self.page = page

    async def pause_for_load(self):
        log.debug("Pause for effect...")
        await self.page.wait_for_load_state("networkidle", timeout=5000)

    async def go_to(self, url: str) -> None:
        await self.pause_for_load()
        log.debug("Going to page", url=url)
        await self.page.goto(url)

    async def snapshot(self):
        await self.pause_for_load()
        return await self.page.accessibility.snapshot()

    async def screenshot(self):
        await self.pause_for_load()
        log.debug("Taking screenshot")
        await self.page.screenshot(path="example.png")

    async def click(self, role: str, text: str) -> None:
        await self.pause_for_load()
        log.debug("Clicking element", element_text=text)
        await self.page.get_by_role(role, name=text).click(timeout=3000)

    async def close(self) -> None:
        await self.pause_for_load()
        log.debug("Closing")
        await self.playwright.stop()
