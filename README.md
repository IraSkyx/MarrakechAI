# PrinceAI
AI for the Marrakech game

## Prince1 :
- AI minimax (2 players) which plays perfectly.
- Works well in 3x3 board size by passing first turn.

## Prince2 :
- AI MiniMax which estimates the plays by stopping the search.
- Works well in 3x3 board size, estimates well in 5x5.

## Prince3 :
- IA alpha beta de base.
- Fonctionne bien en 3x3 en passant le premier tour, 10 min si on commence au tour 1. Pas d'approximations donc 5x5 très long.

## Prince4 :
- Alpha beta avec des optimisations sur l'ordre des coups (shuffle)
- Voir PrinceImg1 et PrinceImg2 pour les résultats d'expérimentation (avec et sans shuffle)
- Table d'ouverture
- Voir PrinceStats1 pour les statistiques recueillies
- Débranchement des optimisations (shuffle) quand on arrive près de la fin de l'arbre

## Prince5 :
- IA maxn 3 joueurs ou plus. Fonctionne bien en 3x3. Pas d'approximations donc 5x5 très long.
- Utilisation de la fonction strategy pour déterminer si current est à remplacer par le score de retour du dernier _maxN() appelé.

## Prince6 :
- IA maxn 3 joueurs ou plus qui approxime le jeu en stoppant la recherche
- Utilisation de la fonction strategy pour déterminer si current est à remplacer par le score de retour du dernier _maxN() appelé.
- Fonctionne bien en 3x3, approxime bien en 5x5.

## Prince7 :
- Variante paranoid de Prince6
- Utilisation de la fonction strategy pour déterminer si current est à remplacer par le score de retour du dernier _maxN() appelé.
- Fonctionne bien en 3x3, approxime bien en 5x5.

## Prince8 :
- Variante offensive de Prince6
- Utilisation de la fonction strategy pour déterminer si current est à remplacer par le score de retour du dernier _maxN() appelé.
- Fonctionne bien en 3x3, approxime bien en 5x5.

## Prince9 :
- Variante complexe (qui joue offensive contre le joueur en tête quand elle perd, paranoid quand elle gagne, classic quand elle est 2ème ou 3ème) de Prince6
- Utilisation de la fonction strategy pour déterminer si current est à remplacer par le score de retour du dernier _maxN() appelé en
choisissant quelle méthode appeler par rapport à la situation actuelle du joueur (premier, dernier, etc ...)
- Fonctionne bien en 3x3, approxime bien en 5x5.
