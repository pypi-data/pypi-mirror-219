from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from crontab import CronTab
from datetime import datetime
import os

IMG_FOLDER = './Pictures'

app = FastAPI()

app.mount("/image", StaticFiles(directory=IMG_FOLDER), name="image")

@app.get("/")
def read_root():
    return {"Hello": "Worm"}

@app.get("/images")
def images():
    out = []
    for fileName in sorted(os.listdir(IMG_FOLDER)):
        name, ext = os.path.splitext(fileName)
        if ext == '.jpg':
            out.append({
                "name": name,
                "path": "/image/" + fileName
            })
    return out

@app.get("/take_picture")
def images():
    now = datetime.now()
    fileName = now.strftime("%Y-%m-%d-%H-%M")
    filePath = f"{IMG_FOLDER}/{fileName}.jpg"
    os.system(f"libcamera-jpeg --width 1024 --height 768 --nopreview -t 1 -o {filePath}")
    return {"picture": f"image/{fileName}.jpg"}


@app.get("/take_picture_every_minute")
def images():
    cron = CronTab(user='root')
    job = cron.new(command='curl localhost:8000/take_picture')
    job.minute.every(1)
    cron.write()