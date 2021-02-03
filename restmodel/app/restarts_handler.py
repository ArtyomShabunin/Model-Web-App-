import asyncio
import glob
import time
import shutil
import os
from functools import reduce
from collections import Counter
import re


async def rewrite_restart():
    pass

    

async def make_restart_copy(model_name, location):
    file_time = time.localtime(time.time())
    file_name = rf'{model_name}_{file_time.tm_year}_{str(file_time.tm_mon).zfill(2)}_{str(file_time.tm_mday).zfill(2)}_{str(file_time.tm_hour).zfill(2)}_{str(file_time.tm_min).zfill(2)}_{str(file_time.tm_sec).zfill(2)}'
    full_name = os.path.basename(location).replace('restart', file_name)

    new_file_dir = r'\\'.join(os.path.dirname(location).split('\\')[0:-1]+['temp_restarts', full_name])

    os.makedirs(os.path.dirname(new_file_dir), exist_ok=True)
    shutil.copy(os.path.abspath(location), os.path.abspath(new_file_dir))

async def restarts_handler(model_name, paths, save_time):
    pattern =  re.compile('.*restart\.rst.*')
    await asyncio.sleep(10)
    while True:
        if time.time() - save_time > 30:
            print('Ошибка сохранения рестарта!')
            break

        restarts = []
        for path in paths:
            restarts += [os.path.join(path,i) for i in os.listdir(path) if pattern.match(i)]

        print(f'Число проектов {len(paths)}')
        print(f'Число рестартов {len(restarts)}')

        if len(restarts) > len(paths):
            restarts_is_new = True
            for restart in restarts:
                restarts_is_new = restarts_is_new and (time.time() - os.path.getmtime(restart) < 10)
                print(f'Рестарт {os.path.basename(restart)} обновлен {time.time() - os.path.getmtime(restart)}c назад')
                if not restarts_is_new:
                    break

            if restarts_is_new:
                print('Сохранение рестартов')
                await asyncio.sleep(8)
                for restart in restarts:
                    await make_restart_copy(model_name, restart)
                print('Restart saved!')
                break
        await asyncio.sleep(4)

def clear_temp_restarts():
    dir_list = glob.glob('./**/temp_restarts', recursive=True)
    for folder in dir_list:
        shutil.rmtree(os.path.abspath(folder))

def show_restarts_list(dir_list):
    prj_count = len(dir_list)
    res_list = []
    for d in dir_list:
        res_list.append(glob.glob(os.path.join(d, '*.rst'), recursive=True))

    res_list = reduce(lambda x,y :x+y, res_list)
    res_list = [os.path.basename(i) for i in res_list]

    restarts_counter = Counter(res_list)

    d = {'restarts': [i for i in restarts_counter if restarts_counter[i] >= prj_count]}
    return d
