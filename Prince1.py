#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# IAMarrakech.py

# Copyright Florent Madelaine, (1/12/2017)

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
import random

debug = False #True

class Prince1(JoueurMarrakech):

    def __init__(self):
        super().__init__()
        self.angle = None
        self.babouches = None
        self.coords = None
        self.evaluationPosition = None
        self.stat_noeuds = 0
        self.stat_feuilles = 0

    def __str__(self):
        return "\033[%dm %d \033[0m"%(self.numero+41, self.numero)

    def setCoup(self, angle=None, babouches=None, coords=None):
        self.angle = angle
        self.babouches = babouches
        self.coords = coords

    def stats(self):
        return "Stats : noeuds internes "+ str(self.stat_noeuds) + " feuilles "+ str(self.stat_feuilles)

    def changer_direction(self,modele):
        print("\nMon IA %s"%self)
        self.setCoup()
        self.stat_noeuds = self.stat_feuilles = 0
        self.evaluationPosition = self._maxSimplet(modele, True)
        print(self.stats())
        print("Choix : dir " + str(self.angle) +" babouches " + str(self.babouches) + " tapis " + str(self.coords))
        print("Evaluation : " + str(self.evaluationPosition))
        return self.angle

    def avancer(self, nb_cartes_deplacement, modele):
        return self.babouches

    def ou_poser_tapis(self, coups_possibles, modele):
        # On sait déjà quoi faire avec le modèle sans aléa
        return self.coords

    def _minSimplet(self, modele):

        numMin=(self.numero+1)%modele.nb_joueurs
        """Meilleur coup local pour Joueur"""
        if len(modele.tapis[-1]) == 0:
            return self._eval(modele)

        worst=float('Inf')

        for angle in [-1,0,1]:
            modele.changeDir(numMin, angle)
            self.stat_noeuds+=1
            babouchesPossibles=[b+1 for b, carte in enumerate(modele.nb_cartes_deplacement[numMin]) if carte > 0]
            for babouches in babouchesPossibles:
                modele.avanceAssam(numMin, babouches)
                self.stat_noeuds+=1
                tapisPossibles=modele.plateau.coups_possibles()
                for coordstapis in tapisPossibles:
                    modele.poseTapis(numMin, coordstapis)
                    self.stat_noeuds+=1

                    current = self._maxSimplet(modele)
                    if current < worst:
                        worst = current
                        if worst == float('-Inf'):
                            modele.undo()
                            modele.undo()
                            modele.undo()
                            return worst
                    modele.undo()
                modele.undo()
            modele.undo()
        return worst


    def _maxSimplet(self,modele, first=False):

        """Meilleur coup local pour Joueur"""
        if len(modele.tapis[-1]) == 0:
            return self._eval(modele)

        best=float('-Inf')

        for angle in [-1,0,1]:
            modele.changeDir(self.numero, angle)
            self.stat_noeuds+=1
            babouchesPossibles=[b+1 for b, carte in enumerate(modele.nb_cartes_deplacement[self.numero]) if carte > 0]
            for babouches in babouchesPossibles:
                modele.avanceAssam(self.numero, babouches)
                self.stat_noeuds+=1
                tapisPossibles=modele.plateau.coups_possibles()
                for coordstapis in tapisPossibles:
                    modele.poseTapis(self.numero, coordstapis)
                    self.stat_noeuds+=1
                    if first and self.angle == None:
                        self.setCoup(angle, babouches, coordstapis)
                    current = self._minSimplet(modele)
                    if current > best:
                        best = current
                        if first:
                            self.setCoup(angle, babouches, coordstapis)
                        if best == float('Inf'):
                            modele.undo()
                            modele.undo()
                            modele.undo()
                            return best
                    modele.undo()
                modele.undo()
            modele.undo()
        return best

    def _eval(self, modele):
        """ evaluation simpliste du coup"""
        self.stat_feuilles+=1
        points = modele.points()
        if len(modele.tapis[-1]) == 0:
            # endgame : dernier joueur n'a plus de tapis
            res=float('Inf')
            for i in range(modele.nb_joueurs):
                if (i == self.numero):
                    pass
                else:
                    if points[i] > points[self.numero]:
                        return float('-Inf')
                    if points[i] == points[self.numero]:
                        res=0
            return res
        # heuristique : calcul partiel des points
        res=0
        for i in range(modele.nb_joueurs):
            if (i == self.numero):
                res+= points[i]
            else:
                res -= points[i]
        return res
