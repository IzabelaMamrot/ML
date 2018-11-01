from flask import Flask, render_template, flash, request, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os
import tensorflow as tf
from decimal import *
import random
import urllib.request
# import sys
# import cv2
# import engine
# from PIL import Image
# import requests
# from io import BytesIO

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
        classify('static/img/' + filename)
        return render_template('index.html', photoSend=photoSend, filename=filename, alphabet=classify('static/img/' + filename))
    return render_template('index.html')


def classify(image_path):
    # Read the image_data
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line
                       in tf.gfile.GFile("/home/iza/Desktop/ML/cnn/logs/trained_labels.txt")]

    # Unpersists graph from file
    with tf.gfile.FastGFile("/home/iza/Desktop/ML/cnn/logs/trained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            wynik = round(score*100)

            print('%s (score = %.5f)' % (human_string, score))
            return str(human_string) + " " + " Prawdopodobieństwo wynosi: " + str(wynik) +"%"


classify('2.jpg')

if __name__ == "__main__":
    app.run(debug=True)