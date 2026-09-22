import pandas as pd
import numpy as np
import os
all_dfs = []

JOIN_REGIONS = True
directory = r'C:\Users\Пользователь\Desktop\urfu\anonymized'
for filename in sorted(os.listdir(directory)):
    if not filename.endswith('.csv'):
        continue
    df = pd.read_csv(os.path.join(directory, filename), sep=';')
    df['patient'] = filename[:-4]
    all_dfs.append(df)
big = pd.concat(all_dfs, ignore_index=True)
print(len(big['patient'].unique()))

df['region'] = df['Image context'].str.split(' - ')[1]
print(df['region'].unique())

def join_regions(region):
#Приводит названия областей к укрупнённым группам.
    if pd.isna(region):
        return region
    r = str(region).lower()

    # Лоб: 4 варианта написания
    if ('лоб' in r) or ('лба' in r):
        return 'Лоб'
    # Гусиные лапки (слева/справа)
    if 'гусиные лапки' in r:
        return 'Гусиные лапки'
    # Носогубная складка (левая/правая)
    if 'носогубная складка' in r:
        return 'Носогубная складка'
    # Скула (левая/правая)
    if 'скула' in r:
        return 'Скула'
    # Щека (левая/правая)
    if 'щека' in r:
        return 'Щека'
    return region
if JOIN_REGIONS:
    df['region'] = df['region'].apply(join_regions)