import os
import json        
   
fname = r"C:\\Users\\Computing\Documents\\annotationDump\\testDir\\testannotations\\annotations\\instances_default.json" #name of COCO file

f = open (fname, 'r')
#read file
data = json.loads(f.read())

#get annotations
annotations = []
for i in data['annotations']:
    annotations.append(i)
f.close()

#print(annotations)
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

count = 1
#change id number ('id' in 'images')
for i in data['images']:
    old = i['id']
    i['id'] = count
    idToNew[old] = i['id']
    count += 1

count = 1


#create new frame names
newFrameImgs = [] #frame images where annotations have been detected, with new indexing
count = 0
#create image name from frame numbers and append to frameImgs
for frameNo in frames:
    strFrame = str(count)
    noLength = len(strFrame)
    frameImgName = templateName[0:-4-noLength] + strFrame + templateName[-4:]
    newFrameImgs.append(frameImgName)
    count +=1

j = 0
#change frame names in json
for i in data['images']:
    i['file_name'] = newFrameImgs[j]
    j += 1

#change image id ('image_id' in annotations) #change this
for i in data['annotations']:
    i['image_id'] = idToNew.get(i['image_id'])
    print(i['image_id'])
    count += 1

#need to change counts in relation to dirNumber
#need to concatenate jsons
newJson = 'C:\\Users\\Computing\\Documents\\annotationDump\\testDir\\testannotations\\annotations' + '\\' + 'reducedCOCO.json'

#output new COCO JSON without redundant (non-annotated) image data
with open(newJson, 'w') as f:
    json.dump(data, f, indent= 1) #indent needs to be changed to reflect COCO #,indent = None

# print("Reworked JSON file created in folder")