import pandas as pd

II_c0 = pd.read_csv("C://Users//arado//Desktop//Full_Stack_Final_Project//CollabFiltering//Item-Item_c0.csv")
II_c1 = pd.read_csv("C://Users//arado//Desktop//Full_Stack_Final_Project//CollabFiltering//Item-Item_c1.csv")
II_c2 = pd.read_csv("C://Users//arado//Desktop//Full_Stack_Final_Project//CollabFiltering//Item-Item_c2.csv")
II_c3 = pd.read_csv("C://Users//arado//Desktop//Full_Stack_Final_Project//CollabFiltering//Item-Item_c3.csv")
II_c4 = pd.read_csv("C://Users//arado//Desktop//Full_Stack_Final_Project//CollabFiltering//Item-Item_c4.csv")
II_c5 = pd.read_csv("C://Users//arado//Desktop//Full_Stack_Final_Project//CollabFiltering//Item-Item_c5.csv")
II_c6 = pd.read_csv("C://Users//arado//Desktop//Full_Stack_Final_Project//CollabFiltering//Item-Item_c6.csv")
II_c7 = pd.read_csv("C://Users//arado//Desktop//Full_Stack_Final_Project//CollabFiltering//Item-Item_c7.csv")
II_c8 = pd.read_csv("C://Users//arado//Desktop//Full_Stack_Final_Project//CollabFiltering//Item-Item_c8.csv")
II_c9 = pd.read_csv("C://Users//arado//Desktop//Full_Stack_Final_Project//CollabFiltering//Item-Item_c9.csv")
II_c10 = pd.read_csv("C://Users//arado//Desktop//Full_Stack_Final_Project//CollabFiltering//Item-Item_c10.csv")
II_c11 = pd.read_csv("C://Users//arado//Desktop//Full_Stack_Final_Project//CollabFiltering//Item-Item_c11.csv")
II_c12 = pd.read_csv("C://Users//arado//Desktop//Full_Stack_Final_Project//CollabFiltering//Item-Item_c12.csv")
II_c13 = pd.read_csv("C://Users//arado//Desktop//Full_Stack_Final_Project//CollabFiltering//Item-Item_c13.csv")
II_c14 = pd.read_csv("C://Users//arado//Desktop//Full_Stack_Final_Project//CollabFiltering//Item-Item_c14.csv")
II_c15 = pd.read_csv("C://Users//arado//Desktop//Full_Stack_Final_Project//CollabFiltering//Item-Item_c15.csv")
II_c16 = pd.read_csv("C://Users//arado//Desktop//Full_Stack_Final_Project//CollabFiltering//Item-Item_c16.csv")
II_c17 = pd.read_csv("C://Users//arado//Desktop//Full_Stack_Final_Project//CollabFiltering//Item-Item_c17.csv")
II_c18 = pd.read_csv("C://Users//arado//Desktop//Full_Stack_Final_Project//CollabFiltering//Item-Item_c18.csv")
II_c19 = pd.read_csv("C://Users//arado//Desktop//Full_Stack_Final_Project//CollabFiltering//Item-Item_c19.csv")

II_cs = [II_c0, II_c1, II_c2, II_c2, II_c4, II_c5, II_c6, II_c7, II_c8, II_c9, II_c10, II_c11, II_c12, II_c13, II_c14, II_c15, II_c16, II_c17, II_c18, II_c19]

def get_ii_filters_with_leba(leba):
    """
    Find DataFrames from II_cs that contain the specified column name.
    
    Parameters:
    -----------
    leba 
        The column name to search for in the DataFrames
    
    Returns:
    --------
    list
        A list of DataFrames that contain the specified column
    """
    return [df for df in II_cs if leba in df['Label Encoded Book-Author'].to_list()]


def updated_itemBCFRatingPredict(data=pd.Series, l = float()):
    '''
    1. take Series data from itemBasedCollabFilter method:
    2. loop through the books which were highly correlated with input book from prev method
    3. Return the list of numBooks number of books
    '''
    global b
    
    ret_list = []
    for s in data.index.to_list():

        #print('Current s value: ' + s)

        L = b.where(b['Label Encoded Book-Author'] == int(s))['AuthorTitleString'].dropna()
        #print('Current L Value: ', L)

        cor = L.iloc[0]
        #print('Current c Value: ', cor)

        ret_list.append(cor)
    
    return ret_list

# Function to search books by title
def user_search_for_books(query):
    # Case-insensitive search
    books = b[b['AuthorTitleString'].str.contains(query, case=False, na=False)]
    return books

def user_book_query():
    # Example usage
    user_query = input("Enter book title or keyword: ")

    officialBookNames = user_search_for_books(user_query)['AuthorTitleString'].unique()

    if officialBookNames.any():
        print(f'Number of Matches found for "{user_query}": {len(officialBookNames)}\n')
        print("Books Found:")

        foundSpecificBook = False
        i=0
        while not foundSpecificBook:

            print(officialBookNames[i])
            nextbook = input('Was this the book you were looking for (Y / N / END)?')

            if nextbook == 'Y':
                foundSpecificBook = True
                return officialBookNames[i]
            
            elif nextbook == 'END':
                return None
            
            else:
                i+=1
    else:
        print("No books found matching your query.")
        return None

def get_recommendations(numReturns = 5):
    book_name = user_book_query()

    #index = title_author[title_author['AuthorTitleString'] == book_name]

    LEBA = set(b.where(b['AuthorTitleString'] == book_name)['Label Encoded Book-Author'].dropna()).pop()


    try: 
        #Determine the dataframe which contains: Label encoded book author (leba)
        y = get_ii_filters_with_leba(LEBA)[0].set_index('Label Encoded Book-Author').T

        numReturns = numReturns
        #cell output
        return(f'Top {numReturns} Similar Reads to ({book_name}) ---> {updated_itemBCFRatingPredict(data = y[LEBA].sort_values(ascending=False)[1:numReturns+1])}')

    except:
        print('\n')
        print("An exception occurred")
        print('\n')
        print('Likely Not enough ratings')
