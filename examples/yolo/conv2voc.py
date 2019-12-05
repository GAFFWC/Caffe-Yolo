
conv2voc.py

import os
import xml.etree.cElementTree as ET
from PIL import Image
import argparse
CLASSES = [&quot;aeroplane&quot;, &quot;bicycle&quot;, &quot;bird&quot;, &quot;boat&quot;,
        &quot;bottle&quot;, &quot;bus&quot;, &quot;car&quot;, &quot;cat&quot;, &quot;chair&quot;, &quot;cow&quot;, &quot;diningtable&quot;,
        &quot;dog&quot;, &quot;horse&quot;, &quot;motorbike&quot;, &quot;person&quot;, &quot;pottedplant&quot;, &quot;sheep&quot;,
        &quot;sofa&quot;, &quot;train&quot;, &quot;tvmonitor&quot;, &quot;truck&quot;, &quot;traffic_light&quot;, &quot;traffic_sign&quot;, &quot;signage&quot;]


parser = argparse.ArgumentParser()
parser.add_argument(&apos;-f&apos;, required = True, help = &apos;folder name&apos;)

args = parser.parse_args() 
PATH_folder = str(args.f)
xml_list = os.listdir(PATH_folder + &quot;xml2/&quot;)
trainval = []
temp = []

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

def label(name):
    if name == &quot;pedestrian&quot;:
        return &quot;person&quot;
    elif name == &quot;motorcycle&quot;:
        return &quot;motorbike&quot;
    elif &quot;traffic_light&quot; in name:
        return &quot;traffic_light&quot;
    return name

def read_xml():
    for xml in xml_list:
        if &quot;.swp&quot; in xml:
            break
        #print(&quot;Open : &quot; + PATH_folder + &quot;xml2/&quot; + xml)
        tree = ET.parse(PATH_folder + &quot;xml2/&quot; + xml)
        parse_xml(tree.getroot())


def parse_xml(root):
    bbox_list = []
    ImageInfo = root.find(&quot;ImageInfomation&quot;)
    ImgFile = ImageInfo.find(&quot;ShowFileName&quot;).text
    ImgFile = ImgFile.split(&quot;.png&quot;)[0] + &quot;.jpg&quot;
    #print(&quot;converting : &quot; + ImgFile)
    img = Image.open(PATH_folder + &quot;Images/&quot; + ImgFile)
    w, h = img.size 
    bbox_list.append(ImgFile)
    bbox_list.append(w)
    bbox_list.append(h)
    for bbox in root.iter(&quot;ImageLabel&quot;):
        box1 = []
        Annotation = bbox.find(&quot;Annotation&quot;)
       
        if Annotation is None:
            continue 

        LabelName = label(Annotation.find(&quot;LabelName&quot;).text)
        if LabelName not in CLASSES:
            continue
        
        if LabelName not in temp:
            temp.append(LabelName)
        box1.append(LabelName)
        Shape = bbox.find(&quot;Shape&quot;)
        
        maxx = 0
        minx = w
        maxy = 0
        miny = h 
        for AnchorPoint in Shape.iter(&quot;AnchorPoint&quot;):
            maxx = max(int(float(AnchorPoint.attrib[&apos;X&apos;])), maxx)
            minx = min(int(float(AnchorPoint.attrib[&apos;X&apos;])), minx)
            maxy = max(int(float(AnchorPoint.attrib[&apos;Y&apos;])), maxy)
            miny = min(int(float(AnchorPoint.attrib[&apos;Y&apos;])), miny)

        if (minx < 0): minx = 0
        if (maxx > w): maxx = w
        if (miny < 0): miny = 0
        if (maxy > h): maxy = h

        if (maxx - minx) < w / 20:
            continue
        if (maxy - miny) < h / 20:
            continue

        box1.append(maxx)
        box1.append(minx)
        box1.append(maxy)
        box1.append(miny)

        bbox_list.append(box1)

    create_xml(bbox_list)

def create_xml(bbox_list):
    if len(bbox_list) == 3:
        return
    
    root = ET.Element(&quot;annotation&quot;)
    ET.SubElement(root, &quot;filename&quot;).text = bbox_list[0]
    ET.SubElement(root, &quot;folder&quot;).text = PATH_folder + &quot;Images&quot;
    size = ET.SubElement(root, &quot;size&quot;)
    ET.SubElement(size, &quot;width&quot;).text = str(bbox_list[1])
    ET.SubElement(size, &quot;height&quot;).text = str(bbox_list[2])
    ET.SubElement(size, &quot;depth&quot;).text = &quot;3&quot;


    bbox_cnt = len(bbox_list) - 3

    for idx in range(bbox_cnt):        
        obj = ET.SubElement(root, &quot;object&quot;)
        ET.SubElement(obj, &quot;name&quot;).text = bbox_list[idx + 3][0]
        ET.SubElement(obj, &quot;pose&quot;).text = &quot;Unspecified&quot;
        ET.SubElement(obj, &quot;truncated&quot;).text = str(0)
        ET.SubElement(obj, &quot;difficult&quot;).text = str(0)

        bbox = ET.SubElement(obj, &quot;bndbox&quot;)
        ET.SubElement(bbox, &quot;xmax&quot;).text = str(bbox_list[idx + 3][1])
        ET.SubElement(bbox, &quot;xmin&quot;).text = str(bbox_list[idx + 3][2])
        ET.SubElement(bbox, &quot;ymax&quot;).text = str(bbox_list[idx + 3][3])
        ET.SubElement(bbox, &quot;ymin&quot;).text = str(bbox_list[idx + 3][4])

    apply_indent(root)
    tree = ET.ElementTree(root)
    #print(bbox_list[0].split(&quot;.png&quot;)[0])
    tree.write(&quot;{}/{}/{}.xml&quot;.format(PATH_folder, &quot;xml&quot;, bbox_list[0].split(&quot;.jpg&quot;)[0]))
    trainval.append(&quot;ss_label/&quot; + PATH_folder + &quot;Images/&quot; + bbox_list[0] + &quot; &quot; + &quot;ss_label/&quot; + PATH_folder + &quot;xml/&quot; + str(bbox_list[0].split(&quot;.jpg&quot;)[0]) + &quot;.xml&quot;)
        
        
    
    
if __name__ == &quot;__main__&quot;:
    read_xml()
    with open(&quot;trainval.txt&quot;, &quot;a&quot;) as file:
        for line in trainval:
            file.write(line)
            file.write(&quot;\n&quot;)

    print(temp)








