from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os
import tensorflow as tf


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
    if request.method == 'POST' and 'photo' in request.files:
        photo_send = True
        filename = photos.save(request.files['photo'])
        classify('static/img/' + filename)
        return render_template('index.html', photoSend=photo_send, filename=filename,
                               alphabet=classify('static/img/' + filename))
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
        soft_max_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(soft_max_tensor, {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            result = round(score*100)

            print('%s (score = %.5f)' % (human_string, score))
            return str(human_string) + ". Prawdopodobieństwo wynosi: " + str(result) + "%"


if __name__ == "__main__":
    app.run(debug=True)
