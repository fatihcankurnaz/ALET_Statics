import json
import numpy as np
import random
prev_result_comb = {}
prev_results_calc = {}
single_prob = np.zeros((54))
object_matrix = np.zeros((54,54))
@lru_cache(true)
def calc(theta,obs):
    global object_matrix
    listToStr = ' '.join([str(s) for s in obs])
    listToStr += str(theta)
    if listToStr in prev_results_calc:
        return prev_results_calc[listToStr]
    if len(obs) == 0:
        prev_results_calc[listToStr] = single_prob[theta]
        return single_prob[theta]
    multip = 1
    sum = 0
    for i in obs:
        sum += object_matrix[theta][i]
    multip = sum* single_prob[theta]
    
    res = comb(obs)
    if res == 0:
        prev_results_calc[listToStr] = 0
        return 0
    prev_results_calc[listToStr] = multip / res
    return multip / res

def comb(arr):
    listToStr = ' '.join([str(s) for s in arr])
    global object_matrix
    if listToStr in prev_result_comb:
        return prev_result_comb[listToStr]
    multip = 1
    if(len(arr) == 1):
        prev_result_comb[listToStr] = single_prob[arr[0]]
        return single_prob[arr[0]]
    if(len(arr) == 2):
        #print(arr)
        res =  object_matrix[arr[1]][arr[0]]*single_prob[arr[1]]
        prev_result_comb[listToStr] = res
        #print(object_matrix[arr[1]][arr[0]])

        return res
    else:
        for i in range(len(arr)):
            multip *= calc( arr[i],arr[i+1:])
    prev_result_comb[listToStr] = multip
    return multip


def main():
    random.seed(0)
    image_dicts = {}
    image_dicts_counted = {}
    id_to_name = {}
    cate = {}
    matrix = np.zeros((1988,54))
    object_count = np.zeros((54))
    global object_matrix 
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
    for i in image_dicts_counted:
        named_dict[i] = {}
        for anns in image_dicts_counted[i]:
            if anns == 55:

                matrix[count][7] = image_dicts_counted[i][anns]
            else:
                matrix[count][anns-1] = image_dicts_counted[i][anns]
            named_dict[i][id_to_name[anns]] = image_dicts_counted[i][anns]
        count += 1
    
    for i in matrix:
        for k in range(len(i)):
            if i[k] >0:
                object_count[k] += 1
                for j in range(54):
                    if j == k:
                        object_matrix[k][j] += (i[k]-1)
                    else:
                        object_matrix[k][j] += i[j]
    for i in object_matrix:
        row_sum = 0
        for k in i:
            row_sum += k
        for k in range(len(i)):
            i[k] = i[k]/row_sum
    all_sum = 0
    for i in range(len(object_matrix[0])):
        for k in object_matrix[i]:
            single_prob[i] += k
            all_sum += k
    for i in range(len(single_prob)):
        single_prob[i] = single_prob[i]/all_sum
    overall = []
    for i in range(3):
        first_item = random.randint(0, 53)
        item_number = random.randint(5,20)
        #print(first_item)
        existing = [first_item]
        k=0
        while(k<item_number):
            random_item = random.randint(0,53)
            prob_of_random_item = calc(random_item,existing)
            print(k,prob_of_random_item,existing,random_item)
            if prob_of_random_item >random.random():
                existing.append(random_item)
                k+=1
            else:
                continue
        overall.append(existing)

    for i in named_dict:
        for anns in named_dict[i]:
            cate[anns] += named_dict[i][anns]
    #probability of one item existing 
    prop_of_one_item = dict(cate)
    
    for i in cate:
        prop_of_one_item[i] = prop_of_one_item[i]/len(named_dict.keys())

    #print(cov_matrix)
    sum = 0
    for i in prop_of_one_item:
        sum+= prop_of_one_item[i]
    #print(prop_of_one_item)
    #print(sum)
    # for i in object_matrix:
    #     my_s = ""
    #     for j in i:
    #         my_s += str(j)+" "
    #     print(my_s)
    print(overall)
    # print(comb([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]))
                

if __name__ == "__main__":
    main()
