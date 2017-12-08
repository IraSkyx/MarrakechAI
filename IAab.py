#-*-coding:utf-8-*-

from ModeleMarrakechSansAlea import *
import copy
import random

#Class definition
class IA (JoueurMarrakech):

    def __init__(self):
        super().__init__()
        self.monCoup = None

    def __str__(self):
        pass

    def changer_direction(self, modele):
        pass

    def avancer(self, nb_cartes_deplacement, modele):
        pass

    def ou_poser_tapis(self, coups_possibles, modele):
        pass

    def max(n, first=False):
        if n <= 0 :
            return float('Inf')

        best=float('-Inf')

        for c in coups_possibles:
            n-=c
            current=min(n)
            if first and monCoup is None :
                monCoup=c
            if current > best :
                best = current
                if first :
                    monCoup=c
        for i in range(len(coups_possibles)):
            modele.undo()
        n+=c
        return best

    def min(n, first=False):
        if n <= 0 :
            return float('-Inf')

        worst=float('Inf')

        for c in coups_possibles:
            n-=c
            current=max(n)
            if current > worst :
                worst = current

        for i in range(len(coups_possibles)):
            modele.undo()
        n+=c
        return worst
