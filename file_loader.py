from lib2to3.pgen2 import token
import os
import pathlib
import requests
from datetime import datetime
import time

PATH_TO_DIR = './'
SAVED_FILENAME = 'file_list.txt'
URL = 'http://192.168.1.1'
TOKEN = 'd24e3rsdfs3rwefsdfse3rwerwerfsdf'
DEVICE_ID = 1
UPDATE_DELAY_SECONDS = 60*10

def create_file_if_not_exists(PATH_TO_DIR, SAVED_FILENAME):
    path = PATH_TO_DIR + '/' + SAVED_FILENAME
    try:
        file = open(path, 'r')
        file.close()
        print('%s is exists' % (path))
    except IOError:
        file = open(path, 'w')
        file.close()
        print('%s is created' % (path))

def read_saved_filenames(path, filename):
    saved_files = []
    with open(path + '//' + filename, 'r') as f:
        saved_files = [line.rstrip('\n') for line in f]
    return saved_files

def save_filenames(files, base_dir, filename):
    path = base_dir + '/' + filename

    with open(path, 'w') as f:
        for s in files:
            f.write(str(s) + '\n')

def get_files(PATH_TO_DIR, SAVED_FILENAME):
    files = list(pathlib.Path(PATH_TO_DIR).glob('**/*.*'))
    files = [file.__str__() for file in files]
    files.remove(SAVED_FILENAME)
    return files

def send_data(URL, file, values):
    r = requests.post(URL, files=file, data=values)
    return r

def main():
    create_file_if_not_exists(PATH_TO_DIR, SAVED_FILENAME)
    files = get_files(PATH_TO_DIR, SAVED_FILENAME)
    saved_files = read_saved_filenames(PATH_TO_DIR, SAVED_FILENAME)
    print(files)
    print('saved', saved_files)

    for filename in files:
        try:
            file =  { filename: open(filename) }
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            values = {
                'date': date_time_str,
                'token': TOKEN,
                'device': DEVICE_ID,
            }
            response = send_data(URL, file, values)

            print(response.status_code)
            if response.status_code == 200:
                saved_files.append(filename)
                save_filenames(saved_files, PATH_TO_DIR, SAVED_FILENAME)

        except Exception as e:
            print(e)

def loop():
    while True:
        print('running')
        main()
        time.sleep(UPDATE_DELAY_SECONDS)


if __name__ == "__main__":
    # main()
    loop()
