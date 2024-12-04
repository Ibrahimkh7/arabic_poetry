
#the following function will return a the types extracted from the dataset
def get_types_from_dataset(dataset, col_containing_type):
    #col_name_as_str
    unique = dataset[col_containing_type].unique()
    #unique will give us the uniquness of the tags as a whole not specifically the ones of the type but this would reduce the loop size
    nb_unique_elements = len(unique)
    types = set()
    #loop over all indices
    for element_index in range(nb_unique_elements):
        #have a variable to check if it is already there
        present = False
        # have the element as a variable
        element = unique[element_index]

        #dissect the whole text so that we could isolate our type
        element_list = str(element).split(',')
        type_p = element_list[0]
        if type_p in types: #checking if it is already in this
            present = True
        elif not present and type_p.split(' ')[0] == 'قصائد': #the second condition is to ensure that the extracted is indeed a type
            types.add(type_p)    
    return types

#this function will return to us values like: 'قصائد شوق' thus to isolate the type we'll implement the following function
def isolating_type(dataset, col_name_as_str):
    unique_types = set()
    general_type = get_types_from_dataset(dataset, col_name_as_str)
    for general in general_type:
        name = general.split()[1] #this is to get the type alone
        if name[:2] == 'ال': #removing al taarif from the unique types
            name = name[2:]
        #adding it to the set:
        unique_types.add(name)
    return unique_types


