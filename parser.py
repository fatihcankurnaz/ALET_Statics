import json
import numpy as np
def main():
    image_dicts = {}
    image_dicts_counted = {}
    id_to_name = {}
    cate = {}
    matrix = np.zeros((1988,54))
    with open("train.json") as json_file:
        data = json.load(json_file)
        for image in data["images"]:
            image_dicts[image['id']] = {}
            image_dicts_counted[image['id']] = {}
        for anns in data['annotations']:
            if anns['category_id'] not in image_dicts[anns['image_id']]:
                image_dicts[anns['image_id']][anns['category_id']] = 1
                image_dicts_counted[anns['image_id']][anns['category_id']] = 1
                
            else:
                image_dicts_counted[anns['image_id']][anns['category_id']] += 1
                
        for cats in data['categories']:
            id_to_name[cats['id']] = cats['name']
            cate[cats['name']] = 0
    with open("test.json") as json_file:
        data = json.load(json_file)
        for image in data["images"]:
            
            image_dicts[image['id']] = {}
            image_dicts_counted[image['id']] = {}
        for anns in data['annotations']:
            if anns['category_id'] not in image_dicts[anns['image_id']]:
                image_dicts[anns['image_id']][anns['category_id']] = 1
                image_dicts_counted[anns['image_id']][anns['category_id']] = 1
                
            else:
                image_dicts_counted[anns['image_id']][anns['category_id']] += 1
                
        
    with open("val.json") as json_file:
        data = json.load(json_file)
        for image in data["images"]:
            image_dicts[image['id']] = {}
            image_dicts_counted[image['id']] = {}
        for anns in data['annotations']:
            if anns['category_id'] not in image_dicts[anns['image_id']]:
                image_dicts[anns['image_id']][anns['category_id']] = 1
                image_dicts_counted[anns['image_id']][anns['category_id']] = 1
  
            else:
                image_dicts_counted[anns['image_id']][anns['category_id']] += 1
                
    
    named_dict = {}
    count = 0
    for i in image_dicts:
        named_dict[i] = {}
        for anns in image_dicts[i]:
            if anns == 55:

                matrix[count][7] = image_dicts[i][anns]
            else:
                matrix[count][anns-1] = image_dicts[i][anns]
            named_dict[i][id_to_name[anns]] = image_dicts[i][anns]
        count += 1

    for i in named_dict:
        for anns in named_dict[i]:
            cate[anns] += named_dict[i][anns]
    #probability of one item existing 
    prop_of_one_item = dict(cate)
    
    for i in cate:
        prop_of_one_item[i] = prop_of_one_item[i]/len(named_dict.keys())
    cov_matrix = np.cov(matrix)
    #print(cov_matrix)
    sum = 0
    for i in prop_of_one_item:
        sum+= prop_of_one_item[i]
    print(prop_of_one_item)
    print(sum)
    

                

if __name__ == "__main__":
    main()
