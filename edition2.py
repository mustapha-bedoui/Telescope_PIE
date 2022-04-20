
import cv2
import numpy as np
from matplotlib import pyplot as plt

def setup_min(picture):
	commande = 'y'
	while commande == 'y' :

		image = cv2.imread(picture, cv2.IMREAD_UNCHANGED)
		# convert image to grayscale
		image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		cv2.imwrite('image_grayscale.png', image_grayscale)
		# convert image to black and white
		##
		print("Donner la borne Min pour la configuration NOIR/BLANC : ")	 	
		mini = int(input())
		##
		thresh, image_black = cv2.threshold(image_grayscale, mini, 255, cv2.THRESH_BINARY)
		cv2.imwrite('image_black.png', image_black)
		image_black = cv2.bitwise_not(image_black)
		cv2.imwrite('image_black_negative.png', image_black)
		cv2.imshow('image', image_black)
		cv2.waitKey(100)
		commande=input('Continuer ? y/n')

	return image_black
# open image file
def recherche(image_black) :
	
	#################################################################################
	#setting threshold of gray image 
	_, threshold = cv2.threshold(image_black, 127, 255, cv2.THRESH_BINARY)
  

	# using a findContours() function
	contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	i = 0

	# list for storing names of shapes
	for contour in contours:
  
    	# here we are ignoring first counter because 
    	# findcontour function detects whole image as shape
    		if i == 0:
        		i = 1
        		continue
  
    	# cv2.approxPloyDP() function to approximate the shape
    		approx = cv2.approxPolyDP(
        	contour, 0.01 * cv2.arcLength(contour, True), True)
      
    	# using drawContours() function
    		cv2.drawContours(image_black, [contour], 0, (0, 0, 0), 2)
  
    	# finding center point of shape
    		M = cv2.moments(contour)
    
	#print(contours)
	cv2.imwrite('contour.png', image_black)
	#######################################################################################
	thresh = cv2.threshold(image_black, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]


	cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	cnts = cnts[0] 
	for c in cnts:
    		# Obtain bounding box coordinates and draw rectangle
    		x,y,w,h = cv2.boundingRect(c)
    		cv2.rectangle(image_black, (x, y), (x + w, y + h), (0,255,0), 2)

    		# Find center coordinate and draw center point
    		M = cv2.moments(c)
    		cx = int(M['m10']/M['m00'])
    		cy = int(M['m01']/M['m00'])
    		cv2.circle(image_black, (cx, cy), 2, (255,255,0), 5)
    		print('Center: ({}, {})'.format(cx,cy))

	cv2.imshow('telescope', image_black)
	cv2.imwrite('Image_centrée_.png', image_black)
	cv2.waitKey()
	return (cx,cy)

def calcul_trajectoire(cx1,cx2,cy1,cy2) :
	return(cx2-cx1,cy2-cy1)	


picture = 'lune2.jpg'
cx1,cy1=recherche(setup_min(picture))
print ("centre :",cx1,cy1)
mode = input('Veuillez choisir le mode de fonctionnement : ')

if mode == "auto" :
	
	commande = 'n'
	while commande == 'n':
		# entrer image suivante
		next_picture = 'lune2Prime.jpg' #ici on doit avoir l'image de telescope qui suive picture pour faire la comparaison 
		cx2,cy2=recherche(setup_min(next_picture))
		# Apres comparaision entre les deux photos successives on peut deduire la trajectoire
		# fonction calcul_trajectoire
		deplacement_suivant_axeX,deplacement_suivant_axeY=calcul_trajectoire(cx1,cx2,cy1,cy2)
		
		# (fonction déplacement) : envoie des coordonnées vers la carte arduino pour envoyer les commandes nessecaires vers le moteur
		#initialiser les coordonnées vers l'etape suivante : 
		cx1,cy1=cx2,cy2
		
		commande = input('Continuer en mode Automatique ? y/n ')

#else : 
	#commande mannuel




	
	
	
	
	
	
	
