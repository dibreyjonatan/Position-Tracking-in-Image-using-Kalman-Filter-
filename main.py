import sys
import cv2
import argparse
import collections
from time import time
import numpy as np
import math

sys.path.append("MODULE")

from detection import Detecting_person,get_single_axis_delta
from command import (connexion,send_command,setXdelta,send_command,
                     getMovementYawAngle,configure_PID,control_servo)
from KalmanFilter import KalmanFilter

parser = argparse.ArgumentParser(description='Enter Camera address,serial port and baud rate')

parser.add_argument('--Camera_adress',type=str,default='0',help="Enter a valid adress ex 0")
parser.add_argument('--Serial_port',type=str,default='none',help="enter a valid port adress ex COM3")
parser.add_argument('--baud_rate',type=int,default=9600,help="Enter a valid baud rate")
args = parser.parse_args()

if args.Camera_adress=='0':
   cap = cv2.VideoCapture(int(args.Camera_adress)) 
else :
   cap = cv2.VideoCapture((args.Camera_adress))  
###connexions
'''
connexion(args.Serial_port,args.baud_rate)   
send_command(0) 
####pid configurations#####""""""
configure_PID()'''

###defining variables to calculate the number of frames per second
fps=0
Tn_1=time()
#Variables for the filter

distance_mini=25
rectangle=1
trace=0


objets_points=[]
objets_id=[]
objets_KF=[]
objets_historique=[]
id_frame=0
id_objet=0
nouveau_objet=1
start=0

def distance(point, liste_points):
    distances=[]
    for p in liste_points:
        distances.append(np.sum(np.sqrt(np.power(p-np.expand_dims(point, axis=-1), 2))))
    return distances
def trace_historique(tab_points, longueur, frame,couleur=(0, 255, 255)):
    historique=np.array(tab_points)
    nbr_point=len(historique)
    longueur=min(nbr_point, longueur)
    for i in range(nbr_point-1, nbr_point-longueur, -1):
        cv2.line(frame,
                 (historique[i-1, 0], historique[i-1, 1]),
                 (historique[i, 0], historique[i, 1]),
                 couleur,
                 2)
        
def track(frame,fps):
    global id_objet,objets_KF,objets_historique,objets_points,nouveau_objet
    # Prediction de l'ensemble des objets + affichage
    for id_obj in range(len(objets_points)):
        etat=objets_KF[id_obj].predict()
        
        etat=np.array(etat, dtype=np.int32)
        objets_points[id_obj]=np.array([etat[0], etat[1], etat[4], etat[5]])
        objets_historique[id_obj].append([etat[0], etat[1]])
        cv2.putText(frame,f'fps : {round(fps)}',(20,20),cv2.FONT_HERSHEY_PLAIN, 1.5,(0, 255, 0),2)
        cv2.circle(frame, (int(etat[0]), int(etat[1])), 5, (0, 0, 255), 2)
        if rectangle:
            cv2.rectangle(frame,
                          (int(etat[0]-etat[4]/2), int(etat[1]-etat[5]/2)),
                          (int(etat[0]+etat[4]/2), int(etat[1]+etat[5]/2)),
                          (0, 0, 255),
                          2)
        cv2.arrowedLine(frame,
                        (int(etat[0]), int(etat[1])),
                        (int(etat[0]+3*etat[2]), int(etat[1]+3*etat[3])),
                        color=(0, 0, 255),
                        thickness=2,
                        tipLength=0.2)
        cv2.putText(frame,
                    "ID{:d}".format(objets_id[id_obj]),
                    (int(etat[0]-etat[4]/2), int(etat[1]-etat[5]/2)),
                    cv2.FONT_HERSHEY_PLAIN,
                    1.5,
                    (255, 0, 0),
                    2)

        if trace:
            trace_historique(objets_historique[id_obj], 42)

        # Permet de suivre l'ID 0 avec une flèche
        if objets_id[id_obj]==0:
            cv2.arrowedLine(frame,
                            (int(etat[0]), int(etat[1]-etat[5]/2-80)),
                            (int(etat[0]), int(etat[1]-etat[5]/2-30)),
                            color=(0, 0, 255),
                            thickness=5,
                            tipLength=0.2)
     # Affichage des données (rectangle) du detecteur

    point=Detecting_person(frame)
    #if detections are made  then 
    if len(point)>0: 
       cx=(point[2]+point[0])/2
       cy=(point[1]+point[3])/2
       h=point[3]-point[1]
       l=point[2]-point[0]
       

       if len(objets_points):
           #calcul de la distance euclidienne
           distances=distance([cx,cy,h,l], objets_points)
           print(distances)
           min=np.min(distances)
           id2=np.where(distances==min)
           print(id2[0])
           if id2[0] is not None and min >=distance_mini :
              objets_KF[id2[0][0]].update(np.expand_dims([cx,cy,h,l], axis=-1))
              nouveaux_objet=0
           else :    
              nouveaux_objet=1
       # Création du filtre de Kalman pour les nouveaux objets 
       if nouveau_objet :
           print("NOUVEAU", [cx,cy,h,l])
           objets_points.append([cx,cy,h,l])
           objets_KF.append(KalmanFilter(0.1, [cx, cy], [h, l]))
           objets_id.append(id_objet)
           objets_historique.append([])
           id_objet+=1      
           nouveau_objet=0
      
    return frame           
    
while True :
    ret, image= cap.read()
    image=cv2.resize(image,(600,600))
     ########calculating frames
    Tn=time()
    delta_t=Tn-Tn_1
    fps=0.9*fps+0.1/delta_t
    Tn_1=time()
    image=track(image,fps)
    cv2.imshow("image",image)
    if cv2.waitKey(1) == ord('q'):  # Break with q
        break

cap.release()
cv2.destroyAllWindows()    