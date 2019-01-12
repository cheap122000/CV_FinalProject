#-*- coding: utf-8 -*-

import cv2
import sys

from PIL import Image

def CatchPICFromVideo(window_name, camera_idx, catch_pic_num, path_name):
    cv2.namedWindow(window_name)
    
    # 獲取 WebCam 路徑
    cap = cv2.VideoCapture(camera_idx)                
    
    # 人臉分辨器路徑
    classfier = cv2.CascadeClassifier("D:/Computer Vision/haarcascade/haarcascade_frontalface_alt2.xml")
    
    # 人臉框的顏色
    color = (0, 255, 0)
    
    num = 0
    takepic = False # 先不要存檔等待使用者按下 '1'
    while cap.isOpened():
        ok, frame = cap.read() # 讀取影像
        frame = cv2.flip(frame,1)
        if not ok:            
            break                
    
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 灰階化           
        
        # 人臉偵測
        faceRects = classfier.detectMultiScale(grey, scaleFactor = 1.2, minNeighbors = 3, minSize = (150, 150))
        
        # 偵測人臉並畫出來
        if len(faceRects) > 0:                                             
            for faceRect in faceRects:  
                x, y, w, h = faceRect                        
                
                # 照片編號並存檔
                img_name = '%s/%d.jpg'%(path_name, num)     
                if w > h:           
                    image = frame[y: y + w, x: x + w]
                else:
                    image = frame[y: y + h, x: x + h]

                # 如果是在拍照模式就存檔
                if takepic == True:
                    cv2.imwrite(img_name, image)                                        
                    num += 1                
                    # 超過指定上限結束程式
                    if num > (catch_pic_num):   
                        break
                
                # 針對辨識出的人畫出方框
                cv2.rectangle(frame, (x, y - 10), (x + w + 10, y + h + 10), color, 2)
                
                # 在畫面中顯示已經擷取了幾張圖片
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame,'num:%d' % (num),(x + 30, y + 30), font, 1, (255,0,255),4)                
        
        # 超過指定上限結束程式
        if num > (catch_pic_num): break                
                       
        # 顯示畫面
        cv2.imshow(window_name, frame)        
        c = cv2.waitKey(10)
        if c & 0xFF == ord('q'):
            break
        if c & 0xFF == ord('1'):
            takepic = True      
    
    # 清理 CAMERA 資源並且關閉所有視窗
    cap.release()
    cv2.destroyAllWindows() 
    
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage:%s camera_id face_num_max path_name\r\n" % (sys.argv[0]))
    else:
        CatchPICFromVideo("擷取人臉", int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])