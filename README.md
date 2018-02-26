# LUNA2016


# Model

    0 -> Resnet2D           -> remove!!
    1 -> 3DNet              -> remove!!
    2 -> 2D3DNet            -> remove!!
    3 -> Resnet3D
    4 -> Densenet3D
    5 -> Densenet2D         -> remove!!
    6 -> ResResnet??        -> remove!!
    


# Train

$ python main.py --TT 'Train' --Model 1 --ImgSize 64 --Epoch 10
    
    --TT : 'Train' / 'Test'
    --Model : 0 / 1 / 2 / ... /
    --Batch : 64 / 128 / 256 / ... /
    --ImgSize : 32 / 48 / 64
    --Epoch : None ~ 
    --Pretrained : True / False
    --Undersampling : True / False


# Test
    
$ python main.py --TT 'Test' --Model 1 --Epoch 0 --ImgSize 64


https://github.com/kenshohara/video-classification-3d-cnn-pytorch

https://github.com/kenshohara/3D-ResNets-PyTorch


