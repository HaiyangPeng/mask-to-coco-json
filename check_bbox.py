import os
from pycocotools.coco import COCO
from skimage import io
from matplotlib import pyplot as plt

json_file = '/path/to/your/project/mask-to-coco-json/examples/train.json'
dataset_dir = '/path/to/your/project/mask-to-coco-json/examples/images/'
coco = COCO(json_file)
catIds = coco.getCatIds(catNms=['0'])  # category ids, e.g., catNms=['0', '1', ...] which is in accordance with the CATEGORIES defined in main.py
imgIds = coco.getImgIds(catIds=catIds )
for i in range(len(imgIds)):
    img = coco.loadImgs(imgIds[i])[0]
    I = io.imread(dataset_dir + img['file_name'])
    plt.axis('off')
    plt.imshow(I)
    annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=None)
    anns = coco.loadAnns(annIds)
    coco.showAnns(anns)
    plt.savefig('/path/to/your/project/mask-to-coco-json/examples/bbox.png')
    plt.show() 

