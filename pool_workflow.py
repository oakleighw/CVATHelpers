import os
import json
import shutil
#This file reads the directory for a coco file (json).
if __name__ == "__main__":
    #family directory to be pooled
    cwd = os.getcwd()
    orgDirs = os.listdir(cwd)
    #orgDirs = [x for x in orgDirs if x[-2:] != "py"]

    #videos need to be in the format (annotations folder, images folder)
    ###continuous dev notes###
    #this code now pools images into one folder. need to format new Json accordingly (use dictionary to new image name?) Json creation is currently commented out

    #insert parent dir here (e.g. parent/   of video 1 folder, video 2 folder)
    parent = r"C:\Users\Computing\Documents\annotationDump\testDir"

    orgDirs = os.listdir(parent)
    orgDirs = [(parent + "\\" + x + "\\annotations") for x in orgDirs]
    # orgDirs = [
    #     r"D:\datasets\greenVerges\annotationsDump\testDir2\day2\annotations",
    #     r"D:\datasets\greenVerges\annotationsDump\testDir2\day3\annotations"
    # ]

    #this will make sure every image saved has a unique image ID regardless of the directory
    globalCount = 0

    #number of images in total, increases on every directory
    totalImgs = 0

    jsonsConnected = [] # contains jsons with items at relevant index (json 1 has images 0...N, json 2 has images N..... N+n)

    for direc in orgDirs:
        #get name of json
        d = os.listdir(direc)
        jsons = []
        for file in d:
            if (file.split('.')[1] == 'json'):
                jsons.append(file)
        print(jsons)
    
        #only include one json in folder
        if len(jsons) > 1:
            print("Too many COCO files in directory. Please only include the one for this set of video frames")
            print("Skipping directory:", direc)
            continue
        if len(jsons) < 1:
            print("COCO Json file not found. Has this program been run from inside CVAT's exported annotations folder?")
            print("Skipping directory:", direc)
            continue
    
        fname = direc + '/' + jsons[0] #name of COCO file

        f = open (fname, 'r')
        #read file
        data = json.loads(f.read())
        f.close()

        #get annotations
        annotations = []
        for i in data['annotations']:
            annotations.append(i)
        

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
        
        #dictionary to update annotations later
        idToNew = {}

        count = totalImgs + 1 

        #change id number ('id' in 'images')
        for i in data['images']:
            old = i['id']
            i['id'] = count
            idToNew[old] = i['id']
            count += 1


        #create new frame names
        newFrameImgs = [] #frame images where annotations have been detected, with new indexing
        count = totalImgs
        #create image name from frame numbers and append to frameImgs
        for frameNo in frames: # incorrect
            strFrame = str(count)
            noLength = len(strFrame)
            frameImgName = templateName[0:-4-noLength] + strFrame + templateName[-4:]
            newFrameImgs.append(frameImgName)
            count +=1

        print("debug1:", len(data['images']))
        j = 0
        #change frame names in json
        for i in data['images']:
            i['file_name'] = newFrameImgs[j]
            j += 1

        count = totalImgs + 1
        #change image id ('image_id' in annotations)
        for i in data['annotations']:
            i['image_id'] = idToNew.get(i['image_id'])
            count += 1

        #increment totalImgs
        totalImgs += len(data['images'])

        #add new formed json to list
        
        jsonsConnected.append(data)

        ###Reduce images to only annotated ones (new folder)###

        pooledPath = os.path.dirname(os.path.dirname(direc))
        #copy images with annotations in into another folder
        
        if not os.path.exists(pooledPath + '\\pooledImages'):  #this is the folder that the images with annotations will be saved in
            os.makedirs(pooledPath + '\\pooledImages')

        sourceFolder = os.path.dirname(direc) + '\\images'
        destFolder = pooledPath + '\\pooledImages'

        # #first check if folder is empty- we don't want to copy more than once!
        # if (len(os.listdir(destFolder)) != 0):
        #     print('Destination Folder already contains images. \n Please delete them first!')
        #     quit()
        #print("len(frameImgs))   error here
        for i in range(0,len(frameImgs)):

            source = sourceFolder + '/' + frameImgs[i]

            newFrameNo = newFrameImgs[i]
            destination = destFolder + '/' + newFrameNo

            # print(source)
            # print(destination)
            if os.path.isfile(source):
                shutil.copy(source,destination) #copy images to filtered folder
        globalCount += 1

    #get total images and annotations array of dictionaries
    imgs = []
    annots = []
    
    for i in range(0, len(jsonsConnected)):
        print(i, "amount images:", len(jsonsConnected[i]['images']))
        print(i, "amount annotations:", len(jsonsConnected[i]['annotations']))
        imgs += jsonsConnected[i]['images']
        annots += jsonsConnected[i]['annotations']

    print(totalImgs)
    print(len(imgs))
    #use first json as template for joinedJsons
    newJson = jsonsConnected[0]
    newJson['images'] = imgs
    newJson['annotations'] = annots

    print(len(newJson['images']))
    print(len(newJson['annotations']))
    #dump new json
    newJsonName = parent + '\\' + 'reducedCOCO.json'
    with open(newJsonName, 'w') as f:
            json.dump(newJson, f, indent= 1) #indent needs to be changed to reflect COCO #,indent = None

    print("Reworked JSON file created in folder")
        


