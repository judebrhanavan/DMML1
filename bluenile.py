import requests
import pandas as pd
import time


num_results= 1000
diamond_list =[]
attribute_list =['color', 'price', 'skus', 'clarity','depth','table', 'lxwRatio', 'fluorescence', 'polish', 'symmetry', 'dateSet','culet']
sort_directions = ['asc', 'desc']
url= 'https://www.bluenile.com/api/public/diamond-search-grid/v2?country=USA&currency=USD&startIndex={startindex}&pageSize={pageSize}&shape=RD&sortColumn={attribute}&sortDirection={sort_direction}&_=1468875090671'

for attribute in attribute_list:
    for order in sort_directions:
        start=0
        for i in range(2):
            print('getting results for', attribute, 'start index' , start, 'sorting direction', order)
            get_url = url.format(startindex=start, pageSize=num_results, attribute=attribute, sort_direction=order)
            print(get_url)
            response = requests.get(get_url)
    
            if response.status_code == 200  :#request was successful 
                json_data = response.json()
    
                for item in json_data['results'] : 
                    diamond = { 'id' : item['id'],
                               'carat' : item['carat'][0],
                               'shapeName' : item['shapeName'][0],
                               'clarity' : item['clarity'][0],
                               'color' : item['color'][0],
                               'culet': item['culet'][0],
                               'cut' : item['cut'][0]['label'],
                               'depth' : item['depth'][0],
                               'fluorescence' : item['fluorescence'][0],
                               'lxwRatio' : item['lxwRatio'][0],
                               'polish' : item['polish'][0],
                               'symmetry' : item['symmetry'][0],
                               'table' : item['table'][0],
                               'price' : item['price'][0]
                               }
                    diamond_list.append(diamond)
    
                start = start +num_results
                time.sleep(60) # api blocks if too many requests received, sleep for a min
        else : 
                print('Error getting data')

    
diamonds = pd.DataFrame(diamond_list)
diamonds = diamonds.drop_duplicates()
print(diamonds.shape)
diamonds.to_csv('bluenile.csv', index=False)