

def xml_to_json(input_folder,
                output_json,
                output_image_folder):
    pass


    
def json_to_xml(json_file,
                output_folder,
                folder_input_images=None):
    pass

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