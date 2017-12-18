import os
import sys
sys.path.insert(0, 'Model')
import model as models
import resnet3D as r3


import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F



from collections import OrderedDict



def model_setter(idx, isTest=False):
    default_batch = 64
    if idx == 0:
        model_name = 'ResNet'
        batch_size = default_batch
        model = models.CNNfor2D_Small(2)
    elif idx == 1:
        model_name = '3DNet'
        batch_size = default_batch
        #model = models.CNNfor3D(2)
        model = models.CNNfor3D_DIFF(2)
    elif idx == 2:
        model_name = '2D3DNet'
        batch_size = default_batch
        #model = models.CNNfor2D3D(100)
        model = models.CNNfor2D3D_DIFF()
    else:
        model_name = 'Resnet3D'
        batch_size = default_batch
        model, _ = generate_3Dmodel('resnet', 18, 64, 2, isPretrained=False)
        
        
    if torch.cuda.is_available():
        model.cuda()
    if torch.cuda.device_count() > 1:
        model = torch.nn.DataParallel(model, device_ids=range(torch.cuda.device_count()))
        
    return model, model_name, batch_size



def modelLoader(model_name, test_index, epoch=-1):
    model_path = '../Model'
    files = os.listdir(model_path)
    model_list = []
    for file in files:
        if '.pt' in file and (model_name + '____' + str(test_index)) in file:
            model_list.append(file)

    model_list.sort()
    
    if len(model_list) < 1:
        return None, -1, None, None
    else:
        if epoch != -1:
            model_name = model_name + '____' + str(test_index) + '__' + str(epoch) + '.pt'
            if os.path.isfile(os.path.join(model_path, model_name)):
                model_out = os.path.join(model_path, model_name)
                model_epoch = epoch
            else:
                print 'NO MODEL!!'
                model_out = os.path.join(model_path, model_list[-1])
                model_epoch = int(model_list[-1].split('__')[-1].split('.')[0])
        else:
            model_out = os.path.join(model_path, model_list[-1])
            model_epoch = int(model_list[-1].split('__')[-1].split('.')[0])  



        f = open(model_out.replace('.pt', '.txt'), 'r')
        line = f.readline()
        
        batch_size = int(line.split(',')[0])
        learning_rate = float(line.split(',')[1])
        f.close()

    
        return model_out, model_epoch, batch_size, learning_rate









def generate_3Dmodel(model_name, model_depth, img_size, num_class, isPretrained=False):
    if model_name == 'resnet':
        
        resnet_shortcut = 'B'
        if model_depth == 10:
            model = r3.resnet10(num_classes=num_class, shortcut_type=resnet_shortcut,
                                        sample_size=img_size)
        elif model_depth == 18:
            model = r3.resnet18(num_classes=num_class, shortcut_type=resnet_shortcut,
                                        sample_size=img_size)
        elif model_depth == 34:
            model = r3.resnet34(num_classes=num_class, shortcut_type=resnet_shortcut,
                                        sample_size=img_size)
        elif model_depth == 50:
            model = r3.resnet50(num_classes=num_class, shortcut_type=resnet_shortcut,
                                        sample_size=img_size)
        elif model_depth == 101:
            model = r3.resnet101(num_classes=num_class, shortcut_type=resnet_shortcut,
                                         sample_size=img_size)
        elif model_depth == 152:
            model = r3.resnet152(num_classes=num_class, shortcut_type=resnet_shortcut,
                                         sample_size=img_size)
        elif model_depth == 200:
            model = r3.resnet200(num_classes=num_class, shortcut_type=resnet_shortcut,
                                         sample_size=img_size)

    
    '''    
    if torch.cuda.is_available():    
        model = model.cuda()
    if torch.cuda.device_count() > 1:
        model = nn.DataParallel(model, device_ids=range(torch.cuda.device_count()))
    '''    

    if isPretrained:
        files = os.listdir('../Model/PretrainedWeight')
        model_path = None
        for file in files:
            if (model_name + '-' + str(model_depth)) in file:
                model_path = os.path.join('./Model/PretrainedWeight', file)
        model_dict = model.state_dict()
        


        pretrain = torch.load(model_path)

        
        new_pretrain_dict = OrderedDict()
        for k, v in pretrain['state_dict'].items():
            name = k[7:]
            if 'fc' not in name:
                new_pretrain_dict[name] = v        
        model_dict.update(new_pretrain_dict)
        
        model.load_state_dict(model_dict)
        model.fc = nn.Linear(model.fc.in_features, num_class)
        
    return model, model.parameters()