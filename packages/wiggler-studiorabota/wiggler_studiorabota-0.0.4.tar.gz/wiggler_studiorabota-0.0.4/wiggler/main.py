from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
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
    for filename in sorted(os.listdir(IMG_FOLDER)):
        name, ext = os.path.splitext(filename)
        if ext == '.jpg':
            out.append({
                "name": name,
                "path": "/image/" + filename
            })
    return out

@app.get("/take_picture")
def images():
    now = datetime.now()
    filename = now.strftime("%Y-%m-%d-%H-%M")
    path = f"{IMG_FOLDER}/{filename}.jpg"
    os.system(f"libcamera-jpeg --width 1024 --height 768 --nopreview -t 1 -o {path}")
    return {"picture": path}
