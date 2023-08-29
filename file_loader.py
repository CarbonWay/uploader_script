from lib2to3.pgen2 import token
import os
import pathlib
import requests
from datetime import datetime
import time

PATH_TO_DIR = './data'
SAVED_FILENAME_PATH = 'file_list.txt'
URL = 'http://127.0.0.1:8000/'
TOKEN = 'token'
DEVICE_ID = 0
UPDATE_DELAY_SECONDS = 60*10

def load_file_list(SAVED_FILENAME_PATH):
    req_url = URL + 'loader/load-file-list'
    r = requests.post(req_url, data={'token': TOKEN})
    saved_file_list = r.json()['files']
    with open(SAVED_FILENAME_PATH, 'w') as f:
        for item in saved_file_list:
            f.write("%s\n" % item)

def read_saved_filenames(path_to_filename):
    saved_files = []
    with open(path_to_filename, 'r') as f:
        saved_files = [line.rstrip('\n') for line in f]
    return saved_files

def save_filenames(files, path_to_filename):
    path = path_to_filename

    with open(path, 'w') as f:
        for s in files:
            f.write(str(s) + '\n')

def get_files(PATH_TO_DIR, SAVED_FILENAME):
    files = list(pathlib.Path(PATH_TO_DIR).glob('**/*.*'))
    files = [file.__str__() for file in files]
    if SAVED_FILENAME in files:
        print('removing file from list', SAVED_FILENAME)
        files.remove(SAVED_FILENAME)
    if PATH_TO_DIR + '/' + SAVED_FILENAME in files:
        print('removing file from list 2', SAVED_FILENAME)
        files.remove(PATH_TO_DIR + '/' + SAVED_FILENAME)

    return files

def send_data(file, values):
    req_URL = URL + 'loader/upload'
    r = requests.post(req_URL, files=file, data=values, cookies={'def': 'defvalue'})
    return r

def main():
    load_file_list(SAVED_FILENAME_PATH)
    files = get_files(PATH_TO_DIR, SAVED_FILENAME_PATH)
    saved_files = read_saved_filenames(SAVED_FILENAME_PATH)
    print('found files', files)
    print('server files', saved_files)

    for filename in files:
        try:
            if filename in saved_files:
                break
            file =  { filename: open(filename, 'rb') }
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            values = {
                'date': date_time_str,
                'token': TOKEN,
                'device': DEVICE_ID,
            }
            print('sending', filename)
            response = send_data(file, values)

            if response.status_code == 200:
                saved_files.append(filename)
                save_filenames(saved_files, SAVED_FILENAME_PATH)

        except Exception as e:
            print(e)

def loop():
    while True:
        print('running')
        main()
        time.sleep(UPDATE_DELAY_SECONDS)


if __name__ == "__main__":
    loop()
