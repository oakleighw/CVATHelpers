import os
import json
import shutil
#This file reads the directory for a coco file (json) . Then
if __name__ == "__main__":
    #get name of json
    d = os.listdir()
    jsons = []
    for file in d:
        if (file.split('.')[1] == 'json'):
            jsons.append(file)
    
    #only include one json in folder
    if len(jsons) > 1:
        print("Too many COCO files in directory. Please only include the one for this set of video frames")
        quit()
    if len(jsons) < 1:
        print("COCO Json file not found. Has this program been run from inside CVAT's exported annotations folder?")
        quit()
    
    fname = jsons[0] #name of COCO file

    f = open (fname, 'r')
    #read file
    data = json.loads(f.read())
    #dump json to analyse
    json.dump(data)
    #get annotations
    annotations = []
    for i in data['annotations']:
        annotations.append(i)
    f.close()

    # #get image no.s with litter from annotations
    # frames = []
    # for i in annotations:
    #     frames.append(i.get('image_id'))

    # #get frame image name from frame num
    # templateName = 'frame_000000.PNG' #format for images outputted by CVAT
    # frameImgs = [] #frame images where litter has been detected

    # #create image name from frame numbers and append to frameImgs
    # for frameNo in frames:
    #     strFrame = str(frameNo)
    #     noLength = len(strFrame)
    #     frameImgName = templateName[0:-4-noLength] + strFrame + templateName[-4:]
    #     frameImgs.append(frameImgName)


    # #copy images with litter in into another folder
    
    # if not os.path.exists('../imagesFiltered'):  #this is the folder that the images with litter will be saved in
    #     os.makedirs('../imagesFiltered')

    # sourceFolder = '../images'
    # destFolder = '../imagesFiltered'