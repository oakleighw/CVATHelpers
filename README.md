# CVATHelpers
When annotating raw video, there may be many frames which do not contain annotations, and if they are not needed, these are redundant. CVAT by default exports all frames from your video.

This Repo contains files which 
1) Sorts frames such that only the annotated remain (in a new folder)
2) Creates an updated JSON COCO file
~~3) Organises and filters annotations; pooling them into one folder and file~~ [Removed due to Error]

These tools work with frames created in .PNG format
# Tools
!!Important!! CVAT Exported files contain "annotations" and "images" directories. Please
place the required file(s) in the "annotations" folder prior to running.

## Reduce Frames
#### "reduceFrames.py"
Creates a folder "imagesFiltered" in the parent directory which contains only frames that contain litter.

## Reduce Json
#### "reduceJSON.py"
Creates a new JSON file using the original exported JSON. This JSON is also on one line. "Images" list data is removed for non-annotated frames. However, image IDs are not changed, but remain to match with the image IDs in the annotations list.

## Reduce CVAT
#### "reduceCVAT.py"
A standalone program that accomplishes both of these tasks.

