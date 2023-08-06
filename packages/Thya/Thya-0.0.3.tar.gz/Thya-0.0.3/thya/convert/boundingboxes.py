from xmltodict import unparse
import json
import os
import shutil
from tqdm import tqdm
import xml.etree.ElementTree as ET
import re

def base_dict(filename, width, height, depth=3):
    return {
        "annotation": {
            "filename": os.path.split(filename)[-1],
            "folder": "VOCCOCO", "segmented": "0", "owner": {"name": "unknown"},
            "source": {'database': "The COCO 2017 database", 'annotation': "COCO 2017", "image": "unknown"},
            "size": {'width': width, 'height': height, "depth": depth},
            "object": []
        }
    }


BBOX_OFFSET = 0


def base_object(size_info, name, bbox):
    x1, y1, w, h = bbox
    x2, y2 = x1 + w, y1 + h

    width = size_info['width']
    height = size_info['height']

    x1 = max(x1, 0) + BBOX_OFFSET
    y1 = max(y1, 0) + BBOX_OFFSET
    x2 = min(x2, width - 1) + BBOX_OFFSET
    y2 = min(y2, height - 1) + BBOX_OFFSET

    return {
        'name': name, 'pose': 'Unspecified', 'truncated': '0', 'difficult': '0',
        'bndbox': {'xmin': x1, 'ymin': y1, 'xmax': x2, 'ymax': y2}
    }


def get_image_info(annotation_root, extract_num_from_imgid=True):
    path = annotation_root.findtext('path')
    if path is None:
        filename = annotation_root.findtext('filename')
    else:
        filename = os.path.basename(path)
    img_name = os.path.basename(filename)
    img_id = os.path.splitext(img_name)[0]
    if extract_num_from_imgid and isinstance(img_id, str):
        img_id = int(re.findall(r'\d+', img_id)[0])

    size = annotation_root.find('size')
    width = int(size.findtext('width'))
    height = int(size.findtext('height'))

    image_info = {
        'file_name': filename,
        'height': height,
        'width': width,
        'id': img_id
    }
    return image_info


def get_coco_annotation_from_obj(obj, label2id):
    label = obj.findtext('name')
    assert label in label2id, f"Error: {label} is not in label2id !"
    category_id = label2id[label]
    bndbox = obj.find('bndbox')
    xmin = int(float(bndbox.findtext('xmin'))) - 1
    ymin = int(float(bndbox.findtext('ymin'))) - 1
    xmax = int(float(bndbox.findtext('xmax')))
    ymax = int(float(bndbox.findtext('ymax')))
    assert xmax > xmin and ymax > ymin, f"Box size error !: (xmin, ymin, xmax, ymax): {xmin, ymin, xmax, ymax}"
    o_width = xmax - xmin
    o_height = ymax - ymin
    ann = {
        'area': o_width * o_height,
        'iscrowd': 0,
        'bbox': [xmin, ymin, o_width, o_height],
        'category_id': category_id,
        'ignore': 0,
        'segmentation': []  # This script is not for segmentation
    }
    return ann

def xml_to_json(input_folder,
                output_json,
                output_image_folder):
    
    output_json_dict = {
        "images": [],
        "annotations": [],
        "categories": []
    }

    annotation_paths = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.xml')]

    bnd_id = 1  # START_BOUNDING_BOX_ID, TODO input as args ?
    print('Start converting !')
    label2id = {}
    for a_path in tqdm(annotation_paths):
        # Read annotation xml
        ann_tree = ET.parse(a_path)
        ann_root = ann_tree.getroot()

        img_info = get_image_info(annotation_root=ann_root,
                                  extract_num_from_imgid=True)
        img_id = img_info['id']
        output_json_dict['images'].append(img_info)

        for obj in ann_root.findall('object'):
            label = obj.findtext('name')
            if label not in label2id:
                label2id[label] = len(label2id) + 1

            ann = get_coco_annotation_from_obj(obj=obj, label2id=label2id)
            ann.update({'image_id': img_id, 'id': bnd_id})
            output_json_dict['annotations'].append(ann)
            bnd_id = bnd_id + 1

    for label, label_id in label2id.items():
        category_info = {'supercategory': 'none', 'id': label_id, 'name': label}
        output_json_dict['categories'].append(category_info)


    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    with open(output_json, 'w') as f:
        f.write(json.dumps(output_json_dict, indent=4))
    print('Conversion finished !')

    
def json_to_xml(json_file,
                output_folder,
                folder_input_images=None):

    filename = json_file
    print("Parse", filename)
    data = json.load(open(filename))


    cate = {x['id']: x['name']
            for x in data['categories']}

    images = {}
    for im in tqdm(data["images"], "Parse Images"):
        img = base_dict(im['file_name'], im['width'], im['height'], 3)
        images[im["id"]] = img

    for an in tqdm(data["annotations"], "Parse Annotations"):
        ann = base_object(images[an['image_id']]['annotation']
                        ["size"], cate[an['category_id']], an['bbox'])
        images[an['image_id']]['annotation']['object'].append(ann)

    dst_base = output_folder
    dst_dirs = {x: os.path.join(dst_base, x)
                for x in ["Annotations", "ImageSets", "JPEGImages"]}
    dst_dirs['ImageSets'] = os.path.join(dst_dirs['ImageSets'], "Main")
    # for k, d in dst_dirs.items():
    #     os.makedirs(d, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)


    for k, im in tqdm(images.items(), "Write Annotations"):
        im['annotation']['object'] = im['annotation']['object'] or [None]
        # print(im['annotation']['filename'])
        unparse(im,
                open(os.path.join(output_folder,
                                f"{os.path.splitext(im['annotation']['filename'])[0]}.xml"), "w"),
                # open(os.path.join(dst_dirs["Annotations"],
                #         "{}.xml".format(str(k).zfill(12))), "w"),
                full_document=False, pretty=True)

        image_name = im['annotation']['filename']
        if folder_input_images is None:
            src = os.path.join(os.path.dirname(json_file),
                            image_name)
        else:
            src = os.path.join(folder_input_images,
                               image_name)

        dst = os.path.join(output_folder,
                        image_name)
        if not os.path.exists(dst):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)

# Extra functions
# COCO = JSON
# VOC = XML
def coco_to_voc(json_file,
                output_folder,
                folder_input_images=None):
    json_to_xml(json_file,
                output_folder,
                folder_input_images)
    
def voc_to_coco(input_folder,
                output_json,
                output_image_folder=None):
    xml_to_json(input_folder,
                output_json,
                output_image_folder)