from datetime import datetime
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, Sequence
from models import CapturedRequest
from sqlalchemy.ext.asyncio import AsyncSession
from playwright.async_api import async_playwright

class TemplateManager:
    templates = Jinja2Templates(directory="visualization/templates")

    @staticmethod
    async def get_template_data(db: AsyncSession):
        captured_requests: Sequence[CapturedRequest] = (await db.execute(select(CapturedRequest))).scalars().all()

        counts = {}
        for request in captured_requests:
            dt = datetime.fromtimestamp(request.request_time)
            date_str = dt.strftime("%Y-%m-%d")
            counts[date_str] = counts.get(date_str, 0) + 1

        return { "request_data": [{"Date": date, "Views": count} for date, count in counts.items()] }

    @staticmethod
    async def populate_template(request, template, db: AsyncSession):
        data = await TemplateManager.get_template_data(db)
        print("data: ", data)
        template_obj = TemplateManager.templates.get_template(template)
        return template_obj.render({"request": request, **data})

    @staticmethod
    async def get_template_bytes(request, template, clip, db: AsyncSession):
        html_content = await TemplateManager.populate_template(request, template, db)
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.set_content(html_content)
            await page.wait_for_load_state('networkidle')
            screenshot_bytes = await page.screenshot(clip=clip)
            await browser.close()
            return screenshot_bytes
