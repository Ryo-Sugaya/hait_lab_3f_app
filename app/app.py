from logging import error
import os
import io
from flask import Flask,render_template,request,session
import base64
from apis import text_to_speech, pic_to_text
import imghdr


app = Flask(__name__,static_folder='static',template_folder='templates')

app.secret_key = 'hogehoge'
UPLOAD_FOLDER = './upload'
OUTPUT_FOLDER = '../'
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

        filename = 'input.' + file_type
        infile_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        img_file.save(infile_path)
        text = pic_to_text(infile_path)
        voice = text_to_speech(text)
        voice_path = os.path.join(app.config['OUTPUT_FOLDER'],voice)
        return render_template('result.html',text = text, voice_path = voice_path)
    
    else:
        return render_template('index.html')
        


if __name__ == "__main__":
    app.run(port=8000, debug=True)