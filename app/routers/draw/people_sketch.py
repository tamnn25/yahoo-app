from fastapi import APIRouter, File, UploadFile
import cv2
import numpy as np
import base64

router = APIRouter(prefix="/api/sketch_people", tags=["People Sketch"])

@router.post("/")
async def create_sketch_people(image: UploadFile = File(...)):
    file_bytes = await image.read()
    npimg = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    _, sketch = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
    _, buffer = cv2.imencode(".png", sketch)
    encoded = base64.b64encode(buffer).decode("utf-8")

    return {"sketch": encoded}
