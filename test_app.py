# -*- coding:utf-8 -*-
###
# @Author: Chris
# Created Date: 2019-12-30 14:25:55
# -----
# Last Modified: 2019-12-30 16:32:35
# Modified By: Chris
# -----
# Copyright (c) 2019
###
import io
import requests
from PIL import Image


def test_app():
    imageFile = "./sample/test.png"
    url = "http://localhost:8300/deblur"
    data = open(imageFile, "rb").read()
    headers = {"Content-Type": "application/octet-stream"}
    r = requests.post(url, data=data, headers=headers)
    img = Image.open(io.BytesIO(r.content))
    img.show()


if __name__ == "__main__":
    test_app()
