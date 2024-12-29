#libraries:
import pandas as pd
from math import log10


# We will base it on tf-idf on the poem_text
#so the similarity would be weighted on the rarity of words used by the user input
# we'll work with dictionnaries cz it is more efficient

#we'll create a mapping from the word to the word count in each poem and then in another function we'll compute the necessary computations
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
            #2 cases are present either the char is already in our dictionnary or is not
            if char in dict_map: 
                #2 cases are present so we have the charachter but either the specific poem is not discovered yet so we need to add to the dictionnary a new key with value 1
                if poem_name not in dict_map[char]:
                    dict_map[char][poem_name] = 1 
                #or the poem_name is already discovered and it is not the first time this charachter is mentioned for this specific poem
                else:
                    dict_map[char][poem_name] +=1
            if char not in dict_map:
                #each poem is gonna have its own term frequency 
                dict_map[char] = {poem_name:1}
    return dict_map
    #we could convert it to a dataframe so that we could better visualize it

#Remember: dict_map is gonna be the charachter mapped to the poem_name which is mapped to the word frequency
#e.g. D1 = "I love cookies", D2 = "I love football" 
#the desired output of the program is gonna be:
#{"I": {D1:1, D2:1}, "love": {D1:1, D2:1}, "cookies": {D1:1}, "football": {D2:1}}

#important notice we should NOT forget to fillnas with zeros when we transform to a dataframe
#or we take a condition later on while calculating the tfidf stating that if the document is not mentioned it should assign 0 to the mapping

#note we could transform this to a pd library using:
# mapping = pd.DataFrame.from_dict(dict_map, orient="index")

def map_wrd_to_poemname_and_tf(dataset, poem_content_col_name , poem_name_col):
# we'll do it on the contents of the poem
    dict_frequency = map_wrd_to_wordcount_and_poemname(dataset, poem_content_col_name, poem_name_col)

    nb_of_rows = len(dataset)
    #we will loop over all poems and get their length and modify the values in dict_freq
    for row in range(nb_of_rows):
        poem_content = dataset.iloc[row][poem_content_col_name].split()
        poem_name = poem_name_col
        nb_words_in_poem = len(poem_content)
        #updating the dict_frequency for each value for the corresponding poem
        for char in dict_frequency:
            if poem_name in dict_frequency[char]:
                dict_frequency[char][poem_name] = dict_frequency[char][poem_name]/nb_words_in_poem
    
    
    #now dict_frequency is the dictionnary of frequency/total nb of words thus
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

#############################################
#Useless
    # map_wrd_to_poem={}
    # map_wrd_tf = {}
    # for char in map_wrd_to_freq_and_poems:
    #     map_wrd_to_poem[char] = map_wrd_to_freq_and_poems[char][1] # this will map words to the poems it was mentioned in
##############################################

    
#let's get the idf:

    map_wrd_idf = map_wrd_to_idf(dataset, poem_content_col_name)

#now we're gonna perform tf*idf by modifying the tf dict_map

    for char in map_wrd_to_freq_and_poems:
        for poem in map_wrd_to_freq_and_poems[char]:
            map_wrd_to_freq_and_poems[char][poem] = map_wrd_to_freq_and_poems[char][poem] * map_wrd_idf[char]
    
    #now the tf dict_mapping is transformed to the tf-idf mapping of each word to the corresponding poem and tf-idf score
    tf_idf_mapping = map_wrd_to_freq_and_poems
    return tf_idf_mapping

#To visualize do the same thing as we did with the tf

      




# from sklearn.feature_extraction.text import TfidfVectorizer
# import pandas as pd
# #directly using it

# # a draw back is that we did not keep track of the poems that the rare words were mentioned in

# def map_poem_name_to_idf(dataset, poem_content_col_name , poem_name_col):
#     vectorizer = TfidfVectorizer()
    
#     poems = dataset[poem_content_col_name].values.tolist()
    
#     tfidf_matrix = vectorizer.fit_transform(poems)

#     tfidf_array = tfidf_matrix.toarray()
#     feature_names = vectorizer.get_feature_names_out()
#     dataframe_tfidf = pd.DataFrame(tfidf_array, columns= feature_names)
#     return dataframe_tfidf
