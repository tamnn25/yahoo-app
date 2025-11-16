from fastapi import APIRouter, File, UploadFile
import cv2
import numpy as np
import base64

router = APIRouter(prefix="/api/sketch", tags=["Sketch"])

@router.post("/")
async def create_sketch(image: UploadFile = File(...)):
    file_bytes = await image.read()
    npimg = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    blur = cv2.GaussianBlur(inv, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256)

    _, buffer = cv2.imencode(".png", sketch)
    encoded = base64.b64encode(buffer).decode("utf-8")
    return {"sketch": encoded}
