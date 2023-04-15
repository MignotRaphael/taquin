###############################################################
#                                                             #
#                             Taquin                          #
#                                                             #
#   Raphaël MIGNOT / Cyprien de SOMMYEVRE / Martin CAUSERO    #
#                                                             #
#                                                             #
#                                                             #
###############################################################








import tkinter as tk
from random import randint
from math import floor
from copy import deepcopy


#Rajouter fonction pour choisir son nombre de case




font="helvetica"  #on definit la police d'ecriture pour l'interface
case=4            #le nombre de case de notre taquin
dimension=800     #la longueur en pixel du canevas
temps=[0,-1]      #la variable stockant le temps s'affichant au chrono
chr=False         #la variable permettant de connaitre l'état du chronomètre






taquin=[]
for i in range (0,case):
    ligne=[]
    for j in range(0,case):
        ligne.append(i*case+j+1)
    taquin.append(ligne)
taquin[case-1][case-1]=0
taquin2=deepcopy(taquin)
taquin_resolu=deepcopy(taquin)




def deplacement (x,y):
    global taquin
    global taquin_resolu
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
    affichage()






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






def affichage():#cette fonction sert à afficher le taquin sur notre canevas
    global taquin
    global chr
    global chrono
    canvas.delete("all")#on commence par retirer tous les éléments présents sur le taquin
    for x in range(0,case):
        for y in range (0,case):#on parcour le taquin, case par case
            if taquin[y][x]!=0:#si la case n'est pas la case vide, alors
                canvas.create_rectangle(x*(dimension/case), y*(dimension/case),x*(dimension/case)+(dimension/case) , y*(dimension/case)+(dimension/case),fill="white",width=3)#dimension/case est égale à la longeur en pixel de chaque case, on place donc un carré blanc aux contours noirs sur chaque case
                canvas.create_text(x*(dimension/case)+(dimension/(case*2)), y*(dimension/case)+(dimension/(case*2)), text = str(taquin[y][x]),font=(font,str(floor(70-case*2+(dimension/200)))))# on écrit le numéro de chaque case sur le carré, avec une taille de police addapté aux dimensions du taquin
    if taquin==taquin_resolu: # si le taquin est dans la même configuration que le tquin résolu, alors
        chr=False#on stop le chrono
        canvas.create_rectangle(100, 250,700 , 650,fill="white",width=3)#on place un cadre blanc, dans lequel on écrit "Victoire" en indiquant le temps réalisé par le joueur
        txt=str(temps[0])+":"+str(temps[1])
        canvas.create_text(400, 450, text = f"Victoire !\n{ txt :^12}",font=(font,"70"))








def clique(coord):
    if taquin!=taquin_resolu:
        x1=floor(coord.x/(dimension/case))
        y1=floor(coord.y/(dimension/case))
        deplacement(x1,y1)












def jeu():
    global chr
    global temps
    temps=[0,-1]
    canvas.delete("all")
    canvas.grid(column=2,row=2,rowspan=5)
    chrono.grid(column=3,row=1)
    titre.grid(column=2,row=1)
    play_again.grid(column=1,row=2)
    racine.bind("<Button-1>", clique)
    melange()
    affichage()
    if chr==False:#on déclenche le chrono si et seulement si il n'est pas déja activé
        chr=True# on indique que le chronon est lancé
        chronometre()#on démare le chrono




def chronometre():
    global chr
    global temps
    if chr==True: #ssi le chrono est activé
        temps[1]=temps[1]+1 #temps[1] correspond au nombre de seconde
        if temps[1]>59:#si on atteint les 60 secondes :
            temps[0]=temps[0]+1 #temps[0] correspond au nombre de minutes
            temps[1]=0#on passe le nombre de seconde à 0
        chrono.config(text=str(temps[0])+":"+str(temps[1]))#on actualise l'afficheur
        racine.after(1000,chronometre)#on recomence une seconde plus tard








racine=tk.Tk()
racine.title("Taquin")
titre = tk.Label(racine, text="Taquin", font=(font, "35"))
chrono=tk.Label(racine,font=(font,"20"))
play_again =tk.Button(racine, text = "Rejouer",font=(font,"45"),command=jeu)
quitter=tk.Button(racine,text="Quitter",font=(font,"20"),command=racine.destroy)
canvas=tk.Canvas(racine,height=dimension,width=dimension,bg="black")
canvas.grid(column=2,row=2,rowspan=5)
titre.grid(column=2,row=1)
play_again.grid(column=1,row=3)
quitter.grid(column=1,row=5)
canvas.bind("<Button-1>", clique)
jeu()
racine.mainloop()
