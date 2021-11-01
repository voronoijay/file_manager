import django
django.setup()
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.http import HttpResponse, JsonResponse
from json import dumps
from django.views.decorators.csrf import csrf_exempt
import os
from management.models import *
import string
import random
import time
from multiprocessing import Process, Pool, Manager
from rdkit import Chem
from rdkit.Chem import Descriptors
from math import ceil
from django.core.paginator import Paginator
from django.db import connection, transaction
import sqlite3

def sorting(lst):
    if not lst:
        return []
    return (sorting([x for x in lst[1:] if x < lst[0]]) + [lst[0]] + sorting([x for x in lst[1:] if x >= lst[0]]))

def functionForMultiwrite(meaningless, size, process_number):
    # conn = sqlite3.connect(r'C:\\Users\\jay\\Documents\\file_manager\\db.sqlite3', isolation_level='EXCLUSIVE', timeout=30.0)
    conn = sqlite3.connect('db.sqlite3', isolation_level='EXCLUSIVE')
    c = conn.cursor()

    STRING_LENGTH = 150
    stringList = []
    subquery = ''
    count = 1

    for i in range(0, size):
        gen_a = ''.join(random.choices(string.ascii_uppercase + string.digits, k = STRING_LENGTH))
        gen_b = ''.join(random.choices(string.ascii_uppercase + string.digits, k = STRING_LENGTH))
        gen_c = ''.join(random.choices(string.ascii_uppercase + string.digits, k = STRING_LENGTH))
        gen_d = ''.join(random.choices(string.ascii_uppercase + string.digits, k = STRING_LENGTH))
        gen_e = ''.join(random.choices(string.ascii_uppercase + string.digits, k = STRING_LENGTH))

        #=========================================================================================
        # Raw
        #=========================================================================================
        # data = {
        #     "string_a":  ''.join(sorting(str(gen_a))),
        #     "string_b":  ''.join(sorting(str(gen_b))),
        #     "string_c":  ''.join(sorting(str(gen_c))),
        #     "string_d":  ''.join(sorting(str(gen_d))),
        #     "string_e":  ''.join(sorting(str(gen_e))),
        # }
        # StringData.objects.create(**data)

        #=========================================================================================
        # bulk insert sql
        #=========================================================================================
        a = ''.join(sorting(str(gen_a)))
        b = ''.join(sorting(str(gen_b)))
        c = ''.join(sorting(str(gen_c)))
        d = ''.join(sorting(str(gen_d)))
        e = ''.join(sorting(str(gen_e)))

        subquery += f'''
            ('{a}', '{b}', '{c}', '{d}', '{e}')
        '''
        #=========================================================================================
        # bulk insert model
        #=========================================================================================
        stringList.append(
            StringData(
                string_a = ''.join(sorting(str(gen_a))),
                string_b = ''.join(sorting(str(gen_b))),
                string_c = ''.join(sorting(str(gen_c))),
                string_d = ''.join(sorting(str(gen_d))),
                string_e = ''.join(sorting(str(gen_e))),
            )
        )
        
        if count % 10000 == 0:
            print("process(" + str(process_number) + "):", count)
            # StringData.objects.bulk_create(stringList)
            # stringList = []

            c = conn.cursor()

            query = 'INSERT INTO management_stringdata (string_a, string_b, string_c, string_d, string_e) VALUES ' + subquery
            subquery = ''
        else:
            subquery += ', '
        
        count += 1

    conn.close()

def multiwriteWrapper(total_data_amount, num_process):
    print("multi_function_by_process")
    
    batch_size = ceil(total_data_amount/num_process)
    process = []
    for i in range(num_process):
        p = Process(target = functionForMultiwrite, args = ([], batch_size, i))

        # 프로세스를 컨트롤 할 수 있게 하기 위해 주소를 저장해둬야함
        process.append(p)

        # 프로세스를 시작해라!
        p.start()

    for p in process:
        # 각 프로세스에게 다른 프로세스들이 일을 다 마칠때까지 이 이상 코드를 진행하지 말아라
        p.join()

#=======================================================================================================================
#=======================================================================================================================
#=======================================================================================================================
#=======================================================================================================================
@transaction.atomic
def functionForMultiread(rows):
    # connection.close()
    
    for row in rows:
        print(row)
    # return meaning

@transaction.non_atomic_requests
def multireadWrapper(paginator, num_process):
    print("#====================================================================================================")
    print("# multi_function_by_process")
    print("#====================================================================================================")

    process = []

    for page in range(1, paginator.num_pages + 1):
        obj = list(paginator.page(page).object_list)
        print("----------------------------------------------------------------")
        p = Process(target = functionForMultiread, args = (obj, None))
    
        # 프로세스를 컨트롤 할 수 있게 하기 위해 주소를 저장해둬야함
        process.append(p)

        # 프로세스를 시작해라!
        p.start()

    for p in process:
        # 각 프로세스에게 다른 프로세스들이 일을 다 마칠때까지 이 이상 코드를 진행하지 말아라
        p.join()
