import json
import os
import random
import time
import logging

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import shutil

import sys

def remove_folder():
    with open('folders.txt',encoding='utf8') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    for folder in lines:
        print(folder)
        try:
            shutil.rmtree(folder)
        except:
            print('failed to remove ' + folder)


def validate_json():
    with open('final_funny2.json',encoding='utf8') as json_file:
        #print(json_file)
        videos = json.load(json_file)
        for video_info in videos:
            dst = video_info['v_dst']
            if not os.path.isfile( dst ):
                dst_dir = os.path.dirname(dst)
                print(dst_dir)

            

#validate_json()
remove_folder()











