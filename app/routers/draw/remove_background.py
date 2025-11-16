from fastapi import APIRouter, File, UploadFile
import cv2
import numpy as np
import base64

router = APIRouter(prefix="/api/remove_background", tags=["Background Removal"])

@router.post("/")
async def remove_background(image: UploadFile = File(...)):
    file_bytes = await image.read()
    npimg = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mask = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 10
    )

    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=1)

    white_bg = np.ones_like(img, dtype=np.uint8) * 255
    fg = cv2.bitwise_and(img, img, mask=mask)
    bg_mask = cv2.bitwise_not(mask)
    bg = cv2.bitwise_and(white_bg, white_bg, mask=bg_mask)
    result = cv2.add(fg, bg)

    _, buffer = cv2.imencode(".png", result)
    encoded = base64.b64encode(buffer).decode("utf-8")

    return {"sketch": encoded}
