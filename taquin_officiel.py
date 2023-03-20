import tkinter as tk
import threading
import time
from random import randint
from math import floor
from copy import deepcopy

#Rajouter fonction pour choisir son nombre de case


nbr=78
font="helvetica"
case=5
dimension=800
temps=[0,0]
mesure_temps=False


taquin=[]
for i in range (0,case):
    ligne=[]
    for j in range(0,case):
        ligne.append(i*case+j+1)
    taquin.append(ligne)
taquin[case-1][case-1]=0
taquin2=deepcopy(taquin)
taquin_resolu=deepcopy(taquin)





def chrono():
    while mesure_temps==True :
        print(temps)
        temps[1]=temps[1]+1
        time.sleep(1)
        if temps[1]==60:
            temps[0]=temps[0]+1
            temps[1]=0
        


def chronometre():
    global temps
    mesure=threading.Thread(target=chrono)
    mesure.start()


def deplacement (x,y):
    global taquin
    taquin2=deepcopy(taquin)
    for i in range (0,case):
        for j in range (0,case):
            if taquin[j][i]==0:
                x0=i
                y0=j
    if y==y0 and x<x0 :
        for i in range (x0,x-1,-1):
            taquin[y][i]=taquin2[y][i-1]
        taquin[y][x]=0
    elif y==y0 and x>x0 :
        for i in range (x0,x):
            taquin[y][i]=taquin2[y][i+1]
        taquin[y][x]=0
    elif x==x0 and y<y0:
        for i in range (y0,y-1,-1):
            taquin[i][x]=taquin2[i-1][x]
        taquin[y][x]=0
    elif x==x0 and y>y0:
        for i in range (y0,y):
            taquin[i][x]=taquin2[i+1][x]
        taquin[y][x]=0




def permutation():
    global taquin
    x1,y1=randint(0,case-1),randint(0,case-1)
    x2,y2=randint(0,case-1),randint(0,case-1)
    while x1==x2 and y1==y2:
        x2,y2=randint(0,case-1),randint(0,case-1)
    taquin[x1][y1],taquin[x2][y2]=taquin[x2][y2],taquin[x1][y1]



def melange():
    global taquin
    x0=0
    y0=0
    for i in range (0, 2*(randint(150,200))+1):
        permutation()
    for x in range (0,case) :
        for y in range (0,case):
            if taquin[x][y]==0:
                x0=x
                y0=y
    if x0==3 and y0==3:
        x1,y1=randint(0,case-1),randint(0,case-1)
        x2,y2=randint(0,case-1),randint(0,case-1)
        while (x1==x2 and y1==y1) or (x1==3 and y1==3) or (x2==3 and y2==3):
            x1,y1=randint(0,case-1),randint(0,case-1)
            x2,y2=randint(0,case-1),randint(0,case-1)
        taquin[x1][y1],taquin[x2][y2]=taquin[x2][y2],taquin[x1][y1]
    else:
        taquin[case-1][case-1],taquin[x0][y0]=taquin[x0][y0],taquin[case-1][case-1]



def affichage():
    canvas.delete("all")
    global taquin
    for x in range(0,case):
        for y in range (0,case):
            if taquin[y][x]!=0:
                canvas.create_rectangle(x*(dimension/case), y*(dimension/case),x*(dimension/case)+(dimension/case) , y*(dimension/case)+(dimension/case),fill="white",width=3)
                canvas.create_text(x*(dimension/case)+(dimension/(case*2)), y*(dimension/case)+(dimension/(case*2)), text = str(taquin[y][x]),font=(font,str(floor(70-case*2+(dimension/200)))))
    if taquin==taquin_resolu:
        canvas.create_rectangle(100, 250,700 , 650,fill="white",width=3)
        canvas.create_text(400, 450, text = "Victoire !",font=(font,"70"))



def rejouer():
    canvas.delete("all")
    melange()
    affichage()



def clique(coord):
    if taquin!=taquin_resolu:
        x1=floor(coord.x/(dimension/case))
        y1=floor(coord.y/(dimension/case))
        deplacement(x1,y1)
        affichage()





def jeu():
    canvas.grid(column=2,row=2,rowspan=5)
    titre.grid(column=2,row=1)
    play_again.grid(column=1,row=2)
    racine.bind("<Button-1>", clique)
    mellange()
    affichage()


racine=tk.Tk()
racine.title("Taquin")
titre = tk.Label(racine, text="Taquin", font=(font, "35"))
play_again =tk.Button(racine, text = "Rejouer",font=(font,"45"),command=rejouer)
quitter=tk.Button(racine,text="Quitter",font=(font,"20"),command=racine.destroy)
canvas=tk.Canvas(racine,height=dimension,width=dimension,bg="black")
canvas.grid(column=2,row=2,rowspan=5)
titre.grid(column=2,row=1)
play_again.grid(column=1,row=3)
quitter.grid(column=1,row=5)
racine.bind("<Button-1>", clique)
melange()
affichage()
chronometre()
racine.mainloop()