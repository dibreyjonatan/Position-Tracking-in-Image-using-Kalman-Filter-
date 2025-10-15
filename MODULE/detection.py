import numpy as np
import cv2 # type: ignore
from time import (time)
# download the model as plain text as a PROTOTXT file and the trained model as a CAFFEMODEL file from  here: https://github.com/djmv/MobilNet_SSD_opencv

# path to the prototxt file with text description of the network architecture
prototxt = "MobileNetSSD_deploy.prototxt"
# path to the .caffemodel file with learned network
caffe_model = "MobileNetSSD_deploy.caffemodel"

# read a network model (pre-trained) stored in Caffe framework's format
net = cv2.dnn.readNetFromCaffe(prototxt, caffe_model)

# dictionary with the object class id and names on which the model is trained
classNames = { 0: 'background',
    1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',
    5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair',
    10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse',
    14: 'motorbike', 15: 'person', 16: 'pottedplant',
    17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor'}

def Detecting_person(image):
    person_detections = []  

    # size of image
    width = image.shape[1] 
    height = image.shape[0]
    # construct a blob from the image
    blob = cv2.dnn.blobFromImage(image, scalefactor = 1/127.5, size = (300, 300), mean = (127.5, 127.5, 127.5), swapRB=True, crop=False)
    # blob object is passed as input to the object
    net.setInput(blob)
    # network prediction
    detections = net.forward()

    for i in range(detections.shape[2]):
        # confidence of prediction
        confidence = detections[0, 0, i, 2]
        # get class id
        class_id = int(detections[0, 0, i, 1])
        # set confidence level threshold to filter weak predictions
        if confidence > 0.5 and class_id==15:
            #print(detections)
            # scale to the frame
            x_top_left = int(detections[0, 0, i, 3] * width) 
            y_top_left = int(detections[0, 0, i, 4] * height)
            x_bottom_right   = int(detections[0, 0, i, 5] * width)
            y_bottom_right   = int(detections[0, 0, i, 6] * height)
            
            person_detections=[x_top_left,y_top_left,x_bottom_right,y_bottom_right]
    
        return person_detections    
def get_single_axis_delta(value1,value2):
    return value2 - value1










    '''
            # draw bounding box around the detected object
            cv2.rectangle(frame, (x_top_left, y_top_left), (x_bottom_right, y_bottom_right),
                          (0, 255, 0))
            if class_id in classNames:
                # get class label
                label = classNames[class_id] + ": " + str(confidence)
                # get width and text of the label string
                (w, h),t = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                y_top_left = max(y_top_left, h)
                # draw bounding box around the text
                cv2.rectangle(frame, (x_top_left, y_top_left - h), 
                                   (x_top_left + w, y_top_left + t), (0, 0, 0), cv2.FILLED)
                cv2.putText(frame, label, (x_top_left, y_top_left),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
            cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
    ########calculating frames
    Tn=time()
    delta_t=Tn-Tn_1
    fps=0.9*fps+0.1/delta_t
    Tn_1=time()

    fps_label=f'Frames per second : {int(fps)} fps'
    cv2.putText(frame, fps_label, (20,20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) >= 0:  # Break with ESC 
        break

cap.release()
cv2.destroyAllWindows() '''