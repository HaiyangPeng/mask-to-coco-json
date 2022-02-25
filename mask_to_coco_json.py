#!/usr/bin/env python3

import datetime
import numpy as np
import cv2


def create_image_info(image_id, file_name, image_size, 
                      date_captured=datetime.datetime.utcnow().isoformat(' '),
                      license_id=1, coco_url="", flickr_url=""):

    image_info = {
            "id": image_id,
            "file_name": file_name,
            "width": image_size[1],
            "height": image_size[0],
            "date_captured": date_captured,
            "license": license_id,
            "coco_url": coco_url,
            "flickr_url": flickr_url
    }

    return image_info


def create_annotation_infos(annotation_id, image_id, category_info, binary_mask):
    
    is_crowd = category_info['is_crowd']
    annotation_infos = []
    
    # pad mask to close contours of shapes which start and end at an edge
    padded_binary_mask = (np.pad(binary_mask, pad_width=1, mode='constant', constant_values=0) * 255).astype('uint8')
    contours, _ = cv2.findContours(padded_binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
    contours = np.subtract(contours, 1)
    
    for i, contour in enumerate(contours):
        if len(contour) < 3:  # filter unenclosed objects
            continue
    
        x, y, w, h = cv2.boundingRect(contour)   
        bounding_box = [x, y, w, h]
        seg_area = cv2.contourArea(contour)
        bbox_area = w * h
        
        if bbox_area < 4:  # filter small objects
            continue

        segmentation = contour.ravel().tolist()
        segmentation = [0 if i < 0 else i for i in segmentation]

        annotation_info = {
            "id": annotation_id,
            "image_id": image_id,
            "category_id": category_info["id"],
            "iscrowd": is_crowd,
            "area": seg_area,  # it's float
            "bbox": bounding_box,
            "segmentation": [segmentation],
            "width": binary_mask.shape[1],
            "height": binary_mask.shape[0],
        } 
        
        annotation_id += 1
        
        annotation_infos.append(annotation_info)

    return annotation_infos, annotation_id
