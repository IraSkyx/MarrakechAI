# Marrakech.py

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
from ModeleMarrakech import *

class InterfaceLDC(object):
    """Interface ligne de commande por Marrakech"""

    def __init__(self, modele, joueurs):
        self.modele = modele
        self.joueurs = joueurs

    def run(self):
        nb_tours = len(self.modele.tapis[0])
        for tour in range(nb_tours):
            print("\n                     Tour", tour)
            
            for i, j in enumerate(joueurs):
                non_confirme = True
                while non_confirme:
                    self.modele.avance_Assam(j, j.changer_direction())
                    self.modele.pose_tapis(j.ou_poser_tapis(self.modele.plateau.coups_possibles()), i)
                    print(self.modele)
                    l = input("Undo (oui/non)")
                    non_confirme = l == 'o' or l == "oui"
                    if non_confirme:
                        self.modele.undo()
                    
class JoueurLDC(JoueurMarrakech):

    def __str__(self):
        return "\033[%dm %d \033[0m"%(self.numero+41, self.numero)

    def changer_direction(self):
        print(self.modele.plateau)
        dict = { 'g' : -1, ' ' : 0, '': 0, 'd' : 1 }
        while True: 
            l = input("Joueur %s. Tourner à gauche, tout droit, à droite ? (g d) "%self)
            if l in dict:
                return dict[l]

    def ou_poser_tapis(self, coups_possibles):
        print(self.modele.plateau)
        for n, c in enumerate(coups_possibles):
            print(n, " : ", c)
        
        while True:
            l = input("Joueur %s. Où poser le tapis ? "%self)
            try:
                n = int(l)
            except ValueError:
                n = -1
            if 0 <= n and n < len(coups_possibles): break
            print("Joueur %s. Entrer un nombre compris entre 0 et %d"%(self, len(coups_possibles)-1))
        return coups_possibles[n]

class JoueurAuHasard(JoueurMarrakech):

    def __str__(self):
        return "\033[%dm %d \033[0m"%(self.numero+41, self.numero)

    def changer_direction(self):
        print("\nJoueur aléatoire %s"%self)
        return random.randint(-1, 1)

    def ou_poser_tapis(self, coups_possibles):
        print(self.modele.plateau)
        return coups_possibles[random.randint(0, -1+len(coups_possibles))]

if __name__ == "__main__":
    #random.seed(0) # pour avoir le même random à chaque fois
    import sys
    # 2 joueurs par défaut 4 au max
    #print(sys.argv)
    argindex = 1
    if len(sys.argv) >=2:
        if sys.argv[1] == "-h":
            sys.stderr.write("Usage : python3 Marrakech.py [-t <taille>] <nb joueurs total> [<nb joueurs humains>]\n")
            sys.exit(-1)
        if sys.argv[argindex] == "-t":
            Plateau.set_taille_plateau(int(sys.argv[argindex+1]))
            argindex = 3
    if len(sys.argv) > argindex:
        nb_joueurs_total = min(int(sys.argv[argindex]), 4)
        nb_joueurs_ldc = 0 if argindex+1 >= len(sys.argv) else min(int(sys.argv[argindex+1]), nb_joueurs_total)
    else:
        nb_joueurs_total = 2
        nb_joueurs_ldc = 0
    
    m = ModeleMarrakech(nb_joueurs_total)
    joueurs = []
    import MonIA
    for i in range(nb_joueurs_ldc): joueurs.append(MonIA.MonIA(m))
    for i in range(nb_joueurs_ldc, nb_joueurs_total): joueurs.append(JoueurLDC(m))
    gui = InterfaceLDC(m, joueurs)
    gui.run()


