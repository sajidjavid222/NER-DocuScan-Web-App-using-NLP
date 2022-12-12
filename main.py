from flask import Flask, request,redirect
from flask import render_template
import settings
import utils
import numpy as np
import cv2
import predictions as pred

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.secret_key = 'document_scanner_app'

from datetime import datetime
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///businessCard.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

docscan = utils.DocumentScan()
db = SQLAlchemy(app)
class Todo(db.Model):
     sno = db.Column(db.Integer, primary_key=True)
     name = db.Column(String, nullable=False)
     org = db.Column(String, nullable=False)
     desg = db.Column(String, nullable=False)
     phone = db.Column(String, nullable=False)
     email = db.Column(String, nullable=False)
     web  =  db.Column(String, nullable=False)
     date_created = db.Column(db.DateTime, default=datetime.utcnow)   
     def _repr_(self) -> str:
         return f"{self.name} - {self.org}"


@app.route('/',methods=['GET','POST'])
def scandoc():
    
    if request.method == 'POST':
        file = request.files['image_name']
        upload_image_path = utils.save_upload_image(file)
        print('Image saved in = ',upload_image_path)
        # predict the coordination of the document
        four_points, size = docscan.document_scanner(upload_image_path)
        print(four_points,size)
        if four_points is None:
            message ='UNABLE TO LOCATE THE COORDIANATES OF DOCUMENT: points displayed are random'
            points = [
                {'x':10 , 'y': 10},
                {'x':120 , 'y': 10},
                {'x':120 , 'y': 120},
                {'x':10 , 'y': 120}
            ]
            return render_template('scanner.html',
                                   points=points,
                                   fileupload=True,
                                   message=message)
            
        else:
            points = utils.array_to_json_format(four_points)
            message ='Located the Cooridinates of Document using OpenCV'
            return render_template('scanner.html',
                                   points=points,
                                   fileupload=True,
                                   message=message)
            
        
        return render_template('scanner.html')
    
    return render_template('scanner.html')



@app.route('/transform',methods=['POST'])
def transform():
    try:
        points = request.json['data']
        array = np.array(points)
        magic_color = docscan.calibrate_to_original_size(array)
        #utils.save_image(magic_color,'magic_color.jpg')
        filename =  'magic_color.jpg'
        magic_image_path = settings.join_path(settings.MEDIA_DIR,filename)
        cv2.imwrite(magic_image_path,magic_color)
        
        return 'sucess'
    except:
        return 'fail'
        
    
@app.route('/prediction')
def prediction():
    # load the wrap image
    wrap_image_filepath = settings.join_path(settings.MEDIA_DIR,'magic_color.jpg') 
    image = cv2.imread(wrap_image_filepath)
    image_bb ,results = pred.getPredictions(image)
    list = [] 
    for x,strgs in results.items():
     delta = ""
     for strng in strgs:
         delta = delta + strng
     list.append(delta)
    db.session.add(Todo(name=list[0],org = list[1],desg=list[2],phone=list[3],email = list[4],web=list[5]))
    db.session.commit()
    bb_filename = settings.join_path(settings.MEDIA_DIR,'bounding_box.jpg') 
    cv2.imwrite(bb_filename,image_bb)
    allTodo =  Todo.query.all()
    print(allTodo)
    
    return render_template('predictions.html',results=results)


@app.route('/about')
def about():
    return render_template('about.html')

with app.app_context():
    db.create_all()
app.app_context()


if __name__ == "__main__":
    app.run(debug=True)