# MarrakechGUI.py

# Copyright Jacques Madelaine, (29/10/2017)
# jacques.madelaine@unicaen.fr

# Ce logiciel est un programme informatique servant à jouer à Marrakech,
# un jeu  de plateau de Dominique Ehrhard distribué et édité par Gigamic,
# dans le but de pouvoir mettre en oeuvre et tester des intelligences
# artificielles pour jouer à ce jeu.
#
# En particulier, si vous aimez ce jeu de plateau, achetez en une copie
# en plus d'utiliser ce logiciel.

# Ce logiciel est régi par la licence CeCILL soumise au droit français et
# respectant les principes de diffusion des logiciels libres. Vous pouvez
# utiliser, modifier et/ou redistribuer ce programme sous les conditions
# de la licence CeCILL telle que diffusée par le CEA, le CNRS et l'INRIA 
# sur le site "http://www.cecill.info".

# En contrepartie de l'accessibilité au code source et des droits de copie,
# de modification et de redistribution accordés par cette licence, il n'est
# offert aux utilisateurs qu'une garantie limitée.  Pour les mêmes raisons,
# seule une responsabilité restreinte pèse sur l'auteur du programme,  le
# titulaire des droits patrimoniaux et les concédants successifs.

# A cet égard  l'attention de l'utilisateur est attirée sur les risques
# associés au chargement,  à l'utilisation,  à la modification et/ou au
# développement et à la reproduction du logiciel par l'utilisateur étant 
# donné sa spécificité de logiciel libre, qui peut le rendre complexe à 
# manipuler et qui le réserve donc à des développeurs et des professionnels
# avertis possédant  des  connaissances  informatiques approfondies.  Les
# utilisateurs sont donc invités à charger  et  tester  l'adéquation  du
# logiciel à leurs besoins dans des conditions permettant d'assurer la
# sécurité de leurs systèmes et ou de leurs données et, plus généralement, 
# à l'utiliser et l'exploiter dans les mêmes conditions de sécurité. 

# Le fait que vous puissiez accéder à cet en-tête signifie que vous avez 
# pris connaissance de la licence CeCILL, et que vous en avez accepté les
# termes.
import tkinter as tk

from ModeleMarrakech import *
from Marrakech import *
import MonIA

L = 60 # la taille d'une case en pixels

from enum import *
class EtatGUI(IntEnum):
    """Les états du GUI """
    Repos = 0
    AssamActif = 1
    PoseTapis1 = 2
    PoseTapis2 = 3

class MarrakechGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        master.title("Marrakech")
        self.master = master
        self.pack()
        self.config(width=15*L)
        self.dir_assam = DirectionAssam(0) # à initialiser depuis le modèle
        self.items_tapis = []
        self.items_assam = []
        self.canvas = self.cree_plateau()
        self.nbj = tk.IntVar(self)
        self.nbj.set(2) # initial value
        self.couleurs = [ "red", "yellow", "blue", "green" ]
        self.cree_espace_controle()

        self.modele = None
        self.refresh_assam()
        self.etat = EtatGUI.Repos

        self.nelle_partie()

    def cree_plateau(self):
        tk.Label(self, text=" ").pack(side=tk.TOP)
        T = Plateau.taille_plateau()
        print(T)
        canvas = tk.Canvas(self, width=(T+2)*L, height=(T+2)*L, background="green")
        canvas.pack(side=tk.TOP)
        for x in range(T+2):
            for y in range(T+2):
                bord = x == 0 or y == 0 or x == (T+1) or y == (T+1)
                fill_color = "darkgreen" if bord else "orange"
                id = canvas.create_rectangle((x*L, y*L, (x+1)*L, (y+1)*L), fill=fill_color, outline="green")
                if not bord: 
                    canvas.tag_bind(id, "<Button-1>", self.clic1)
        for t in range(1, T+1):
            # renvois en haut
            self.cree_renvoi(canvas, t, 0, 0, t%2!=0)
            # renvois à droite
            self.cree_renvoi(canvas, T+1, t, 1, t%2==0)
            # renvois en bas
            self.cree_renvoi(canvas, t, T+1, 2, t%2!=0)
            # renvois à gauche
            self.cree_renvoi(canvas, 0, t, 3, t%2==0)
        #cree_renvoi en haut à droite
        self.cree_renvoi_angle(canvas, T+1, 0, 0)
        self.cree_renvoi_angle(canvas, 0, T+1, 2)
        
        return canvas

    def affiche_tapis(self, canvas, coords, couleur):
        """
        affiche le tapis donné par coords de la forme ((x0, y0), (x1, y1))
        épaisseur e permet de décaler l'image
        """
        # on cherche les coordonnées N-W, S-E
        # si on jouait en 3D :
        #xmin = min( [ c[0] for c in coords] )
        #xmax = max( [ c[0] for c in coords] )
        #ymin = min( [ c[1] for c in coords] )
        #ymax = max( [ c[1] for c in coords] )
        xmin = min(coords[0][0], coords[1][0])
        xmax = max(coords[0][0], coords[1][0])
        ymin = min(coords[0][1], coords[1][1])
        ymax = max(coords[0][1], coords[1][1])
        l = 12 # le tapis fait L-l × 2L-l
        dx = dy = 2
        # e épaisseur moyenne des 2 cases
        e = min(self.modele.plateau.epaisseur(coords[0][0], coords[0][1]), self.modele.plateau.epaisseur(coords[1][0], coords[1][1]))
        e %= 4 # l'épaisseur permet de décaler le tapis
        dx += e*3
        dy += e*3
        bbox = (L*(xmin+1)+dx, L*(ymin+1)+dy, L*(xmax+2)+dx-l, L*(ymax+2)+dy-l)
        t = canvas.create_rectangle(bbox, fill=couleur, outline=couleur)
        canvas.tag_bind(t, "<Button-1>", self.clic1)
        self.items_tapis.append(t)

    def nelle_partie(self):
        m = ModeleMarrakech(self.nbj.get())
        JoueurMarrakech.numero = 0
        joueurs = []
        for j in range(self.nbj.get()):
            joueur = self.dict_types_joueurs[self.type_joueurs[j].get()](m)
            # print("Joueur", j, joueur)
            joueurs.append(joueur)
        self.modele = m
        self.controleur = ControleurPartie(self, m, joueurs)
        self.controleur.run()
        self.refresh()

    def set_nb_joueurs(self, event):
        # print(self.nbj.get(), "joueurs")
        for j, id in enumerate(self.id_options_type_joueurs):
            id.config(state="disabled" if j >= self.nbj.get() else "active")
        # scores
        for j in range(4):
            color = "black" if j < self.nbj.get() else "DarkGrey"
            for id in self.ids_scores[j]:
                id.config(fg=color)

    def cree_espace_controle(self):

        self.controle = tk.Frame(self.master)
        self.controle.pack()
        
        l = tk.Label(self.controle, text="      Message    ")
        l.grid(row=0, column=0, columnspan=8, sticky="we")
        self.messages = tk.Text(self.controle, height=10, background="LightSlateGrey", state="disabled")
        self.messages.grid(row=2, rowspan=5, columnspan=8)

        option = tk.OptionMenu(self.controle, self.nbj, 2, 3, 4, command=self.set_nb_joueurs) 
        option.grid(row=8, column=0)

        l = tk.Label(self.controle, text="Joueurs")
        l.grid(row=8, column=1)
        self.type_joueurs = []
        self.id_options_type_joueurs = []
        self.dict_types_joueurs = {"humain" : JoueurGUI, "ia0" : JoueurAuHasard, "clavier": JoueurLDC, "super ia": MonIA.MonIA}
        for j in range(4):
            type_var = tk.StringVar(self)
            type_var.set("humain" if j == 0 else "super ia" if j == 1 else "ia0")
            self.type_joueurs.append(type_var)
            id = tk.OptionMenu(self.controle, type_var, *self.dict_types_joueurs.keys()) 
            id.grid(row=8, column=2+j)
            # id.config(background=self.couleurs[j])
            if j >= self.nbj.get(): id.config(state="disabled")
            self.id_options_type_joueurs.append(id)

        b = tk.Button(self.controle, text="Nouvelle partie", command=self.nelle_partie)
        b.grid(row=8, column=6, columnspan=2)

        self.ids_scores = []
        for j in range(4):
            self.ids_scores.append([])
       
        self.dirhams = self.ligne_score(9, "Dirhams", 30)
        
        self.nb_tapis = self.ligne_score(10, "Tapis", 0)        

        self.totaux = self.ligne_score(11, "Total", 30, True)

        # Tours
        self.nb_tours_var = tk.StringVar(self)
        self.nb_tours_var.set("Tour 1")
        l = tk.Label(self.controle, textvariable = self.nb_tours_var)
        l.grid(row=9, column=6, columnspan=2)

        # Joueur courant
        tk.Label(self.controle, text = "Joueur").grid(row=10, column=6, sticky="e")
        l = tk.Label(self.controle, text = "      ", bg="red")
        l.grid(row=10, column=7, sticky="w")
        self.label_joueur_courant = l

        ## Bouton undo
        #self.bouton_undo = tk.Button(self.controle, text="Annuler le coup", command=self.undo, state="disabled")
        #self.bouton_undo.grid(row=11, column=6)

        # Bouton tour suivant nécessaire pour utiliser le undo

    def ligne_score(self, row, texte, valeur, couleur=False):
        liste_vars = []
        l = tk.Label(self.controle, text=texte)
        l.grid(row=row, column=1)
        for j in range(4):
            var = tk.StringVar(self)
            var.set(valeur)
            color = "black" if j < self.nbj.get() else "DarkGrey"
            id = tk.Label(self.controle, textvariable = var, fg = color)
            id.grid(row=row, column=2+j)
            if couleur:
                id.config(background=self.couleurs[j])
            self.ids_scores[j].append(id)
            liste_vars.append(var)
        return liste_vars

    def message(self, text):
        "Insère le texte dans la zone de message"
        self.messages.config(state="normal")
        self.messages.insert(tk.END, text)
        self.messages.see(tk.END)
        self.messages.config(state="disabled")

    @staticmethod
    def isometrie(coords, x0, y0, rot90, symx):
        """Applique sur les coordonnées une translation de vecteur(x0, y0), une rotation de rot90 × 90° et une éventuelle symétrique droite sur l'axe des y"""
        c = []
        for (x, y) in coords:
            if symx: x = L-x
            if rot90%4 == 1:
                x, y =  L-y, x
            elif rot90%4 == 2:
                x, y = L-x, L-y
            elif rot90%4 == 3:
                x, y = y, L-x
            c.append(x0+x)
            c.append(y0+y)
        return c

    def cree_renvoi(self, canvas, x0, y0, rot90, symx):
        """crée une flèche de renvoi translatée de (x0, y0) tournée de rot90 × 90° et symétrique en miroir sur x si symx"""
        coords = ((0, L/3), (3*L/8, L/2), (3*L/8, 2*L/3), (L/2, L), (5*L/8, 2*L/3), (5*L/8, L/4), (3*L/8, L/4), (0, L/12), (0, L/3))
        canvas.create_polygon(self.isometrie(coords, L*x0, L*y0, rot90, symx), fill="lightgreen")

    def cree_renvoi_angle(self, canvas, x0, y0, rot90):
        coords = ((0, L/3), (3*L/8, L/2), (3*L/8, 2*L/3), (2*L/3, L), (11*L/12, L), (5*L/8, 2*L/3), (5*L/8, L/4), (3*L/8, L/4), (0, L/12), (0, L/3))
        canvas.create_polygon(self.isometrie(coords, L*x0, L*y0, rot90, False), fill="lightgreen")     

    def cree_assam(self, canvas, x0, y0, rot90):

        for id in self.items_assam:
            canvas.delete(id)
        self.items_assam = []

        coordsEpauleG = ((L/12, 5*L/12), (L/2, 7*L/12))
        id = canvas.create_rectangle(self.isometrie(coordsEpauleG, L*x0, L*y0, rot90, False), fill="black")
        canvas.tag_bind(id, "<Button-1>", self.clic_assam_gauche)
        self.items_assam.append(id)

        id = canvas.create_rectangle(self.isometrie(coordsEpauleG, L*x0, L*y0, rot90, True), fill="black")
        canvas.tag_bind(id, "<Button-1>", self.clic_assam_droite)
        self.items_assam.append(id)
        coordsChapeau = ((L/3-2, L/3-2), (2*L/3+2, 2*L/3+2))

        id = canvas.create_arc(self.isometrie(coordsChapeau, L*x0, L*y0, rot90, False), extent=359, fill="darkred", outline="darkred")
        canvas.tag_bind(id, "<Button-1>", self.clic_assam)
        self.items_assam.append(id)
        coordsNez = ((L/2, L/6), (5*L/12, L/3), (7*L/12, L/3), (L/2, L/6))

        id = canvas.create_polygon(self.isometrie(coordsNez, L*x0, L*y0, rot90, False), fill="white")
        self.items_assam.append(id)

    def refresh_assam(self, chgt_dir = 0):
        if self.modele:
            x = self.modele.plateau.assam.x+1
            y = self.modele.plateau.assam.y+1
            dir = self.modele.plateau.assam.dir + chgt_dir
        else:
            x, y, dir = (4, 4, 2) 
            
        self.cree_assam(self.canvas, x, y, dir)
        print("Assam", x, y, "dir", dir)

    def active_assam(self, activer=True):
        self.etat = EtatGUI.AssamActif if activer else EtatGUI.Repos
        # print("Assam est actif", self.etat)

    def clic_assam_gauche(self, event):
        if self.etat == EtatGUI.AssamActif:
            self.dir_assam.clic_assam_gauche(event)
            self.refresh_assam(self.dir_assam.changement_direction())

    def clic_assam_droite(self, event):
        if self.etat == EtatGUI.AssamActif:
            self.dir_assam.clic_assam_droite(event)
            self.refresh_assam(self.dir_assam.changement_direction())

    def clic_assam(self, event):
        if self.etat == EtatGUI.AssamActif:
            # print("Assam avance")
            nb_cases = self.modele.avance_Assam(self.controleur.joueur_courant(), self.dir_assam.changement_direction())
            self.message("Assam avance de %d\n"%nb_cases)
            self.refresh_assam()
            self.dir_assam.__init__(0)
            self.etat = EtatGUI.PoseTapis1
            self.les_coups_possibles = self.modele.plateau.coups_possibles()
            self.les_cases_possibles = self.cases_possibles()
            # print(self.cases_possibles)
            self.message("Choisir case du tapis en commençant à côté d'Assam %s\n" % self.les_cases_possibles)
            self.montre_cases_possibles()

    def montre_cases_possibles(self):
        self.id_cases_possibles = []
        if self.etat == EtatGUI.PoseTapis1:
            for coup in self.les_coups_possibles:
                # dessiner un rectangle à cheval sur les 2 cases du coup
                d = 0.25
                if coup[0][1] == coup[1][1]: # orientation ← ou →
                    #on donne de la hauteur
                    d01 = -d/2; d11 = d/2
                    if coup[0][0] > coup[1][0]: 	# orientation ←
                        d00 = -d; d10 = d
                    else: 					# orientation →
                        d00 = d; d10 = -d
                else: 				# orientation ↓ ou ↑
                    # on donne de la largeur
                    d00 = -d/2; d10 = d/2
                    if coup[0][1] > coup[1][1]: 	# orientation ↑
                        d01 = -d; d11 = d
                    else: 					#orientation ↓
                        d01 = d; d11 = -d
                bbox = (L*(coup[0][0]+1.5+d00), L*(coup[0][1]+1.5+d01), L*(coup[1][0]+1.5+d10), L*(coup[1][1]+1.5+d11))
                id = self.canvas.create_rectangle(bbox, fill="white", outline="black")
                self.id_cases_possibles.append(id)
        for c in self.les_cases_possibles:
            id = self.canvas.create_text((1.5+c[0])*L, (1.5+c[1])*L, text="?", fill="white", font="helvetica 20 bold")
            self.id_cases_possibles.append(id)
            self.canvas.tag_bind(id, "<Button-1>", self.clic1)

    def cache_cases_possibles(self):
        for id in self.id_cases_possibles:
            self.canvas.delete(id)

    def clignote_cases_possibles(self):
        for id in self.id_cases_possibles:
            self.canvas.itemconfig(id, fill="magenta")
        self.after(50, self.gnotecli_cases_possibles)

    def gnotecli_cases_possibles(self):
        for id in self.id_cases_possibles:
            self.canvas.itemconfig(id, fill="white")

    def refresh_tapis(self):
        for id in self.items_tapis:
            self.canvas.delete(id)
        for coup in self.modele._coups:
            self.affiche_tapis(self.canvas, coup.coords, self.couleurs[coup.tapis.couleur()])

    def refresh_score(self):
        for i, v in enumerate(self.modele.dirhams): 
            self.dirhams[i].set(v)
        for i, v in enumerate(self.modele.nb_tapis_exposes()): 
            self.nb_tapis[i].set(v)
        for i, v in enumerate(self.modele.points()): 
            self.totaux[i].set(v)

    def refresh(self):
        self.refresh_tapis()
        self.refresh_assam()
        self.refresh_score()

    @staticmethod
    def flat(l):
        """ aplatit la liste de paires """
        res = []
        for cc in l:
            for c in cc:
                res.append(c)
        return res

    def cases_possibles(self):
        """les cases possibles pour poser le tapis"""
        cp = []
        if self.etat == EtatGUI.PoseTapis1:
            cp2 = self.flat(self.les_coups_possibles)
            # print("Cases posibles",self.les_coups_possibles, "\n→", cp2)
            x, y = self.modele.plateau.assam.x, self.modele.plateau.assam.y
            deplacement_case4 = ((0, -1), (1, 0), (0, 1), (-1, 0))
            for dx, dy in deplacement_case4:
                c = x+dx, y+dy
                if c in cp2: cp.append(c)
        elif self.etat == EtatGUI.PoseTapis2:
            for c1, c2 in self.les_coups_possibles:
                if c1 == self.coords1_tapis:
                    cp.append(c2)
                if c2 == self.coords1_tapis:
                    cp.append(c1)
        # print("Cases possibles ", cp)
        return cp

    @staticmethod
    def case(event):
        "Donne le couple de coordonnées de la case en fonction de l'evt clic"
        return (int(event.x/L)-1, int(event.y/L)-1) 

    def clic1(self, event):
        if self.etat == EtatGUI.PoseTapis1 or self.etat == EtatGUI.PoseTapis2:
            case = self.case(event)
            # est-ce possible ?
            if not case in self.les_cases_possibles:
                print("Buzz", case, self.les_coups_possibles)
                self.clignote_cases_possibles()
                return
            self.cache_cases_possibles()
            if self.etat == EtatGUI.PoseTapis1:
                self.coords1_tapis = case
                self.etat = EtatGUI.PoseTapis2
                self.les_cases_possibles = self.cases_possibles()
                self.message("Choisir la 2e case du tapis %s\n"%self.les_cases_possibles)
                self.montre_cases_possibles()
            else: # self.etat == EtatGUI.PoseTapis2:
                print("Pose tapis", self.coords1_tapis, case)
                self.modele.pose_tapis((self.coords1_tapis, case), self.controleur.num_joueur_courant())
                self.refresh_tapis()
                self.etat = EtatGUI.Repos
                self.controleur.fin_coup()

    def undo(self):
        self.modele.undo()
        self.controleur.undo()

class DirectionAssam(object):
    "Gestion des changements de direction d'Assam"
    def __init__(self, direction):
        self.direction = direction
        self.nbGauche = self.nbDroite = 0
        print ("Direction Assam : ", self.direction)

    def clic_assam_gauche(self, event):
        if self.nbGauche - self.nbDroite < 1:
            self.nbGauche += 1
            print("Assam tourne à gauche")
            self.direction -= 1
            self.direction %= 4
        else:
            print("Assam ne peut pas tourner à gauche")
        print(self.changement_direction())

    def clic_assam_droite(self, event):
        if self.nbDroite - self.nbGauche < 1:
            self.nbDroite += 1
            print("Assam tourne à droite")   
            self.direction += 1
            self.direction %= 4
        else:
            print("Assam ne peut pas tourner à droite")
        print(self.changement_direction())

    def changement_direction(self):
        return self.nbDroite - self.nbGauche 

class JoueurGUI(JoueurMarrakech):

    pass

class ControleurPartie(object):
    """Contrôleur pour Interface graphique de Marrakech"""

    def __init__(self, gui, modele, joueurs):
        self.gui = gui
        self.modele = modele
        self.joueurs = joueurs

    def run(self):
        self.nb_tours = len(self.modele.tapis[0])
        self.num_tour = 0
        self.gui.nb_tours_var.set("Tour %d"%(1+self.num_tour)) 
        self.num_joueur = 0
        self.jouer_un_coup()

    def undo(self):
        self.num_joueur -= 1
        if self.num_joueur < 0: 
            self.num_joueur = len(self.joueurs)-1
            self.num_tour -= 1
            self.gui.nb_tours_var.set("Tour %d"%(1+self.num_tour)) 
        self.gui.refresh()
        self.jouer_un_coup()

    def fin_coup(self):
        #self.gui.bouton_undo.config(state="active")
        self.gui.refresh()
        self.num_joueur += 1
        if self.num_joueur >= len(self.joueurs):
            self.num_tour += 1
            self.num_joueur = 0
            m = "\n                     Tour %s\n" % self.num_tour
            self.gui.message(m)
            print(m)
        if self.num_tour < self.nb_tours:
            self.gui.nb_tours_var.set("Tour %d"%(1+self.num_tour)) 
            self.gui.label_joueur_courant.config(bg=self.gui.couleurs[self.num_joueur])
            self.gui.after(1000, self.jouer_un_coup)
        else:
            self.gui.message("Partie terminée")
            print(self.modele)

    def jouer_un_coup(self):
        print("jouer_un_coup", self.num_joueur)
        j = self.joueur_courant()
        if isinstance(j, JoueurGUI):
            self.gui.message("Cliquer sur les épaules d'Assam pour le faire tourner puis\nsur son chapeau pour le faire avancer\n")
            self.gui.active_assam(True)
        else:
            self.modele.avance_Assam(j, j.changer_direction())
            self.gui.refresh()
            # afin de profiter du refresh on fait la fin après 100ms
            self.gui.after(500, self.jouer_un_coup_fin)

    def jouer_un_coup_fin(self):
        j = self.joueur_courant()
        self.modele.pose_tapis(j.ou_poser_tapis(self.modele.plateau.coups_possibles()), self.num_joueur)
        self.fin_coup()

    def num_joueur_courant(self):
        return self.num_joueur

    def joueur_courant(self):
        return self.joueurs[self.num_joueur]


if __name__ == "__main__":

    import sys
    if len(sys.argv) == 1:
        pass
    elif len(sys.argv) == 3:
        if sys.argv[1] == "-t":
            Plateau.set_taille_plateau(int(sys.argv[2]))
    else:
        sys.stderr.write("Usage : python3 MarrakechGUI.py [-t <taille>]]\n")
        sys.exit(-1)    

    root = tk.Tk()
    app = MarrakechGUI(master=root)
    root.mainloop()


