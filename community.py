import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import random
import itertools



community_members = 10
community_quantity = 100

tendency_effect_upper = 20
tendency_effect_lower = -10

type_effect_upper = 20
type_effect_lower = -10
type_upper = 0
type_lower = -10

threshold_effect_upper = 0
threshold_effect_lower = 0
threshold_upper = 10
threshold_lower = -10

class Person:
    
    def __init__(self, id):
        view_points = ['binary', 'non-binary']
        self.id = id
        self.type = random.randint(type_lower, type_upper)/ 10
        self.view_point = random.choice(view_points)
        self.threshold = random.randint(threshold_lower, threshold_upper)/ 10
        self.tendency_to_pair = np.array([[i, random.random()] for i in range(10000, 10000 + community_members)])

class Community:

    def __init__(self):
        self.members = [Person(i) for i in range(10000, 10000 + community_members)]

    def interact(self, p1 = Person, p2 = Person):
        id = np.where(p1.tendency_to_pair == p2.id)
        id[1][0] = id[1][0] + 1
        p1_tendency_to_pair = p1.tendency_to_pair[id]

        id_2 = np.where(p2.tendency_to_pair == p1.id)
        id_2[1][0] = id_2[1][0] + 1
        p2_tendency_to_pair = p2.tendency_to_pair[id_2]

        if p1.view_point == 'binary':
            if p2.type < p1.threshold:
                return 'fail'
            if p2.type > p1.threshold:
                p1.tendency_to_pair[id][0] += random.randint(tendency_effect_lower, tendency_effect_upper)/ 100
                p2.tendency_to_pair[id_2][0] += random.randint(tendency_effect_lower, tendency_effect_upper)/ 100
                p2.type += random.randint(type_effect_lower, type_effect_upper)/ 100
                p1.type += random.randint(type_effect_lower, type_effect_upper)/ 100
                p2.threshold += random.randint(threshold_effect_lower, threshold_effect_upper)/ 1000
                p1.threshold += random.randint(threshold_effect_lower, threshold_effect_upper)/ 1000
                return 'success'

        if p1.view_point == 'non-binary':
            if p1_tendency_to_pair < p1.threshold:
                return 'fail'
            if p1_tendency_to_pair > p1.threshold:
                p1.tendency_to_pair[id][0] += random.randint(tendency_effect_lower, tendency_effect_upper)/ 100
                p2.tendency_to_pair[id_2][0] += random.randint(tendency_effect_lower, tendency_effect_upper)/ 100
                p1.type += random.randint(type_effect_lower, type_effect_upper)/ 100
                p2.type += random.randint(type_effect_lower, type_effect_upper)/ 100
                p2.threshold += random.randint(threshold_effect_lower, threshold_effect_upper)/ 1000
                p1.threshold += random.randint(threshold_effect_lower, threshold_effect_upper)/ 1000
                return 'success'

    def start(self):
        
        pairs = itertools.combinations(self.members, 2)
        results = []
        for person in pairs:
            result = self.interact(person[0], person[1])
            results.append(result)
        return results







dataframes = []
for i in range(community_quantity):
    comm = Community()
    for i in range(4):
        results = comm.start()
    try:
        ratio = results.count('success') / results.count('fail')
    except:
        ratio = results.count('success')
    data = {'id': [i.id for i in comm.members],
            'view_point': [i.view_point for i in comm.members],
            'type': [i.type for i in comm.members],
            'threshold': [i.threshold for i in comm.members],
            'tendency_to_pair': [i.tendency_to_pair for i in comm.members],
            'result': [ratio for i in range(len(comm.members))]}

    df = pd.DataFrame(data)
    dataframes.append(df)




data = []
for item in dataframes:
    tendency = [item['tendency_to_pair'][i][:,1] for i in range(len(item))]
    row = [len(item[item['view_point'] == 'binary']) / len(item[item['view_point'] == 'non-binary']),
            item['type'].mean(),
            item['threshold'].mean(),
            np.mean(tendency),
            item['result'].mean()]
    data.append(row)

df = pd.DataFrame(data, columns=['binary_to_non-binary_ratio', 'type_mean', 'threshold_mean', 
                    'tendency_to_pair_mean', 'result'])


print('binary_to_non-binary_ratio: ', df['binary_to_non-binary_ratio'].corr(df['result']))
print('type_mean', df['type_mean'].corr(df['result']))
print('threshold_mean', df['threshold_mean'].corr(df['result']))
print('tendency_to_pair', df['tendency_to_pair_mean'].corr(df['result']))

