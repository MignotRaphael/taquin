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
from pathlib import Path
from pathlib import __file__




font="helvetica" #on definit la police d'ecriture pour l'interface
case=4           #le nombre de case de notre taquin
dimension=800    #la longueur en pixel du canevas
temps=[0,-1]     #la variable stockant le temps s'affichant au chrono
chr=False        #la variable permettant de connaitre l'état du chronomètre
select=0         #variable stockant le nom de la sauvegarde que le joueur veut charger
coup=[]          #cette liste stocke les configurations précédentes du taquin
cliquable=0      #cette variable nous indique si la souris survol ou non le canevas
path=  "files/sauvegarde.json" #on definit le chemin du fichieer sauvegarde.json, dans lequel sont stockées nos sauvegarde
taille_damier={"3*3":3,"4*4":4,"5*5":5,"6*6":6,"7*7":7,"8*8":8}#dico servant de liste de valeur à afficher dans les menus déroulants
taille_fentre={"300*300":300,"500*500":500,"800*800":8}#dico servant de liste de valeur à afficher dans les menus déroulants




def creation_taquin():#cette fonction crée une liste imbriquée servant de taquin, dont les dimensions dépendent de la variable case
    global taquin
    global taquin2
    global taquin_resolu
    taquin=[]
    for i in range (0,case):#cette boucle crée le taquin, organisé dans l'ordre
        ligne=[]
        for j in range(0,case):
            ligne.append(i*case+j+1)
        taquin.append(ligne)
    taquin[case-1][case-1]=0#on place la case vide
    taquin2=deepcopy(taquin)#on crée taquin2 en copiant taquin
    taquin_resolu=deepcopy(taquin)#on crée taquin_resolu, une variable stockant la configuration du taquin resolu




def deplacement (x,y): #cette fonction permet de gérer le déplacement des cases dans le taquin, x et y étant les indices de la case cliquée par le joueur
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
    affichage()






def permutation():#cette fonction permet d'intervertir deux cases aléatoires
    global taquin
    x1,y1=randint(0,case-1),randint(0,case-1)#on choisit une case aléatoirement
    x2,y2=randint(0,case-1),randint(0,case-1)#on choisit une autre case aléatoirement
    while x1==x2 and y1==y2:#on s'assure que les deux cases ne sont pas les mêmes
        x2,y2=randint(0,case-1),randint(0,case-1)
    taquin[x1][y1],taquin[x2][y2]=taquin[x2][y2],taquin[x1][y1]#on intervertit les deux cases






def melange():#cette fonction permet de mélanger le taquin, en respectant la solubilité
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
    global chr
    global chrono
    global coup
    global dimension
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








def jeu():#cette fonction sert à lancer la partie
    global chr
    global temps
    global coup
    global case
    temps=[0,-1]#on reinitialise le chrono
    canvas.delete("all")#on retire tous les éléments du canevas
    for widget in racine.winfo_children():#on retire tous les widgets de la fenètre
        widget.grid_forget()
    creation_taquin()#on crée le(s) taquin(s)
    canvas.grid(column=2,row=2,rowspan=5)#on place les éléments nécessaires pour jouer
    chrono.grid(column=3,row=1)
    titre.grid(column=2,row=1)
    play_again.grid(column=1,row=2)
    Bouton_sauvegarde.grid(column=1,row=1)
    Bouton_reprendre_coup.grid(column=3,row=2)
    Bouton_retour.grid(column=1,row=3)
    canvas.bind("<Button-1>", clique)#on bind le clique gauche sur le canevas
    melange()#on melange le taquin et on l'affiche
    affichage()
    if chr==False:#on lance le chrono si ça n'etait pas encore le cas
        chr=True
        chronometre()






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






def sauvegarde():
    global temps
    global case
    global taquin_resolu
    global taquin2
    global coup
    if taquin!=taquin_resolu:#on peut sauvegarder sauf si on a déja gagné
        fichier = open (path,"r")#on ouvre le fichier contenat les sauvegardes en mode lecture
        str_save=fichier.read()#on passe le fichier en str
        fichier.close()#on ferme le fichier en lecture
        str_save=json.loads(str_save)#on passe le fichier du str en dico
        fichier = open (path,"w")#on ouvre le fichier en ecriture
        str_save[str(datetime.now())]=[temps,taquin,case,taquin_resolu,taquin2,coup]#on ajoute au  dico la liste contenant le chrono, la variable taquin,taquin 2, taquin resolu, le nombre de cases, et la liste de nos derniers coups, ave comme clé, la date et l'heure à laquelle la sauvegarde est effectuée
        json.dump(str_save,fichier,indent=0)#on sauvegarde le dico au format json et on ferme le fichier
        fichier.close
        menu_sauvegarde.config(values=list(str_save))#on met à jour le menu deroulant, pour qu'il affiche la nouvelle sauvegarde






def selec(event):#cette fonction récupère le nom de la sauvegarde sélectionnée
    global select
    select=menu_sauvegarde.get()






def charge():
    global temps
    global taquin
    global taquin2
    global select
    global case
    global taquin_resolu
    global chr
    global coup
    if taquin!=taquin_resolu:
        jeu()#on relance une partie
        fichier = open (path,"r")#on auvre le fichier des sauvegardes
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
        fichier = open (path,"r")#on ouvre le fichier json des sauvegardes
        str_save=fichier.read()
        str_save=json.loads(str_save)#on passe le contenu du fichier json au format d'un dictionaire
        fichier.close()
        str_save.pop(select)#on supprime la sauvegarde sélectionnée
        fichier = open (path,"w")#on ouvre le fichier des sauvegardes
        json.dump(str_save,fichier,indent=0)#on remplace le contenu du fichier par le dico sans la sauvegarde à supprimer
        fichier.close
        fichier = open (path,"r")
        str_save=fichier.read()
        fichier.close()
        str_save=json.loads(str_save)
        menu_sauvegarde.config(values=list(str_save))#on met à jour le menu deroulant de sélection des sauvegardes, grace au contenu du fichier json








def reprendre_coup():#cette fonction permet de revenir en arrière
    global taquin
    global taquin2
    global coup
    taquin=deepcopy(coup[-1])#on remplace la valuer actuelle du taquin par la dernière valeur ajouté à la liste coup
    taquin2=deepcopy(coup[-1])#de même pour taquin2
    coup.pop(-1)#on supprime la dernière valeur ajouté à la liste coup
    affichage()




def entre(self):#cette fonction met à jour la valuer de cliquable quand le curseur survol sur le canevas
    global cliquable
    cliquable=True




def sort(self):#cette fonction met àjour la valuer de cliquable quand le curseur quitte le canevas
    global cliquable
    cliquable=False






def damier(event):#cette fonction récupère la valeur sélectionnée pour le nombre de case du taquin et l'assigne à la variable case
    global case
    case=(taille_damier[(menu_damier.get())])


def taille(event):#cette fonction récupère la valeur en pixel sélectionnée par le jour et modifie la taille du canevas en conséquence
    global dimension
    dimension=(taille_fentre[menu_taille_fenetre.get()])
    canvas.config(height=dimension,width=dimension)


def nouvelle_partie():#cette fonction définie le menu de parametrage de la nouvelle partie
    for widget in racine.winfo_children():#on retire tous les widgets
        widget.grid_forget()
    menu_damier.grid(column=1,row=1,padx=125,pady=50)#on affiche le menu de sélection du nombre de case du taquin
    Bouton_jouer.grid(column=1,row=2)#on affiche le bouton pour lancer la partie
    Bouton_retour.grid(column=0,row=3)




def menu_charger_partie():#cette fonction définie le menu de charge d'une sauvegarde
    for widget in racine.winfo_children():#on retire tous les widgets
        widget.grid_forget()
    menu_sauvegarde.grid(column=1,row=1,padx=70,pady=30)#on affiche le menu déroulant affichant les sauvegardes
    Bouton_charge.grid(column=1,row=2)#on affiche le bouton permettant de charger une sauvegarde
    Bouton_supprimer_sauvegarde.grid(column=1,row=3,pady=50)#on affiche le bouton permettant de supprimer une sauvegarde
    Bouton_retour.grid(column=0,row=3)






def main_menu():#cette fonction définie le menu principal
    for widget in racine.winfo_children():#on retire tous les widgets
        widget.grid_forget()
    titre.grid(column=2,row=0,padx=100)#on place les éléments de l'écran d'acceuil
    menu_taille_fenetre.grid(column=2,row=3,pady=20)
    Bouton_comencer_partie.grid(column=2,row=1,pady=20)
    Bouton_charger_partie.grid(column=2,row=2)
    quitter.grid(column=2,row=4)




racine=tk.Tk()#on crée la fenetre racine, que l'on renomme
racine.title("Taquin")
fichier = open (path,"r")#on ouvre le fichier des sauvegardes
str_save=fichier.read()
str_save=json.loads(str_save)#on recupère le dico stocké dans le json
fichier.close()
menu_sauvegarde=ttk.Combobox(racine,values=list(str_save))#on crée le menu deroulant de sélection des sauvegardes, avec le nom des sauvegardes comme valeur affichées
menu_taille_fenetre=ttk.Combobox(racine,values=["300*300","500*500","800*800"])#on crée le menu déroulant de sélection de la taille de canevas
menu_damier=ttk.Combobox(racine,values=["3*3","4*4","5*5","6*6","7*7","8*8"])#on crée le mennu deroulant de séclection du nombre de cases du canevas
titre = tk.Label(racine, text="Taquin", font=(font, "45"))#on crée des labels
chrono=tk.Label(racine,font=(font,"20"))
play_again =tk.Button(racine, text = "Rejouer",font=(font,"45"),command=jeu)#on crée des boutons
quitter=tk.Button(racine,text="Quitter",font=(font,"20"),command=racine.destroy)
Bouton_sauvegarde=tk.Button(racine,text="sauvegarder", font=(font,"20"),command=sauvegarde)
Bouton_charge=tk.Button(racine,text="Charger une partie", font=(font,"20"),command=charge)
Bouton_comencer_partie=tk.Button(racine,text="Nouvelle partie",font=(font,30),command=nouvelle_partie)
Bouton_charger_partie=tk.Button(racine,text="Charger partie",font=(font,"20"),command=menu_charger_partie)
Bouton_supprimer_sauvegarde=tk.Button(racine,text="Supprimer sauvegarde",font=(font,"10"),command=supprimer_sauvegarde)
Bouton_reprendre_coup=tk.Button(racine,text="Reprendre son coup",font=(font,"15"),command=reprendre_coup)
Bouton_jouer=tk.Button(racine,text="Commencer",font=(font,"30"),command=jeu)
Bouton_retour=tk.Button(racine,text="<<<",font=(font,"10"),command=main_menu)
canvas=tk.Canvas(racine,height=dimension,width=dimension,bg="black")#on crée le canevas
canvas.bind("<Button-1>", clique)#on bind le clique gauche sur le canevas
canvas.bind("<Enter>", entre)#cess deux binds permettent de s'assurer que le curseur survol le taquin
canvas.bind("<Leave>", sort)
menu_sauvegarde.bind("<<ComboboxSelected>>", selec)#ces lignes permettent de détecter la sélection dans les menus déroulants
menu_taille_fenetre.bind("<<ComboboxSelected>>", taille)
menu_damier.bind("<<ComboboxSelected>>", damier)
main_menu()
racine.mainloop()



