#!C:\Users\XBRC7657\AppData\Local\Programs\Python\Python38\python.exe

import threading
import cv2 
import time							
import pytesseract					  
#Also needs to install tesseract and set environment path locally	# Please refer: https://tesseract-ocr.github.io/tessdoc/Home.html
# from googletrans import Translator 		#Internet needs to remain connected while running
from google_trans_new import google_translator 
from os import path
import img2pdf 
from PIL import Image 
import os

starttime = time.time()

translator = google_translator()	#Translator()	

threads =[] #Stores threads

langDict = {"Auto": ["",""] ,"English" : ["eng","en"], "French": ["fra","fr"]}

infolog = " "

#Declaring variables and values for writing in the image
font_scale = 0.75		#this is dynamically changed according to the box width below
color = (255, 0, 0)
thickness = 1
font = cv2.FONT_HERSHEY_SIMPLEX    
line_type = cv2.LINE_AA

    # Adding custom options for tesseract-ocr
custom_config = r'--oem 3 -l fra --psm 6'
    # print(pytesseract.image_to_string(img, config=custom_config))

def textToEng(frenchText,img,x,y,h, inLang, outLang):				#function translates french words to englishprint("trans")
	try:
		translateResponse = translator.translate(frenchText, lang_src=inLang, lang_tgt=outLang)	#converting found text from french to english info: src can be removed if source is not known
		cv2.putText(img, translateResponse, (x,y), font, font_scale * (h /30), color, thickness, line_type) #inserting converted text in the image
		# log = log+ " \n"+frenchText+" : "+ translateResponse.text	# printing converted text to console for debugging purposes
	    	
	except:
		# infolog = infolog + "error"
		pass
		# infolog = infolog +"\n"+frenchText+" : Error whille translating!!!"
	 


def img_trans(imgLocation, inLang, outLang):
    
	custom_config = r'--oem 3 -l '+langDict[inLang][0]+' --psm 6'

	img = cv2.imread(imgLocation)
    
    # For boxes around each word:
	try:
		d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, config=custom_config)
	except Exception:
		print("Error while processing file!!!")
		exit()

	# print(d.keys())		#Prints the available keys in the dictionary d
	
	print("debugging")
	n_boxes = len(d['text'])	#Number of texts found
	for i in range(n_boxes):
		if int(d['conf'][i]) > 50:				#Check if confidence score is greater than 60
			(x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])	#calculating boundaries for boxes
			img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)			#inserting box in img
            
			textToEng(d['text'][i],img,x,y,h, langDict[inLang][1], langDict[outLang][1])


	endtime = time.time()
	print("Time taken : " + str(endtime - starttime)+" Secs")
	fileName, ext = path.splitext(imgLocation)	#splitting file name and extension
	cv2.imwrite(fileName+"_converted"+ext, img)
	pdf_path = fileName+"_converted" + ".pdf"
	image = Image.open(fileName+"_converted"+ext)
	pdf_bytes = img2pdf.convert(image.filename)
	file = open(pdf_path, "wb")
	file.write(pdf_bytes)
	image.close()
	file.close()

	return fileName+"_converted"+ext

def img_trans_threading(imgLocation, inLang, outLang):

	

	custom_config = r'--oem 3 -l '+langDict[inLang][0]+' --psm 6'            
	img = cv2.imread(imgLocation)		#reading image


	try:
		d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, config=custom_config)
	except Exception as e:
		print("Error while processing file!!!")
		print("Details: "+ str(e))
		exit()

	# print(d.keys())		#Prints the available keys in the dictionary d
	
	n_boxes = len(d['text'])	#Number of texts found
	
	for i in range(n_boxes):
		if int(d['conf'][i]) > 50:				#Check if confidence score is greater than 60
			(x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])	#calculating boundaries for boxes
			img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)			#inserting box in img
			#----------------Threading in this block below----------------------
			t = threading.Thread(target = textToEng, args = (d['text'][i],img,x,y,h, langDict[inLang][1], langDict[outLang][1]))			#using threads as getting response from server may take some time
			if threading.activeCount() > 8:						#checks if the num of active threads of this procss is greater than 8 (can be changes depending on processor)
				time.sleep(0.5)									#if lots of threads then sleep for 0.5 secs

			t.start()
			threads.append(t)


	for t in threads:			#wait for all the threads to finish
		t.join()
	    
	endtime = time.time()
	print("Time taken: " + str(endtime-starttime)+" Secs")


	# cv2.imshow(imgLocation, img)
	fileName, ext = path.splitext(imgLocation)	#splitting file name and extension
	cv2.imwrite(fileName+"_converted"+ext, img)	#storing file with _Eng in file name
	pdf_path = fileName+"_converted" + ".pdf"
	image = Image.open(fileName+"_converted"+ext)
	pdf_bytes = img2pdf.convert(image.filename)
	file = open(pdf_path, "wb")
	file.write(pdf_bytes)
	image.close()
	file.close()

	return fileName+"_converted"+ext , pdf_path

	# cv2.waitKey(0)

def word(wordLoc):
	pass

def voice(voiceLoc):
	pass