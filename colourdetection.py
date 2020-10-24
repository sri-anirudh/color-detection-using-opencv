import argparse
import cv2
import pandas as pd

#ask the image path
ap=argparse.ArgumentParser()
ap.add_argument("image",help="image path")
args=ap.parse_args()
img_path=args.image
#load the iamge using opencv
img=cv2.imread(img_path)

#read csv file add index coloumns
index=['color','colorname','hex','R','G','B']
data=pd.read_csv('colors.csv',names=index,header=None)

#declaring global variables (are used later on)
clicked = False
r = g = b = xpos = ypos = 0

#draw function
def draw(event,x,y,flags,param):
    if event==cv2.EVENT_FLAG_LBUTTON:
        global b,g,r,xpos,ypos,clicked
        clicked=True
        xpos=x
        ypos=y
        b,g,r=img[y,x]
        b,g,r=int(b),int(g),int(r)

def getcname(R,G,B):
    min=10000
    for i in range(len(data)):
        d=abs(R-int(data.loc[i,"R"]))+abs(G-int(data.loc[i,"G"]))+abs(B-int(data.loc[i,"B"]))
        if d<min:
            min=d
            cname=data.loc[i,"colorname"]
    return cname


cv2.namedWindow('image')
cv2.setMouseCallback('image',draw)

#display image
while True:
    cv2.imshow("image",img)
    if clicked:
        cv2.rectangle(img,(20,20),(750,60),(b,g,r),-1)
        text=getcname(r,g,b)
        cv2.putText(img,text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)
        if (r+g+b>=600):
            cv2.putText(img,text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
        clicked=False
    if cv2.waitKey(20) & 0xFF==27:
        break
cv2.destroyAllWindows()