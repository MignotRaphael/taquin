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
import json
from random import randint
from math import floor
from copy import deepcopy
from datetime import datetime
from tkinter import ttk




font="helvetica" #on definit la police d'ecriture pour l'interface
case=4           #le nombre de case de notre taquin
dimension=800    #la longueur en pixel du canevas
temps=[0,-1]     #la variable stockant le temps s'affichant au chrono
chr=False        #la variable permettant de connaitre l'état du chronomètre
select=0         #variable stockant le nom de la sauvegarde que le joueur veut charger
coup=[]          #cette liste stocke les configurations précédentes du taquin
cliquable=0      #cette variable nous indique si la souris survol ou non le canevas

taquin=[]
for i in range (0,case): #cette fonction crée le taquin, organisé dans l'ordre
    ligne=[]
    for j in range(0,case):
        ligne.append(i*case+j+1)
    taquin.append(ligne)
taquin[case-1][case-1]=0 #on place la case vide en bas à gauche
taquin2=deepcopy(taquin)#on copie ce taquin dans une variable taquin2
taquin_resolu=deepcopy(taquin)#on recupère le taquin resolu, pour controler si le joueur a gagner


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
    global coup
    canvas.delete("all")#on commence par retirer tous les éléments présents sur le taquin
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



def clique(coord):#cette fonction récupère  les coordonnées du clique, et renvoie la case sur laquelle le joueur a cliqué
    global taquin
    global taquin2
    global coup
    global cliquable
    if taquin!=taquin_resolu:#on peut cliquer sauf si le joueur a déja gagné
        if cliquable==True:#si le curseur survol le canevas
            x1=floor(coord.x/(dimension/case))#la partie entière de la division des coordonnées par les dimensions d'unu case, donc l'indice de la case dans la variable taquin
            y1=floor(coord.y/(dimension/case))
            coup.append(deepcopy(taquin))#on ajoute la configuration actuelle du taquin à la liste des coups précédents
            deplacement(x1,y1) #on déplace les cases en prenant les indices  de la case cliquée
    if len(coup)>20:#on limite le nombre de coup enregistrés
        coup.pop(0)




def jeu():#cette fonction
    global chr
    global temps
    global coup
    temps=[0,-1]#on réinitialise le chrono
    canvas.delete("all")#on retire tous les éléments du canevas
    canvas.grid(column=2,row=2,rowspan=5)#on place les éléments nécessaires sur l'interface graphique
    chrono.grid(column=3,row=1)
    titre.grid(column=2,row=1)
    play_again.grid(column=1,row=2)
    melange()#on mélange le taquin et on l'affiche
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



def sauvegarde():#cette fonction permet de sauvegarder une partie en cours sur un fichier json
    global temps
    global case
    global taquin_resolu
    global taquin2
    global coup
    if taquin!=taquin_resolu:#on peut sauvegarder sauf si on a déja gagné
        fichier = open ("files/sauvegarde.json","r")#on ouvre le fichier contenat les sauvegardes en mode lecture
        str_save=fichier.read()#on passe le fichier en str
        fichier.close()#on ferme le fichier en lecture
        str_save=json.loads(str_save)#on passe le fichier du str en dico
        fichier = open ("files/sauvegarde.json","w")#on ouvre le fichier en ecriture
        str_save[str(datetime.now())]=[temps,taquin,case,taquin_resolu,taquin2,coup]#on ajoute au  dico la liste contenant le chrono, la variable taquin,taquin 2, taquin resolu, le nombre de cases, et la liste de nos derniers coups, ave comme clé, la date et l'heure à laquelle la sauvegarde est effectuée
        json.dump(str_save,fichier,indent=0)#on sauvegarde le dico au format json et on ferme le fichier
        fichier.close
        menu_sauvegarde.config(values=list(str_save))#on met à jour le menu deroulant, pour qu'il affiche la nouvelle sauvegarde


def selec(event):#cette fonction récupère le nom de la sauvegarde sélectionnée
    global select
    select=menu_sauvegarde.get()



def charge():#cette fonction permet de lire une sauvegarde
    global temps
    global taquin
    global taquin2
    global select
    global case
    global taquin_resolu
    global chr
    global coup
    if taquin!=taquin_resolu:#à condition que l'on est pas déja gagné
        temps=[0,0]
        fichier = open ("files/sauvegarde.json","r")#on auvre le fichier des sauvegardes
        str_save=fichier.read()
        str_save=json.loads(str_save)#on stock le contenu du fichier au format d'un dico, et on ferme le fichier
        fichier.close()
        temps=str_save[select][0]#on actualise les variables de jeu avec celles stockées dans la sauvegarde
        taquin=str_save[select][1]
        case=str_save[select][2]
        taquin_resolu=str_save[select][3]
        taquin2=str_save[select][4]
        coup=str_save[select][5]
        affichage()#on affiche la partie chargée




def supprimer_sauvegarde():# cette fonction permet de supprimer une sauvegarde sélectionnée
    global select
    if taquin!=taquin_resolu:#on peut supprimer une sauvegarde sauf si on a déja gagné
        fichier = open ("files/sauvegarde.json","r")#on ouvre le fichier json des sauvegardes
        str_save=fichier.read()
        str_save=json.loads(str_save)#on passe le contenu du fichier json au format d'un dictionaire
        fichier.close()
        str_save.pop(select)#on supprime la sauvegarde sélectionnée
        fichier = open ("files/sauvegarde.json","w")#on ouvre le fichier des sauvegardes
        json.dump(str_save,fichier,indent=0)#on remplace le contenu du fichier par le dico sans la sauvegarde à supprimer
        fichier.close
        fichier = open ("files/sauvegarde.json","r")
        str_save=fichier.read()
        fichier.close()
        str_save=json.loads(str_save)
        menu_sauvegarde.config(values=list(str_save))#on met à jour le menu deroulant de sélection des sauvegardes, grace au contenu du fichier json



def reprendre_coup():#cette fonction permet de revenir en arrière
    global taquin
    global taquin2
    global coup
    taquin=deepcopy(coup[-2])#on remplace la valuer actuelle du taquin par l'avant dernière valeur ajouté à la liste coup
    taquin2=deepcopy(coup[-2])#de même pour taquin2
    coup.pop(-2)#on supprime les deux dernières valeurs ajoutés à la liste coup
    coup.pop(-1)
    affichage()


def entre(self):#cette fonction met à jour la valuer de cliquable quand le curseur survol sur le canevas
    global cliquable
    cliquable=True


def sort(self):#cette fonction met àjour la valuer de cliquable quand le curseur quitte le canevas
    global cliquable
    cliquable=False




racine=tk.Tk()#on crée la fenetre racine, que l'on renomme
racine.title("Taquin")
fichier = open ("files/sauvegarde.json","r")#on ouvre le fichier des sauvegardes
str_save=fichier.read()
str_save=json.loads(str_save)#on recupère le dico stocké dans le json
fichier.close()
menu_sauvegarde=ttk.Combobox(racine,values=list(str_save))#on crée le menu deroulant de sélection des sauvegardes, avec le nom des sauvegardes comme valeur affichées
titre = tk.Label(racine, text="Taquin", font=(font, "35"))#on crée differents textes
chrono=tk.Label(racine,font=(font,"20"))
play_again =tk.Button(racine, text = "Rejouer",font=(font,"45"),command=jeu)#on crée différents boutons
quitter=tk.Button(racine,text="Quitter",font=(font,"20"),command=racine.destroy)
Bouton_sauvegarde=tk.Button(racine,text="sauvegarder", font=(font,"10"),command=sauvegarde)
Bouton_charge=tk.Button(racine,text="Charger une partie", font=(font,"10"),command=charge)
Bouton_supprimer_sauvegarde=tk.Button(racine,text="Supprimer sauvegarde",font=(font,"10"),command=supprimer_sauvegarde)
Bouton_reprendre_coup=tk.Button(racine,text="Retour arière",font=(font,"15"),command=reprendre_coup)
canvas=tk.Canvas(racine,height=dimension,width=dimension,bg="black")#on crée le canvas, avec un fond noir
canvas.grid(column=2,row=2,rowspan=5)#on place les boutons, labels, menus deroulants et canvas
titre.grid(column=2,row=1)
chrono.grid(column=3,row=1)
play_again.grid(column=3,row=0)
quitter.grid(column=1,row=6)
Bouton_sauvegarde.grid(column=1,row=1)
Bouton_charge.grid(column=1,row=4)
Bouton_supprimer_sauvegarde.grid(column=1,row=5)
Bouton_reprendre_coup.grid(column=3,row=0)
menu_sauvegarde.grid(column=1,row=3)
canvas.bind("<Button-1>", clique)#on traque les cliques gauches sur le canvas
canvas.bind("<Enter>", entre)#cette ligne permet de savoir si oui ou non, le curseur survol le canevas
canvas.bind("<Leave>", sort)
menu_sauvegarde.bind("<<ComboboxSelected>>", selec)#cette ligne détecte les sélections dans les mmenus déroulants
jeu()
racine.mainloop()