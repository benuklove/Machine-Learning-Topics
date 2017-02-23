"""

  Created on 1/21/2017 by Ben

  benuklove@gmail.com
  
  

"""

import pandas as pd
from pandas import DataFrame
import numpy as np
import zillow
import time
from apikey import apikey

# Read in relevant data
ar = pd.read_csv('../../../pyjsviz/RealEstate/statewide.csv', low_memory=False)
address_cols = ['NUMBER', 'STREET', 'CITY', 'REGION', 'POSTCODE']
ar_select = ar[address_cols]

# Select only Bella Vista addresses and reset index
bv = ar_select.loc[ar_select['CITY'] == 'Bella Vista'].reset_index(drop=True)

# Check for NaN (and print total)
# print bv.isnull().sum().sum()

# Combine NUMBER and STREET to make ADDRESS column (type: string)
bv['ADDRESS'] = bv[['NUMBER',
                    'STREET',
                    'CITY',
                    'REGION']].apply(lambda x: ' '.join(x), axis=1)


""" Loop over selected rows of bv, get Zillow data, append to df, save to csv"""


def house_info(source_df, start, stop):
    # Gets information from Zillow, returns pandas DataFrame of range of houses
    key = apikey
    houses_df = DataFrame()
    # Call Zillow API for each house
    errors = 0
    successes = 0
    for row in range(start, stop):
        address = source_df.iloc[row][5]
        postal_code = source_df.iloc[row][4]
        api = zillow.ValuationApi()
        # Handle exceptions for lack of information from Zillow
        while True:
            try:
                data = api.GetDeepSearchResults(key, address, postal_code)
                house = {
                    'bathrooms': data.extended_data.bathrooms,
                    'bedrooms': data.extended_data.bedrooms,
                    'sqft': data.extended_data.finished_sqft,
                    'last_sold_price': data.extended_data.last_sold_price,
                    'last_sold_date': data.extended_data.last_sold_date,
                    'lot_size_sqft': data.extended_data.lot_size_sqft,
                    'year_built': data.extended_data.year_built,
                    'comps_link': data.links.comparables,
                    'home_details': data.links.home_details,
                    'graphs_data': data.links.graphs_and_data,
                    'map': data.links.map_this_home,
                    'zestimate': data.zestiamte.amount,
                    'valuation_range_high': data.zestiamte.valuation_range_high,
                    'valuation_range_low': data.zestiamte.valuation_range_low
                    }
                s_house = pd.Series(house, index=['bathrooms', 'bedrooms',
                                                  'sqft', 'last_sold_price',
                                                  'last_sold_date', 'lot_size_sqft',
                                                  'year_built', 'comps_link',
                                                  'home_details', 'graphs_data',
                                                  'map', 'zestimate',
                                                  'valuation_range_high',
                                                  'valuation_range_low'])
                successes += 1
                # print "one pass"
                break
            except ValueError:
                s_house = pd.Series([np.NaN, np.NaN, np.NaN, np.NaN, np.NaN,
                                     np.NaN, np.NaN, np.NaN, np.NaN, np.NaN,
                                     np.NaN, np.NaN, np.NaN, np.NaN],
                                    index=['bathrooms', 'bedrooms',
                                           'sqft', 'last_sold_price',
                                           'last_sold_date', 'lot_size_sqft',
                                           'year_built', 'comps_link',
                                           'home_details', 'graphs_data',
                                           'map', 'zestimate',
                                           'valuation_range_high',
                                           'valuation_range_low'])
                errors += 1
                break
            except:
                s_house = pd.Series([np.NaN, np.NaN, np.NaN, np.NaN, np.NaN,
                                     np.NaN, np.NaN, np.NaN, np.NaN, np.NaN,
                                     np.NaN, np.NaN, np.NaN, np.NaN],
                                    index=['bathrooms', 'bedrooms',
                                           'sqft', 'last_sold_price',
                                           'last_sold_date', 'lot_size_sqft',
                                           'year_built', 'comps_link',
                                           'home_details', 'graphs_data',
                                           'map', 'zestimate',
                                           'valuation_range_high',
                                           'valuation_range_low'])
                errors += 1
                # print "ZillowError likely"
                break
        # Append each new pd.Series house to dataframe, and pause for next loop
        houses_df = houses_df.append(s_house, ignore_index=True)
        time.sleep(1)
    # Log success/error counts
    with open("Errors.txt", "a") as text_file:
        text_file.write("Successes: {} ".format(successes))
        text_file.write("Errors: {}\n".format(errors))
    return houses_df


""" Change 3 sections each time """

# Call the function over desired range (Zillow only allows 1000 calls per day)
new_df = house_info(bv, 13000, 13964)    # start inclusive, stop exclusive

"""set the range of rows on bv in frames for specified range of new_df"""
# Combine the old info with the new, side by side, each row a house
df1 = bv.loc[13000:13963].reset_index()    # start and stop inclusive
result = pd.concat([df1, new_df], axis=1)

# Send final dataframe to csv
result.to_csv('houses14.csv', encoding='utf-8')
