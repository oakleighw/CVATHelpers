# CVATHelpers
When annotating raw video, there may be many frames which do not contain annotations, and if they are not needed, these are redundant. CVAT by default exports all frames from your video.

This Repo contains files which 
1) Sorts frames such that only the annotated remain (in a new folder)
2) Creates an updated JSON COCO file
3) Organises and filters annotations; pooling them into one folder and file

These tools work with frames created in .PNG format
# Tools
!!Important!! CVAT Exported files contain "annotations" and "images" directories. Please
place the required file(s) in the "annotations" folder prior to running.

## Reduce Frames
Creates a folder "imagesFiltered" in the parent directory which contains only frames that contain litter.

## Reduce Json
Creates a new JSON file using the original exported JSON. This JSON is also on one line. "Images" list data is removed for non-annotated frames. However, image IDs are not changed, but remain to match with the image IDs in the annotations list.

## Reduce CVAT
A standalone program that accomplishes both of these tasks.

# Image and annotation pooling
This sorts annotations and frames into ONE folder and ONE Json file. It is handy for reducing the amount of uploading into external conversion software or creating training/ testing directories.

## Pooling Instructions:
1. Replace the line of code specified in this file with the name of the parent directory.
2. Within this directory, include a folder for each video. 
3. Each video folder must contain a folder called "annotations" (includes ONE json coco file exported from CVAT)
4. Each video folder must contain a folder called "images" (All the frames from video exported from CVAT)

## Output
1. In the parent folder specified, a "pooledImages" folder will be created, containing TOTAL frames that ONLY have at least one annotation (similar to "Reduce Frames")
2. Also in the parent folder will be a new json file containing all the frames and annotations.
3. Note: Frames and annotations have reassigned names and ID's based on the new index.
