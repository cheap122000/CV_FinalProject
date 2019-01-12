import cv2
import sys
import gc
from face_train_use_keras import Model
import time
import base64
from azure.storage.blob import BlockBlobService, ContentSettings
import requests
import json

def pushimagetoLine(oriframe, thename, picname):
    # 照片存檔
    cv2.imwrite(picname, oriframe) 

    # 上傳到 Azure Blob
    block_blob.create_blob_from_path('tatunglinebot', picname, picname, content_settings=ContentSettings(content_type='image/jpeg'))

    # Post Message To LineBot
    url = 'https://tatunglinebot.herokuapp.com/pushimage'
    message = {}
    message['message'] = '辨識結果是 {0} ，請問要開門嗎？'.format(thename)
    message['image'] = picname
    requests.post(url, json.dumps(message, ensure_ascii=False).encode('utf-8'))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage:%s camera_id\r\n" % (sys.argv[0]))
        sys.exit(0)

    # 載入 Azure BLOB
    block_blob = BlockBlobService(account_name='acc_name', account_key='acc_key')
        
    # 載入訓練好的模型
    model = Model()
    model.load_model(file_path = './model/me.face.model.gpu3.h5')    

    # 記憶
    faceDictionary = {}
              
    # 框框顏色       
    color = (0, 255, 0)
    
    # 取得CAMERA
    cap = cv2.VideoCapture(int(sys.argv[1]))
    
    # 分辨器的路徑
    cascade_path = "D:/Computer Vision/haarcascade/haarcascade_frontalface_alt2.xml"    
    
    # 辨識人臉迴圈
    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame,1)        

        # 灰階化
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 使用人臉辨識的分辨器
        cascade = cv2.CascadeClassifier(cascade_path)                

        # 找人臉
        faceRects = cascade.detectMultiScale(frame_gray, scaleFactor = 1.2, minNeighbors = 3, minSize = (100, 100))        
        if len(faceRects) > 0:                 
            for faceRect in faceRects: 
                x, y, w, h = faceRect
                
                # 把臉輸入給模型
                if w > h:
                    image = frame[y: y + w, x: x + w]
                else:
                    image = frame[y: y + h, x: x + h]
                #image = frame[y : y + h, x: x + w ]
                faceID = model.face_predict(image)   
                
                # 如果是我
                if faceID == 0:                                                        
                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, thickness = 2)
                    cv2.putText(frame,'kai', 
                                (x + 30, y + 30),                      
                                cv2.FONT_HERSHEY_SIMPLEX,              
                                1,                                     
                                (255,0,255),                           
                                2)       
                    try:
                        oldtime = faceDictionary[faceID]
                        if int(time.time()) - oldtime > 10:
                            pushimagetoLine(frame, 'Kai', 'azure{0}.jpg'.format(faceID))
                            faceDictionary[faceID] = int(time.time())
                    except:
                        faceDictionary[faceID] = int(time.time())
                        pushimagetoLine(frame, 'Kai', 'azure{0}.jpg'.format(faceID))
                        faceDictionary[faceID] = int(time.time())                              
                elif faceID == 2:                                                        
                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), (255,0,0), thickness = 2)
                    
                    cv2.putText(frame,'hong', 
                                (x + 30, y + 30),                      
                                cv2.FONT_HERSHEY_SIMPLEX,              
                                1,                                     
                                (255,0,255),                           
                                2)  

                    try:
                        oldtime = faceDictionary[faceID]
                        if int(time.time()) - oldtime > 10:
                            pushimagetoLine(frame, 'hong', 'azure{0}.jpg'.format(faceID))
                            faceDictionary[faceID] = int(time.time())
                    except:
                        faceDictionary[faceID] = int(time.time())
                        pushimagetoLine(frame, 'hong', 'azure{0}.jpg'.format(faceID))
                        faceDictionary[faceID] = int(time.time())  
                elif faceID == 3:                                                        
                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), (255,0,0), thickness = 2)
                    
                    cv2.putText(frame,'teacher', 
                                (x + 30, y + 30),                      
                                cv2.FONT_HERSHEY_SIMPLEX,              
                                1,                                     
                                (255,0,255),                           
                                2)  

                    try:
                        oldtime = faceDictionary[faceID]
                        if int(time.time()) - oldtime > 10:
                            pushimagetoLine(frame, 'teacher', 'azure{0}.jpg'.format(faceID))
                            faceDictionary[faceID] = int(time.time())
                    except:
                        faceDictionary[faceID] = int(time.time())
                        pushimagetoLine(frame, 'teacher', 'azure{0}.jpg'.format(faceID))
                        faceDictionary[faceID] = int(time.time()) 
                elif faceID == 4:                                                        
                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), (255,0,0), thickness = 2)
                    
                    cv2.putText(frame,'yu', 
                                (x + 30, y + 30),                     
                                cv2.FONT_HERSHEY_SIMPLEX,             
                                1,                                    
                                (255,0,255),                          
                                2)  

                    try:
                        oldtime = faceDictionary[faceID]
                        if int(time.time()) - oldtime > 10:
                            pushimagetoLine(frame, 'yu', 'azure{0}.jpg'.format(faceID))
                            faceDictionary[faceID] = int(time.time())
                    except:
                        faceDictionary[faceID] = int(time.time())
                        pushimagetoLine(frame, 'yu', 'azure{0}.jpg'.format(faceID))
                        faceDictionary[faceID] = int(time.time()) 
                elif faceID == -1:                                                        
                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), (0,0,255), thickness = 2)
                    
                    cv2.putText(frame,'unknown', 
                                (x + 30, y + 30),                     
                                cv2.FONT_HERSHEY_SIMPLEX,             
                                1,                                    
                                (255,0,255),                          
                                2)  

                    try:
                        oldtime = faceDictionary[faceID]
                        if int(time.time()) - oldtime > 10:
                            pushimagetoLine(frame, 'unknown', 'azure{0}.jpg'.format(faceID))
                            faceDictionary[faceID] = int(time.time())
                    except:
                        faceDictionary[faceID] = int(time.time())
                        pushimagetoLine(frame, 'unknown', 'azure{0}.jpg'.format(faceID))
                        faceDictionary[faceID] = int(time.time())
                else:
                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), (255,0,0), thickness = 2)
                    
                    cv2.putText(frame,'yun', 
                                (x + 30, y + 30),               
                                cv2.FONT_HERSHEY_SIMPLEX,       
                                1,                              
                                (255,0,255),                    
                                2)   

                    try:
                        oldtime = faceDictionary[faceID]
                        if int(time.time()) - oldtime > 10:
                            pushimagetoLine(frame, 'yun', 'azure{0}.jpg'.format(faceID))
                            faceDictionary[faceID] = int(time.time())
                    except:
                        faceDictionary[faceID] = int(time.time())
                        pushimagetoLine(frame, 'yun', 'azure{0}.jpg'.format(faceID))
                        faceDictionary[faceID] = int(time.time()) 
                            
        cv2.imshow("result", frame)
        
        # 等待按鍵
        k = cv2.waitKey(10)
        # 退出迴圈
        if k & 0xFF == ord('1'):
            break

    # 釋放CAMERA資源
    cap.release()
    cv2.destroyAllWindows()