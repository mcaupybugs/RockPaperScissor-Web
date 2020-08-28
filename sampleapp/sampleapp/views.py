from .forms import ImageForm
import numpy as np
from django.http import HttpResponse
from django.shortcuts import render
import cv2
from tensorflow import keras
from tensorflow.keras import models


def home(request):
    return render(request, 'home.html')


def predict(request):
    hand_cascade = cv2.CascadeClassifier('hand.xml')
    model = models.load_model('./best_model.h5')
    from time import sleep

    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        # fgmask = fgbg.apply(img)
        # img=cv2.imread('./data/validation/rock2.png')
        # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # hand = hand_cascade.detectMultiScale(gray,minSize=(10,10))
        # for (x,y,w,h) in hand:
        #     cv2.rectange(img,(x,y),(x+w,y+h),(255,0,0),2)
        top, right, bottom, left = 10, 350, 400, 790
        # cv2.imshow('cam',img)
        img = cv2.flip(img, 1)
        img = img[top:bottom, right:left]
        # cv2.imshow('img', img)
        cv2.imwrite('static/me.png', img)
        k = 0
        if k != 27:
            k = 32

        if k == 27:
            break
        elif k == 32:

            img = cv2.resize(img, (128, 128))
            img = img.reshape(1, 128, 128, 3)
            prediction = model.predict_classes(img)
            if prediction == 1:
                prediction = 'rock'
            elif prediction == 2:
                prediction = 'scissors'
            elif prediction == 0:
                prediction = 'paper'
            print(prediction)
            k = 27
            break
    cap.release()
    cv2.destroyAllWindows()
    return render(request, 'home.html', {'result': prediction})


def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, 'home.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
    return render(request, 'home.html', {'form': form})
