# -*- coding:utf-8 -*-
###
# @Author: Chris
# Created Date: 2019-12-30 13:15:25
# -----
# Last Modified: 2019-12-30 16:07:08
# Modified By: Chris
# -----
# Copyright (c) 2019
###
import os
from datetime import datetime
from scripts.deblur_image import Deblur
from flask import Flask, request, send_file

app = Flask(__name__)
app.secret_key = os.urandom(12)

global mode
mode = Deblur("./generator.h5")


@app.route("/deblur", methods=["POST"])
def deblur():
    image = request.get_data()
    return send_file(
        mode.deblurOne(image),
        mimetype="image/png",
        as_attachment=True,
        attachment_filename="%s.png" % str(datetime.now()),
    )


if __name__ == "__main__":
    app.run(host="localhost", port=8300, debug=True)

