
# we'll isolate the important words in the user input and return them
# using the common words used in arabic for demanding stuff

def getting_keyword_from_user_input(user_input):
    #there are common words used to request a poem so we'll put them in this list 
    common_words = ["أعطني", "ابحث", "أريد", "أطلب", "هات", "أرني", "اعثر", "قصيدة", "عن","في","كي"]
    #now we'll split the input into different words
    wrds_in_input = user_input.split()
    
    important_words = []
    #we're gonna remove the common words from the phrase
    for wrd in wrds_in_input:
        if wrd not in common_words:
            important_words.append(wrd)
    return important_words

#next we'll check if the user mentioned the specific type
from .preprocess_data import isolating_type

types = isolating_type(dataset, col_name_as_str)
def imprt_words_and_check_type(s, types):
    #we'll get the imprt words
    imprtant_wrds = getting_keyword_from_user_input(s)
        
    keywords = types
    #we will loop over them to check for the type in case of the possible flaw mentioned below:
    for typ in keywords:
        if typ in s:
            return(typ, imprtant_wrds)
    # if the user did not mention any type that our dataset has then the type must be -1
    return (-1, imprtant_wrds)

#we could also do more functions regarding the era the poet to be even more precise
