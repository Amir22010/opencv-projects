# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 17:14:13 2019

@author: Amir.Khan
"""

import os
from flask import Flask, render_template, request
import cv2

app = Flask(__name__)

#client = SightengineClient('{api_user}', '{api_secret}') # don't forget to add your credentials
app.config['UPLOAD_FOLDER'] = 'static/'

# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set([ 'png', 'jpg', 'jpeg', 'JPG'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():

    file = request.files['image']
    
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
    if file and allowed_file(file.filename):
    
        file.save(f)
        
        containNoFaces = False
        
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
        #output = client.check('nudity', 'wad', 'celebrities', 'scam', 'face-attributes').set_file(f)
        #load the image with the imread function of the cv2 module 
        image = cv2.imread(f)
        
        #to convert from RGB to gray, we use the COLOR_BGR2GRAY code
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
        #scaleFactor and minNeighbors 1.3, 5
        faces = face_cascade.detectMultiScale(grayImage, 1.3, 5)
     
    #    print (len(faces))
        if len(faces) == 0:
            print("No faces found")
            containNoFaces = True
     
        else:
            print(faces)
            print(faces.shape)
            print("Number of faces detected: " + str(faces.shape[0]))
            containNoFaces = False
     
        for (x,y,w,h) in faces:
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),1)
     
        cv2.rectangle(image, ((0,image.shape[0] -25)),(270, image.shape[0]), (255,255,255), -1)
        cv2.putText(image, "Number of faces detected: " + str(faces.shape[0]), (0,image.shape[0] -10), cv2.FONT_HERSHEY_TRIPLEX, 0.5,  (0,0,0), 1)
     
    #    cv2.imshow('Image with faces',image)
        cv2.imwrite(app.config['UPLOAD_FOLDER'] + "detected-boxes.jpg", image)

    return render_template('index.html', containNoFaces=containNoFaces, user_image = image, init=True)


if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=int("5000"),
        debug=True
)