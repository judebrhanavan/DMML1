import requests
import pandas as pd
import time


num_results= 1000
diamond_list =[]
attribute_list =['color', 'price', 'skus', 'clarity','depth','table', 'lxwRatio', 'fluorescence', 'polish', 'symmetry', 'dateSet','culet']
url= 'https://www.bluenile.com/api/public/diamond-search-grid/v2?country=USA&currency=USD&startIndex=0&pageSize={pageSize}&shape=RD&sortColumn={attribute}&sortDirection=desc&_=1468875090671'

for attribute in attribute_list:
    print('getting results for', attribute)
    get_url = url.format(pageSize=num_results, attribute=attribute)
    print(get_url)
    response = requests.get(get_url)
    
    if response.status_code == 200  :#request was successful 
        print('Request success' , attribute)
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
    else : 
        print('Error getting data')
    time.sleep(60) # api blocks if too many requests received, sleep for a min
    
diamonds = pd.DataFrame(diamond_list)
diamonds = diamonds.drop_duplicates()
print(diamonds.shape)
diamonds.to_csv('bluenile_desc.csv', index=False)

df_asc = pd.read_csv('bluenile.csv')

df_bf = pd.concat([diamonds, df_asc], axis=0)
df_bf = df_bf.drop_duplicates()
df_bf.to_csv('bluenile_xl.csv', index=False)