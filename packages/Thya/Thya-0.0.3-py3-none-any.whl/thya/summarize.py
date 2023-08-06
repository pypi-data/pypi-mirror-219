import xlsxwriter
import xml.etree.ElementTree as ET
from collections import Counter

# Read list of XML files and summarize the information into a table in XLS format
def summarize_xmls(xmls, output_file, add_total=False):
    workbook = xlsxwriter.Workbook(output_file)
    worksheet = workbook.add_worksheet()

    # Add headers
    worksheet.write(0, 0, "File name")

    # Keep memory of classes
    classes = []

    #kKeep memory of total
    if add_total:
        cnt_total = Counter()

    # Loop over XMLs
    for i, xml in enumerate(xmls):
        # Read XML
        tree = ET.parse(xml)
        root = tree.getroot()

        # Get file name
        file_name = root.find("filename").text

        # Get counter of objects
        my_counter = Counter(obj.find("name").text for obj in root.findall("object"))

        # Add to total
        if add_total:
            cnt_total += my_counter
        
        # Add new classes to classes
        for cls_name in my_counter:
            if cls_name not in classes: 
                classes.append(cls_name)
                worksheet.write(0, len(classes), cls_name)

        # Write file name and counter
        worksheet.write(i+1, 0, file_name)
        for j, cls_name in enumerate(classes):
            if cls_name in my_counter:
                worksheet.write(i+1, j+1, my_counter[cls_name])

    # Write total
    if add_total:
        worksheet.write(len(xmls)+1, 0, "TOTAL")
        for j, cls_name in enumerate(classes):
            if cls_name in cnt_total:
                worksheet.write(len(xmls)+1, j+1, cnt_total[cls_name])
    
    # Close workbook
    workbook.close()
