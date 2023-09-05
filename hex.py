import os
# from PIL import Image
import numpy as np
import requests
import cv2
# from collections import Counter
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
the_image = 'static/uploads/test4.0.png'


@app.route('/', methods=['GET', 'POST'])
def home():
    available = False

    if request.method == "POST":
        available = True
        if request.files['image']:
            print('Yes')
            # Get the image file from the request
            image_file = request.files["image"]
            # Save the image file to a directory
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join("static/uploads", image_filename))
            image_file = 'static/uploads/' + image_file.filename
            print(image_file)

        else:
            available = False
            print('No')
            image_file = 'static/uploads/test4.0.png'

    else:
        image_file = 'static/uploads/test4.0.png'

    image = cv2.imread(image_file)
    (height, width, channels) = image.shape

    # Convert the image to RGB color space.
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create a dictionary to store the colors and their corresponding frequencies.
    color_counts = {}

    # Iterate over all pixels in the image.
    for i in range(height):
        for j in range(width):
            # Get the RGB value of the current pixel.
            r, g, b = image[i][j]

            # Convert the RGB value to a hex color code.
            color_code = '#%02x%02x%02x' % (r, g, b)

            # If the color code is not already in the dictionary, add it.
            if color_code not in color_counts:
                color_counts[color_code] = 0

            # Increment the frequency of the current color.
            color_counts[color_code] += 1

    # Calculate the percentage of each color.
    color_percentages = {}
    for color, count in color_counts.items():
        color_percentages[color] = count / (height * width) * 100

    hex_code_lists = []
    hex_code_percentage = []
    color_percentages_by_color = sorted(color_percentages.items(), key=lambda x: x[1], reverse=True)
    color_percentages = dict(color_percentages_by_color)
    color_percentages = dict(list(color_percentages.items())[0: 50])

    for item in color_percentages.keys():
        if item[1] in color_percentages.keys():
            hex_code_lists.remove(item)
        else:
            hex_code_lists.append(item)

    for item in color_percentages.values():
        item = round(item, 4)
        hex_code_percentage.append(item)

    colors = hex_code_lists
    unique_colors = np.unique(colors, axis=0).tolist()

    hex_code_dict = []
    for item in unique_colors:
        hex_code_dict.append(item)


    # percentage = hex_code_percentage
    # hex_code_dict = {}
    # for num in range(len(unique_colors)):
    #     hex_code = {unique_colors[num]: percentage[num]}
    #     hex_code_dict.update(hex_code)
    #
    # hex_code_dict = hex_code_dict

    return render_template('index.html', hex_code_dict=hex_code_dict, image_file=image_file, available=available)


@app.route('/url', methods=['POST'])
def url_work():
    available = True
    input_answer = request.form.get('url')
    if input_answer:
        img_url = input_answer
        response = requests.get(img_url)
        if response.status_code:
            fp = open('static/uploads/image.png', 'wb')
            fp.write(response.content)
            fp.close()
            image_file = 'static/uploads/image.png'

    else:
        available = False
        image_file = 'static/uploads/test4.0.png'

    try:
        image = cv2.imread(image_file)
        (height, width, channels) = image.shape

    except AttributeError:
        image = cv2.imread('static/uploads/test4.0.png')
        (height, width, channels) = image.shape
    # Convert the image to RGB color space.
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create a dictionary to store the colors and their corresponding frequencies.
    color_counts = {}

    # Iterate over all pixels in the image.
    for i in range(height):
        for j in range(width):
            # Get the RGB value of the current pixel.
            r, g, b = image[i][j]

            # Convert the RGB value to a hex color code.
            color_code = '#%02x%02x%02x' % (r, g, b)

            # If the color code is not already in the dictionary, add it.
            if color_code not in color_counts:
                color_counts[color_code] = 0

            # Increment the frequency of the current color.
            color_counts[color_code] += 1

    # Calculate the percentage of each color.
    color_percentages = {}
    for color, count in color_counts.items():
        color_percentages[color] = count / (height * width) * 100

    hex_code_lists = []
    hex_code_percentage = []
    color_percentages_by_color = sorted(color_percentages.items(), key=lambda x: x[1], reverse=True)
    color_percentages = dict(color_percentages_by_color)
    color_percentages = dict(list(color_percentages.items())[0: 50])

    for item in color_percentages.keys():
        if item[1] in color_percentages.keys():
            hex_code_lists.remove(item)
        else:
            hex_code_lists.append(item)

    for item in color_percentages.values():
        item = round(item, 4)
        hex_code_percentage.append(item)

    colors = hex_code_lists
    unique_colors = np.unique(colors, axis=0).tolist()

    hex_code_dict = []
    for item in unique_colors:
        hex_code_dict.append(item)
    # percentage = hex_code_percentage
    # hex_code_dict = {}
    # for num in range(len(colors)):
    #     hex_code = {colors[num]: percentage[num]}
    #     hex_code_dict.update(hex_code)
    #
    # hex_code_dict = hex_code_dict

    return render_template('index.html', hex_code_dict=hex_code_dict, image_file=image_file, available=available)


if __name__ == '__main__':
    app.run(debug=True)
