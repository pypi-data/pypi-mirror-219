from sklearn.metrics import mean_absolute_error
from collections import OrderedDict

from torchvision import transforms as T

import torch.nn as nn
import torch

from ..backbones import get_cmt_model
from ..data.image import get_torchImage
from ..face.alignment import face_align
from ..data import LMARK_REF

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

gender_dict={0:'F',1:'M'}

# "/data/notebook/arcface_GenderAge/best_cmt_models/20220119-2_arcface-0610_predAge.pth"
class Arcface_GenderAge:
    def __init__(self,model_path,out_size=112):

        self.model_path = model_path
        #self.taskname = 'attribute'
        self.out_size=112

        if ("pth" in self.model_path) or ("pt" in self.model_path): # torch model
            self.net = get_cmt_model("", 512)
            load_weight = torch.load(self.model_path)

            if type(load_weight)==OrderedDict:
                try:
                    self.net.load_state_dict(load_weight)
                except:
                    new_state_dict = OrderedDict()
                    for n, v in load_weight.items():
                        name = n.replace("module.","") 
                        new_state_dict[name] = v
                    self.net.load_state_dict(new_state_dict)
            else:
                try:
                    self.net.load_state_dict(load_weight.module.state_dict())
                except:
                    self.net.load_state_dict(load_weight.state_dict())

            self.net.to(device)
            self.net.eval()  

    @torch.no_grad()
    def get(self,img,face):

        aimg = face_align(img,LMARK_REF,face.kps, face.pos_x, face.pos_y, face.det_scale, self.out_size)
        sf_gender, sf_age = self.net(aimg)

        sf_gender = sf_gender.cpu().numpy()
        sf_age = sf_age.cpu().numpy()

        pred_g,pred_a = get_pred(sf_genderm sf_age)

        face.gender = gender_dict[pred_g]
        face_age = pred_a

        return face.gender, face.age



    def get_pred(sf_gender, sf_age)#,resize):
        age_female = sf_age[:,:101]
        age_male = sf_age[:,101:]

        #p_female = np.reshape(sf_gender[:,0],(resize,1))*age_female
        #p_male = np.reshape(sf_gender[:,1],(resize,1))*age_male

        p_female = sf_gender[:,0][0]*age_female
        p_male = sf_gender[:,1][0]*age_male

        p_age = p_female+p_male

        pred_gender = np.argmax(sf_gender)#,axis=1)
        pred_age = np.argmax(p_age)#,axis=1)


        return pred_gender, pred_age






