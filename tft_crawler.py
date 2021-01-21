from bs4 import BeautifulSoup
import requests
import re
import lxml
from selenium import webdriver
import pandas as pd
import numpy as np
browser = webdriver.Chrome(executable_path=r'chromedriver.exe')
url = 'https://tftactics.gg/champions'
browser.get(url)

html = browser.page_source

###Get all champion names
tft_champ_list = browser.find_element_by_class_name("characters-list")
champion = tft_champ_list.text
champion = champion.replace(' ', '_')
champion = champion.replace('\n', ' ')
champion_list = list(champion.split(" "))
champion_list = [x.lower() for x in champion_list]

traits_min_df = pd.DataFrame(columns=['traits', 'min_requirements'])
champion_traits_df = pd.DataFrame(columns=['champion', 'champ_cost', 'traits_1', 'traits_2', 'traits_3'])

###Crawl all champion traits and the minimum requirements to get the traits
for champion_name in champion_list:

    ###Crawl the champions
    browser.get(url + '/' + champion_name)
    traits = browser.find_elements_by_class_name("ability-description")
    champ_cost = int(browser.find_elements_by_class_name("stats-list")[0].text.split('\n', 1)[0].split(' ', 1)[1])
    ###Get the minimum count of traits
    min_counts = browser.find_elements_by_class_name("ability-bonus-count")
    count_list = []
    for i in range(0, len(min_counts)):
        count_list.append(min_counts[i].text)

    count_list = list(map(int, count_list))
    min_traits_list = []
    min_number = 99
    for number in count_list:
        if (number < min_number or min_number == 1) and number != 4:
            min_traits_list.append(number)
        min_number = number

    ###Get the traits
    traits_list = []
    min_counts_list = []
    for j in range(1, len(traits)):
        single_traits = traits[j].text.split('\n', 1)[0]
        min_counts = min_traits_list[j-1]

        print(champion_name)
        print([single_traits, min_counts])
        ###Get the traits and the minimum requirements in the df
        traits_min_df.loc[len(traits_min_df)] = [single_traits, min_counts]

        ###Get all the traits of the champion in a list for the next df
        traits_list.append(single_traits)
    traits_list.insert(0, champ_cost)
    traits_list.insert(0, champion_name)

    ###Insert the information into the dataframe

    if len(traits) == 3:
        traits_list.append(np.nan)
        champion_traits_df.loc[len(champion_traits_df)] = traits_list

    else:
        champion_traits_df.loc[len(champion_traits_df)] = traits_list
    #print(traits_min_df)
    #print(champion_traits_df)

###dropping duplicate values
traits_min_df = traits_min_df.drop_duplicates().sort_values(by='min_requirements')


traits_min_df.to_csv('traits_min_df.csv')
champion_traits_df.to_csv('champion_traits_df.csv')
