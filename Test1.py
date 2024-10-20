# import openai library
from openai import OpenAI
import json
import pandas as pd

# Set your OpenAI API key
OPENAI_API_KEY = 



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# import require libraries for json and pandas
import json
import pandas as pd


# load a json file and convert it to a pandas dataframe
def load_json_to_df(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)


# print the first 5 rows of the dataframe
def print_df(df):
    print(df.head())


# print the column names
def print_columns(df):
    print(df.columns)


# print the column data types
def print_dtypes(df):
    print(df.dtypes)


# print the first item from each column labels by its column name
def print_first_item_in_column(df):
    for column in df.columns:
        # print the first item in the column along with its column name
        print(f"Column: {column}")
        print(df[column].iloc[0])


# print the first 5 "title" column entries
def print_first_5_title_entries(df):
    print(df["title"].head())


def openai_api_call(prompt):
    client = OpenAI(api_key=OPENAI_API_KEY)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content.strip()


def openai_prompt_creating(title, classifications, classification_dict):
    prompt = (
        f"Does the title '{title}' belong mostly in one of the following classifications: {classifications}? If not, please provide a new classification for the title"
        f"and add that new classification to the list of classifications."
        f" Have your response be in the format of 'Title - Classification : Classification_list'. "
        f"For example, 'How to write a book - Writing Ideas : 'Writing Ideas', 'Software Projects'..."
    )
    response = openai_api_call(prompt)
    # parse the response from the openai api
    response_list = response.split(":")
    try:
        title_classification = response_list[0].split("-")[1].strip()

    except:
        print('Error on line 84')
        print(response_list)
        exit()
    title_classification = response_list[0].split("-")[1].strip()
    classification_list = response_list[1].split(",")
    classifications = [c.strip() for c in classification_list]
    classification_dict[title] = title_classification


def classify_titles(df, classifications=["none"]):
    # classify the title using openai api
    if classifications[0] == "none":
        classifications = ["Software Project", "Writing Ideas", "Things You've Learned"]
    # define a list of classifications

    # create a dictionary to store title and classification
    classification_dict = {}

    for title in df["title"]:
        openai_prompt_creating(title, classifications, classification_dict)
    # return the classification
    return classifications, classification_dict


# Example usage:
if __name__ == "__main__":
    # Load the JSON data into a DataFrame
    df = load_json_to_df(r"C:\Users\edens\Downloads\ChatGPTRawData_2024-08-03\conversations.json")
    #
    # # Print the first 5 rows of the DataFrame
    print_df(df)
    #
    # # Print the column names
    print_columns(df)
    #
    # # Print the column data types
    print_dtypes(df)
    #
    # # Print the first item in each column
    print_first_item_in_column(df)
    #
    # # Print the first 5 entries of the "title" column
    print_first_5_title_entries(df)
    #
    # # Classify the titles
    classifications, classification_dict = classify_titles(df)
    #
    # # Print the classifications and classification dictionary
    print("Classifications:", classifications)
    print("Classification Dictionary:", classification_dict)

    #save the classification dictionary to a json file and classifications
    with open("classification_dict.json", "w") as f:
        json.dump(classification_dict, f)
    with open("classifications.json", "w") as f:
        json.dump(classifications, f)




    '''#test the openai api call with one title
    title = "How to write a book"
    #create a dictionary to store title and classification
    classification_dict = {}
    classifications = ["Software Project", "Eating", "Things You've Learned"]'''

   # openai_prompt_creating(title, classifications, classification_dict)

    #print("Classification Dictionary after testing one title:", classification_dict)

