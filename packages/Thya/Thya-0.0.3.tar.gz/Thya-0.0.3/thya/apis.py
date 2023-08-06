import requests
import json
import datetime
import imagesize


class Model:
    def __init__(self, 
                 api_key=None, 
                 project_id=None, 
                 url="https://api-infer.thya-technology.com/api/v1/inference"):
        self.api_key = api_key
        self.project_id = project_id
        self.url = url


    def run_inference(self, image_path):

        headers = {
            'x-api-key': self.api_key,
        }
        files = {
            'projectId': (None, self.project_id),
            'images': (image_path, open(image_path, 'rb'), 'image/jpeg') 
        }

        response = requests.request("POST", self.url, headers=headers, files=files)

        return self.post_process(response, image_path)
    

    def post_process(self, response, image_path):

        width, height = imagesize.get(image_path)

        data_json_coco = {
            "info": {
                "year": datetime.datetime.now().strftime("%Y"),
                "version": "1.0",
                "description": "Exported from Thya Technology",
                "contributor": "Thya Technology",
                "url": "https://www.thya-technology.com",
                "date_created": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            },
            "licenses": [
                # {
                # "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
                # "id": 1,
                # "name": "Attribution-NonCommercial-ShareAlike License"
                # }, 
            ],
            "categories": [
                # {
                #     "id": 2,
                #     "name": "cat",
                #     # "supercategory": "animal"
                # },
            ],
            "images": [
                {
                    "id": 0,
                    # "license": 1,
                    "file_name": image_path,
                    "height": height,
                    "width": width,
                    # "date_captured": null
                },
            ],
            "annotations": [
                # {
                #     "id": 0,
                #     "image_id": 0,
                #     "category_id": 2,
                #     "bbox": [260, 177, 231, 199],
                #     "segmentation": [],
                #     "area": 45969,
                #     "iscrowd": 0
                # },
            ]
        }

        data_json = json.loads(response.text)

        # Loop over annotations
        for rect in data_json["body"]["annotations"][0]["rects"]:

            # Handle label list and append to list if needed
            labelName = rect["labelName"]
            labelList = [cat["name"] for cat in data_json_coco["categories"]]
            if labelName in labelList:
                category_id = labelList.index(labelName)
            else: 
                category_id = len(data_json_coco["categories"])
                data_json_coco["categories"].append({
                    "id": category_id,
                    "name": labelName,
                })

            # Append annotation
            data_json_coco["annotations"].append({
                "id": len(data_json_coco["annotations"]),
                "image_id": 0,
                "category_id": category_id,
                "bbox": [rect["rect"]["x"], 
                         rect["rect"]["y"], 
                         rect["rect"]["x"] +rect["rect"]["width"], 
                         rect["rect"]["y"] +rect["rect"]["height"]],
                "segmentation": [],
                "area": rect["rect"]["width"] * rect["rect"]["height"],
                "iscrowd": 0,
                # "confidence": 1.0
            })
            
        

        return data_json_coco
    

def init_model(project_id, api_key):
    return Model(project_id=project_id, api_key=api_key)
    

def inference_model(model, image_path):
    return model.run_inference(image_path)
    
