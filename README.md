# Parsing the data in "Large-scale Multiview 3D Hand Pose Dataset"

**Code Author: Shih-Yao (Mike) Lin**

## Platform
+ Ubuntu/MacOS

## Dependencies
+ python3
+ opencv-python

## some parsing results [[video 1](https://youtu.be/dgS_X_bqhpM)] [[video 2](https://youtu.be/2Mk39D_Zyuw)] [[video 3](https://youtu.be/QRbjeIfjeyc)]  [[video 4](https://youtu.be/YEqsGvIn1tE)]
[![](img/demo.png)](https://youtu.be/YEqsGvIn1tE)

## hand keypoint labels in the dataset
![](img/hand_lm3d.png)

## Dataset
http://www.rovit.ua.es/dataset/mhpdataset/

## Quick Start
+ write 2D hand images
```
python save_hand_pose.py -i [input_file_path] -v [camera_veiw] -o [output_img_path]
```

+ write 3D hand images
```
python save_hand_pose.py -i [input_file_path] -o [output_img_path]
```



