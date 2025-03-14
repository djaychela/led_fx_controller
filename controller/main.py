from fastapi import FastAPI, applications
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from . import models
from .database import engine
from .dependencies import get_db

from apscheduler.schedulers.background import BackgroundScheduler  # runs tasks in the background
from apscheduler.triggers.cron import CronTrigger  # allows us to specify a recurring time for execution

from .routers import effects, state, html
from .crud import sonos
from .config import SONOS_INTERVAL

from os import path
import pathlib

models.Base.metadata.create_all(bind=engine)

scheduler = BackgroundScheduler()
scheduler.add_job(sonos.get_sonos_state, "interval", seconds=SONOS_INTERVAL)
scheduler.start()

app = FastAPI()

assets_path = str(pathlib.Path(__file__).parent.resolve() / "static")
if path.exists(assets_path + "/swagger-ui.css") and path.exists(assets_path + "/swagger-ui-bundle.js"):
    app.mount("/assets", StaticFiles(directory=assets_path), name="static")
    def swagger_monkey_patch(*args, **kwargs):
        return get_swagger_ui_html(
            *args,
            **kwargs,
            swagger_favicon_url="",
            swagger_css_url="/assets/swagger-ui.css",
            swagger_js_url="/assets/swagger-ui-bundle.js",
        )
    applications.get_swagger_ui_html = swagger_monkey_patch


app.include_router(effects.router)
app.include_router(state.router)
app.include_router(html.router)

