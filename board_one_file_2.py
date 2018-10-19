import cv2
import numpy as np
import os
def board():
	print('CURRECTNT DIR: ', os.getcwd())
	frames=	["frame1.png","frame2.png","frame3.png","frame4.png","frame5.png","frame6.png","frame7.png","frame8.png","frame9.png","frame10.png"]
	fold="shots2"
	ratio_arr = []
	for f in frames:
		
		name=fold+"/"+f
		try:
			im = cv2.imread(name)
			print(name)
			BLUE=[255,255,255]
			im1 = cv2.copyMakeBorder(im,10,10,10,10,cv2.BORDER_CONSTANT,value=BLUE)
			im1 = cv2.medianBlur(im1,5)
			kernel=np.ones((2,2),np.uint8)
			erosion=cv2.erode(im1, kernel, iterations=4)
			#cv2.imshow("Show",constant)
			#cv2.imshow("Show",erosion)
			imgray = cv2.cvtColor(erosion, cv2.COLOR_BGR2GRAY)

			ret, thresh = cv2.threshold(imgray, 95, 255, cv2.THRESH_BINARY)
			#cv2.imshow("Show",thresh)
			im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
			#cv2.imshow('image',erosion)
			#print("Hier: ",hierarchy)
			children=[]
			childrencontours=[]
			originalindices=[]
			if hierarchy[0,0,2]!=-1:
				next1=hierarchy[0,0,2]
				while next1!=-1:
					children.append(hierarchy[0,next1])
					childrencontours.append(contours[next1])
					originalindices.append(next1)
					next1=hierarchy[0,next1,0]
			#print(childrencontours)

			#print(contours)
			#print(cv2.contourArea(countour[]))
			#print("original",originalindices)

			areas = [cv2.contourArea(c) for c in childrencontours]
			#print("areas",areas)
			max_index = originalindices[np.argmax(areas)]
			#print(max_index,"max")
			cnt=contours[max_index]
			#print("max index", max_index)
			#print("max contour:", cnt)
			#cnt = max(contours, key=lambda x:cv2.contourArea(x))

			#cnt = max(contours, key=lambda x:cv2.contourArea(x))

			#mask = np.zeros_like(im) # Create mask where white is what we want, black otherwise

			#cv2.drawContours(mask, contours, max_index, (0,0,255), 3) # Draw filled contour in mask
			#cv2.imshow("MAsk",mask)
			#out = np.zeros_like(im) # Extract out the object and place into output image
			#cv2.imshow('Output', out)
			#out[mask == 255] = im[mask == 255]

			# Show the output image
			#cv2.imshow('Output 1', out)

			#cv2.drawContours(im, contours, max_index, (0,0,255), 3)
			x,y,w,h = cv2.boundingRect(cnt)
			#cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),3)

			'''
			for c in contours:
				x,y,w,h = cv2.boundingRect(c)
				cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),3)
			'''
			#cv2.imshow("Show",im)
			crop_img = im[y:y+h, x:x+w]
			#cv2.imwrite(fold+"/"+"crop_"+f, crop_img)
			crop_imgray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
			ret, thresh = cv2.threshold(crop_imgray, 127, 255, cv2.THRESH_BINARY_INV)
			kernelA=np.ones((5,5),np.uint8)
			dilation = cv2.erode(thresh,kernelA,iterations = 4)
			#cv2.imwrite(fold+"/"+"crop_"+f,thresh)
			#cv2.imshow("Dilation",dilation)
			crop_im2, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

			###############

			######################
			cv2.drawContours(crop_img, contours, -1, (0,0,255), 3)
			areas = [cv2.contourArea(c) for c in contours]
			#print("AREAS:",areas)
			val=sum(x<10000 for x in areas)
			crop_ar=w*h
			ar1=sum(areas)
			ratio_1 = val/crop_ar
			ratio_2 = val/ar1
			white = np.sum(dilation == 255)
			blk = np.sum(dilation == 0)
			height, width = dilation.shape
			bwratio = blk/(blk+white)
			ratio_arr.append(bwratio)
			print("x")
		except Exception as e:
			print(e)
			print("Failed: ",name)
	print(ratio_arr)
	my_sum = 0
	avg = 0
	total_frames = len(ratio_arr)
	if total_frames > 0:
		for i in ratio_arr:
			my_sum = my_sum + i
		print(my_sum)
		avg = my_sum / total_frames
	print(" percentage of board: ", avg)
	return avg
#board('test-2.mp4')
