import tkinter as tk
import json
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
    global taquin_resolu
    taquin2=deepcopy(taquin)#on stock dans taquin2 la configuration initiale de taquin
    for i in range (0,case):#cette boucle permet de localiser la case vide, et d'en stocker les coordonnées x0 et y0
        for j in range (0,case):
            if taquin[j][i]==0:
                x0=i
                y0=j
    if y==y0 and x<x0 :#le déplacement si la case cliquée et la case vide sont sur la même ligne et la case vide à droite de la case cliquée
        for i in range (x0,x-1,-1):
            taquin[y][i]=taquin2[y][i-1]#toutes les cases de la ligne sont décalées d'une case vers la droite
        taquin[y][x]=0#on place la case vide sur la case cliquée
    elif y==y0 and x>x0 :#le déplacement si la case cliquée et la case vide sont sur la même lignee et la case vide à gauche de la case cliquée
        for i in range (x0,x):
            taquin[y][i]=taquin2[y][i+1]
        taquin[y][x]=0
    elif x==x0 and y<y0:#le déplacement si la case vide et la case cliquée sont sur la même colonne et la case vide en dessous de la case cliquée
        for i in range (y0,y-1,-1):
            taquin[i][x]=taquin2[i-1][x]
        taquin[y][x]=0
    elif x==x0 and y>y0:#le déplacement si la case vide et la case cliquée sont sur la même colonne et la case vide au dessus de la case cliquée
        for i in range (y0,y):
            taquin[i][x]=taquin2[i+1][x]
        taquin[y][x]=0




def permutation():#cette fonction permet d'intervertir deux cases aléatoires
    global taquin
    x1,y1=randint(0,case-1),randint(0,case-1)#on choisit une case aléatoirement
    x2,y2=randint(0,case-1),randint(0,case-1)#on choisit une case aléatoirement
    while x1==x2 and y1==y2:#on s'assure que les deux cases ne sont pas les mêmes
        x2,y2=randint(0,case-1),randint(0,case-1)
    taquin[x1][y1],taquin[x2][y2]=taquin[x2][y2],taquin[x1][y1]#on intervertit les deux cases






def melange():#cette fonction permet de moélanger le tquin, de telle sorte que la cpnfiguration soit soluble
    global taquin
    x0=0
    y0=0
    for i in range (0, 2*(randint(150,200))+1):#on intervertit les cases du taquin un nombre impair de fois, on a donc une configuration insoluble
        permutation()
    for x in range (0,case) :#on repère les coordonnées de la case vide
        for y in range (0,case):
            if taquin[x][y]==0:
                x0=x
                y0=y
    if x0==case-1 and y0==case-1:#si la case vide est en bas à droite
        x1,y1=randint(0,case-1),randint(0,case-1)#on choisit deux cases aléatoirement
        x2,y2=randint(0,case-1),randint(0,case-1)
        while (x1==x2 and y1==y1) or (x1==case-1 and y1==case-1) or (x2==3-case-1 and y2==case-1): #on s'assure que les deux cases sont différentes et qu'aucune des deux est en bas à droite
            x1,y1=randint(0,case-1),randint(0,case-1)
            x2,y2=randint(0,case-1),randint(0,case-1)
        taquin[x1][y1],taquin[x2][y2]=taquin[x2][y2],taquin[x1][y1]#on intervertit les deux cases, on a donc un nombre de permutation pair, et la case vide en bas à droite
    else:
        taquin[case-1][case-1],taquin[x0][y0]=taquin[x0][y0],taquin[case-1][case-1]#sinon, on intervertit la case en bas à droite avec la case vide, on obtient donc une configuratioin au nombre de permutation pair, donc une configuration soluble






def affichage():#cette fonction sert à afficher le taquin sur notre canevas
    global taquin
    for x in range(0,case):
        for y in range (0,case):#on parcour le taquin, case par case
            if taquin[y][x]!=0:#si la case n'est pas la case vide, alors
                canvas.create_rectangle(x*(dimension/case), y*(dimension/case),x*(dimension/case)+(dimension/case) , y*(dimension/case)+(dimension/case),fill="white",width=3)#dimension/case est égale à la longeur en pixel de chaque case, on place donc un carré blanc aux contours noirs sur chaque case
                canvas.create_text(x*(dimension/case)+(dimension/(case*2)), y*(dimension/case)+(dimension/(case*2)), text = str(taquin[y][x]),font=(font,str(floor(70-case*2+(dimension/200)))))#on écrit le numéro de chaque case sur le carré, avec une taille de police addapté aux dimensions du taquin
    if taquin==taquin_resolu:# si le taquin est dans la même configuration que le tquin résolu, alors
        chr=False#on stop le chrono
        canvas.create_rectangle(100, 250,700 , 650,fill="white",width=3)#on place un cadre blanc, dans lequel on écrit "Victoire" en indiquant le temps réalisé par le joueur
        txt=str(temps[0])+":"+str(temps[1])
        canvas.create_text(400, 450, text = f"Victoire !\n{ txt :^12}",font=(font,"70"))



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



