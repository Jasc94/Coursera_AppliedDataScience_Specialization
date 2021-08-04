import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings('ignore')

pd.options.display.max_rows = 4000
import re

# Solution

# Remember to change paths before submission!

def answer_one():
    
    # --- DataFrame - Energy ---
    # Step 1: Import
    Energy = pd.read_excel('/Users/jonathansuarezcaceres/Downloads/1_Data Science/Intro to DS with Python/Course1_Resources/assignments/assignment3/assets/Energy Indicators.xls',
                    usecols = 'C:F', skiprows = 17, nrows=227, na_values = '...')
    
    # Step 2: Columns rename
    Energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    
    # Step 3: Units conversion
    Energy['Energy Supply'] = Energy['Energy Supply'] * 1000000
    
    # Middle step: Index update to country
    Energy = Energy.set_index('Country')
    
    # Step 4: Country renaming
    Energy = Energy.rename(index = {'Republic of Korea' : 'South Korea',
                        'United States of America20' : 'United States',
                        'United Kingdom of Great Britain and Northern Ireland19' : 'United Kingdom',
                        'China, Hong Kong Special Administrative Region3' : 'Hong Kong'})
    
    # Step 5: Country column cleaning
    index = pd.DataFrame(Energy.index)
    new_index = index.replace(to_replace = '[\d]+$', value = '', regex = True)
    Energy.index = new_index['Country']
    
    
    # --- DataFrame - GDP ---
    # Step 1: Import
    GDP = pd.read_csv('Course1_Resources/assignments/assignment3/assets/world_bank.csv',
                 skiprows = 4)
    
    # Middle step: Index update to country
    GDP.set_index('Country Name', inplace = True)
    
    # Step 2: Country renaming
    GDP.rename({'Korea, Rep.' : 'South Korea', 'Iran, Islamic Rep.' : 'Iran',
           'Hong Kong SAR, China' : 'Hong Kong'}, inplace = True)
    
    
    # --- DataFrame - ScimEn ---
    # Step 1: Import
    ScimEn = pd.read_excel('Course1_Resources/assignments/assignment3/assets/scimagojr-3.xlsx')
    
    # Middle step: Index update to country
    ScimEn.set_index('Country', inplace = True)
    
    # --- Merging ---
    # We will first merge ScimEn and GDP
    
    # Step 1: Filtering the top 15 universities
    ScimEn_top = ScimEn[ScimEn['Rank'] < 16]
    
    # Step 2: Filtering the years of interest (2006 - 2015)
    years_of_interest = [str(x) for x in list(range(2006, 2016))]
    GDP_2006_2015 = GDP[years_of_interest]
    
    # Step 3: Now we merge both
    first_merger = pd.merge(ScimEn_top, GDP_2006_2015, how = 'left',
                            left_index = True, right_index = True)
    
    # Step 4: Now we proceed with merging the resulting dataframe with Energy
    final_df = pd.merge(first_merger, Energy, how = 'left', left_index = True,
                       right_index = True)
    
    # Step 5: We set the index to Rank
    #final_df = final_df.reset_index()
    #final_df.set_index('Country', inplace = True)
    
    return final_df
    
    raise NotImplementedError()

df = answer_one()
print(df.columns)