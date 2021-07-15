from pathlib import Path
from shutil import copy
from random import randint
import csv

## With this class we can control to what set we nned to send the data and in what csv should be tagged
## The user can select the percentage he wants for the first set and then change 
class SetsDistributionController :
	def __init__(self, total, perc, staring_set, category = ""):
		self.total = total
		self.current = 0
		self.max_perc = perc
		self.__staring_set = staring_set
		self.current_set = staring_set
		self.category = category

	## Retrives the current porcentage progress, or in the n next iterations (as add)
	def get_percentage(self, add = 0):
		return (self.current + add)/self.total * 100

	## Increments the percentage by i (1 as default) iterations and returns how many iteretions there have been
	def inc(self, i = 1):
		if self.current+i > self.total:
			return -1
		self.current+=i
		return self.current

	## Checks if it's time to change the set it should be distributing to
	## Returns if it was changed or not
	def check_set(self):
		changed = False
		if self.get_percentage() > self.max_perc and self.current_set == self.__staring_set:
			self.current_set = self.__staring_set.replace('train',"test")
			changed = True
		return changed



## Recursive function that will do a deep search to get to all the files inside the dir
## Once it finds a file it will be added to the proper set
def searching_all_files(directory: Path, send_to_set, parent = "", sets_distro = object() ):   

    for x in directory.iterdir():
    	## If the current path is a file we will send the data to the appropiate set
        if x.is_file():
        	## Checking is a valid file for the set
        	if "." == x.name[0] or "train" in x.parent.name or "test" in x.parent.name: 
        		continue
        	## Check / update the set we need to send the data to
        	sets_distro.check_set()
        	## Create a random prefix so when the set's files are in order we dont have the categories in order
        	rand_prefix = randint(10**(5-1),(10**5)-1)
        	## Add the data to the appropiate set
        	if sets_distro.inc() == -1 :
        		continue
        	copy_to_set(sets_distro.current_set, x.absolute(), str(rand_prefix)+"_"+x.name, x.parent.name)

        else:        	
        	## Checking is a valid directories (categories) for the sets
        	if "." == x.name[0] or "train" in x.name or "test" in x.name:
        		continue
        	## Create the new directory and get amount of samples it contains. 
        	new_directory = directory/x.name
        	total_dir =len(list(new_directory.iterdir()))
        	## Create the set controller so we have 80% of the data for training set and 20% for the testing set
        	## We'll also add not valid data but in a much less quantity
        	perc = 80
        	if "not_valid" in x.name:
        		total_dir = round(total_dir * .07)
        		perc = 60
        	distro = SetsDistributionController(total_dir, perc, send_to_set, x.name)
        	searching_all_files(directory/x.name,send_to_set, x.name, distro)


## Add the data to the folder set it belongs to
def copy_to_set(set_name , src_file , new_name, class_type = "not valid" ):
	add_tag_to_csv(set_name, new_name, class_type)
	if not set_name in new_name:
		new_name = set_name+"/"+new_name
	print(src_file,new_name)
	copy(src_file, new_name)



## Create temps to store the tagged info for each set
train_csv = []
test_csv = []

## we add the name of the image and it's category as tags. 
## The info is saved according to the set it belogns to
def add_tag_to_csv(set_name, name, class_type):
	class_type = class_type.replace('_', ' ')
	if "train" in set_name:
		train_csv.append({"img_name":name, "category": class_type})
	else:
		test_csv.append({"img_name":name, "category": class_type})



## Create the paths and directories we'll be working with
base_path = Path("curated_data")
Path("curated_data/train").mkdir(parents=True, exist_ok=True)
Path("curated_data/test").mkdir(parents=True, exist_ok=True)

## Do a deep separations between training and testing sets
searching_all_files(base_path,base_path.name+"/train")

## Write the csvs that will have the taggs corresponfing to the category
sort_train_csv = sorted(train_csv, key=lambda k: k['img_name']) 
with open('train_data_ordered.csv', mode='w', encoding='utf8') as csv_file:
	headers = ['img_name', 'category']
	writer = csv.DictWriter(csv_file, fieldnames=headers)
	writer.writeheader()
	for row in sort_train_csv:
		writer.writerow(row)

sort_test_csv = sorted(test_csv, key=lambda k: k['img_name']) 
with open('test_data_ordered.csv', mode='w', encoding='utf8') as csv_file:
	headers = ['img_name', 'category']
	writer = csv.DictWriter(csv_file, fieldnames=headers)
	writer.writeheader()
	for row in sort_test_csv:
		writer.writerow(row)

