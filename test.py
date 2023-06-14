import pymongo
import pandas as pd
client = pymongo.MongoClient()
db = client['barge2']



from rembg import remove
from PIL import Image
  
# Store path of the image in the variable input_path
input_path =  r"C:\Users\Moeen\Desktop\New folder\download.jpg"
  
# Store path of the output image in the variable output_path
output_path = r"C:\Users\Moeen\Desktop\New folder\download2.jpg"
  
# Processing the image
input = Image.open(input_path)
  
# Removing the background from the given Image
output = remove(input)
output = output.convert("RGB")
#Saving the image in the given path
output.save(output_path)