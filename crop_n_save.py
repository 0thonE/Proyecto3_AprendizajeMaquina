import sys
import cv2
import re
import time
from csv import DictReader
from pathlib import Path


## Getting the arguments passed from bash
csv_path = sys.argv[1] if len(sys.argv)>1 else "taco-trash/data.csv" # if there is no path for the csv we use the default one
curated_path = sys.argv[2] if len(sys.argv)>2 else "curated_data" # if there is no path to save the treated data we use a default one


## Will crop the image in the section the object to classify is and then save it to the selected path
def cropNsave(path,x,y,width,height,save2path):
    x = int(float(x))
    y = int(float(y))
    x_end = int(float(width))+x
    y_end = int(float(height))+y

    ## If the values to crop don't make sense will skip saving that image
    if x < 0 or y < 0 or x_end < 0 or y_end < 0:
        return

    ## Open and crop the image in the roi
    img = cv2.imread(path)
    crop = img[y:y_end,x:x_end]

    ## If we are able to save the image we'll notigy the user what image was cropped and where it was saved
    if cv2.imwrite(save2path, crop):
        print("Image ", path, "saved in ", save2path)
    else:         
        sys.stdout.flush()
        print("Image ", path, "couldn't be saved in ", save2path)


start_time = time.time()

## Open and read the csv that has the images and the section of the image where the object is
file_handle = open(csv_path, "r", encoding="utf8")
csv_reader=DictReader(file_handle)

## Iterate all the data rows in order to classify them according to the tags we have
for row in csv_reader:
    img_id, ann_id, path, x, y, width, height=  row['img_id'],row['ann_id'],row['img_file'],row['x'],row['y'], row['width'], row['height']
    cat_name = row['cat_name'].lower()
    if cat_name == "drink can":
        Path(f"{curated_path}/drink_can").mkdir(parents=True, exist_ok=True)
        save2path = f"{curated_path}/drink_can/" +img_id+ "_"+ann_id+ "_" + re.sub(r'batch_\d+/', '', path)
    elif cat_name == "cigarette":
        Path(f"{curated_path}/cigarette").mkdir(parents=True, exist_ok=True)
        save2path = f"{curated_path}/cigarette/" +img_id+ "_"+ann_id+ "_" + re.sub(r'batch_\d+/', '', path)
    elif cat_name == "plastic straw":
        Path(f"{curated_path}/plastic_straw").mkdir(parents=True, exist_ok=True)
        save2path = f"{curated_path}/plastic_straw/" +img_id+ "_"+ann_id+ "_" + re.sub(r'batch_\d+/', '', path)
    elif cat_name == "metal bottle cap":
        Path(f"{curated_path}/metal_bottle_cap").mkdir(parents=True, exist_ok=True)
        save2path = f"{curated_path}/metal_bottle_cap/" +img_id+ "_"+ann_id+ "_" + re.sub(r'batch_\d+/', '', path)
    # elif cat_name == "plastic bottle cap":
    #     Path(f"{curated_path}/plastic_bottle_cap").mkdir(parents=True, exist_ok=True)
    #     save2path = f"{curated_path}/plastic_bottle_cap/" +img_id+ "_"+ann_id+ "_" + re.sub(r'batch_\d+/', '', path)
    elif cat_name == "crisp packet":
        Path(f"{curated_path}/crisp_packet").mkdir(parents=True, exist_ok=True)
        save2path = f"{curated_path}/crisp_packet/" +img_id+ "_"+ann_id+ "_" + re.sub(r'batch_\d+/', '', path)
    else : 
        Path(f"{curated_path}/not_valid").mkdir(parents=True, exist_ok=True)
        save2path = f"{curated_path}/not_valid/" +img_id+ "_"+ann_id+ "_" + re.sub(r'batch_\d+/', '', path)

    ## We execute this function that will save the img with the information provided. 
    ## After running this function the image will be saved into a folder and now we now all the images inside
    ##   that folder are the same class/type
    dir_path = csv_path.replace('.csv','') #taco-trash uses the same naming for the dir and the csv so we just delete the extension
    cropNsave(f"{dir_path}/{path}",x,y,width,height,save2path)


file_handle.close
print("--- %s seconds ---" % (time.time() - start_time))

# cropNsave("cig_butts/train/images/00000007.jpg","340.5","259.5","92.0","53.0","que_loco.jpg")
