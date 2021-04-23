from django.views.generic import TemplateView

# import the necessary packages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pyzbar import pyzbar
import numpy as np
import cv2
import json
import base64


# Create your views here.
class HelloWorldView(TemplateView):
    template_name = "index.html"


@csrf_exempt
def _get_barcode_data(request):
    # initialize the data dictionary to be returned by the request
    data = {"success": False, "result": ""}

    # check to see if this is a post request
    if request.method == "POST":
        # check to see if an image was uploaded
        if request.FILES.get("image", None) is not None:
            # grab the uploaded image
            data["result"] = _scan_barcode(stream=request.FILES["image"])
        else:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            img_url = body.get("dataURL", None)
            data["result"] = _scan_barcode(img_url=img_url)

        data["success"] = True if data["result"] else False

    # return a JSON response
    return JsonResponse(data)


def _scan_barcode(img_url=None, stream=None):
    # if the path is not None, then load the image from disk
    if img_url is not None:
        decoded_image_data = base64.b64decode(img_url)
        image_arr = np.fromstring(decoded_image_data, np.uint8)
    elif stream is not None:
        # if stream use bytearray
        data = stream.read()
        image_arr = np.asarray(bytearray(data), dtype="uint8")

    if image_arr is not None:
        image = cv2.imdecode(image_arr, cv2.IMREAD_COLOR)
        barcode = pyzbar.decode(image)
        if len(barcode):
            return barcode[0].data.decode("utf-8")

    return ""


def home(request):
    data = {"success": False, "result": ""}
    return JsonResponse(data)
