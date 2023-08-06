# model list

#### detection
## # 1. scrfd 

    * single scale
    - scrfd 10g bnkps
        : '/data/notebook/NAS/PTAS_Shared/resource/model/face/detection/scrfd_10g_bnkps' (.onnx / .v7.trt .v8.trt /.xml .bin)
    - scrfd 500m bnkps
        : '/data/notebook/NAS/PTAS_Shared/resource/model/face/detection/scrfd_500m_bnkps' (.onnx / .v7.trt .v8.trt /.xml .bin)
    - scrfd 10g
        : '/data/notebook/NAS/PTAS_Shared/resource/model/face/detection/scrfd_10g' (.onnx / .v7.trt .v8.trt /.xml .bin)
    - scrfd 500m
        : '/data/notebook/NAS/PTAS_Shared/resource/model/face/detection/scrfd_500m' (.onnx / .v7.trt .v8.trt /.xml .bin)
        
    * multi scale
    - scrfd 10g bnkps ( trt 현재 사용 불가, 추후 수정 예정 )
        : '/data/notebook/NAS/PTAS_Shared/resource/model/face/detection/scrfd_10g_bnkps_multiple' (.onnx / .v7.trt .v8.trt /.xml .bin)
        
    

## # 2. dlib
    - '/data/notebook/NAS/Gender-Age/source/SSR-Pytorch/datasets/shape_predictor_68_face_landmarks.dat'
## # 3. retinaface_insightface 
    - resnet50 : '/data/notebook/NAS/PTAS_Shared/resource/model/face/detection/retinaface_r50_insightface' (.onnx / .v8.trt /.xml .bin)
    - mobilenet : '/data/notebook/NAS/FaceDetection/models/retinaface-mobileNet/mnet.25' (.onnx / .v8.trt /.xml .bin)

## # 4. retinaface_torch
    - single_scale : '/data/notebook/NAS/PTAS_Shared/resource/model/face/detection/retinaface_torch_r50' (.onnx / .v8.trt /.xml .bin) - input BGR
    - multi_scale : '/data/notebook/NAS/FaceDetection/models/retinaface_torch/retinaface_r50_final_multiple' (.onnx / .v7.trt .v8.trt / .xml .bin )

#### landmark
## # 1. 3ddfa
    - '/data/notebook/NAS/PTAS_Shared/resource/model/face/landmark/3ddfa_v2'(.onnx / .v7.trt .v8.trt /.xml .bin)

#### recognition
## # 1. arcface r50 torch
    - "/data/notebook/insightface/recognition/arcface_torch/backbones/recog_arc_r50.pth"
## # 2. arcface r50
    - "/data/notebook/NAS/PTAS_Shared/resource/model/face/embedding/res50_arcface_20220210" (.onnx / .v7.trt .v8.trt /.xml .bin)

##### genderage
## # 1. arcface_cmt torch
    - '/data/notebook/NAS/PTAS_Shared/resource/model/face/agender/cmt_r50_arcface_best_20220119-2.pt'
## # 2. arcface_cmt onnx
    - "/data/notebook/NAS/PTAS_Shared/resource/model/face/agender/cmt_r50_arcface_best_20220119-2.onnx"
## # 3. arcface_cmt trt 
    - "/data/notebook/NAS/PTAS_Shared/resource/model/face/agender/cmt_r50_arcface_best_20220119-2.v8.trt"


# inference
    - package 의 inference_example ipynb 코드 참고
    
    - from model_zoo.get_models import get_detection_model,get_landmark_model, get_ageGender_model,get_recognition_model
    - from face.get_result import *

    - read_image : img = read_image(input_path)
### detection
-> model = get_detection_model(detection_name,detection_path,load_multi=True) # if multiscale model load, load_multi=True
-> faces,time_dict = get_detection(detection_name,detection_model,img,thresh=detection_thresh,height_min=detection_height_min, \
                                resize_way='resize',input_size=input_size,target_size=800,max_size=1200,time_return=True)
    - height_min : if height_min>0 : detection 된 이미지의 사이즈가 height_min 이상인것만 인정
    - resize_way : 'resize' or 'pad' ,  multiscale 은 resize 만 가능
    - input_size :  single scale input 을 사용할 경우, default (640,640)
    - target_size, max_size :  multiscale input 을 사용할 경우 설정 필요
    - time_return : speed check 같이 하는 경우, time dictionary 가 같이 return






