import json
 
def main():
    image_dicts = {}
    id_to_name = {}
    cate = {}
    with open("train.json") as json_file:
        data = json.load(json_file)
        for image in data["images"]:
            image_dicts[image['id']] = {}
        for anns in data['annotations']:
            if anns['category_id'] not in image_dicts[anns['image_id']]:
                image_dicts[anns['image_id']][anns['category_id']] = 1
            else:
                image_dicts[anns['image_id']][anns['category_id']] += 1
        for cats in data['categories']:
            id_to_name[cats['id']] = cats['name']
            cate[cats['name']] = 0
    with open("test.json") as json_file:
        data = json.load(json_file)
        for image in data["images"]:
            
            image_dicts[image['id']] = {}
        for anns in data['annotations']:
            if anns['category_id'] not in image_dicts[anns['image_id']]:
                image_dicts[anns['image_id']][anns['category_id']] = 1
            else:
                image_dicts[anns['image_id']][anns['category_id']] += 1
        
    with open("val.json") as json_file:
        data = json.load(json_file)
        for image in data["images"]:
            image_dicts[image['id']] = {}
        for anns in data['annotations']:
            if anns['category_id'] not in image_dicts[anns['image_id']]:
                image_dicts[anns['image_id']][anns['category_id']] = 1
            else:
                image_dicts[anns['image_id']][anns['category_id']] += 1
    
    named_dict = {}
    for i in image_dicts:
        named_dict[i] = {}
        for anns in image_dicts[i]:
            named_dict[i][id_to_name[anns]] = image_dicts[i][anns]
    for i in named_dict:
        for anns in named_dict[i]:
            cate[anns] += named_dict[i][anns]
    print(cate)

                

if __name__ == "__main__":
    main()
