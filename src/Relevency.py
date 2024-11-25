# We will base it on tf-idf on the poem_text
#so the similarity would be weighted on the rarity of words used by the user input
# we'll work with dictionnaries cz it is more efficient

def map_poem_name_to_frequency(dataset, poem_content_col_name , poem_name_col):
# we'll do it on the contents of the poem
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
    #now we got the document frequency let's get the tf:
    
    total = 0

    #now getting the total number of words in all of the poems
    for key in dict_map:
        total += dict_map[key][0]
    
    #modifying the values
    for key in dict_map:
        dict_map[key][0] = dict_map[key][0] / total 
    
    return dict_map


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