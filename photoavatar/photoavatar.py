from msilib.schema import Error
from photoavatar.photoavatarterror import PhotoAvatarError
from photoavatar.imageprocess import ImageProcess
from photoavatar.photolab import Photolab
import os
import time

class PhotoAvatar:

    @classmethod
    def process_images(cls,src_images,dst_folderpath,action_url):
        '''
        Process image list using funcion in photolab,then output to dst_folder

        Args:
            src_images:list of image file path
            dst_folder:output folder path, the destination file name will be the same source image file path
            action_url:action link to photolab
        Returns:

        Raise:

        '''
        for src_imagepath in src_images:
            try:
                localtm = time.localtime()
                filename = time.strftime("%Y%m%d%H%M%S.jpg")
                dst_filepath = os.path.join(dst_folderpath,filename)
                cls.process_oneimage(src_imagepath,dst_filepath,action_url)
                time.sleep(2)
            except PhotoAvatarError as err:
                print("error:{}".format(err))

    @classmethod
    def process_oneimage(cls,src_imagepath,dst_imagepath,action_url):
        '''
        Process image  using funcion in photolab,then output to dst_folder

        Args:
            src_image:image file path
            dst_folder:output folder path, the destination file name will be the same source image file path
            action_url:action link to photolab
        Returns:

        Raise:
            PhotoAvatarError(1001):Invalid Image
            PhotoAvatarError(1002):Can not process image using action _url
        '''

        faceImagepath = ImageProcess.ExtractFace(src_imagepath)
        Photolab.submitImageForProcess(faceImagepath,dst_imagepath,action_url)
        ImageProcess.RemoveWatermark(dst_imagepath)
        ImageProcess.UpdateFacethumbnail(dst_imagepath)