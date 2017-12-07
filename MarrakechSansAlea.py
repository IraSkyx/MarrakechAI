#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# MarrakechSansAlea.py

# Copyright Jacques Madelaine, (13/10/2017)
# jacques.madelaine@unicaen.fr
# Florent Madelaine (changements mineurs controleur 4/12/2017)

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
from ModeleMarrakechSansAlea import *
import copy

debug = True

class InterfaceLDC(object):
    """Interface ligne de commande pour Marrakech (version sans alea)"""

    def __init__(self, modele, joueurs):
        self.modele = modele
        self.joueurs = joueurs

    def run(self):
        """Version avec controleur minimal : deepclone du modele pour une IA avec vérification que la pose du tapis est possible, pas de clone pour JoueurLDC auquel on délègue le travail de controle. Les autres vérifications sont faites dans le modele pour l'instant. C'est un peu moche. À terme il faudrait tout faire ici dans le controlleur, voir avoir une version bretelle et ceinture qui vérifie des 2 côtés.
        """
        # Au cas où la partie est commencée.
        # On suppose pour simplifier le code que tout le monde a joué le même nombre de coups.
        tour0= self.modele.nb_tapis_par_joueur - len(self.modele.tapis[0]) + 1
        tourfin = self.modele.nb_tapis_par_joueur
        for tour in range(tour0,tourfin+1):
            print("\n                     Tour", tour)
            for i, j in enumerate(joueurs):
                #if debug: print(j)
                modele = self.modele if j.__class__.__name__ == "JoueurLDC" else copy.deepcopy(self.modele)
                self.modele.changeDir(i,j.changer_direction(modele))
                modele = self.modele if j.__class__.__name__ == "JoueurLDC" else copy.deepcopy(self.modele)
                self.modele.avanceAssam(i, j.avancer(self.modele.nb_cartes_deplacement[j.numero],modele))
                modele = self.modele if j.__class__.__name__ == "JoueurLDC" else copy.deepcopy(self.modele)
                cp = self.modele.plateau.coups_possibles()
                c = j.ou_poser_tapis(cp, modele)
                swapc = (c[1], c[0])
                if (c in cp or swapc in cp) :    
                    self.modele.poseTapis(i, c)
                else :
                    raise ValueError("Erreur : ni " + str(c) + " ni " + str(swapc)+" dans " + str(cp) + ". IA " + str(j.__class__.__name__) + "(joueur "+ str(i) +") est-elle en train de tricher?")
                print(self.modele)
        scores=self.modele.points()
        for winner in [i for i, j in enumerate(scores) if j == max(scores)]:
            print("Joueur " + str(i) + " gagne avec " + str(scores[i]) + " points")

class JoueurLDC(JoueurMarrakech):
    """Pas besoin de cloner le jeu"""
    def __str__(self):
        return "\033[%dm %d \033[0m"%(self.numero+41, self.numero)

    def changer_direction(self, modele):
        print(modele.plateau)
        dict = { 'g' : -1, ' ' : 0, '': 0, 'd' : 1 }
        while True: 
            l = input("Joueur %s. Tourner à gauche, tout droit, à droite ? (g d) "%self)
            if l in dict:
                return dict[l]

    def avancer(self, nb_cartes_deplacement, modele):
        """ renvoie un nombre (de cases) légal"""
        mess = "Cartes de déplacements "
        nb_possibles = ""
        for i, nb in enumerate(nb_cartes_deplacement):
            mess += "%d babouches (reste %d) "%(i+1, nb)
            if nb > 0: nb_possibles += "%d "%(1+i)
        print(mess)
        while True:
            l = input("Joueur %s. Combien de cases avancer ? "%self)
            try:
                n = int(l)
            except ValueError:
                n = -1
            if 0 < n and n < 1+len(nb_cartes_deplacement) and nb_cartes_deplacement[n-1] > 0: break
            print("Joueur %s. Entrer un des nombres %s"%(self, nb_possibles))
        return n

    def ou_poser_tapis(self, coups_possibles, modele):
        print(modele.plateau)
        for n, c in enumerate(coups_possibles):
            print(n, " : ", c)
        
        while True:
            l = input("Joueur %s. Où poser le tapis ? "%self)
            try:
                n = int(l)
            except ValueError:
                n = -1
            if 0 <= n and n < len(coups_possibles): break
            #print("Joueur %s. Entrer un nombre compris entre 0 et %d"%(self, len(coups_possibles)-1))
        return coups_possibles[n]

class JoueurAuHasard(JoueurMarrakech):

    def __str__(self):
        return "\033[%dm %d \033[0m"%(self.numero+41, self.numero)

    def changer_direction(self,modele):
        print("\nJoueur aléatoire %s"%self)
        return random.randint(-1, 1)

    def avancer(self, nb_cartes_deplacement,modele):
        c = random.randrange(len(nb_cartes_deplacement))
        while True:
            if nb_cartes_deplacement[c] > 0:
                return c+1 # on avance d'une case de plus que l'index
            c = (c+1)%len(nb_cartes_deplacement)
            
    def ou_poser_tapis(self, coups_possibles,modele):
        #print(modele.plateau)
        return coups_possibles[random.randint(0, -1+len(coups_possibles))]

if __name__ == "__main__":
    random.seed(0) # pour avoir le même random à chaque fois
    import sys
    # 2 joueurs par défaut 4 au max
    argindex=1
    if len(sys.argv) >=2:
        if sys.argv[1] == "-h":
            sys.stderr.write("Usage : python3 "+ sys.argv[0] + " [-t <taille>] <nb joueurs total> [<nb joueurs humains>]\n")
            sys.exit(-1)
        if sys.argv[argindex] == "-t":
            Plateau.set_taille_plateau(int(sys.argv[argindex+1]))
            argindex += 2
    if len(sys.argv) > argindex:
        nb_joueurs_total = min(int(sys.argv[argindex]), 4)
        nb_joueurs_ldc = 0 if argindex+1 >= len(sys.argv) else min(int(sys.argv[argindex+1]), nb_joueurs_total)
    else:
        nb_joueurs_total = 2
        nb_joueurs_ldc = 0
    
    m = ModeleMarrakechSansAlea(nb_joueurs_total)
    joueurs = []
    #for i in range(nb_joueurs_ldc): joueurs.append(JoueurLDC())
    for i in range(nb_joueurs_ldc): joueurs.append(JoueurAuHasard())
    from MonIASimpletteSansAlea import *
    #for i in range(nb_joueurs_ldc, nb_joueurs_total): joueurs.append(JoueurAuHasard())
    for i in range(nb_joueurs_ldc, nb_joueurs_total): joueurs.append(MonIASimpletteSansAlea())

    #on joue quelques coups pour rendre l'arbre plus petit.
    for toursAuPif in range(1,2):
        for i, j in enumerate(joueurs):
            m.changeDir(i,random.randint(-1,1))# au pif
            m.avanceAssam(i,random.randint(1,2))# au pif
            m.poseTapis(i, random.choice((m.coups_possibles())))
    for c in m._coups:
        print(str(c))
    gui = InterfaceLDC(m, joueurs)
    gui.run()


