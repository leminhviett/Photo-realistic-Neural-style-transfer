from flask import Flask, render_template, request, url_for, redirect
import os, shutil


from skimage.color import rgb2gray
import skimage.filters as filters
from skimage.io import imsave
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = ".\\upload"

output = [""]

@app.route('/')
def home():
	return render_template('index.html')
	
@app.route('/uploader', methods = ['POST'])
def upload_file():
    clean_up() ##delet all files from previous session
    if request.method == 'POST':
        f_dict = request.files
        content = f_dict["content"]
        style = f_dict["style"]	
        # print(f_dict)



        content_path = os.path.join(app.config['UPLOAD_FOLDER'], "content\\in1." + str(content.filename).split(".")[-1])
        style_path = os.path.join(app.config['UPLOAD_FOLDER'], "style\\in1." + str(style.filename).split(".")[-1])

      
        content.save(content_path)
        style.save(style_path)

        semantic_segment('upload/content/in1.' + str(content.filename).split(".")[-1], 'content')
        semantic_segment('upload/style/in1.' + str(style.filename).split(".")[-1], 'style')

        output[0] = "in1." + str(content.filename).split(".")[-1]

        return redirect(url_for('stylize', output = output))


def semantic_segment(originPath, resultPath):
      resultPath = './segment_res/' + resultPath
      s = 'python -u segment_model/test.py --imgs ' + originPath + ' --resPath ' + resultPath
      os.system(s)


@app.route('/stylization')
def stylize():
    #hard code
	os.system('python transfer.py --option_unpool cat5 -e -s --content ./upload/content --style ./upload/style --content_segment ./segment_res/content --style_segment ./segment_res/style/ --output ./static/ --verbose --image_size 512')
	res_path = 'static/' + output[0]
	return render_template("result.html", source = res_path)

def clean_up():
	folders = ['./upload/content/', './upload/style/', 'static/', 'segment_res/content/', 'segment_res/style/']
	for folder in folders:
		for filename in os.listdir(folder):
		    file_path = os.path.join(folder, filename)
		    try:
		        if os.path.isfile(file_path) or os.path.islink(file_path):
		            os.unlink(file_path)
		        elif os.path.isdir(file_path):
		            shutil.rmtree(file_path)
		    except Exception as e:
		        print('Failed to delete %s. Reason: %s' % (file_path, e))

if __name__ == '__main__':
    clean_up() ##delet all files from previous session
    app.run(debug = True)




