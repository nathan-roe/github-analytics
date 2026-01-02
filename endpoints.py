from io import BytesIO
from PIL import Image
from fastapi import Depends, FastAPI
from fastapi.requests import Request
from fastapi.responses import Response
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.staticfiles import StaticFiles

from database import get_db, create_db_and_tables
from models import CapturedRequest, IdentifiedRequestSource
from visualization import TemplateManager

app = FastAPI()
app.mount("/static", StaticFiles(directory="visualization/templates"), name="static")

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

async def save_request_data(request: Request, page: str, session: AsyncSession, commit = False, from_hidden = False):
    if request.headers.get('referer') is not None:
        return
    retrieved_host = request.headers.get('x-forwarded-for')
    if retrieved_host is None:
        retrieved_host = request.headers.get('host') # catch all, as the host will be the local one

    result = await session.execute(select(IdentifiedRequestSource)
                                   .where(IdentifiedRequestSource.ip == retrieved_host))
    request_source = result.scalar_one_or_none()

    if request_source is None:
        request_source = IdentifiedRequestSource(ip=retrieved_host)
        session.add(request_source)
        await session.flush() # Push to DB to get ID without committing

    captured_request = CapturedRequest(headers=dict(request.headers), request_source=request_source, from_hidden=from_hidden, page=page)
    session.add(captured_request)
    if commit:
        await session.commit()

@app.get("/", responses={200: {"content": {"image/png": {}}}}, response_class=Response)
async def retrieve_beacon(request: Request, page: str = '', session: AsyncSession = Depends(get_db)):
    await save_request_data(request, page, session)
    response = await TemplateManager.get_template_bytes(request, "graph_template.html", {
        'x': 0, 'y': 0,
        'width': 927.5,
        'height': 194
    }, session)
    await session.commit()
    return Response(content=response, media_type="image/png")

@app.get("/hidden", responses={200: {"content": {"image/png": {}}}}, response_class=Response)
async def retrieve_beacon_hidden(request: Request, page: str = '', session: AsyncSession = Depends(get_db)):
    await save_request_data(request, page, session, True, True)
    img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
    byte_io = BytesIO()
    img.save(byte_io, format='PNG')
    return Response(content=byte_io.getvalue(), media_type="image/png")