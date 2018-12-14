import os
import numpy as np
import pandas as pd

frames_per_batch = 5
timesteps = 1000
start_frame = 100 // frames_per_batch
end_frame = (start_frame + timesteps) // frames_per_batch

columns = pd.read_csv("columns.tsv", sep="\t").columns

# create empty dataset for training
data = pd.DataFrame(columns = columns)

def processData(inFile, classification):
    frames = pd.read_csv(inFile, sep="\t", usecols=columns);

    # hack(?) to average frames in groups of `frames_per_batch`
    frames = frames.groupby(frames.index // frames_per_batch).mean()

    # calculate the difference (i.e. velocity between batchframes)
    for col in columns:
        if "p1" not in col:
            next

        dkey = col[0:-2] + 'd' + col[-1]
        frames[dkey] = frames[col].diff()

    # classify
    frames["classification"] = 1 if classification == "dancing" else 0

    return frames.iloc[start_frame:end_frame]

res = None
for file in os.listdir(os.getcwd()):
	if file.startswith("dancing") and file.endswith(".tsv"):
		res = processData(file, "dancing")
	elif file.startswith("notdancing") and file.endswith(".tsv"):
		res = processData(file,"not dancing")

	if res is not None:
		data = pd.concat([data, res], sort=False)
	res = None

print(len(data))

data.to_csv("cleaned_data.csv")
