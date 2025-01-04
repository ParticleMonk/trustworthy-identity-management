# import openai library
from openai import OpenAI
from pydantic import BaseModel
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

class Classifcations(BaseModel):
    title: str
    classification: str
    classifications: list[str]
def openai_api_call(prompt):
    client = OpenAI(api_key=OPENAI_API_KEY)
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        response_format=Classifcations
    )

    return completion


def openai_prompt_creating(title, classifications, classification_dict):
    prompt = (
        f"Does the title '{title}' belong mostly in one of the following classifications: {classifications}? If not, please provide a new classification for the title"
        # f"and add that new classification to the list of classifications."
        # f" Have your response be in the format of 'Title - Classification : Classification_list'. "
        # f"For example, 'How to write a book - Writing Ideas : 'Writing Ideas', 'Software Projects'..."
    )
    print('Title:', title)
    print('Classifications:', classifications)
    response = openai_api_call(prompt)
    # parse the response from the openai api

    title_classification = response.choices[0].message.parsed
    print("[0] response.choices from open ai:", title_classification)
    print("\nThe Type of the ojbects just printed:", type(title_classification))

    classification_list = title_classification.classifications
    classifications = [c.strip() for c in classification_list]
    classification_dict[title] = title_classification.title


def classify_titles(df, classifications=["none"]):
    if classifications[0] == "none":
        classifications = ["Software Project", "Writing Ideas", "Things You've Learned"]

    classification_dict = {}
    print(df.head())
    total = len(df)
    print(f"Beginning classification process for {total} titles...")

    for i, title in enumerate(df, start=1):
        print(f"Classifying {i}/{total} titles: {title}")
        openai_prompt_creating(title, classifications, classification_dict)

    print("All titles classified.")
    return classifications, classification_dict



# Example usage:
if __name__ == "__main__":
    # Load the JSON data into a DataFrame
    df = load_json_to_df(r"C:\Users\edens\Downloads\ChatGPTRawData_2024-08-03\conversations.json")
    #
    # # Print the first 5 rows of the DataFrame
    print_df(df)

    #drop all the columns except the title column
    df = df["title"]

    # save the df to a json file
    df.to_json("titles.json")

    print("DF object shape:", df.shape)
    print("head before pass through;\n" ,df.head())


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

