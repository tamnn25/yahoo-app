from fastapi import APIRouter, File, UploadFile
import cv2
import numpy as np
import base64

router = APIRouter(prefix="/api/crop_3_4", tags=["Crop"])

@router.post("/")
async def crop_3_4(image: UploadFile = File(...)):
    file_bytes = await image.read()
    npimg = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    h, w, _ = img.shape
    target_ratio = 3 / 4
    current_ratio = w / h

    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        start_x = (w - new_w) // 2
        img_cropped = img[:, start_x:start_x + new_w]
    else:
        new_h = int(w / target_ratio)
        start_y = (h - new_h) // 2
        img_cropped = img[start_y:start_y + new_h, :]

    img_cropped = cv2.resize(img_cropped, (300, 400))

    _, buffer = cv2.imencode(".png", img_cropped)
    encoded = base64.b64encode(buffer).decode("utf-8")
    return {"sketch": encoded}
