import numpy as np
import os
import glob
from tqdm import tqdm
import cv2
import mask_to_coco_json
import json

 
ROOT_DIR = '/path/to/your/project/mask-to-coco-json/examples'
IMAGE_DIR = os.path.join(ROOT_DIR, "images")
ANNOTATION_DIR = os.path.join(ROOT_DIR, "masks")
SINGLE_MASK_DIR = os.path.join(ROOT_DIR, "single_masks")
 
INFO = {
    "description": "facade Dataset",
}
 
LICENSES = [
    {
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike License",
        "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
    }
]
 
CATEGORIES = [
    {
        'id': 0,
        'name': 'xx',
        'supercategory': 'xx',
        'color': [0, 255, 255]  # the color used to mask the object
    }
]

 
def main():
 
    coco_output = {
        "info": INFO,
        "licenses": LICENSES,
        "categories": CATEGORIES,
        "images": [],
        "annotations": []
    }
    
    # initial ids
    image_id = 1
    segmentation_id = 1
   
    # find image and mask paths
    image_files = glob.glob(IMAGE_DIR + '/*.jpg')
    label_files = glob.glob(ANNOTATION_DIR + '/*.png')
 
    # go through each image
    for image_filename in tqdm(image_files):
        image = cv2.imread(image_filename)

        # skip the image without label file
        base_name = os.path.basename(image_filename)
        label_name = os.path.join(ANNOTATION_DIR, os.path.splitext(base_name)[0] + '.png')
        if label_name not in label_files:
            continue
        
        mask = cv2.imread(label_name)  # bgr mask 
        
        image_info = mask_to_coco_json.create_image_info(
            image_id, os.path.basename(image_filename), image.shape)
        coco_output["images"].append(image_info)        
        
        # go through each existing category
        for category_dict in CATEGORIES:
            color = category_dict['color']
            class_id = category_dict['id']
            category_info = {'id': class_id, 'is_crowd': 0}  # do not support the crowded type
            
            binary_mask = np.all(mask == color, axis=-1).astype('uint8')  # quick search
            
            cv2.imwrite(os.path.join(SINGLE_MASK_DIR, base_name), binary_mask * 255)            
            
            annotation_info, annotation_id = mask_to_coco_json.create_annotation_infos(
                segmentation_id, image_id, category_info, binary_mask)

            coco_output["annotations"].extend(annotation_info)

            segmentation_id = annotation_id

        image_id = image_id + 1
 
    with open('{}/train.json'.format(ROOT_DIR), 'w') as output_json_file:
        json.dump(coco_output, output_json_file)
 
 
if __name__ == "__main__":
    main()