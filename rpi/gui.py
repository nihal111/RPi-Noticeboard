#!/usr/bin/python
# Hostel Noticeboard App
# By Manish Goregaokar
#
# Tested on Ubuntu
# Meant to run on Raspian


from Tkinter import *
from threading import *
from PIL import Image, ImageTk
import json
import time
import os
import sys
import datetime
class App:

    def __init__(self, master):
        print "Starting Noticeboard: " + (datetime.datetime.fromtimestamp(int("1284101485")).strftime('%Y-%m-%d %H:%M:%S'))
        
        self.config={'directories':['Academics','Cultural','Sports','Technical','Hostel'],
        'delimiter':"         ",
        'tickerspeed':[1,10], # x pixels per y milliseconds
        'tickerpad':[0,2], #lower, upper
        'tickerstyle':['white',("Helvectica", "24")], #fill,font(face,size)
        'canvasbg':'white',
        'tickerrectcolor':'black',
        'picspeed':2000, #Switch images every x seconds
        'picsatatime':4, # 1,2, or 4
        'tilingpad':[2,2], #horiz,vert
        'refreshcount':{1:10,2:10,4:10}, #After how many iterations ought I refresh? [PAT1,PAT2,PAT3]
        'mainpad':[[1,1],[50,1]], #Central canvas margins, [[left,right],[top,bottom]]
         'logoscale':[200,40] 
        }
        try:
            x=open('config.json')
            self.config=json.loads(x.read())
            x.close()
        except Exception as e:
            print "Error loading config, using default config"
            print e
        
        
        self.tickerlist=""
        self.piclist=[]
        self.piclist2={}
        self.itercount=0
        self.frame = Frame(master)
        self.frame.pack()
        master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))
        self.windowd=[master.winfo_screenwidth(), master.winfo_screenheight()]
        #master.wm_state(ZOOMED)
        self.rt=master
        self.rt.overrideredirect(True)
        self.can = Canvas(self.rt, bg="black",borderwidth=0,highlightthickness=0,background=self.config['canvasbg'])
        self.can.pack(expand=True,fill=BOTH)
        self.can.bind('<Double-1>',self.close)
        self.getticker()
        self.tickertext=self.can.create_text(self.can.canvasx(0),self.can.canvasy(0),text=self.tickerlist,  fill=self.config['tickerstyle'][0], font=self.config['tickerstyle'][1])
        a=self.can.bbox(self.tickertext)
        print a
        self.imgbbox=[self.windowd[0]-self.config['mainpad'][0][0]-self.config['mainpad'][0][1],self.windowd[1]-self.config['tickerpad'][0]-self.config['tickerpad'][1]-(a[3]-a[1])-self.config['mainpad'][1][0]-self.config['mainpad'][1][1]]
        self.getpiclist()
        self.tickerrect=self.can.create_rectangle(0,self.imgbbox[1]+self.config['mainpad'][1][0]+self.config['mainpad'][1][1],self.windowd[0],self.windowd[1],fill=self.config['tickerrectcolor'])
        self.can.tag_lower(self.tickerrect)
        singleimgbox=[self.imgbbox[0],self.imgbbox[1]]
        if self.config['picsatatime']>=2:
            singleimgbox[0]=singleimgbox[0]/2-self.config['tickerpad'][0]
        if self.config['picsatatime']==4:
            singleimgbox[1]=singleimgbox[1]/2-self.config['tickerpad'][1]/2
        print "Recommended image size: "+str(singleimgbox[0])+"x"+str(singleimgbox[1])+" (Screen size: "+str(self.windowd[0])+"x"+str(self.windowd[1])+")"
        self.can.move(self.tickertext,-a[0],self.windowd[1]+a[1]-self.config['tickerpad'][1])
        self.tickerstate=0
        
        if self.config['picsatatime']==1:
            self.picindex=[0]
            self.imgs=[self.can.create_image(self.imgbbox[0]/2+self.config['mainpad'][0][0],self.imgbbox[1]/2 +self.config['mainpad'][1][0],image=self.photos[0],anchor=CENTER)]
        elif self.config['picsatatime']==2:
            self.picindex=[0,0]

            self.imgs=[0,0]
            self.imgs[0]=self.can.create_image(self.imgbbox[0]/4-self.config['tilingpad'][0],self.imgbbox[1]/2,image=self.photos[self.config['directories'][0]][self.picindex[0]],anchor=CENTER)
            self.imgs[1]=self.can.create_image(3*self.imgbbox[0]/4+self.config['tilingpad'][0],self.imgbbox[1]/2,image=self.photos[self.config['directories'][1]][self.picindex[1]],anchor=CENTER)
        elif self.config['picsatatime']==4:
            self.picindex=[0,0,0,0]

            self.imgs=[0,0,0,0]
            
            self.imgs[0]=self.can.create_image(self.imgbbox[0]/4-self.config['tilingpad'][0]/2,self.imgbbox[1]/4-self.config['tilingpad'][1]/2,image=self.photos[self.config['directories'][0]][self.picindex[0]],anchor=CENTER)
            self.imgs[1]=self.can.create_image(3*self.imgbbox[0]/4+self.config['tilingpad'][0]/2,self.imgbbox[1]/4-self.config['tilingpad'][1]/2,image=self.photos[self.config['directories'][1]][self.picindex[1]],anchor=CENTER)
            self.imgs[2]=self.can.create_image(self.imgbbox[0]/4-self.config['tilingpad'][0]/2,3*self.imgbbox[1]/4+self.config['tilingpad'][1]/2,image=self.photos[self.config['directories'][2]][self.picindex[2]],anchor=CENTER)
            self.imgs[3]=self.can.create_image(3*self.imgbbox[0]/4+self.config['tilingpad'][0]/2,3*self.imgbbox[1]/4+self.config['tilingpad'][1]/2,image=self.photos[self.config['directories'][3]][self.picindex[3]],anchor=CENTER)
        self.loadLogo()
        self.updLogo()
        master.after(self.config['tickerspeed'][1],self.moveticker)
        master.after(self.config['picspeed'],self.movepic)
        


    def moveticker(self):
        
        self.can.move(self.tickertext,-self.config['tickerspeed'][0],0)

        a=self.can.bbox(self.tickertext)
        if self.tickerstate is 1:
            self.can.move(self._tickertext,-self.config['tickerspeed'][0],0)
            a=self.can.bbox(self._tickertext)
            if a[0]<0:
                self.can.delete(self.tickertext)
                self.tickertext=self._tickertext
                self.tickerstate=0
        elif a[2]<self.windowd[0] and self.tickerstate is 0:
            self.getticker()
            self.tickerstate=1
            self._tickertext=self.can.create_text(self.can.canvasx(0),self.can.canvasy(0),text=self.config['delimiter']+self.tickerlist, fill=self.config['tickerstyle'][0], font=self.config['tickerstyle'][1])
            a=self.can.bbox(self._tickertext)
            self.can.move(self._tickertext,self.windowd[0]-a[0],self.windowd[1]+a[1]-self.config['tickerpad'][0])
        self.rt.after(self.config['tickerspeed'][1],self.moveticker)



    def movepic(self):
        self.itercount+=1
        for i in range(0,len(self.imgs)):
            self.can.delete(self.imgs[i])
        if self.itercount==self.config['refreshcount'][str(self.config['picsatatime'])]:
            self.getpiclist()
            self.itercount=0    
        if self.config['picsatatime']==1:
            self.picindex[0]+=1
            if self.picindex[0] >= len(self.piclist):
                self.picindex=[0]
            self.imgs[0]=self.can.create_image(self.imgbbox[0]/2+self.config['mainpad'][0][0],self.imgbbox[1]/2 +self.config['mainpad'][1][0],image=self.photos[self.picindex[0]],anchor=CENTER)
        elif self.config['picsatatime']==2:
            for i in range(0,2):
                self.picindex[i]+=1
                if self.picindex[i]>=len(self.piclist2[self.config['directories'][i]]): 
                    self.picindex[i]=0
            self.imgs[0]=self.can.create_image(self.imgbbox[0]/4-self.config['tilingpad'][0],self.imgbbox[1]/2,image=self.photos[self.config['directories'][0]][self.picindex[0]],anchor=CENTER)
            self.imgs[1]=self.can.create_image(3*self.imgbbox[0]/4+self.config['tilingpad'][0],self.imgbbox[1]/2,image=self.photos[self.config['directories'][1]][self.picindex[1]],anchor=CENTER)
        elif self.config['picsatatime']==4:
            for i in range(0,4):
                self.picindex[i]+=1
                if self.picindex[i]>=len(self.piclist2[self.config['directories'][i]]): 
                    self.picindex[i]=0
                    #self.getpiclist()
            self.imgs[0]=self.can.create_image(self.imgbbox[0]/4-self.config['tilingpad'][0]/2,self.imgbbox[1]/4-self.config['tilingpad'][1]/2,image=self.photos[self.config['directories'][0]][self.picindex[0]],anchor=CENTER)
            self.imgs[1]=self.can.create_image(3*self.imgbbox[0]/4+self.config['tilingpad'][0]/2,self.imgbbox[1]/4-self.config['tilingpad'][1]/2,image=self.photos[self.config['directories'][1]][self.picindex[1]],anchor=CENTER)
            self.imgs[2]=self.can.create_image(self.imgbbox[0]/4-self.config['tilingpad'][0]/2,3*self.imgbbox[1]/4+self.config['tilingpad'][1]/2,image=self.photos[self.config['directories'][2]][self.picindex[2]],anchor=CENTER)
            self.imgs[3]=self.can.create_image(3*self.imgbbox[0]/4+self.config['tilingpad'][0]/2,3*self.imgbbox[1]/4+self.config['tilingpad'][1]/2,image=self.photos[self.config['directories'][3]][self.picindex[3]],anchor=CENTER)
        self.updLogo()
        self.rt.after(self.config['picspeed'],self.movepic)



    def getticker(self):
        temp=[]
        try:
            for i in self.config['directories']:
                #print [os.listdir(i)]
                temp+=[open(os.path.join(i,f)).read() for f in os.listdir(i) if f.endswith('.txt')]
            self.tickerlist=self.config['delimiter'].join(temp).replace('\n',self.config['delimiter']) if temp !=[] else self.tickerlist
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)


    def getpiclist(self):

        t2={}
        temp=[]
        try:
            for i in self.config['directories']:
                #print [os.listdir(i)]
                t2[i]=[os.path.join(i,f) for f in os.listdir(i) if (f.endswith('.png') or f.endswith('.jpg') or f.endswith('.gif'))]
                temp+=t2[i]
            x=False
            if self.piclist==temp:
                x=True
            if len(self.config['directories'])>=4 and self.config['picsatatime']==4:
                for i3 in range(4,len(self.config['directories'])):
                    t2[self.config["directories"][i3-4]]+=t2[self.config["directories"][i3]]
            self.piclist2=t2 if t2 !={} else self.piclist2
            self.piclist = temp if temp!=[] else self.piclist
            if t2!={} and not x:
                
                if self.config['picsatatime']==1:
                    self.photos=[]
                    for i in range(0,len(temp)):
                        self.photos+= [Image.open(temp[i])]
                        self.photos[i].thumbnail((self.imgbbox[0],self.imgbbox[1]))
                        self.photos[i] = ImageTk.PhotoImage(self.photos[i])
                elif self.config['picsatatime']==2:
                    self.photos={}
                    for i in self.config['directories']:
                        self.photos[i]=[]
                        for j in range(0,len(t2[i])):
                            self.photos[i]+=[Image.open(t2[i][j])]
                            self.photos[i][j].thumbnail((self.imgbbox[0]/2-self.config['tilingpad'][0],self.imgbbox[1]))
                            self.photos[i][j] = ImageTk.PhotoImage(self.photos[i][j])
                elif self.config['picsatatime']==4:
                    self.photos={}
                    ctr=0
                    for i in self.config['directories']:
                        i2=i
                        jd=0
                        if ctr>=4:
                            i2=self.config['directories'][ctr-4]
                            jd=len(self.photos[i2])
                        else:
                            self.photos[i2]=[]
                        ctr+=1
                        for j in range(0,len(t2[i])):
                            #print [i,i2,j,t2[i][j],j+jd]
                            self.photos[i2]+=[Image.open(t2[i][j])]
                            self.photos[i2][j+jd].thumbnail((self.imgbbox[0]/2-self.config['tilingpad'][0],self.imgbbox[1]/2-self.config['tilingpad'][1]))
                            self.photos[i2][j+jd] = ImageTk.PhotoImage(self.photos[i2][j+jd])
            print "Image fetch&parse successful"
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
    
    def updLogo(self):
         self.logoC=self.can.create_image(self.windowd[0],0,image=self.logo,anchor=NE)
		
    def loadLogo(self):
         self.logo=Image.open("logo.png") 
         self.logo.thumbnail((self.config['logoscale'][0],self.config['logoscale'][0]))
         self.logo = ImageTk.PhotoImage(self.logo)
         
    def close(self,event):
        self.frame.quit()

root = Tk()

app = App(root)

root.mainloop()
