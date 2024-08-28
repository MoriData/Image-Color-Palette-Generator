import numpy as np
from PIL import Image
from flask import Flask, render_template, redirect, url_for
from tkinter import filedialog
import shutil
import os
from sklearn.cluster import KMeans


def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route("/upload", methods=["GET", "POST"])
def upload():
    return redirect(url_for('home'))


@app.route("/", methods=["GET", "POST"])
def home():
    home = True
    return render_template("index.html", home=home)


@app.route("/start", methods=["GET", "POST"])
def start():
    try:
        # Open a file dialog to select an image
        file_name = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])

        if not file_name:
            return redirect(url_for('home'))

        # Open the image
        my_img = Image.open(file_name)
        img_array = np.array(my_img)

        pixels = img_array.reshape(-1, 3)
        # Apply KMeans to cluster colors
        kmeans = KMeans(n_clusters=10, random_state=42)
        kmeans.fit(pixels)

        dominant_colors = kmeans.cluster_centers_.astype(int)
        # Convert the array of dominant colors to a list of tuples
        color_list = [tuple(color) for color in dominant_colors]

        # Copy the image to the static folder
        destination = 'static/assets/img/1.jpg'
        shutil.copy(file_name, destination)
        # rgb to hex code
        hex_codes = []
        for hex in color_list:
            code = rgb_to_hex(hex)
            hex_codes.append(code)

        # Render the index.html with the color data and image path
        return render_template("index.html", colors=color_list, pic=destination, hex=hex_codes)

    except Exception as error:
        print('Caught this error: ' + repr(error))
        return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
