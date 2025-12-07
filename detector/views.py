from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import tempfile
import os
import numpy as np
try:
    import cv2
except Exception:
    cv2 = None
from ultralytics import YOLO
from PIL import Image
import io

model = YOLO("best.pt")  # load model once

def index(request):
    return render(request, "detector/index.html")


def upload_image(request):
    if request.method != "POST" or "file" not in request.FILES:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    file = request.FILES["file"]
    img = Image.open(file)

    results = model(img)

    annotated = results[0].plot()  # numpy array
    img_io = io.BytesIO()
    Image.fromarray(annotated).save(img_io, format="JPEG")
    img_io.seek(0)

    return HttpResponse(img_io.read(), content_type="image/jpeg")


def upload_video(request):
    # support video uploads; will process each frame and return an annotated MP4
    if request.method != "POST" or "file" not in request.FILES:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    if cv2 is None:
        return JsonResponse({"error": "OpenCV (cv2) is not installed. Install opencv-python to enable video processing."}, status=500)

    file = request.FILES["file"]
    # save to a temporary file
    tmp_in = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1] or '.mp4')
    for chunk in file.chunks():
        tmp_in.write(chunk)
    tmp_in.flush()
    tmp_in.close()

    tmp_out = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tmp_out.close()

    try:
        cap = cv2.VideoCapture(tmp_in.name)
        if not cap.isOpened():
            return JsonResponse({"error": "Unable to read uploaded video file"}, status=400)

        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 640)
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 480)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(tmp_out.name, fourcc, fps, (w, h))

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # frame is in BGR
            try:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # perform inference on numpy image
                results = model(rgb)
                annotated = results[0].plot()  # returns RGB numpy array
                bgr = cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR)
                out.write(bgr)
            except Exception as e:
                # if inference fails, write original frame and continue
                out.write(frame)

        cap.release()
        out.release()

        # return annotated video
        with open(tmp_out.name, 'rb') as f:
            content = f.read()
        return HttpResponse(content, content_type='video/mp4')
    finally:
        try:
            os.unlink(tmp_in.name)
        except Exception:
            pass
        try:
            os.unlink(tmp_out.name)
        except Exception:
            pass
