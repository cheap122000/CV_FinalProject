import random

import numpy as np
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import SGD, Adam
from keras.utils import np_utils
from keras.models import load_model
from keras import backend as K

from load_face_dataset import load_dataset, resize_image, IMAGE_SIZE


class Dataset:
	# 初始化
    def __init__(self, path_name):
        # 訓練圖片
        self.train_images = None
        self.train_labels = None
        
        # 驗證圖片
        self.valid_images = None
        self.valid_labels = None
        
        # 測試圖片
        self.test_images  = None            
        self.test_labels  = None
        
        # 圖片路徑
        self.path_name    = path_name
        
        # 圖片的維度
        self.input_shape = None
        
    # 載入數據並且按照交叉驗證的原則化分數具並進行相關的預處理
    def load(self, img_rows = IMAGE_SIZE, img_cols = IMAGE_SIZE, 
             img_channels = 3, nb_classes = 0):
        # 載入數據到記憶體
        images, labels = load_dataset(self.path_name)        
        
        train_images, valid_images, train_labels, valid_labels = train_test_split(images, labels, test_size = 0.3, random_state = random.randint(0, 100))        
        _, test_images, _, test_labels = train_test_split(images, labels, test_size = 0.5, random_state = random.randint(0, 100))                
        
        # 如果現在的維度是 th 則輸入的順序為 channels,rows,cols 否則是 rows,cols,channels
        # 根據 keras 要求的維度順序訓練模組
        if K.image_dim_ordering() == 'th':
            train_images = train_images.reshape(train_images.shape[0], img_channels, img_rows, img_cols)
            valid_images = valid_images.reshape(valid_images.shape[0], img_channels, img_rows, img_cols)
            test_images = test_images.reshape(test_images.shape[0], img_channels, img_rows, img_cols)
            self.input_shape = (img_channels, img_rows, img_cols)            
        else:
            train_images = train_images.reshape(train_images.shape[0], img_rows, img_cols, img_channels)
            valid_images = valid_images.reshape(valid_images.shape[0], img_rows, img_cols, img_channels)
            test_images = test_images.reshape(test_images.shape[0], img_rows, img_cols, img_channels)
            self.input_shape = (img_rows, img_cols, img_channels)            
            
            # 印出訓練圖片、驗證圖片、測試圖片的數量
            print(train_images.shape[0], 'train samples')
            print(valid_images.shape[0], 'valid samples')
            print(test_images.shape[0], 'test samples')
        
            # 此模型用 categorical_crossentropy 作為損失函數，將圖片根據要訓練的人數向量化
            train_labels = np_utils.to_categorical(train_labels, nb_classes)                        
            valid_labels = np_utils.to_categorical(valid_labels, nb_classes)            
            test_labels = np_utils.to_categorical(test_labels, nb_classes)                        
        
            # 將數值標準化
            train_images = train_images.astype('float32')            
            valid_images = valid_images.astype('float32')
            test_images = test_images.astype('float32')
            
            # 將數值標準化至 0-1 之間
            train_images /= 255
            valid_images /= 255
            test_images /= 255            
        
            self.train_images = train_images
            self.valid_images = valid_images
            self.test_images  = test_images
            self.train_labels = train_labels
            self.valid_labels = valid_labels
            self.test_labels  = test_labels

# 建立 CNN 的模型            
class Model:
    def __init__(self):
        self.model = None 
        
    # 建立模型
    def build_model(self, dataset, nb_classes = 0):
        # 開始初始化並且建立模型
        self.model = Sequential() 
        dataset.train_images.shape[0]
        
        # 開始加入要訓練的層數
        # 先加入一個捲積層以及池化層，並告入模型訓練的維度
        # DROP 30% 的神經元
        self.model.add(Convolution2D(32, 3, 3, border_mode='same', input_shape = dataset.input_shape))   
        self.model.add(Activation('relu'))                                 
        self.model.add(MaxPooling2D(pool_size=(2, 2), strides=(2,2), border_mode='same'))                   
        self.model.add(Dropout(0.3))                                      

        # 第二層積層以及池化層
        # DROP 30% 的神經元
        self.model.add(Convolution2D(64, 3, 3, border_mode='same'))        
        self.model.add(Activation('relu'))                                                               
        self.model.add(MaxPooling2D(pool_size=(2, 2), border_mode='same')) 
        self.model.add(Dropout(0.3))                                      

        # 加入平坦層
        self.model.add(Flatten())

        # 加入第一層分類層                                         
        self.model.add(Dense(512))                                         
        self.model.add(Activation('relu'))                                 
        self.model.add(Dropout(0.35))                                       

        # 加入第二層分類層，並輸出結果
        self.model.add(Dense(nb_classes))                                  
        self.model.add(Activation('softmax'))                         
        
        # 印出模型的概況
        self.model.summary()
    
    # 訓練模型
    def train(self, dataset, batch_size = 20, nb_epoch = 10, data_augmentation = True):        
        sgd = SGD(lr = 0.01, decay = 1e-6, momentum = 0.9, nesterov = True) # 原本採用 SGD 分辨器，發現效果不好，改成下方的 adam 分類器  
        adam = Adam(lr = 1e-4) # ADAM 分類器
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])   # 完成模型配置的工作
        
        # 不使用數據提升(在圖片中利用旋轉、翻、加躁的方法創建新的數據)
        if not data_augmentation:            
            self.model.fit(dataset.train_images,
                           dataset.train_labels,
                           batch_size = batch_size,
                           nb_epoch = nb_epoch,
                           validation_data = (dataset.valid_images, dataset.valid_labels),
                           shuffle = True)
        # 使用數據提升
        else:            
            # 調用 python 的數據生成器
            datagen = ImageDataGenerator(
                featurewise_center = False,             # 數據去中心化(平均為0)，
                samplewise_center  = False,             # 書入數據的樣本平均值為 0
                featurewise_std_normalization = False,  # 數據標準化
                samplewise_std_normalization  = False,  # 將樣本除以標準差
                zca_whitening = False,                  # ZCA 白化
                rotation_range = 20,                    # 隨機轉動角度(0-180)
                width_shift_range  = 0.2,               # 水平偏移幅度(0-1)
                height_shift_range = 0.2,               # 垂直偏移幅度(0-1)
                horizontal_flip = True,                 # 水平翻轉
                vertical_flip = False)                  # 垂直翻轉

            # 計算整個訓練 DATA 的數量
            datagen.fit(dataset.train_images)                        

           # 開始生成訓練模型
            self.model.fit_generator(datagen.flow(dataset.train_images, dataset.train_labels,
                                                   batch_size = batch_size),
                                     samples_per_epoch = dataset.train_images.shape[0],
                                     nb_epoch = nb_epoch,
                                     validation_data = (dataset.valid_images, dataset.valid_labels))

    def save_model(self, file_path):
        self.model.save(file_path)

    def load_model(self, file_path):
        self.model = load_model(file_path)

    def evaluate(self, dataset):
        score = self.model.evaluate(dataset.test_images, dataset.test_labels, verbose = 1)
        print("%s: %.2f%%" % (self.model.metrics_names[1], score[1] * 100))


# 辨識人臉
    def face_predict(self, image):    
        # 維度
        if K.image_dim_ordering() == 'th' and image.shape != (1, 3, IMAGE_SIZE, IMAGE_SIZE):
            image = resize_image(image)                             
            image = image.reshape((1, 3, IMAGE_SIZE, IMAGE_SIZE))   
        elif K.image_dim_ordering() == 'tf' and image.shape != (1, IMAGE_SIZE, IMAGE_SIZE, 3):
            image = resize_image(image)
            image = image.reshape((1, IMAGE_SIZE, IMAGE_SIZE, 3))                    
        
        # 數據標準化
        image = image.astype('float32')
        image /= 255
        
        # 每個圖片的機率
        result = self.model.predict_proba(image)
        print('result:', result)
        
        # 給出答案
        good = False
        for percent in result[0]:
            if percent >= 0.55:
                good = True

        result = self.model.predict_classes(image)    

        # 輸出預測結果
        if good == True:
            outputresult = result[0]
        else:
            outputresult = -1
        print(outputresult)
        return outputresult




if __name__ == '__main__':
    dataset = Dataset('data2')    
    dataset_number = 5

    dataset.load(nb_classes=dataset_number)
    
    
    model = Model()

    
    model.build_model(dataset, nb_classes=dataset_number)
    
    # 測試訓練函數
    model.train(dataset)
    model.save_model(file_path = './model/me.face.model.gpu3.h5')
    

    model.load_model(file_path = './model/me.face.model.gpu3.h5')
    model.evaluate(dataset)