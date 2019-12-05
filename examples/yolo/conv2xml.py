conv2xml.py

import os
import xml.etree.cElementTree as ET
from PIL import Image
import numpy as np

CLASSES = [&quot;aeroplane&quot;, &quot;bicycle&quot;, &quot;bird&quot;, &quot;boat&quot;,
        &quot;bottle&quot;, &quot;bus&quot;, &quot;car&quot;, &quot;cat&quot;, &quot;chair&quot;, &quot;cow&quot;, &quot;diningtable&quot;,
        &quot;dog&quot;, &quot;horse&quot;, &quot;motorbike&quot;, &quot;person&quot;, &quot;pottedplant&quot;, &quot;sheep&quot;,
        &quot;sofa&quot;, &quot;train&quot;, &quot;tvmonitor&quot;, &quot;truck&quot;, &quot;traffic_light&quot;]

key = 0
trainval = []
temp = []
data = {}

def apply_indent(elem, level = 0):
    # tab = space * 2
    indent = &quot;\n&quot; + level * &quot;  &quot;
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent + &quot;  &quot;
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent
        for elem in elem:
            apply_indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = indent


def label_mapping(label):
    if (label == &quot;pedestrian&quot;):
        return &quot;person&quot;
    elif (label == &quot;Red&quot;):
        return &quot;traffic_light&quot;
    elif (label == &quot;RedLeft&quot;):
        return &quot;traffic_light&quot;
    elif (label == &quot;Yellow&quot;):
        return &quot;traffic_light&quot;
    elif (label == &quot;YellowLeft&quot;):
        return &quot;traffic_light&quot;
    elif (label == &quot;Green&quot;):
        return &quot;traffic_light&quot;
    elif (label == &quot;GreenLeft&quot;):
        return &quot;traffic_light&quot;
    elif (label == &quot;biker&quot;):
        return &quot;bicycle&quot;
    else:
        return label
    
def create_xml():
    #print(voc)
    global key
    key += 1
    
    for img, boxes in data.items():
        root = ET.Element(&quot;annotation&quot;)
        ET.SubElement(root, &quot;filename&quot;).text = img
        ET.SubElement(root, &quot;folder&quot;).text = &quot;object-dataset/Images&quot;
        size = ET.SubElement(root, &quot;size&quot;)
        ImgFile = Image.open(&quot;Images/&quot; + img)
        w, h = ImgFile.size
        ET.SubElement(size, &quot;width&quot;).text = str(w)
        ET.SubElement(size, &quot;height&quot;).text = str(h)
        ET.SubElement(size, &quot;depth&quot;).text = &quot;3&quot;

        for voc in boxes:
            print(voc)
            obj = ET.SubElement(root, &quot;object&quot;)
            ET.SubElement(obj, &quot;name&quot;).text = voc[0]
            ET.SubElement(obj, &quot;pose&quot;).text = &quot;Unspecified&quot;
            ET.SubElement(obj, &quot;truncated&quot;).text = str(0)
            ET.SubElement(obj, &quot;difficult&quot;).text = str(0)
            bbox = ET.SubElement(obj, &quot;bndbox&quot;)
            ET.SubElement(bbox, &quot;xmax&quot;).text = str(voc[1])
            ET.SubElement(bbox, &quot;xmin&quot;).text = str(voc[2])
            ET.SubElement(bbox, &quot;ymax&quot;).text = str(voc[3])
            ET.SubElement(bbox, &quot;ymin&quot;).text = str(voc[4])

        apply_indent(root)
        tree = ET.ElementTree(root)
        tree.write(&quot;{}/{}.xml&quot;.format(&quot;xml&quot;, img.split(&quot;.jpg&quot;)[0]))
        trainval.append(&quot;object-dataset/Images/&quot; + img + &quot; &quot; + &quot;object-dataset/xml/&quot; + str(img.split(&quot;.jpg&quot;)[0]) + &quot;.xml&quot;)

def readFile(filename):
    with open(filename, &apos;r&apos;) as file:
        lines = file.readlines()
        labels = []
        XmlPrefix = &quot;&quot;
        for line in lines:
            ImagePrefix = &quot;Images/&quot;
            line = line.strip()
            image_label = line.split()
            
	    #print(len(image_label))
            l = len(image_label)
            voc = []
            if (label_mapping(image_label[int(l) - 1])) not in CLASSES:
                continue
            voc.append(label_mapping(image_label[int(l) - 1]))
            if not (label_mapping(image_label[int(l) - 1])) in temp:
                temp.append(label_mapping(image_label[int(l) - 1]))
            voc.append(image_label[3])
            voc.append(image_label[1])
            voc.append(image_label[4])
            voc.append(image_label[2])
            voc.append(image_label[0])
            print(voc)
            if image_label[0] not in data.keys():
                data[image_label[0]] = []
                data[image_label[0]].append(voc)
            else:
                data[image_label[0]].append(voc)

    create_xml()
            
        
    



if __name__ == &quot;__main__&quot;:
##############################
    filename = &quot;label.txt&quot;   # change this to your label txt file.
##############################    
    readFile(filename)
    with open(&quot;/home/guest/Wonjun/caffe-yolo/data/yolo/trainval.txt&quot;, &quot;a&quot;) as file:
        for line in trainval:
            file.write(line)
            file.write(&quot;\n&quot;)

    print(temp)
