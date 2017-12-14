# ModeleMarrakech.py

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

############################
# Jeu de Marrakech avec dé : chaque joueur lance un dé pour déplacer Assan. Bref, ce n'est pas vraiment lui qui joue mais le moteur de jeu.
# On est dans un jeu où le "tour d'un joueur" est en fait composé de trois actions de jeu successives :
# 1) le joueur choisit la direction d'Assan; puis,
# 2) le moteur de jeu (noeud chance) choisit la distance parcourue par Assan; puis,
# 3) le joueur pose un tapis.

import random
from UnionFind import *

debug = True


class JoueurMarrakech(object):

    numero = 0

    def __init__(self, modele):
        self.modele = modele
        self.numero = JoueurMarrakech.numero
        JoueurMarrakech.numero += 1

    def changer_direction(self):
        """ renvoie -1, 0 ou +1 pour tourner à gauche, aller tout droit ou tourner à gauche"""
        pass

    def ou_poser_tapis(self, coups_possibles):
        """ renvoie un élément de coups_possibles """
        pass

class ModeleMarrakech(object):
    """Le modèle du jeu Marrakech
    
    Attributs :
    plateau : le plateau
    nb_joueurs : le nombre de joueurs
    tapis      : liste indexée par le numéro du joueur contenant à la position de ce dernier la liste de ces tapis qui ne sont pas sur le plateau (pas encore joués)
    dirhams    : liste indexée par le numéro du joueur contenant à la position de ce dernier le nombre des dirhams qu'il possède à ce moment du jeu
    _coups     : liste des coups joués (historique)
    coup_courant : coup en construction (puisque un tour de jeu d'un joeur se décompose en plusieurs micro-actions, on ne met dans l'historique que des coups complets)
    _coup_supprimes : pour faire un redo (futur qu'on pourrait rejouer)

    """
    
    def __init__(self, nb_joueurs):
        "Initialise les tapis, le plateau, … "
        self.plateau = Plateau()
        assert(2 <= nb_joueurs and nb_joueurs <= 4)
        self.nb_joueurs = nb_joueurs
        # le plateau est un entier impair au moins égal à 3 (pour que les coins fonctionnent) voir classe plateau
        t = Plateau.taille_plateau()
        # le nombre de tapis et de dirhams suit les règles pour la taille de plateau standard
        if (t == 7) :
            nb_dirhams_par_joueur = 30
            if (self.nb_joueurs == 4):
                nb_tapis_par_joueur = 12
            elif (self.nb_joueurs == 3):
                nb_tapis_par_joueur = 15
        # sinon on a choisit de prendre l'aire du plateau divisé par le nombre de joueurs
        # (en gros à la fin de la partie l'épaisseur moyenne par case doit être 2 tapis à peu près comme dans les règles classiques)
        # et un nombre de dirhams égal à l'aire optimale des tapis d'un joueur (tapis fois 2)
        else :
            nb_tapis_par_joueur = int(t*t/nb_joueurs)
            nb_dirhams_par_joueur = 2*nb_tapis_par_joueur
        # initialisation des tapis
        self.tapis = []
        for i in range(nb_joueurs):
            l = []
            self.tapis.append(l)
            for t in range(nb_tapis_par_joueur):
                l.append(Tapis(i))
        # initialisation des dirhams
        self.dirhams = []
        for i in range(nb_joueurs):
            self.dirhams.append(nb_dirhams_par_joueur)

        # Pour le undo
        # La liste de tous les coups joués (note : permet de stocker une partie)
        self._coups = []
        ### c'est moche. Pourquoi juste pas none avec undo qui ne fait rien si _coups est vide et/ou coup_courant est vide?
        self.coup_courant = Coup((0, 0, 0), self.plateau.assam.clone())
        
        # La liste des coups que l'on peut rejouer
        # cette liste est remise à vide si un nouveau coup est joué
        self._coups_supprimes = [] 

    def undo(self):
        "Anulle le dernier coup joué"
        coup = self._coups.pop()
        self._coups_supprimes.append(coup)
        # vraiment défaire
        # 0/ remettre Assam à sa place
        self.plateau.assam.replace(coup.assam)
        # 1/ rendre l'argent
        self.paye(coup.paiement[1], coup.paiement[0], coup.paiement[2])
        # 2/ enlever le tapis et le remettre sur la pile de l'utilisateur
        self.plateau.depose_tapis(coup.coords, coup.tapis)
        self.tapis[coup.tapis.couleur()].append(coup.tapis)
        # 3/ rafraîchir le plateau
        self.plateau.refresh(self._coups)

    def redo_possible():
        return bool(self._coups_supprimes)

    def redo(self):
        "Refait le dernier coup annulé s'il existe"
        raise NotImplementedError

    def pose_tapis(self, coords, num_joueur): 
        "enfile coup dans la liste coups, met à jour le plateau"
        self.coup_courant.set_tapis(self.tapis[num_joueur].pop(), coords)
        self._coups.append(self.coup_courant)
        if debug: print(self.coup_courant)
        self.plateau.pose_tapis(self.coup_courant.coords, self.coup_courant.tapis)
        self.plateau.calcul_region()

    def avance_Assam(self, joueur, dir, nb_cases=0):
        """ change_dir vaut -1, 0, +1 pour à gauche, tout droit ou à droite
        """
        self._coups_supprimes = [] # plus de redo possible
        assam_clone = self.plateau.assam.clone()
        if nb_cases == 0: 
            # On lance le dé spécial qui n'est pas numéroté de 1 à 6. 
            # Choice permet simplement de ne pas donner
            # la même probabilité à chaque nombre
            # On limite à au plus la largeur du plateau pour ne faire qu'un débordement du plateau maximum pour ne pas trouvler les humains qui essayent de jouer ou de regarder
            nb_cases = min(Plateau.TAILLEPLATEAU, random.choice([1,2,2,3,3,4]))
        print("Assam %s et avance de %d" % (("tourne à gauche", "va tout droit", "tourne à droite")[dir+1], nb_cases))
        self.plateau.avance_Assam(dir, nb_cases)
        donneur = joueur.numero
        receveur = self.plateau.couleur_assam()
        montant_a_payer = self.plateau.taille_region_assam() if donneur != receveur else 0
        self.coup_courant = Coup((donneur, receveur, montant_a_payer), assam_clone)
        self.paye(donneur, receveur, montant_a_payer)
        return nb_cases

    def paye(self, donneur, receveur, dirhams):
        if dirhams != 0:
            print("Joueur %s paye à %d : %d Dirhams"%(donneur, receveur, dirhams))
            if self.dirhams[donneur] < dirhams:
                print("Joueur", donneur, "insolvable")
                self.dirhams[receveur] += self.dirhams[donneur]
                self.dirhams[donneur] = 0
            else:
                self.dirhams[receveur] += dirhams
                self.dirhams[donneur] -= dirhams

    def coups_possibles(self):
        "demande au plateau de calculer tous les coups possibles, retourne une liste de Coups avec un tapis égal à None"
        return self.plateau.coups_possibles()

    def nb_tapis_exposes(self):
        return self.plateau.nb_tapis_exposes(self.nb_joueurs)

    def points(self):
        points = self.nb_tapis_exposes()
        for i in range(self.nb_joueurs): points[i] += self.dirhams[i]
        return points
        
    def __str__(self):
        ret = self.plateau.__str__()
        ret += "\n\nJoueurs "
        for i in range(self.nb_joueurs): ret += "\033[%dm %2d \033[0m"%(i+41, i)
        ret += "\ndirhams "
        for i in range(self.nb_joueurs): ret += "%4d"%self.dirhams[i]
        ret += "\ntapis   "
        nb_tapis_exposes = self.plateau.nb_tapis_exposes(self.nb_joueurs)
        for i in range(self.nb_joueurs): ret += "%4d"%nb_tapis_exposes[i]
        ret += "\n\ntotal   "
        points = self.points()
        for i in range(self.nb_joueurs): ret += "%4d"%points[i]
        return ret

    def __eq__(self, other):
        """Pas clair qu'il faille le mettre, il y a un comparateur par défaut?
        To check : doit-on définir un comparateur récursivement pour les objets apparaissant dans le modèle?"""
        return self.__dict__ == other.__dict__

class Tapis(object):
    """
    Permet simplement de savoir si c'est le même tapis qui est sur 2 cases adjacentes
    couleur varie de 0 à 3
    """
    def __init__(self, couleur):
        self._couleur = couleur

    def couleur(self):
        return self._couleur
        
    def __str__(self):
        return "%d"%self._couleur

class Coup(object):
    """ Le coup joué par un joueur 
    Attributs:
        coords: un tuple contenant les coordonnées des cases occupées par le tapis ex. : ((1,1),(2,1))
        tapis: le tapis concerné
        paiement: un tuple (joueur_payeur, joueur_payé, argent)
        assam: un clone d'Assam
    """
    def __init__(self, paiement, assam, coords=None, tapis=None):
        self.paiement = paiement
        self.assam = assam
        self.coords = coords
        self.tapis = tapis

    def set_tapis(self, tapis, coords):
        self.tapis = tapis
        self.coords = coords

    def __str__(self):
        return "Coup (%s) %s %s"%(self.coords, self.tapis, self.assam)

class Case(object):
    """Une case du Plateau.
    Attributs :
        tapis : le tapis qui la recouvre
        taille_region : la taille de la région de couleur uniforme à laquelle elle appartient
        etiquette_region : pour l'étiquetage des régions
        epaisseur : le nombre de tapis empilés (a priori pas besoin de cet attribut sauf si on veut faire des dessins en 3D...)
    """
    def __init__(self):
        self.tapis = None
        self.epaisseur = 0
        self.taille_region = 0
        self.etiquette_region = Plateau.TAILLEPLATEAU*Plateau.TAILLEPLATEAU # supérieur au nombre possible de régions (équivalent à +∞)
        # ?    self.coords = coords ### pas de coordonnées. C'est le plateau qui connaît les cases

    def couleur(self):
        if self.tapis == None:
            return None
        return self.tapis.couleur()

class Plateau(object):
    """ Le plateau est un tableau à 2 dimensions de Cases réalisé en Python par une liste de listes
    Il est mis à jour après chaque coup joué
    Il est reconstruit complètement à chaque undo car il ne connaît pas l'historique de chaque case
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
        for l in range(Plateau.TAILLEPLATEAU):
            ligne=[]
            for c in range(Plateau.TAILLEPLATEAU):
                ligne.append(Case())
            self.plateau.append(ligne)
        self._taille_region = []
    
    def pose_tapis(self, coords, tapis):
        # print("Pose tapis ", tapis._couleur, coords.__str__())
        self.plateau[coords[0][0]][coords[0][1]].tapis = tapis
        self.plateau[coords[1][0]][coords[1][1]].tapis = tapis
        self.plateau[coords[0][0]][coords[0][1]].epaisseur += 1
        self.plateau[coords[1][0]][coords[1][1]].epaisseur += 1

    def depose_tapis(self, coords, tapis):
        assert(self.plateau[coords[0][0]][coords[0][1]].tapis is tapis)
        assert(self.plateau[coords[1][0]][coords[1][1]].tapis is tapis)

        # est-ce nécessaire vu que l'on va faire un refresh complet du plateau ???
        self.plateau[coords[0][0]][coords[0][1]].tapis = None
        self.plateau[coords[1][0]][coords[1][1]].tapis = None
        self.plateau[coords[0][0]][coords[0][1]].epaisseur -= 1
        self.plateau[coords[1][0]][coords[1][1]].epaisseur -= 1

    def epaisseur(self, x, y):
        return self.plateau[x][y].epaisseur

    def _cases_voisines(self, x, y):
        "Génère les couples (case_voisine_valide, direction) pour la case (x, y)"
        deplacement_case4 = ((0, -1), (1, 0), (0, 1), (-1, 0))
        for d in range(4):
            c = self.coords_voisines((x, y), deplacement_case4[d])
            if self.coords_valides(c):
                yield self.plateau[c[0]][c[1]], d

    def _etiquettes_voisines(self, x, y, t):
        "Retourne (liste des étiquettes voisines, valeur mini) pour les voisins de même couleur que le tapis t"
        mini = Plateau.TAILLEPLATEAU*Plateau.TAILLEPLATEAU # > nombre max de régions
        etiquettes = []
        for c, d in self._cases_voisines(x, y):
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
        for y in range(Plateau.TAILLEPLATEAU):
            for x in range(Plateau.TAILLEPLATEAU):
                self.plateau[x][y].etiquette_region = Plateau.TAILLEPLATEAU*Plateau.TAILLEPLATEAU
       # 1re passe
        etiquette_region = 0 
        for y in range(Plateau.TAILLEPLATEAU):
            for x in range(Plateau.TAILLEPLATEAU):
                c = self.plateau[x][y]
                t = c.tapis
                if t != None:
                    etiquettes, mini = self._etiquettes_voisines(x, y, t)
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
        for y in range(Plateau.TAILLEPLATEAU):
            for x in range(Plateau.TAILLEPLATEAU):
                c = self.plateau[x][y]
                nelle_etiquette = union_find[c.etiquette_region]
                c.etiquette_region = nelle_etiquette 
                if nelle_etiquette not in self._taille_region:
                    self._taille_region[nelle_etiquette] = 1
                else:
                    self._taille_region[nelle_etiquette] += 1
        # par convention le fond a une région de taille 0
        self._taille_region[Plateau.TAILLEPLATEAU*Plateau.TAILLEPLATEAU] = 0
        return 0

    def couleur_assam(self):
        t = self.plateau[self.assam.coords()[0]][self.assam.coords()[1]].tapis
        return None if t == None else t.couleur()

    def taille_region_assam(self):
        return self.taille_region(self.assam.coords()[0], self.assam.coords()[1])

    def taille_region(self, x, y):
        e = self.plateau[x][y].etiquette_region
        return self._taille_region[e] if e in self._taille_region else 0

    @staticmethod
    def coords_voisines(coords, deplacement):
        "Donne les coords de la case avec un delta deplacement"
        #Pour le fun : return tuple(map(lambda x, y: x+y, coords, deplacement))
        return ((coords[0]+deplacement[0], coords[1]+deplacement[1]))

    @staticmethod
    def coords_valides(coords):
        "Est-ce que les coords sont dans le plateua ?"
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
                c_tapis = self.plateau[c[0]][c[1]].tapis
                for depl in deplacement_voisine_case4[d]:
                    cc = self.coords_voisines(self.assam.coords(), depl)
                    if self.coords_valides(cc):
                        if c_tapis == None:
                            ret.append((c, cc))
                        else:
                            cc_tapis =  self.plateau[cc[0]][cc[1]].tapis
                            if (cc_tapis == None) or (not (c_tapis is cc_tapis)):
                                ret.append((c, cc))
        return ret

    # def avance_Assam_de_1(self, dir, assam=None):
    #     """Avance Assam d'une case dans la direction indiquée en tenant compte des renvois en bout de ligne/colonne
    #     Le code peut sûrement être factorisé et perdre en clarté (déjà qu'il est touffu !)
    #     """
    #     if assam is None: assam = self.assam
    #     assam.tourne(dir)
    #     if assam.dir == 0: # Nord
    #         assam.y -= 1 #distance 1
    #         if assam.y < 0:
    #             if assam.x == Plateau.TAILLEPLATEAU-1:
    #                 # on change de direction N → W
    #                 assam.dir = 3
    #                 # on recule à partir du bout
    #                 assam.x = Plateau.TAILLEPLATEAU + assam.y
    #                 # on est en première ligne
    #                 assam.y = 0
    #             else:
    #                 # on revient en arrière
    #                 assam.dir = 2
    #                 # -1 car le passage par l'extérieur ne compte pas de point
    #                 assam.y = -assam.y - 1
    #                 # on change de colonne en fonction de la parité de la colonne
    #                 if assam.x % 2 == 0:
    #                     assam.x += 1
    #                 else:
    #                     assam.x -= 1
    #     elif assam.dir == 1: # Est
    #         assam.x+= 1 #distance 1
    #         if assam.x >= Plateau.TAILLEPLATEAU:
    #             if assam.y == 0:
    #                 assam.dir = 2
    #                 assam.y = assam.x - Plateau.TAILLEPLATEAU
    #                 assam.x = Plateau.TAILLEPLATEAU-1
    #             else:
    #                 assam.dir = 3
    #                 assam.x = Plateau.TAILLEPLATEAU - (assam.x - Plateau.TAILLEPLATEAU) - 1
    #                 if assam.y % 2 == 0:
    #                     assam.y -= 1
    #                 else:
    #                     assam.y += 1
    #     elif assam.dir == 2: # Sud
    #         assam.y += 1 #distance 1
    #         if assam.y >= Plateau.TAILLEPLATEAU:
    #             if assam.x == 0:
    #                 assam.dir = 1
    #                 assam.x = assam.y - Plateau.TAILLEPLATEAU
    #                 assam.y = Plateau.TAILLEPLATEAU-1
    #             else:
    #                 assam.dir = 0
    #                 assam.y = Plateau.TAILLEPLATEAU - (assam.y - Plateau.TAILLEPLATEAU) - 1
    #                 if assam.x % 2 == 0:
    #                     assam.x -= 1
    #                 else:
    #                     assam.x += 1
    #     elif assam.dir == 3: # Ouest
    #         assam.x -= 1 #distance 1
    #         if assam.x < 0:
    #             if assam.y == Plateau.TAILLEPLATEAU-1:
    #                 assam.dir = 0
    #                 assam.y = Plateau.TAILLEPLATEAU + assam.x
    #                 assam.x = 0
    #             else:
    #                 assam.dir = 1
    #                 assam.x = -assam.x - 1
    #                 if assam.y % 2 == 0:
    #                     assam.y += 1
    #                 else:
    #                     assam.y -= 1
                        
    def avance_Assam(self, dir, nb_cases, assam=None):
        """Avance Assam en tenant compte du fait que le plateau est un pseudo torre 
        """
        assert(nb_cases >=0)
        if assam is None: assam = self.assam
        assam.tourne(dir)
        if assam.dir == 0: # Nord
            assam.y -= nb_cases
            if assam.y < 0:
                if assam.x == Plateau.TAILLEPLATEAU-1:
                    # on change de direction N → W
                    assam.dir = 3
                    # on recule à partir du bout
                    assam.x = Plateau.TAILLEPLATEAU + assam.y
                    # on est en première ligne
                    assam.y = 0
                else:
                    # on revient en arrière
                    assam.dir = 2
                    # -1 car le passage par l'extérieur ne compte pas de point
                    assam.y = -assam.y - 1
                    # on change de colonne en fonction de la parité de la colonne
                    if assam.x % 2 == 0:
                        assam.x += 1
                    else:
                        assam.x -= 1
        elif assam.dir == 1: # Est
            assam.x+= nb_cases
            if assam.x >= Plateau.TAILLEPLATEAU:
                if assam.y == 0:
                    assam.dir = 2
                    assam.y = assam.x - Plateau.TAILLEPLATEAU
                    assam.x = Plateau.TAILLEPLATEAU-1
                else:
                    assam.dir = 3
                    assam.x = Plateau.TAILLEPLATEAU - (assam.x - Plateau.TAILLEPLATEAU) - 1
                    if assam.y % 2 == 0:
                        assam.y -= 1
                    else:
                        assam.y += 1
        elif assam.dir == 2: # Sud
            assam.y += nb_cases
            if assam.y >= Plateau.TAILLEPLATEAU:
                if assam.x == 0:
                    assam.dir = 1
                    assam.x = assam.y - Plateau.TAILLEPLATEAU
                    assam.y = Plateau.TAILLEPLATEAU-1
                else:
                    assam.dir = 0
                    assam.y = Plateau.TAILLEPLATEAU - (assam.y - Plateau.TAILLEPLATEAU) - 1
                    if assam.x % 2 == 0:
                        assam.x -= 1
                    else:
                        assam.x += 1
        elif assam.dir == 3: # Ouest
            assam.x -= nb_cases
            if assam.x < 0:
                if assam.y == Plateau.TAILLEPLATEAU-1:
                    assam.dir = 0
                    assam.y = Plateau.TAILLEPLATEAU + assam.x
                    assam.x = 0
                else:
                    assam.dir = 1
                    assam.x = -assam.x - 1
                    if assam.y % 2 == 0:
                        assam.y += 1
                    else:
                        assam.y -= 1

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
        """ Repose tous les tapis suivant les coups """
        for coup in coups:
            self.pose_tapis(coup.coords, coup.tapis)
        self.calcul_region()

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
                t = self.plateau[x][y].tapis
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
                t = self.plateau[x][y].tapis
                t_ansi_color = 0 if t is None else 40+t.couleur()+1
                if t is None or x == 0 or not self.plateau[x-1][y].tapis is t:
                    ret += "│" 
                else:
                    ret += "\033[%dm \033[0m"%t_ansi_color
                #b = "%2d"%self.plateau[x][y].etiquette_region
                b = "%2d"%self.taille_region(x, y)
                ret += "%s\033[%dm%s%s\033[0m"%(a, t_ansi_color, aa, b)
                #ret += "│%c%s "% (a, " " if t is None else t.couleur())
            ret +=  "│ " + "┘┐"[y%2] + " %d"%y
            ret += eol + "   " + "│ "[y%2]
            if y < Plateau.TAILLEPLATEAU-1:
                ret += " ├"
                for x in range(Plateau.TAILLEPLATEAU):
                    t = self.plateau[x][y].tapis
                    if not t is None and t is self.plateau[x][y+1].tapis:
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
        return ret

class Assam(object):
    "Attributs : x, y les coordonnées, dir la direction 0 à 3 pour N, E, S, W"
    def __init__(self, x=-1, y=-1, dir = 2):
        if x < 0: x = int(Plateau.taille_plateau()/2)
        if y < 0: y=int(Plateau.taille_plateau()/2)
        self.x=x
        self.y=y
        self.dir=dir
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

if __name__ == "__main__":
    # un test tout simple du modèle
    random.seed(0) # pour avoir le même random à chaque fois
    import sys
    # 2 joueurs par défaut 4 au max
    nb_joueurs = 2 if len(sys.argv) < 2 else min(int(sys.argv[1]), 4)
    m = ModeleMarrakech(nb_joueurs)
    m.plateau.calcul_region()
    print(m.plateau)
    nb_tapis = len(m.tapis[0])
    joueurs =[]
    for i in range(nb_joueurs):
        joueurs.append(JoueurMarrakech(m))
    for i in range(nb_tapis*nb_joueurs):
        print("Coup ", i)
        #if i == 5: 
        debug = True
        m.avance_Assam(joueurs[-1+i%3], 0)
        print("Coups possibles : ",m.plateau.assam.coords())
        coups_possibles = m.plateau.coups_possibles()
        print(coups_possibles)
        m.pose_tapis(coups_possibles[random.randint(0, -1+len(coups_possibles))], i%nb_joueurs)
        m.plateau.calcul_region()
        print(m.plateau)

    for t in m.tapis:
        assert(len(t) == 0)


