#libraries:
import pandas as pd
from math import log10


# We will base it on tf-idf on the poem_text
#so the similarity would be weighted on the rarity of words used by the user input
# we'll work with dictionnaries cz it is more efficient

#we'll create a mapping from the word to the word count in each poem and then in another function we'll compute the necessary
# we're doing it across ALL poems so that the tf-idf would reflect the uniquness of the charachters




def map_wrd_to_wordcount_and_poemname(dataset, poem_content_col_name, poem_name_col):
# this will give us a dictionnary with keys -> charachters/words and value -> the list: [the nb of occurence across all poems, name of poems it occured in
    nb_of_rows = len(dataset)
    dict_map = {}
    for row_i in range(nb_of_rows):
        all_charachters_in_poem_of_index_i = dataset.iloc[row_i][poem_content_col_name].split()
        #we will append it to the dicttionnary while keeping track of the names of the poems that we encountered
        poem_name = dataset.iloc[row_i][poem_name_col]
        for char in all_charachters_in_poem_of_index_i:
            if char in dict_map:
                if poem_name not in dict_map[char][1]:
                    dict_map[char][0] +=1
                    dict_map[char][1].append(poem_name)
                else:
                    dict_map[char][0] +=1
            if char not in dict_map:
                dict_map[char] = (1,[poem_name])
    return dict_map
    #we could convert it to a dataframe but not necessary



def map_wrd_to_poemname_and_tf(dataset, poem_content_col_name , poem_name_col):
# we'll do it on the contents of the poem
    dict_frequency = map_wrd_to_wordcount_and_poemname(dataset, poem_content_col_name, poem_name_col)
    #now we got the document frequency let's get the tf:
    
    total = 0

    #now getting the total number of words in all of the poems
    for key in dict_frequency:
        total += dict_frequency[key][0]
    
    #modifying the values
    for key in dict_frequency:
        dict_frequency[key][0] = dict_frequency[key][0] / total 
    
    #now dict_frequency is the dictionnary of frequuency/total nb of words thus
    dict_tf = dict_frequency
    return dict_tf


#so now we are searching the inverse- DOCUMENT - frequency thus we can't use map_poem_to_wordcount 
# cz this counts the frequency as a whole

#document frequency:
def map_wrd_to_document_frequency(dataset, poem_content_col_name):
    dict_map = {}

    total_rows = len(dataset[poem_content_col_name]) 
    useless_rows =  sum(dataset[poem_content_col_name].isnull()) 
    nb_of_rows = total_rows - useless_rows

    for row_i in range(nb_of_rows):
        all_charachters_in_poem_of_index_i = dataset.iloc[row_i][poem_content_col_name].split()
#we won't add it the poem name because we already we added the while computing the term-frequenc mapping
#i.e. we got all the poems where a certain charachter was mentioned in the process of computing the dict_map of the tf
        for char in all_charachters_in_poem_of_index_i:
            if char not in dict_map:
                dict_map[char] = 1

    return dict_map


# the formula for idf log(1+N/1+dict_map[key])
# we're adding one to prevent division by zero and to prevent log(0)

def map_wrd_to_idf(dataset, poem_content_col_name):
# we'll do it on the contents of the poem

    dict_map_df = map_wrd_to_document_frequency(dataset, poem_content_col_name)

#it is inevitable that there are null values thus we need to 
 
    nb_of_rows = len(dataset)
    nb_of_null_rows = sum(dataset[poem_content_col_name].isnull())
    nb_non_null_poems =  nb_of_rows - nb_of_null_rows

#now we're gonna compute the idf and return the dictinary relating the charachters to their corresponding idf value
    for i in dict_map_df:
        dict_map_df[i] =  log10((1+nb_non_null_poems)/ (dict_map_df[i]+1))
# now we got the characters mapped to the idf

#It is time for the TF-IDF mapping!:

def map_wrd_to_tfidf(dataset, poem_content_col_name, poem_name_col):
    map_wrd_to_freq_and_poems = map_wrd_to_poemname_and_tf(dataset, poem_content_col_name, poem_name_col)
    
    map_wrd_to_poem={}
    map_wrd_tf = {}
    for i in map_wrd_to_freq_and_poems:
        map_wrd_to_poem[i] = map_wrd_to_freq_and_poems[i][1] # this will map words to the poems it was mentioned in

#Maybe It would be better to dissect it into 2 from the start or no?


        map_wrd_tf[i] =  map_wrd_to_freq_and_poems[i][0]
    
#let's get the idf:

    map_wrd_idf = map_wrd_to_idf(dataset, poem_content_col_name)

#now we're gonna perform tf.idf
    tf_idf_map = {}
    for i in map_wrd_idf:
        tf_idf_map[i] = map_wrd_idf[i] * map_wrd_tf[i] 
    
    return (tf_idf_map, map_wrd_to_poem)
