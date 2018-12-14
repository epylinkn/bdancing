import pandas
import os
import numpy as np

numFrames_training = 1000
numFrames_test = 500
startFrame = 50;
endFrame_train = startFrame+numFrames_training
endFrame_test = endFrame_train+numFrames_test
def getColumns():
	c = pandas.read_csv("columns.tsv", sep="\t")
	return c.columns

columns = getColumns();

#create empty datasets for training and testing data
train = pandas.DataFrame(columns = columns)
test = pandas.DataFrame(columns = columns)

def processData(inFile, classification):
		data = pandas.read_csv(inFile, sep="\t", usecols=columns);
		
		#get dancer's name from filename 
		#todo: serialize user's name as an id cuz everything should be a number
		user = file.split("_")[1].split(".")[0]		
		
		#add column for the user's name
		data["user"] = user; 

		#todo: classification should be 0 or 1 instead of 'dancing' 'not dancing'
		data["classification"] = classification;

		t = data[endFrame_train:endFrame_test] #sample frames for testing
		data = data[startFrame:endFrame_train] #sample frames for training

		return (t,data)

r = None 

for file in os.listdir(os.getcwd()):
	if file.startswith("dancing") and file.endswith(".tsv"):
		r = processData(file, "dancing")
	elif file.startswith("notdancing") and file.endswith(".tsv"):
		r = processData(file,"not dancing")

	#if the file was processed, add it to the end of the training and testing data
	if r is not None:
		train = pandas.concat([train,r[1]], sort=False)
		test = pandas.concat([test,r[0]], sort= False)
	r = None


print(len(train))
print(len(test))

train.to_csv("training_data.csv")	
test.to_csv("testing_data.csv")
