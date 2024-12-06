#libraries:
import pandas as pd
import math


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
def map_wrd_to_document_frequency_and_poemname(dataset, poem_content_col_name , poem_name_col):
    dict_map = {}
    for row_i in range(nb_of_rows):
        all_charachters_in_poem_of_index_i = dataset.iloc[row_i][poem_content_col_name].split()
    #we will append it to the dicttionnary while keeping track of the names of the poems that we encountered
        poem_name = dataset.iloc[row_i][poem_name_col]
        for char in all_charachters_in_poem_of_index_i:
            if char in dict_map and poem_name not in dict_map[char][1]:
                dict_map[char][1].append(poem_name)

            if char not in dict_map:
                dict_map[char] = (1,[poem_name])
    return dict_map
# the formula for tf-idf log(1+N/1+dict_map[key][1])
# we're adding one to prevent division by zero and to prevent log(0)

def map_wrd_to_poemname_and_idf(dataset, poem_content_col_name , poem_name_col):
# we'll do it on the contents of the poem

    dict_map_document = map_wrd_to_document_frequency_and_poemname(dataset, poem_content_col_name , poem_name_col)

#it is inevitable that there are null values thus we need to 
 
    nb_of_rows = len(dataset)
    nb_of_null_rows = sum(dataset[poem_content_col_name].isnull())
    non_null_poems =  nb_of_rows - nb_of_null_rows

#now we're gonna compute the idf and return the dictinary relating the charachters to their corresponding idf value


""""
To    DOOO:
get the idf mapping to the charachters
""""

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
