#!/usr/bin/env python3

from gato_eda import *

# Reading data
dataframe = pd.read_csv('out.csv')

print("------------------------------------------------------")
print("Beggining of the information: ")

#information = 
print("******************************************************")
print(get_invalid_values(dataframe))
print("******************************************************")                         
print("******************************************************") 
dictionary = feature_observe(dataframe)
'''
message = dictionary['message']
columns_missing_between_zero_and_five_pct = dictionary['features less than 5%']
columns_missing_more_than_five_pct = dictionary['features over 5%']'''

for i, j in dictionary.items():
    print(f'{i}: {j}')
    
'''
print(message)##
print(columns_missing_between_zero_and_five_pct)##
print(columns_missing_more_than_five_pct)##'''
print("******************************************************")                         
print("******************************************************") 
print('Missing:')
print(miss_df(dataframe))

print("******************************************************")                         
print("******************************************************") 
sift = sift_data_type(dataframe)
for i, j in sift.items():
    print(f'{i}: {j}')                         
print("******************************************************") 
print('invalid items:')
inval = get_invalid_values(dataframe)
print(inval)
## transforming the invalid item.
df = transform_to_nan("--", dataframe, "categories")
print('filling in nans')
df_mode = filler_of_the_nans('mode', df, ['categories'])
df_mean = filler_of_the_nans('mean', df_mode, ['normal'])
df_final = filler_of_the_nans('interpolate', df_mean, ['continuous'])

print(df_final.to_markdown(index=False))
    
print("End of the information: ")

print("******************************************************")                         
print("******************************************************") 
print("empirical rule")
print(empirical(df, 'normal'))

print("******************************************************") 
print("Stats")
print(estadisticas(df_final, 'continuous'))


print("******************************************************") 
print("plots")
print(distribution(df_final, 'normal'))



