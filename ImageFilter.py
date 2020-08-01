import os
import PIL
from PIL import Image
import datetime
import pathlib

ImgSuffixes = ['.JPEG','.JPG','.PNG','.BMP']

Directory = input('Enter Directory: ')

Directory = Directory.replace('"','')

if os.path.isdir(Directory):

	#Time Stamp Start (Process Duration)
	pStart = datetime.datetime.now().timestamp()
					
	UniqueArray = [] #Array of Already Processed Files
	Counter = 0 #Removed Files Counter
	TotalFiles = 0 # Total Files Counter
	Files = os.listdir(Directory)

	for File in Files:
		try:
			TotalFiles = TotalFiles + 1
			Suffix = pathlib.Path(File).suffix
			
			if Suffix.upper() in ImgSuffixes:

				if File not in UniqueArray:
					
					#Time Stamp Start (File Duration)
					Start = datetime.datetime.now().timestamp()
					
					print('Analyzing File: ' + File)
					
					#Root Image Size
					RootImage = Image.open(Directory + '\\' + File)
					RootWidth, RootHeight = RootImage.size

					#Root Image Pixel Array
					RootPixels = list(RootImage.getdata())
									
					#- Comparison -
					for nFile in Files:
						if (nFile != File) and (nFile not in UniqueArray):					  
							nSuffix = pathlib.Path(nFile).suffix

							if nSuffix.upper() in ImgSuffixes:
								
								#Next Image Size
								nImage = Image.open(Directory + '\\' + nFile)
								Width, Height = nImage.size

								# - 1st Filter (Size Comparison) -
								if Width == RootWidth and Height == RootHeight:
												  
									#Next Image Pixel Array
									nPixels = list(nImage.getdata())

									# - 2nd Filter (Pixels Comparison) -
									if nPixels == RootPixels:
										os.remove(Directory + '\\' + nFile)
										UniqueArray.append(nFile)
										Counter = Counter + 1
										print('Identical Copy - ' + nFile + ' (Removed)')

					UniqueArray.append(File); # Mark as Processed

					#Time Stamp End (File Duration)
					End = datetime.datetime.now().timestamp() 

					#Duration (File Duration)
					print("Duration: " + str(End - Start) + " Seconds")
					print('\n')
		except:
			print(File + ' - Process Failed!')

	#Time Stamp End (Process Duration)
	pEnd = datetime.datetime.now().timestamp()

	#Duration (File Duration)
	print("Duration: " + str(pEnd - pStart) + " Seconds")
						
	print('Files Removed: ' + str(Counter) + '/' + str(TotalFiles))
	print('Finished...')		   
	
else:
	print('Invalid Directory: ' + Directory)

