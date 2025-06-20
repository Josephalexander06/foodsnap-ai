from django.shortcuts import render, redirect
from .forms import UploadImageForm
from cnn_model import predict_image 
import os
from django.conf import settings
import sqlite3


def get_nutrition_from_db(food_name):
    conn = sqlite3.connect("nutrition.db")
    cur = conn.cursor()
    cur.execute("SELECT calories, protein, fat, carbs FROM nutrition WHERE foodName = ?", (food_name,))
    result = cur.fetchone()
    # print('result',result)
    conn.close()
    return result


def upload_view(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['file']
            pre = form.save()
            url = request.session['uploaded_file_url'] = pre.file.url 
            image_path = os.path.join(settings.MEDIA_ROOT, image_file.name)
            with open(image_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)

            # Call the prediction function
            prediction = predict_image(image_path)
           
            nutrition = get_nutrition_from_db(prediction)
            print(nutrition)
            # os.remove(temp_path)    

        return render(request, 'upload_success.html', {
                'food': prediction,
                'calories': nutrition[0],
                'protein': nutrition[1],
                'fat': nutrition[2],
                'carbs': nutrition[3],
                'image_url':  url 
            })
    else:
        form = UploadImageForm()
    return render(request, 'index.html', {'form': form})



def upload_success(request):
    return render(request, 'upload_success.html')  # Create this template