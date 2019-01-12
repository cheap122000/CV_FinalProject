import os
import sys
import numpy as np
import cv2

IMAGE_SIZE = 64

# 調整照片尺寸
def resize_image(image, height = IMAGE_SIZE, width = IMAGE_SIZE):
    top, bottom, left, right = (0, 0, 0, 0)
    
    # 獲取圖片的長寬
    h, w, _ = image.shape
    
    # 如果長寬不對等，使其等長寬
    longest_edge = max(h, w)    
    if h < longest_edge:
        dh = longest_edge - h
        top = dh // 2
        bottom = dh - top
    elif w < longest_edge:
        dw = longest_edge - w
        left = dw // 2
        right = dw - left
    else:
        pass 
    
    # RGB 顏色(補黑)
    BLACK = [0, 0, 0]
    
    # 把不夠長或是不夠寬的地方補黑
    constant = cv2.copyMakeBorder(image, top , bottom, left, right, cv2.BORDER_CONSTANT, value = BLACK)
    
    # 輸出調整完的圖片
    return cv2.resize(constant, (height, width))

# 讀取圖片
images = []
labels = []
def read_path(path_name):    
    for dir_item in os.listdir(path_name):
        # 從給定的路徑開始讀取圖片
        full_path = os.path.abspath(os.path.join(path_name, dir_item))
        
        if os.path.isdir(full_path):    # 判定是否為資料夾
            read_path(full_path)
        else: 
            if dir_item.endswith('.jpg'):
                image = cv2.imread(full_path)                
                image = resize_image(image, IMAGE_SIZE, IMAGE_SIZE)
                
                # 輸出調整完的結果
                #cv2.imwrite('1.jpg', image)
                
                images.append(image)                
                labels.append(path_name)                                
                    
    return images,labels
    

# 從給定的資料夾讀取圖片
def load_dataset(path_name):
    images,labels = read_path(path_name)    
    #print(images, labels)
    
    # 將輸入的圖片轉成四維的數據(彩色圖片)
    images = np.array(images)
    #print(images.shape)    
    
    # 給圖片的答案
    labels = np.array([0 if label.endswith('kai') else 2 if label.endswith('hong') else 3 if label.endswith('yuhong') else 4 if label.endswith('yu') else 1 for label in labels])    
    
    return images, labels

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage:%s path_name\r\n" % (sys.argv[0]))    
    else:
        images, labels = load_dataset(sys.argv[1])