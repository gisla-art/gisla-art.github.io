import pandas as pd
import sys
import os

root = "werksverzeichnis/"
# open table with picture files
df = pd.read_csv(os.path.join(root,'Gisla_WV.csv'), sep=',')
img_folder = os.path.join(root,'images')
#  now get all jpg-images in the folder
files = os.listdir(img_folder)
#  get the names of the pictures
img_names = [os.path.splitext(f)[0] for f in files]
# now check on all files it they are in the table
for img_name in img_names:
    if img_name not in df["Nummer"].values:
        topic = img_name[:3]
        print(f"{topic},,{img_name},na,na,na,na,missing,")
print("Done")
