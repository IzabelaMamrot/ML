from flask import Flask, render_template, flash, request, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES
from PIL import Image
#import requests
from io import BytesIO
import os
import cv2
#import engine
import random
import urllib.request

# Folder config.
if not os.path.isdir('./static/img'):
    os.makedirs('./static/img')

# App config.
app = Flask(__name__)

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)


@app.route("/", methods=['GET', 'POST'])
def upload():
    urlSend = False
    photoSend = False
    if request.method == 'POST' and 'photo' in request.files:
        photoSend = True
        filename = photos.save(request.files['photo'])
        return render_template('index.html', photoSend=photoSend, filename=filename, result=engine.ocrEngine(filename),
                               alphabet=engine.neuralEngine(filename))
    if request.method == 'POST':
        urlSend = True
        url = request.form['url']
        # pobierz obrazek na server
        filename = str(random.randint(0, 100000)) + ".png"
        urllib.request.urlretrieve(url, 'static/img/' + filename)
        info = ('Link do twojego zdjecia: ' + url)
        return render_template('index.html', urlSend=urlSend, filename=filename, result=engine.ocrEngine(filename),
                               info=info, alphabet=engine.neuralEngine(filename))
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)