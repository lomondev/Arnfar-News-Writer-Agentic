import sys, asyncio
from playwright.async_api import async_playwright
async def main(url, out, w, h):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": w, "height": h}, device_scale_factor=2, color_scheme="dark")
        await pg.goto(url, wait_until="networkidle", timeout=45000)
        await pg.wait_for_timeout(1500)
        await pg.screenshot(path=out)
        await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])))
