import os
import cv2
import numpy as np
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
    operation_selection = request.form['image_type_selection']
    image_file = request.files['file']
    filename = secure_filename(image_file.filename)
    reading_file_data = image_file.read()
    image_array = np.fromstring(reading_file_data, dtype='uint8')
    decode_array_to_img = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)


    # Write code for Select option for Gray and Sketch
    if operation_selection == 'gray':
    	file_data = make_grayscale(decode_array_to_img)

    elif operation_selection == 'sketch':
    	file_data = image_sketch(decode_array_to_img)

    elif operation_selection == 'oil':
    	file_data = oil_effect(decode_array_to_img)

    elif operation_selection == 'rgb':
    	file_data = rgb_effect(decode_array_to_img)

    elif operation_selection == 'invert':
        file_data = invert_effect(decode_array_to_img)

    elif operation_selection == 'water color':
        file_data = water_color_effect(decode_array_to_img)

    elif operation_selection == 'hdr':
        file_data = hdr_effect(decode_array_to_img)

    else:
    	print("No Image Selected")

    # Ends here

    with open(os.path.join('static/', filename),
                  'wb') as f:
        f.write(file_data)

    return render_template('upload.html', filename=filename)

def make_grayscale(decode_array_to_img):

    convert_gray_img = cv2.cvtColor(decode_array_to_img, cv2.COLOR_RGB2GRAY)
    status, output_image = cv2.imencode('.PNG', convert_gray_img)

    return output_image


# Write code for Sketch function
def image_sketch(decode_array_to_img):
	convert_gray_img = cv2.cvtColor(decode_array_to_img, cv2.COLOR_RGB2GRAY)
	sharp_gray_image = cv2.bitwise_not(convert_gray_img)
	blur_img = cv2.GaussianBlur(sharp_gray_image, (111, 111), 0)
	sharp_blur_image = cv2.bitwise_not(blur_img)
	sketch_img = cv2.divide(convert_gray_img, sharp_blur_image, scale = 256.0)
	status, output_image = cv2.imencode('.PNG', sketch_img)

	return output_image

# Ends here
def oil_effect(decode_array_to_img):
	covert_oil_img = cv2.xphoto.oilPainting(decode_array_to_img, 7, 1)
	status, output_image = cv2.imencode('.PNG', covert_oil_img)

	return output_image

def rgb_effect(decode_array_to_img):
	convert_rgb_img = cv2.cvtColor(decode_array_to_img, cv2.COLOR_BGR2RGB)
	status, output_image = cv2.imencode('.PNG', convert_rgb_img)

	return output_image

def invert_effect(decode_array_to_img):
    convert_invert_img = cv2.bitwise_not(decode_array_to_img)
    status, output_image = cv2.imencode('.PNG', convert_invert_img)

    return output_image

def water_color_effect(decode_array_to_img):
    convert_water_color_img = cv2.stylization(decode_array_to_img, sigma_s = 60, sigma_r = 0.6)
    status, output_image = cv2.imencode('.PNG', convert_water_color_img)

    return output_image

def hdr_effect(decode_array_to_img):
    convert_hdr_img = cv2.detailEnhance(decode_array_to_img, sigma_s = 12, sigma_r = 0.15)
    status, output_image = cv2.imencode('.PNG', convert_hdr_img)

    return output_image

@app.route('/display/<filename>')
def display_image(filename):

    return redirect(url_for('static', filename=filename))



if __name__ == "__main__":
    app.run()










