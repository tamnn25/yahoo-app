from fastapi import APIRouter, File, UploadFile
import cv2
import numpy as np
import base64
from PIL import Image, ImageEnhance

router = APIRouter(prefix="/api/graffiti", tags=["Graffiti"])

@router.post("/")
async def graffiti_effect(image: UploadFile = File(...)):
    file_bytes = await image.read()
    npimg = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    pil_img = ImageEnhance.Color(pil_img).enhance(2.5)
    pil_img = ImageEnhance.Contrast(pil_img).enhance(1.8)
    pil_img = ImageEnhance.Brightness(pil_img).enhance(1.1)

    img_rgb = np.array(pil_img)
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    img_poster = (img_rgb // 64) * 64
    graffiti = cv2.addWeighted(img_poster, 0.8, edges_colored, 0.5, 0)
    graffiti = cv2.bilateralFilter(graffiti, 9, 75, 75)

    _, buffer = cv2.imencode(".png", cv2.cvtColor(graffiti, cv2.COLOR_RGB2BGR))
    encoded = base64.b64encode(buffer).decode("utf-8")

    return {"sketch": encoded}
