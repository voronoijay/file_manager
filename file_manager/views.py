from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from json import dumps
from django.views.decorators.csrf import csrf_exempt
import os
from django.shortcuts import render
from management.models import *
import string    
import random 
import time

def sorting(lst):
    if not lst:
        return []
    return (sorting([x for x in lst[1:] if x < lst[0]]) + [lst[0]] + sorting([x for x in lst[1:] if x >= lst[0]]))

@csrf_exempt
def read(request):
    start = time.time()

    objs = StringData.objects.all()
    length = len(objs)

    end = time.time()

    measure = end - start

    print("length:", length)
    print("measured time: ", measure)
    
    return JsonResponse({"result":"success", "time": measure})
@csrf_exempt
def write(request):
    STRING_LENGTH = 150
    start = time.time()

    for i in range(0, 10000):
        gen_a = ''.join(random.choices(string.ascii_uppercase + string.digits, k = STRING_LENGTH))
        gen_b = ''.join(random.choices(string.ascii_uppercase + string.digits, k = STRING_LENGTH))
        gen_c = ''.join(random.choices(string.ascii_uppercase + string.digits, k = STRING_LENGTH))
        gen_d = ''.join(random.choices(string.ascii_uppercase + string.digits, k = STRING_LENGTH))
        gen_e = ''.join(random.choices(string.ascii_uppercase + string.digits, k = STRING_LENGTH))

        data = {
            "string_a":  ''.join(sorting(str(gen_a))),
            "string_b":  ''.join(sorting(str(gen_b))),
            "string_c":  ''.join(sorting(str(gen_c))),
            "string_d":  ''.join(sorting(str(gen_d))),
            "string_e":  ''.join(sorting(str(gen_e))),
        }
        StringData.objects.create(**data)
    
    end = time.time()

    measure = end - start

    print("measured time: ", measure)
    
    return JsonResponse({"result":"success", "time": measure})


@csrf_exempt
def upload(request):
    uploaded_file = request.FILES['document']
    # with open('/mnt/hdd2/jay_test/' + uploaded_file.name, 'wb+') as destination:
    #     for chunk in uploaded_file.chunks():
    #         destination.write(chunk)

    data = {
        "worksheet_name": "kinase_image.png",
        "my_file": uploaded_file
    }
    FileManager.objects.create(**data)
    
    return render(request, 'index.html', {'form': {}})

@csrf_exempt
def download(request):
    file_path = '/mnt/hdd2/jay_test/sub_dir/kinase_image.png'
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response


@csrf_exempt
def index(request):
    return render(request, 'index.html', {'form': {}})