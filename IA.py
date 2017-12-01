#-*-coding:utf-8-*-

import os
os.chdir("/home/etud/adlenoir/data/2A/modelisation")

#Class definition
class Node:
	def __init__(self, ID, Father, nbRemaining):
		self.ID = ID
		self.Father = Father
		self.nbRemaining = nbRemaining

# @param n = remaining matchs
# @param father = Father ID
def J2Nim(n, father=0):

	#Variables
	global Index, TreeMap, Height, CanIncrement
	r=[]
	i=1
	t=0

	#Increment ID
	Index+=1

	#Add new Node to array
	no=Node(Index,father,n)
	TreeMap.append(no)

	#Compute tree Height
	if CanIncrement:
		Height+=1

	#Stop incrementing tree Height
	if n<=0:
		CanIncrement=False
		return -1

	#Iterate on sons
	while n-i>=0 and i<=4:
		t=J1Nim(n-i, no.ID)
		r.append(t)
		i+=1
	return min(r)

# @param n = remaining matchs
# @param father = Father ID
def J1Nim(n, father=0):

	#Variables
	global Index, TreeMap, Height, CanIncrement
	r=[]
	i=1 
	t=0

	#Increment ID
	Index+=1

	#Add new Node to array
	no=Node(Index,father,n)
	TreeMap.append(no)

	#Compute tree Height
	if CanIncrement:
		Height+=1

	#Stop incrementing tree Height
	if n<=0:
		CanIncrement=False
		return 1

	#Iterate on sons
	while n-i>=0 and i<=4:
		t=J2Nim(n-i, no.ID)
		r.append(t)
		i+=1
	return max(r)



##### MAIN #####

Height=-1
CanIncrement=True
TreeMap=[]
Index=0
file = open("Graphe.txt", "w")

#Display
print("Le joueur 1 gagne !" if J1Nim(5) == 1 else "Le joueur 2 gagne !")
print("Taille de l'arbre : " + str(len(TreeMap)-1))
print("Hauteur de l'arbre : " + str(Height))


##### File writing #####

#Dot header
file.write("digraph G {\n")

#Print each nodes
for index, val in enumerate(TreeMap):
	file.write(str(val.ID) + " [label=" + str(val.nbRemaining) + "]\n")
	if(index != 0):
		file.write(str(val.Father) + " -> " + str(val.ID) + "\n")

#Dot Footer
file.write("}\n")
