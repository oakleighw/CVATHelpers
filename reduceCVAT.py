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

    #get annotations
    annotations = []
    for i in data['annotations']:
        annotations.append(i)
    f.close()

    #get image no.s with annotations
    frames = []
    for i in annotations:
        frames.append((i.get('image_id'))-1)#-1 as id's are framenumber +1

    #get frame image name from frame num
    templateName = 'frame_000000.PNG' #format for images outputted by CVAT
    frameImgs = [] #frame images where annotations have been detected

    #create image name from frame numbers and append to frameImgs
    for frameNo in frames:
        strFrame = str(frameNo)
        noLength = len(strFrame)
        frameImgName = templateName[0:-4-noLength] + strFrame + templateName[-4:]
        frameImgs.append(frameImgName)
    
    #remove duplicates
    frameImgs = list(set(frameImgs))
    
    ###Create new COCO JSON###

    #find indices of redundant (non-annotated) image data
    imageListSize = len(data['images'])
    toDelete = [] #stores indexes of entries to delete
    for i in range(0, imageListSize):
        if (data['images'][i].get('file_name') not in frameImgs):
            toDelete.append(i)


    #sort indices to delete to allow for 'pop'
    toDelete = sorted(toDelete, reverse=True)
    #delete JSON image dictionaries which store info about redundant (non-annotated) image data
    for i in toDelete:
        data['images'].pop(i)

    #output new COCO JSON without redundant (non-annotated) image data
    with open('reducedCOCO.json', 'w') as f:
        json.dump(data, f, indent= None) #indent needs to be changed to reflect COCO
    
    print("Reworked JSON file created in folder")

    ###Reduce images to only annotated ones (new folder)###

    #copy images with annotations in into another folder
    
    if not os.path.exists('../imagesFiltered'):  #this is the folder that the images with annotations will be saved in
        os.makedirs('../imagesFiltered')

    sourceFolder = '../images'
    destFolder = '../imagesFiltered'

    #first check if folder is empty- we don't want to copy more than once!
    if (len(os.listdir(destFolder)) != 0):
        print('Destination Folder already contains images. \n Please delete them first!')
        quit()

    for frameN in frameImgs:
        source = sourceFolder + '/' + frameN
        destination = destFolder + '/' + frameN
        if os.path.isfile(source):
            shutil.copy(source,destination) #copy images to filtered folder