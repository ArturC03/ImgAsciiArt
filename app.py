from flask import Flask, render_template, request
from ImgToAscii import ImageToAsciiArtBytes  # Assuming your module is named 'your_module.py'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if request.method == 'POST':
        image_url = request.form['imageURL']
        ascii_art_image = ImageToAsciiArtBytes(image_url)
        if ascii_art_image:
            return render_template('result.html', ascii_art_image=ascii_art_image)
        else:
            return 'Could not convert the image.', 400

if __name__ == '__main__':
    app.run(debug=True)

