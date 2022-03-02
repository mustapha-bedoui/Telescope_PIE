





import cv2
import numpy as np
from matplotlib import pyplot as plt

def setup_min():
	 print("Donner valeur Min pour la configuration NOIR/BLANC : ")
	 min = int(input())
	 return min 	

# open image file
def recherche(picture) :
	image = cv2.imread(picture, cv2.IMREAD_UNCHANGED)

	# convert image to grayscale
	image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	cv2.imwrite('image_grayscale.png', image_grayscale)
	# convert image to black and white
	##	
	min = setup_min()
	##
	thresh, image_black = cv2.threshold(image_grayscale, min, 255, cv2.THRESH_BINARY)
	cv2.imwrite('image_black.png', image_black)
	image_black = cv2.bitwise_not(image_black)
	cv2.imwrite('image_black_negative.png', image_black)

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


picture = 'lune5.jpg'
cx1,cy1=recherche(picture)

mode = input('choisir le mode de fonctionnement : ')
print(mode)
if mode == auto :
	
	commande = 'N'
	while commande == 'N':
		# entrer image suivante
		# cx2,cy2=recherche(next_picture)
		# fonction calcul_trajectoire
		# (fonction déplacement) : envoie des coordonnées vers la carte arduino pour envoyer les commandes nessecaires vers le moteur
		print(mode)
		commande = input('quitter le mode auto ? Y/N : ')
else : 
	#on deplace manuellement









	
	
	
	
	
	
	
