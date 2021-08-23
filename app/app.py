from logging import error
import os
import io
from flask import Flask,render_template,request,redirect,url_for,flash,session
import base64
from apis import text_to_speech, pic_to_text
import imghdr

app = Flask(__name__,static_folder='./output')

app.secret_key = 'hogehoge'
UPLOAD_FOLDER = './upload'
OUTPUT_FOLDER = './output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
ALLOWED_EXTENSIONS = ['jpg', 'jpeg','png','jfif']

def allowed_file(filetype):
    return filetype in ALLOWED_EXTENSIONS


@app.route('/',methods = ['POST','GET'])
def result():

    if request.method == 'POST':
        img_file = request.files['img_file']
        file_type = imghdr.what(img_file)

        if not allowed_file(file_type):
            error = '拡張子が不適切です。'
            return render_template('index.html',error = error)

        filename = 'input.' + file_type
        infile_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        img_file.save(infile_path)
        text = pic_to_text(infile_path)
        voice = text_to_speech(text)
        return render_template('result.html',text = text, voice_path = voice)
    
    else:
        return render_template('index.html')
        


if __name__ == "__main__":
    app.run(port=8000, debug=True)