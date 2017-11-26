from config import CONFIG

input_list = [(465, 45, 'cup', 17168.0), (450, 0, 'glasscase', 3661.0), (615, 195, 'greenbar', 16221.0), (675, 225, 'pencilcase', 16312.0), (450, 45, 'rice', 19506.0), (270, 165, 'scissors', 6489.0), (435, 0, 'shave', 5439.0), (645, 225, 'snack', 17071.0), (435, 30, 'socks', 17555.0), (390, 180, 'spaghetti', 13576.0)] 


'''
parser_detector : list -> list, list, list
parser_detector : result list from detector -> coordinate list, item list, value list
'''
def parser_detector(result_list):
    coord_list, item_list, value_list = [], [], []
    for i in result_list:
        coord_list.append((i[0],i[1]))
        item_list.append(i[2])
        value_list.append(i[3])
    return coord_list, item_list, value_list


'''
calculator : list of string -> list of int, int
calculator : item list -> list of cost, total cost 
'''
def calculator(item_list = []):
    # print the item list and price
    if len(item_list) == 0:
        print("Err : empty item list")
        return None
    total_cost = 0
    cost_list = []
    for j in item_list:
        cost_list.append(CONFIG[j])
        if CONFIG[j] == 'end':
            break
        total_cost += CONFIG[j]

    return  cost_list, total_cost

print(calculator(parser_detector(input_list)[1]))
# Program Starts from Here    
