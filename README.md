# CAFFE for YOLO (More Implementations with Data & Inference)

## Reference

> You Only Look Once: Unified, Real-Time Object detection

> http://arxiv.org/abs/1506.02640

## Usage

### Data preparation
```Shell
  cd data/yolo
  ln -s /your/path/to/VOCdevkit/ .
  python ./get_list.py
  # change related path in script convert.sh
  ./convert.sh 
```

### + Data preparation (udacity, your own data ... )

> for your own data, there's some needs to data preparation  


   It needs a text file for label like(format):  
  
  ```Shell
    name(for <name>.jpg file)  xmax  xmin  ymax  ymin  label
  ```  
  
  
   If you prepared a label text file like above, you can use a python script file data/yolo/conv2xml.py.
     
   It converts the label text to xml file (to PASCAL VOC format).
     
   Please sure that the images are in folder 'Images/', and you have to change some codes in main func (maybe file paths)    
        
  ```Shell
    python conv2xml.py
  ```
    
  And If you already have .xml files but doesn't fit to PASCAL VOC format, then try with data/yolo/conv2voc.py.  
  
  you have to prepare :  
  ```shell
    Main/Images : images
    Main/xml : empty (converted xml path)
    Main/xml2 : your own xml files
  ```
    
  Then,  
  ```shell
    python conv2voc.py -f <Main Dir>
  ```
  
### Train
```Shell
  cd examples/yolo
  # change related path in script train.sh
  mkdir models
  nohup ./train.sh &
```

### Test
```Shell
  # if everything goes well, the map of gnet_yolo_iter_32000.caffemodel may reach ~56.
  cd examples/yolo
  ./test.sh model_path gpu_id
  The model is here (link: https://pan.baidu.com/s/1jHAN6xK password: kvee)
```
