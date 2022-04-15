from photoavatar.photoavatarterror import PhotoAvatarError
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import cv2
import numpy
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import os
from urllib.parse import urlparse
import photoavatar
class Photolab:
    @staticmethod
    def downloadfile(url,dest_filepath):
        url2 = url.replace("https","http")
        filepath = urlparse(url2)
        r = requests.get(url2, allow_redirects=True)
        open(dest_filepath, 'wb').write(r.content)    

    @staticmethod
    def submitImageForProcess(src_imagepath,dst_imagepath,action_url):
        '''automating web browser for submitting local image to photolab to process,
        then download the result image to local folder

        Args
            src_image:source image file path
            dst_folder:destination folder for result image
            action url:url for process
        return:
            destination image path            
        Exception:
            PhotoAvatarError
        '''
        mouse = PyMouse()
        key =PyKeyboard()    
        browser = webdriver.Chrome()
        browser.get(action_url)
        time.sleep(1)
        applyPhoto = browser.find_element_by_id('js-pickfiles')
        try:
            cookiebtn = browser.find_element_by_class_name("js-app-cookieBtn")
            ActionChains(browser).click(cookiebtn).perform()
            time.sleep(1)
        except:
            pass


        ActionChains(browser).click(applyPhoto).perform()
        time.sleep(1)
        #save to local file

        key.type_string(src_imagepath)
        time.sleep(1)
        key.tap_key(key.enter_key)
        time.sleep(1)
        key.tap_key(key.enter_key)

        # continue
        for i in range(200):
            try:
                continue_btn = browser.find_element_by_class_name("js-continue")
                ActionChains(browser).click(continue_btn).perform()
                time.sleep(1)
                break
            except:
                time.sleep(1)
                print("find continue button")
                pass

        # download
        print("download image")
        time.sleep(10)
        for i in range(500):
            try:
                img_box = browser.find_element_by_id("js-res-img")
                print("download image1")
                img_url = img_box.get_attribute("data-src")
                print("download image2:"+img_url)
                time.sleep(1)
                Photolab.downloadfile(img_url,dst_imagepath)
                print("download image3")
                break
            except:
                time.sleep(1)
                print("find res-img")
     

