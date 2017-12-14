#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ModeleMarrakechSansAlea.py

# Copyright Jacques Madelaine, (13/10/2017)
# jacques.madelaine@unicaen.fr
# Florent Madelaine, (1/12/2017)

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


############################
# Jeu de Marrakech sans dé : chaque joueur reçoit au moins autant de cartes de déplacements que de tapis et va les utilise à la place du dé du jeu classique.
# On est donc dans un jeu où le tour d'un joueur est en fait composé de trois actions de jeu successives par ce joueur :
# 1) le joueur choisit la direction d'Assan (comme dans le jeu normal); puis,
# 2) le joueur choisit la distance parcourue par Assan en sélectionnant une carte de déplacement; puis,
# 3) le joueur pose un tapis.

import random
from UnionFind import *

debug = True


class JoueurMarrakech(object):
    """Un joueur est représenté par son numéro.
    Il est recommandé de cloner profondèment le modèle avant de le passer en paramètre au joueur, en particulier si ce joueur est une IA, pour éviter toute pollution intempestive du vrai jeu par l'IA... aka de la triche.
    """
    numero = 0

    def __init__(self):
        self.numero = JoueurMarrakech.numero
        JoueurMarrakech.numero += 1

    def changer_direction(self, modele):
        """ renvoie -1, 0 ou +1 pour tourner à gauche, aller tout droit ou tourner à gauche"""
        pass

    def avancer(self, nb_cartes_deplacement, modele):
        """ renvoie un nombre (de cases)
        nb_cartes_deplacement est un tableau des cartes de déplacement disponibles avec à l'index i le nombre de cartes disponibles pour avancer de i+1 pas (babouches).
        Le joueur doit renvoyer un index i pour lequel nb_cartes_deplacements est strictement positif.
        """
        pass

    def ou_poser_tapis(self, coups_possibles, modele):
        """ renvoie un élément de coups_possibles """
        pass

class ModeleMarrakechSansAlea(object):
    """Le modèle du jeu Marrakech

    Attributs :
    plateau : le plateau
    nb_joueurs : le nombre de joueurs
    tapis      : liste indexée par le numéro du joueur contenant à la position de ce dernier la liste de ces tapis qui ne sont pas sur le plateau (pas encore joués)
    dirhams    : liste indexée par le numéro du joueur contenant à la position de ce dernier le nombre des dirhams qu'il possède à ce moment du jeu
    _coups     : liste des coups joués (historique)
    coup_courant : coup en construction (puisque un tour de jeu d'un joeur se décompose en plusieurs micro-actions, on ne met dans l'historique que des coups complets)
    _coup_supprimes : pour faire un redo (futur qu'on pourrait rejouer)
    _ coefs_deplacements : liste dont l'index (+1) corresponds au nombre de pas autorisés pour Assan, la valeur indiquant le nombre de face du dé donnant cette distance. (le dé a autant de faces que la somme des éléments de cette liste, par exemple [1, 2, 2, 1] pour les règles classiques avec un dé à 6 faces).

    Nouveau dans la version sans alea
    nb_cartes_deplacement : liste indexée par le numéro du joueur contenant à la position de ce dernier la liste des cartes de déplacement qu'il n'a pas encore jouées
                            Par exemple [1, 2, 2, 1] voudrait dire 1 carte de distance 1, 2 de distances 2, 2 de distance 3 et 1 de distance 4.
    """

    def __init__(self, nb_joueurs):
        "Initialise les tapis, le plateau, … "
        self.plateau = Plateau()
        assert(2 <= nb_joueurs and nb_joueurs <= 4)
        self.nb_joueurs = nb_joueurs
        # le plateau est un entier impair au moins égal à 3 (pour que les coins fonctionnent) voir classe plateau
        t = Plateau.taille_plateau()
        # le nombre de tapis et de dirhams suit les règles pour la taille de plateau standard
        if t == 7 and self.nb_joueurs in [3, 4] :
            self.nb_dirhams_par_joueur = 30
            if self.nb_joueurs == 4:
                self.nb_tapis_par_joueur = 12
            elif self.nb_joueurs == 3:
                self.nb_tapis_par_joueur = 15
        # sinon on a choisit de prendre l'aire du plateau divisé par le nombre de joueurs
        # (en gros à la fin de la partie l'épaisseur moyenne par case doit être 2 tapis à peu près comme dans les règles classiques)
        # et un nombre de dirhams égal à l'aire optimale des tapis d'un joueur (tapis fois 2)
        else :
            self.nb_tapis_par_joueur = int(t*t/self.nb_joueurs)
            self.nb_dirhams_par_joueur = 2*self.nb_tapis_par_joueur
        # initialisation des tapis
        self.tapis = []
        for i in range(self.nb_joueurs):
            l = []
            self.tapis.append(l)
            for t in range(self.nb_tapis_par_joueur):
                l.append(Tapis(i))
        # initialisation des dirhams
        self.dirhams = []
        for i in range(self.nb_joueurs):
            self.dirhams.append(self.nb_dirhams_par_joueur)
        # On calcule la distance maximale en fonction de la taille du plateau de sorte qu'on puisse faire au plus 1 seul retour
        # contre le bord. Les tailles t de plateau sont toujours impaires, on prend donc comme distance max la partie entière supérieure de t/2
        # Pour les probabilités, on augmente les coefs de 1 jusqu'à la moitié de cette distance max.
        # En gros on veut : pour t=3 [1, 1}, pour t=5 [1, 2, 1], pour t=7 [1, 2, 2, 1], pour t=9 [1, 2, 3, 2, 1] etc
        t = Plateau.taille_plateau() # à cause de la boucle avec t au dessus.
        distance_max=int(t/2)+1
        self.coefs_deplacements = list(range(1, int(distance_max/2)+1))
        coefs_fin=self.coefs_deplacements[:] # on fait une copie (avec [:]) inversée du début
        coefs_fin.reverse()
        if (distance_max%2==1) :
            self.coefs_deplacements.append(self.coefs_deplacements[-1]+1)
        self.coefs_deplacements.extend(coefs_fin)

        # IMPORTANT.
        # différence avec modèle classique ici pour la version sans aléa.
        # chaque joueur reçoit des cartes de déplacement
        # nb_cartes_deplacement contient le nombre de cartes disponibles pour chaque joueur et chaque distance
        repeats=int(self.nb_tapis_par_joueur/sum(self.coefs_deplacements))+1
        self.modele_nb_cartes_deplacement = [i*repeats for i in self.coefs_deplacements]
        # mode simplifié : on ne peut pas choisir la distance (pratique pour débug / proto rapide d'IA).
        #if debug: self.modele_nb_cartes_deplacement=[self.nb_tapis_par_joueur]
        #
        self.nb_cartes_deplacement = []
        for i in range(nb_joueurs):
            self.nb_cartes_deplacement.append(self.modele_nb_cartes_deplacement[:])
        #print(self.nb_cartes_deplacement)

        # La liste de tous les coups joués
        self._coups = []

        ### obsolète
        # self.coup_courant = Coup((0, 0, 0), self.plateau.assam.clone(), 0)

        # La liste des coups que l'on peut rejouer (au sens classique d'un do/undo dans une interface par exemple).
        # cette liste est remise à vide si un nouveau coup est joué
        self._coups_supprimes = []

    def undo(self, history=False):
        """Annule la dernière action jouée (3 undo à faire pour le tour entier d'un joueur).
        history fait de facto référence à l'anti-histoire, i.e. la pile d'action à rejouer dans le cadre du redo.
        Typiquement une interface appelle avec l'option history=True alors qu'une IA va utiliser False"""
        try :
            coup = self._coups.pop()
        except IndexError as e:
            print("Attention, pas de coups à défaire :"+ str(e))
            raise e
        if history :
            self._coups_supprimes.append(coup)
        else :
            self._coups_supprimes = []
        coup.undo(self)#appel du undo spécifique en fonction du type de coup

    def _undoChangeDir(self, coup):
        """Redirige Assam en place (direction sens opposée à l'original)"""
        self.plateau.assam.tourne(-coup.dir)


    def _undoAvanceAssam(self, coup):
        """Remet Assam en place (demi tour, mouvement, demi tour, rembourse, repre,d carte mouvement"""
        self.plateau.avance_Assam(2, coup.babouches) # demi-tour et avance de la même distance (i.e. recule)
        self.plateau.assam.tourne(2) # remet Assam dans le bon sens
        if coup.joueur_payé is not None:
            self.paye(coup.joueur_payé, coup.joueur, coup.dirhams)
        self.nb_cartes_deplacement[coup.joueur][coup.babouches-1]+=1

    def _undoPoseTapis(self, coup):
        # plateau.plateau un peu moche, je devrais appeller un truc de plateau qui fait tout ça
        assert(self.plateau.plateau[coup.coords[0][0]][coup.coords[0][1]].tasdetapis[-1] is coup.tapis)
        assert(self.plateau.plateau[coup.coords[1][0]][coup.coords[1][1]].tasdetapis[-1] is coup.tapis)
        # on enlève le tapis
        self.plateau.plateau[coup.coords[0][0]][coup.coords[0][1]].tasdetapis.pop()
        self.plateau.plateau[coup.coords[1][0]][coup.coords[1][1]].tasdetapis.pop()
        # on remet le tapis sur le tas du joueur
        self.tapis[coup.tapis.couleur()].append(coup.tapis)

    def redo(self):
        """Refait le dernier coup annulé s'il existe"""
        try :
            coup = self._coups_supprimes.pop()
        except IndexError as e:
            print("Attention, pas de coups à refaire :"+ str(e))
            raise e
        coup.redo(self)
        self._coups.append(coup)

    def _ChangeDir(self, coup):
        self.plateau.assam.tourne(coup.dir)

    def changeDir(self, joueurNum, dir):
        """ change_dir vaut -1, 0, +1 pour à gauche, tout droit ou à droite
        """
        self._coups_supprimes = [] # plus de redo possible
        coup = CoupChangeDir(joueurNum, dir)
        self._ChangeDir(coup)
        self._coups.append(coup)

    def _AvanceAssam(self, coup):
        """Note : sauf en cas de redo, on ne connaît pas la partie dette qu'on doit calculer."""
        self.plateau.avance_Assam(0, coup.babouches)#0 c'est la direction. Nota Bene : on devrait probablement changer l'API en enlevant ce paramètre
        if coup.joueur_payé is None :
            coup.joueur_payé = self.plateau.couleur_assam() # peut encore être None si pas de tapis
            if coup.joueur_payé is not None and coup.joueur != coup.joueur_payé:
                ### insolvable à gérer ici pour que le undo marche correctement (c'est l'argent de joueur qui paye qui permet de savoir si il est solvable)!
                coup.dirhams = min(self.plateau.taille_region_assam(),self.dirhams[coup.joueur])
                self.paye(coup.joueur, coup.joueur_payé, coup.dirhams)
            else :
                coup.dirhams = 0
        self.nb_cartes_deplacement[coup.joueur][coup.babouches-1]-=1

    def avanceAssam(self, joueurNum, babouches):
        # Vérification des babouches devrait aller dans le controleur pour être cohérent?
        self._coups_supprimes = [] # plus de redo possible
        nb_cartes = self.nb_cartes_deplacement[joueurNum][babouches-1]
        if babouches <= 0:
            # on pourrait juste faire le raise...
            print ("Joueur %s veut tricher"%joueur)
            size = len(self.nb_cartes_deplacement[joueurNum])
            i = 0
            while nb_cartes <= 0 :
                if (i > size) :
                    print ("Joueur %s ne veut pas forcément tricher : il n'a plus de cartes"%joueur)
                    raise RuntimeError("Aucune carte de mouvement disponible")
                    break
                babouches = babouches%size + 1
                babouches = self.nb_cartes_deplacement[joueurNum][babouches-1]
                i += 1
        coup = CoupAvanceAssam(joueurNum, babouches)
        self._AvanceAssam(coup)
        self._coups.append(coup)

    def _PoseTapis(self, coup):
        self.plateau.pose_tapis(coup.coords, coup.tapis)

    def poseTapis(self, num_joueur, coords):
        """Légèrement unsafe : on ne vérifie pas si le tapis a le droit d'être posé .
        C'set au controleur de le faire
        """
        # On pourrait changer l'API et délèguer au controleur le soin de récupérer un numéro d'index valide de coups_possibles?
        # Demanderait à gérer un flag sur coups possible...
        self._coups_supprimes = [] # plus de redo possible
        coup = CoupPoseTapis(num_joueur, coords, self.tapis[num_joueur].pop())
        self._PoseTapis(coup)
        self._coups.append(coup)

    def paye(self, donneur, receveur, dirhams):
        """on vérifie quand même que le donneur est solvable (vérif normalement inutile maintenant puisqu'on le fait dans avanceAssan)"""
        if dirhams != 0:
            # print("Joueur", donneur, "paye à", receveur, ":", dirhams, "Dirhams")
            if self.dirhams[donneur] < dirhams:
                #print("Joueur", donneur, "insolvable")
                self.dirhams[receveur] += self.dirhams[donneur]
                self.dirhams[donneur] = 0
            else:
                self.dirhams[receveur] += dirhams
                self.dirhams[donneur] -= dirhams

    def coups_possibles(self):
        "demande au plateau de calculer tous les coups possibles, retourne une liste de Coups avec un tapis égal à None"
        return self.plateau.coups_possibles()

    def points(self):
        points = self.plateau.nb_tapis_exposes(self.nb_joueurs)
        for i in range(self.nb_joueurs): points[i] += self.dirhams[i]
        return points

    def __str__(self):
        ret = self.plateau.__str__()
        ret += "\n\nJoueurs     "
        for i in range(self.nb_joueurs): ret += "\033[%dm %2d \033[0m"%(i+41, i)
        # babouches restantes
        for c in range(len(self.nb_cartes_deplacement[0])):
            ret += "\n"+str(c+1)+" babouche"
            ret += "s" if c > 0 else " "
            for i in range(self.nb_joueurs): ret += "%4d"%self.nb_cartes_deplacement[i][c]
        ret += "\ndirhams    "
        for i in range(self.nb_joueurs): ret += "%4d"%self.dirhams[i]
        ret += "\ntapis      "
        nb_tapis_exposes = self.plateau.nb_tapis_exposes(self.nb_joueurs)
        for i in range(self.nb_joueurs): ret += "%4d"%nb_tapis_exposes[i]
        ret += "\n\ntotal      "
        points = self.points()
        for i in range(self.nb_joueurs): ret += "%4d"%points[i]
        return ret

    def pretty_historique(self):
        """retourne l'historique (string)"""
        ret="\n"
        for i,c in enumerate(self._coups):
            ret+=str(c)
            if i%3==2: # action d'un joueur = 3 micro coups
                ret+="\n"
        return(ret)

    def __eq__(self, other):
        """Pas clair qu'il faille le mettre, il y a un comparateur par défaut?
        To check : doit-on définir un comparateur récursivement pour les objets apparaissant dans le modèle?"""
        #return self.__dict__ == other.__dict__#Semble rentre différents même des choses semblables?
        return self.dirhams == other.dirhams ### seul le pognon pose problème dans le undo?


class Assam(object):
    "Attributs : x, y les coordonnées, dir la direction 0 à 3 pour N, E, S, W"
    def __init__(self, x=-1, y=-1, dir = 2):
        if x < 0: x = int(Plateau.taille_plateau()/2)
        if y < 0: y = int(Plateau.taille_plateau()/2)
        self.x = x
        self.y = y
        self.dir = dir
    def tourne(self, dir):
        "dir vaut -1, 0, +1 pour à gauche, tout droit ou à droite"
        self.dir += dir
        self.dir %= 4
    def est_a(self, x, y):
        return self.x == x and self.y == y
    def coords(self):
        return (self.x, self.y)
    def replace(self, assam):
        self.x = assam.x
        self.y = assam.y
        self.dir = assam.dir
    def str_dir(self):
        return  ( "↑", "→", "↓", "←")[self.dir]
    def __str__(self):
        return "Assam (%d, %d)%s" % (self.x, self.y, self.str_dir())
    def clone(self):
        return Assam(self.x, self.y, self.dir)

class Tapis(object):
    """
    Permet simplement de savoir si c'est le même tapis qui est sur 2 cases adjacentes
    couleur varie de 0 à 3
    """
    def __init__(self, couleur):
        self._couleur = couleur

    def couleur(self):
        return self._couleur

    #def __str__(self):
    #    return "%d"%self._couleur

class Coup(object):
    """Classe abstraite dont vont hériter les différents coups concrets du jeu : pratique pour Marrakech où un joueur fait plusieurs actions.
    Un Attribut : joueur (le *numéro* du joueur qui va faire l'action)
    Deux méthodes : undo et redo.
    Un truc bizare : refresh qui devrait aller habiter dans le monde des tapis?
    """
    def __init__(self, joueur=-1):
        self.joueur=joueur

    def undo(self, modele):
        pass
    def redo(self, modele):
        pass
    def refresh(self, modele):
        "redo partiel qui ne fait que poser les tapis"#c'est moche avancer et tourner assan n'a rien à voir avec les tapis.
        pass

class CoupChangeDir(Coup):
    """Action correspondant à un changement de direction de Assam.
    Attribut hérité : le joueur faisant le coup
    Attribut : la direction -1, 0 ou +1 pour gauche, tout droit ou à droite.
    """
    dirToStr = {-1 : "à gauche", 0 : "tout droit" , 1 : "à droite"}

    def __init__(self, joueur, dir):
        assert(dir in [-1, 0, 1])
        self.dir = dir
        super().__init__(joueur)

    def __str__(self):
        return "Joueur "+ str(self.joueur) + " fait aller Assam " + self.dirToStr[self.dir]+"."

    def undo(self, modele):
        modele._undoChangeDir(self)

    def redo(self, modele):
        modele._ChangeDir(self)

class CoupAvanceAssam(Coup):
    """action correspondant à une avancée de Assam.
    Attribut hérité : le joueur faisant le coup
    babouches : la distance parcourue par Assam
    joueur_payé : couleur du tapis sur lequel Assam tombe
    dirhams : somme payée par joueur (faisant le coup) à joueur_payé.
    """

    def __init__(self, joueur, babouches, joueur_payé=None, dirhams=0):
        assert(dirhams>=0)
        super().__init__(joueur)
        self.babouches = babouches
        self.joueur_payé = joueur_payé
        self.dirhams = dirhams

    def __str__(self):
        ret = "Joueur "+ str(self.joueur) + " avance Assam de " + str(self.babouches)
        if (self.dirhams > 0) :
            ret +=" et paye " + str(self.dirhams) + " à Joueur " + str(self.joueur_payé) +"."
        else :
            ret+="."
        return ret

    def undo(self, modele):
        modele._undoAvanceAssam(self)

    def redo(self, modele):
        modele._AvanceAssam(self)

class CoupPoseTapis(Coup):
    """action correspondant au dépôt d'un tapis sur le plateau.
    Attribut hérité : le joueur faisant le coup
    coords : un tuple contenant les coordonnées des cases occupées par le tapis ex. : ((1, 1), (2, 1))
    tapis : le tapis concerné
    """

    def __init__(self, joueur, coords, tapis):
        assert(tapis.couleur()==joueur)
        super().__init__(joueur)
        self.coords = coords
        self.tapis = tapis

    def __str__(self):
        return "Joueur "+ str(self.joueur) + " pose son tapis en " + str(self.coords) +"."

    def undo(self, modele):
        modele._undoPoseTapis(self)

    def redo(self, modele):
        modele._PoseTapis(self)

    def refresh(self, modele):
        modele.pose_tapis(self.coords, self.tapis)

class Case(object):
    """Une case du Plateau.
    Attributs :
        tasdetapis : les tapis qui la recouvre [ pile de tapis ]
        taille_region : la taille de la région de couleur uniforme à laquelle elle appartient
        num_region : pour l'étiquetage des régions
        ? coords : coordonnées ?
    """
    def __init__(self):
        self.tasdetapis = []
        self.taille_region = 0
        self.etiquette_region = Plateau.TAILLEPLATEAU*Plateau.TAILLEPLATEAU # supérieur au nombre possible de régions (équivalent à +∞) %%% utiliser infty???
        # ?    self.coords = coords

    def letapis(self):
        if self.tasdetapis:
            return self.tasdetapis[-1]
        return None

    def couleur(self):
        if self.tasdetapis:
            return self.tasdetapis[-1].couleur()
        return None


class Plateau(object):
    """ Le plateau est un tableau à 2 dimensions de Cases réalisé en Python par une liste de colonne.
    Les colonnes sont représentées par une liste de Case.
    Il est mis à jour après chaque coup joué.
    Attributs.
    assam :
    plateau qui est un tableau à 2 dimensions de Cases.

    """
    TAILLEPLATEAU = 7 # côté du plateau carré

    @staticmethod
    def set_taille_plateau(t):
        """taille plateau est un entier impair supérieur ou égal à 3"""
        if (t <= 3):
            Plateau.TAILLEPLATEAU = 3
        else :
            Plateau.TAILLEPLATEAU = t
            Plateau.taille_plateau()

    @staticmethod
    def taille_plateau():
        """Le premier appel normalise la taille à l'impair supérieur si nécessaire"""
        if Plateau.TAILLEPLATEAU % 2 == 0:
            Plateau.TAILLEPLATEAU += 1
        return Plateau.TAILLEPLATEAU

    def __init__(self):
        self.assam = Assam()
        self.plateau = []
        for col in range(Plateau.TAILLEPLATEAU):
            colonne=[]
            for c in range(Plateau.TAILLEPLATEAU):
                colonne.append(Case())
            self.plateau.append(colonne)

        for x, colonne in enumerate(self.plateau):
            for y, case in enumerate(colonne):
                case.voisines = self._calcul_cases_voisines(x, y)

        self._taille_region = []

    def pose_tapis(self, coords, tapis):
        self.plateau[coords[0][0]][coords[0][1]].tasdetapis.append(tapis)
        self.plateau[coords[1][0]][coords[1][1]].tasdetapis.append(tapis)
        # print("Pose tapis ", tapis.couleur(), coords, tapis, self.plateau[coords[1][0]][coords[1][1]].tasdetapis)

    def depose_tapis(self, coords, tapis):
        # assert(self.plateau[coords[0][0]][coords[0][1]].tasdetapis[-1] is tapis)
        # assert(self.plateau[coords[1][0]][coords[1][1]].tasdetapis[-1] is tapis)
        t1= self.plateau[coords[0][0]][coords[0][1]].tasdetapis.pop()
        t2 =self.plateau[coords[1][0]][coords[1][1]].tasdetapis.pop()
        assert(t1 == t2 and t1 == tapis)

    def _calcul_cases_voisines(self, x, y):
        "Génère les couples (case_voisine_valide, direction) pour la case (x, y)"
        deplacement_case4 = ((0, -1), (1, 0), (0, 1), (-1, 0))
        voisines = []
        for d in range(4):
            c = self.coords_voisines((x, y), deplacement_case4[d])
            if self.coords_valides(c):
                voisines.append((self.plateau[c[0]][c[1]], d))
        return voisines

    def _etiquettes_voisines(self, case, t):
        "Retourne (liste des étiquettes voisines, valeur mini) pour les voisins de même couleur que le tapis t"
        mini = Plateau.TAILLEPLATEAU*Plateau.TAILLEPLATEAU # > nombre max de régions
        etiquettes = []
        for c, d in case.voisines:
            #print(x, y, "↑→↓←"[d], c.etiquette_region, t.couleur(), c.couleur())
            e = c.etiquette_region
            if e != Plateau.TAILLEPLATEAU*Plateau.TAILLEPLATEAU and t.couleur() == c.couleur():
                etiquettes.append(e)
                if (mini > e): mini = e
        # print(x, y, etiquettes, " : ", mini)
        return (etiquettes, mini)

    def calcul_region(self):
        """etiquète les régions unicolores et calcule leurs tailles
        L'algo est décrit à https://en.wikipedia.org/wiki/Connected-component_labeling
        """
        union_find = UnionFind()
        for x, colonne in enumerate(self.plateau):
            for y, case in enumerate(colonne):
                case.etiquette_region = Plateau.TAILLEPLATEAU*Plateau.TAILLEPLATEAU
       # 1re passe
        etiquette_region = 0
        for x, colonne in enumerate(self.plateau):
            for y, c in enumerate(colonne):
                t = c.letapis()
                if t != None:
                    etiquettes, mini = self._etiquettes_voisines(c, t)
                    if len(etiquettes) == 0:
                        assert(mini == Plateau.TAILLEPLATEAU*Plateau.TAILLEPLATEAU)
                        # pas de voisines étiquetées
                        # on assigne une nouvelle étiquette région
                        c.etiquette_region = etiquette_region
                        # que l'on range dans la structure union_find
                        union_find[etiquette_region]
                        etiquette_region += 1
                    else:
                        # on affecte la plus petite étiquette voisine
                        c.etiquette_region = mini
                        # les étiquettes voisines sont équivalentes (i.e. même région)
                        union_find.union(etiquettes)
        ##if debug:
        ##    print(union_find.parents)
        ##    partition={}
        ##    for (k, v) in union_find.parents.items():
        ##        if v in partition:
        ##            partition[v].append(k)
        ##        else:
        ##            partition[v] = [k]
        ##    print("Partition étiquettes :", partition.values())
        # 2e passe et calcul taille région
        self._taille_region = {}
        for x, colonne in enumerate(self.plateau):
            for y, c in enumerate(colonne):
                nelle_etiquette = union_find[c.etiquette_region]
                c.etiquette_region = nelle_etiquette
                if nelle_etiquette not in self._taille_region:
                    self._taille_region[nelle_etiquette] = 1
                else:
                    self._taille_region[nelle_etiquette] += 1
        # par convention le fond a une région de taille 0
        self._taille_region[Plateau.TAILLEPLATEAU*Plateau.TAILLEPLATEAU] = 0

    def taille_region(self, x, y):
        e = self.plateau[x][y].etiquette_region
        return self._taille_region[e] if e in self._taille_region else 0

    def couleur_assam(self):
        return self.plateau[self.assam.coords()[0]][self.assam.coords()[1]].couleur()

    def taille_region_assam(self):
        return self.calcul_taille_region(self.plateau[self.assam.coords()[0]][self.assam.coords()[1]])

    def calcul_taille_region(self, case, init = True, p = 0):
        if case.couleur() is None:
            #pas de tapis, pas de région
            return 0
        if init: # marquer toutes les cases à False
            for colonne in self.plateau:
                for c in colonne:
                    c.marque = False
        case.marque = 1
        taille = 1
        for c, d in case.voisines:
            if c.marque:
                continue
            if c.couleur() == case.couleur():
                taille += self.calcul_taille_region(c, False, p+1)#à quoi sert p?
        return taille

    @staticmethod
    def coords_voisines(coords, deplacement):
        "Donne les coords de la case avec un delta deplacement"
        #Pour le fun : return tuple(map(lambda x, y: x+y, coords, deplacement))
        return ((coords[0]+deplacement[0], coords[1]+deplacement[1]))

    @staticmethod
    def coords_valides(coords):
        "Est-ce que les coords sont dans le plateau ?"
        return 0 <= coords[0] and coords[0] < Plateau.TAILLEPLATEAU and 0 <= coords[1] and coords[1] < Plateau.TAILLEPLATEAU

    def coups_possibles(self):
        "calcule tous les coups possibles, retourne une liste de Coups avec un tapis égal à None"
        ret = []

        deplacement_case4 = ((0, -1), (1, 0), (0, 1), (-1, 0))
        deplacement_voisine_case4 =(
            ((-1, -1), ( 0, -2), (+1, -1)),
            (( 1, -1), ( 2, 0), ( 1,  1)),
            (( 1, 1), ( 0,  2), (-1,  1)),
            ((-1, -1), (-2,  0), (-1,  1))
        )
        for d in range(4):
            c = self.coords_voisines(self.assam.coords(), deplacement_case4[d])
            if self.coords_valides(c):
                c_tapis = self.plateau[c[0]][c[1]].letapis()
                for depl in deplacement_voisine_case4[d]:
                    cc = self.coords_voisines(self.assam.coords(), depl)
                    if self.coords_valides(cc):
                        if c_tapis == None:
                            ret.append((c, cc))
                        else:
                            cc_tapis =  self.plateau[cc[0]][cc[1]].letapis()
                            if (cc_tapis == None) or (not (c_tapis is cc_tapis)):
                                ret.append((c, cc))
        return ret

    def avance_Assam(self, dir, nb_cases):
        """Avance Assam en connaissant les renvois en bout de ligne/colonne
        Le code peut sûrement être factorisé et perdre en clarté (déjà qu'il est touffu !)

        Nouveau : Assam change de direction puis il bouge.
        """
        self.assam.tourne(dir)
        if self.assam.dir == 0: # Nord
            self.assam.y -= nb_cases
            if self.assam.y < 0:
                if self.assam.x == Plateau.TAILLEPLATEAU-1:
                    # on change de direction N → W
                    self.assam.dir = 3
                    # on recule à partir du bout
                    self.assam.x = Plateau.TAILLEPLATEAU + self.assam.y
                    # on est en première ligne
                    self.assam.y = 0
                else:
                    # on revient en arrière
                    self.assam.dir = 2
                    # -1 car le passage par l'extérieur ne compte pas de point
                    self.assam.y = -self.assam.y - 1
                    # on change de colonne en fonction de la parité de la colonne
                    if self.assam.x % 2 == 0:
                        self.assam.x += 1
                    else:
                        self.assam.x -= 1
        elif self.assam.dir == 1: # Est
            self.assam.x+= nb_cases
            if self.assam.x >= Plateau.TAILLEPLATEAU:
                if self.assam.y == 0:
                    self.assam.dir = 2
                    self.assam.y = self.assam.x - Plateau.TAILLEPLATEAU
                    self.assam.x = Plateau.TAILLEPLATEAU-1
                else:
                    self.assam.dir = 3
                    self.assam.x = Plateau.TAILLEPLATEAU - (self.assam.x - Plateau.TAILLEPLATEAU) - 1
                    if self.assam.y % 2 == 0:
                        self.assam.y -= 1
                    else:
                        self.assam.y += 1
        elif self.assam.dir == 2: # Sud
            self.assam.y += nb_cases
            if self.assam.y >= Plateau.TAILLEPLATEAU:
                if self.assam.x == 0:
                    self.assam.dir = 1
                    self.assam.x = self.assam.y - Plateau.TAILLEPLATEAU
                    self.assam.y = Plateau.TAILLEPLATEAU-1
                else:
                    self.assam.dir = 0
                    self.assam.y = Plateau.TAILLEPLATEAU - (self.assam.y - Plateau.TAILLEPLATEAU) - 1
                    if self.assam.x % 2 == 0:
                        self.assam.x -= 1
                    else:
                        self.assam.x += 1
        elif self.assam.dir == 3: # Ouest
            self.assam.x -= nb_cases
            if self.assam.x < 0:
                if self.assam.y == Plateau.TAILLEPLATEAU-1:
                    self.assam.dir = 0
                    self.assam.y = Plateau.TAILLEPLATEAU + self.assam.x
                    self.assam.x = 0
                else:
                    self.assam.dir = 1
                    self.assam.x = -self.assam.x - 1
                    if self.assam.y % 2 == 0:
                        self.assam.y += 1
                    else:
                        self.assam.y -= 1

    def nb_tapis_exposes(self, nb_joueurs):
        """ Calcule le nombre de cases occupées par les tapis pour chaque joueur """
        nb_tapis_exposes = []
        for i in range(nb_joueurs):
            nb_tapis_exposes.append(0)
        for y in range(Plateau.TAILLEPLATEAU):
            for x in range(Plateau.TAILLEPLATEAU):
                 c = self.plateau[x][y].couleur()
                 if c != None: nb_tapis_exposes[c] += 1
        return nb_tapis_exposes

    def refresh(self, coups):
        """ Repose tous les tapis si il s'agit de dépôt de tapis. Non utilisé. """
        for coup in coups:
            coup.refresh(self)

    def __7bits_str__(self):
        "sortie en ascii art 7 bits"
        inter_ligne = "\n    "
        for y in range(Plateau.TAILLEPLATEAU):
            inter_ligne += "+---"
        inter_ligne += "+\n"
        ret = "   "
        for y in range(Plateau.TAILLEPLATEAU):
            ret += "%4d"%y
        ret += inter_ligne
        for y in range(Plateau.TAILLEPLATEAU):
            ret += " %d  "% y # 4 espaces en début de ligne
            for x in range(Plateau.TAILLEPLATEAU):
                a = " " if not self.assam.est_a(x, y) else self.assam.str_dir()
                t = self.plateau[x][y].letapis()
                tt = " " if t == None else t.__str__()
                ret += "|%c%s "% (a, tt)
            ret += "|"
            ret += inter_ligne
        return ret

    def __str__(self):
        "sortie en unicode art"
        # Les codes ANSI d'échappement https://en.wikipedia.org/wiki/ANSI_escape_code
        # permettent de changer la couleur du fond ESC[4?m
 	# soit 41, 42, 43, 44 pour respectivement Red, Green, Yellow, Blue
        eol = "\n    "
        ret = eol+"      "
        for c in range(0, Plateau.TAILLEPLATEAU): ret += "%2d  "%c
        ret += eol+"     "
        for c in range(0, int(Plateau.TAILLEPLATEAU/2+1)): ret += "  ┌───┐ "
        ret += eol+"     ┌───"
        for c in range(0, Plateau.TAILLEPLATEAU-1): ret += "┬───"
        ret += "┐ │  "
        for y in range(Plateau.TAILLEPLATEAU):
            renvoi = "┌└"[y%2]
            ret += eol+" %d %c "% (y, renvoi)
            for x in range(Plateau.TAILLEPLATEAU):
                if self.assam.est_a(x, y):
                    a = self.assam.str_dir()
                    aa = ""
                else:
                    a = ""
                    aa = " "
                t = self.plateau[x][y].letapis()
                t_ansi_color = 0 if t is None else 40+t.couleur()+1
                if t is None or x == 0 or not self.plateau[x-1][y].letapis() is t:
                    ret += "│"
                else:
                    ret += "\033[%dm \033[0m"%t_ansi_color
                b = "  " #if not Plateau.use_unionfind else "%2d"%self.taille_region(x, y)
                ret += "%s\033[%dm%s%s\033[0m"%(a, t_ansi_color, aa, b)
            ret +=  "│ " + "┘┐"[y%2] + " %d"%y
            ret += eol + "   " + "│ "[y%2]
            if y < Plateau.TAILLEPLATEAU-1:
                ret += " ├"
                for x in range(Plateau.TAILLEPLATEAU):
                    t = self.plateau[x][y].letapis()
                    if not t is None and t is self.plateau[x][y+1].letapis():
                        ret += "\033[%dm   \033[0m"%(40+t.couleur()+1)
                    else:
                        ret += "───"
                    if x < Plateau.TAILLEPLATEAU-1: ret += "┼"
                ret += "┤ " +  " │"[y%2]
                pass
        ret += " └───"
        for c in range(0, Plateau.TAILLEPLATEAU-1): ret += "┴───"
        ret += "┘"
        ret += eol+" "
        for c in range(0, int(Plateau.TAILLEPLATEAU/2+1)): ret += "  └───┘ "
        ret += eol+"      "
        for c in range(0, Plateau.TAILLEPLATEAU): ret += "%2d  "%c
        # if debug :
        #     ret+=str(self.assam)+"\n"
        return ret

if __name__ == "__main__":
    random.seed(0) # pour avoir le même random à chaque fois
    # import sys
    # # 2 joueurs par défaut 4 au max
    # nb_joueurs = 2 if len(sys.argv) < 2 else min(int(sys.argv[1]), 4)
    # m = ModeleMarrakech(nb_joueurs)
    # print(m.plateau)
    # nb_tapis = len(m.tapis[0])
    # #for i in range(6):
    # for i in range(nb_tapis*nb_joueurs):
    #     print("Coup %d"%i)
    #     #if i == 5:
    #     debug = True
    #     m.avance_Assam(-1+i%3)
    #     print("Coups possibles : "+m.plateau.assam.coords().__str__())
    #     coups_possibles = m.plateau.coups_possibles()
    #     print(coups_possibles)
    #     m.pose_tapis(coups_possibles[random.randint(0, -1+len(coups_possibles))], i%nb_joueurs)
    #     print(m.plateau)

    # for t in m.tapis:
    #     assert(len(t) == 0)
    Plateau.set_taille_plateau(3)
    m = ModeleMarrakechSansAlea(2)
    # for c in m.coups_possibles() :
    #     print(c)
    m.poseTapis(1,((2, 1), (2, 0)))
    print(m)
    print("*** historique *** ", m.pretty_historique())
    m.undo()

    print(m)
    print("*** historique *** ", m.pretty_historique())
    m.poseTapis(1,((2, 1), (2, 0)))
    print(m)
    print("*** historique *** ", m.pretty_historique())
    m.changeDir(0,-1)
    print(m)
    print("*** historique *** ", m.pretty_historique())
    m.avanceAssam(0,1)
    print(m)
    print("*** historique *** ", m.pretty_historique())
    m.undo()
    print(m)
    print("*** historique *** ", m.pretty_historique())
    m.undo()
    print(m)
    print("*** historique *** ", m.pretty_historique())
    m.changeDir(0,1)
    print(m)
    print("*** historique *** ", m.pretty_historique())
    m.avanceAssam(0,1)
    print(m)
    print("*** historique *** ", m.pretty_historique())
    m.undo()
    print(m)
    print("*** historique *** ", m.pretty_historique())
    m.undo()
    print(m)
    print("*** historique *** ", m.pretty_historique())
    #print(m.__dict__)
