# Parsing the data in "Large-scale Multiview 3D Hand Pose Dataset"

**Code Author: Shih-Yao (Mike) Lin**

## Platform
+ Ubuntu/MacOS

## Dependencies
+ python3
+ opencv-python

## Dataset
http://www.rovit.ua.es/dataset/mhpdataset/

## some parsing results [[video 1](https://youtu.be/dgS_X_bqhpM)] [[video 2](https://youtu.be/2Mk39D_Zyuw)] [[video 3](https://youtu.be/QRbjeIfjeyc)]  [[video 4](https://youtu.be/YEqsGvIn1tE)]
[![](img/demo.png)](https://youtu.be/YEqsGvIn1tE)

## hand keypoint labels in the dataset
![](img/hand_lm3d.png)

## processed data
[cropped hand images (3.2 GB)](https://drive.google.com/uc?id=12GNRqZRtjQYu303uh9AlYMcJUsvg6XRT&export=download)
[modified keypoint labels (4.2 MB)](https://drive.google.com/file/d/1yqwlv3IbG0syB1bj4gpZW9YSrdirp8uO/view?usp=sharing)
[cropped hand images with keypoints (3.6GB)](https://drive.google.com/uc?id=1Xu9JhLEWuQWqnaxS1DlCGJEfyKexWg4-&export=download)

## Quick Start
+ Data Pre-processing
```
python script_pre-processing.py -i [dataset_path] -o [output_path] 
```
```
sh _bash4preprocessing.sh
```



## Usages of other scripts
+ write 2D hand images
```
python save_hand_pose.py -i [input_file_path] -v [camera_veiw] -o [output_img_path]
```

+ write 3D hand images
```
python save_hand_pose.py -i [input_file_path] -o [output_img_path]
```

+ crop hand 
```
python crop_hand.py -i [input_file_path] -v [camera_veiw] -o [output_img_path]
```


