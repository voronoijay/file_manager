import django
django.setup()
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
from .functions import *
from multiprocessing import Pool
from django.core.paginator import Paginator
import concurrent.futures
from django.db import connection

@transaction.atomic
def generate_book_metadata(book_ids, rows):
    connection.close()
    # print(rows[0])
    for row in rows:
        print(row)

@transaction.non_atomic_requests
@csrf_exempt
def multiread(request):

    start = time.time()

    count = 0

    book_ids = StringData.objects.all().values_list('string_a', 'string_b', flat=False)
    
    # cast it to list to make sure no database connection is copied
    book_ids = list(book_ids)

    chunks = 3
    # add one to ensure the all the ids are included in the chunks
    # if the length of ids is even (so if ids is even, chunks become 5 although
    #  it's better if the 4th chunk have one extra id)
    elements_per_chunk = int((len(book_ids) + 1) / chunks)
    book_id_chunks = [
        book_ids[x:x+elements_per_chunk]
        for x
        in range(0, len(book_ids), elements_per_chunk)
    ]

    process = []

    # connections are copied into the new process
    # to prevent that, close current connections in the main thread
    # new connections will be created automatically in the spawned
    # process
    django.db.connections.close_all()
    print("===========================================================")
    for book_id_chunk in book_id_chunks:
        print("-----------------------------------------------------------")
        p = Process(target=generate_book_metadata, args=([], book_id_chunk))
        process.append(p)

        p.start()

    for p in process:
        # 각 프로세스에게 다른 프로세스들이 일을 다 마칠때까지 이 이상 코드를 진행하지 말아라
        p.join()

    end = time.time()
    measure = end - start
    print("measured time: ", measure)
    
    return HttpResponse("SUCCESS")

@csrf_exempt
def multiwrite(request):
    start = time.time()

    multiwriteWrapper(total_data_amount=500000, num_process=5)

    end = time.time()
    measure = end - start
    print("measured time: ", measure)
    
    return JsonResponse({"result":"success", "time": measure})


@csrf_exempt
def deleteAll(request):

    start = time.time()
    StringData.objects.all().delete()
    end = time.time()
    measure = end - start
    print("measured time: ", measure)

    return JsonResponse({"result":"success", "time": measure})
