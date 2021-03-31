from zipfile import ZipFile
import os
for iteration in os.listdir("./Iterations"):
	for fold in os.listdir("./Iterations/"+iteration):
		# Create a ZipFile Object and load sample.zip in it
		print(fold)
		with ZipFile("./Iterations/"+iteration+"/"+fold, 'r') as zipObj:
			# Get a list of all archived file names from the zip
			listOfFileNames = zipObj.namelist()
			# Iterate over the file names
			for fileName in listOfFileNames:
				# Check filename endswith csv
				if fileName.endswith('.csv'):
					# Extract a single file from zip
					print("./Iterations/"+iteration+"/"+fold)
					zipObj.extract(fileName, "./Iterations/"+iteration)

		os.remove("./Iterations/"+iteration+"/"+fold)

		
