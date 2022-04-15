from photoavatar.photoavatarterror import PhotoAvatarError
import photoavatar
import cv2
import numpy as np
import os
import time
class ImageProcess:
    @staticmethod
    def ExtractFace(src_image):
        """Parse the area of face,then output the area to another file
        
        Args:
            src_image:path of source image
        return:
            image with face region
        Exception:
            PhotoAvatarError:Invalid Image
        """
        facedb =photoavatar.variables["facedb"]
        face_cascade = cv2.CascadeClassifier(facedb)
        img = cv2.imread(src_image)
        (imgh,imgw) = img.shape[0:2]
        # 转灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 进行人脸检测
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        # 绘制人脸矩形框
        if len(faces) == 1:
            (x, y, w, h) = faces[0]
            if w<512 or h<512:
                raise PhotoAvatarError(PhotoAvatarError.IMAGE_ERROR,"Invalid Face image")

            x0 = x - (int)(w*0.3)
            y0 = y-(int)(h*0.3)
            w0 = x+(int)(w*1.3)
            h0 = y+(int)(h*1.3)
            if x0<0:
                x0=0
            if y0<0:
                y0=0
            if x0+w0>imgw:
                w0 = imgw-x0
            if y0+h0>imgh:
                h0 = imgh-y0

            face_Img = img[y0:y0+h0,x0:x0+w0]
            localtm = time.localtime()
            tmpfilename = time.strftime("%H%M%S.jpg")
            cache_folderpath = photoavatar.variables["cachepath"]
            temp_imagepath = os.path.join(cache_folderpath,tmpfilename)
            cv2.imwrite(temp_imagepath,face_Img)    

            return temp_imagepath
        else:
            raise PhotoAvatarError(PhotoAvatarError.IMAGE_ERROR,"No Face in Image")

    @staticmethod
    def RemoveWatermark(image_filepath):
        img = cv2.imread(image_filepath)
        #image[y1:y2,x1:x2]
        #image.shape(row,col)
        y_max = img.shape[0]
        x_max =img.shape[1]
        roi_y_min = y_max-112
        roi_y_max= y_max-12
        roi_x_min = x_max - 180
        roi_x_max = x_max - 12
        roi = img[roi_y_min:roi_y_max,roi_x_min:roi_x_max]
        roi_hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
        lower = np.array([0,0,221])
        upper = np.array([180,30,255])
        #创建水印蒙层
        kernel = np.ones((3,3),np.uint8)
        mask = cv2.inRange(roi_hsv,lower,upper)
        #对水印蒙层进行膨胀操作
        dilate = cv2.dilate(mask,kernel,iterations=1)
        res = cv2.inpaint(roi,dilate,7,flags=cv2.INPAINT_TELEA)
        img[roi_y_min:roi_y_max,roi_x_min:roi_x_max] = res
        cv2.imwrite(image_filepath,img)

    @staticmethod
    def UpdateFacethumbnail(ima_filepath):
        pass