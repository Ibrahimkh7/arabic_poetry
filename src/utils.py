
# We should create a normalizing function for a consistent processing phase
# and we could also use it on the user querie

def read_arabic_dataset(name):
    assert name[-4:] == '.txt', "this is not a dataset"
    dataset = pd.read_csv(name, on_bad_lines= 'skip')
    # for this specific dataset there is a column called 
    # this step is not necessary since this column will not intervene in the processing phase
    # It's just neater
    try:
        dataset.drop('Unnamed: 6', axis=1)
    except:
        print('There is no such file in the dataset')
def clean_data(dataset):
    dataset.fillna('', inplace = True)
    #Might add additional stuff in case