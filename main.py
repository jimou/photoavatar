from sqlalchemy import false
from photoavatar import *
import photoavatar
import win32api,win32con
import os
import time
if __name__ == "__main__":
    localtm = time.localtime()
    filename = time.strftime("%Y%m%d%H%M%S.jpg")
    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders',0,win32con.KEY_READ)
    myDocumentFolder = win32api.RegQueryValueEx(key,'Personal')[0]
    dest_folderpath = os.path.join(myDocumentFolder,"photoavatar")
    cache_folderpath = os.path.join(dest_folderpath,"cache")    
    if os.path.exists(dest_folderpath) == True:
        pass
    else:
        os.makedirs(dest_folderpath)

    if os.path.exists(cache_folderpath) == True:
        pass
    else:
        os.makedirs(cache_folderpath)

    photoavatar.variables["cachepath"] = cache_folderpath
    photoavatar.variables["facedb"] = r"C:\ProgramData\Anaconda3\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml"
    srcImags = [r'D:\sampleimages\face1.jpg',r'D:\sampleimages\aaa.jpg']
    #srcImags = [r'D:\sampleimages\face1.jpg']
    action_url = 'https://photolab.me/r/jVwlgdA'
    PhotoAvatar.process_images(srcImags,dest_folderpath,action_url)
