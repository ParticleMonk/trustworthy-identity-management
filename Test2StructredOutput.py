# -------------------------------
#  import libraries
# -------------------------------
from openai import OpenAI
from pydantic import BaseModel
import json
import pandas as pd



def print_hi(name):
    """
    Simple function to print a greeting. Example usage: print_hi("Jon")
    """
    print(f'Hi, {name}')


# -------------------------------
#  function to load JSON to DataFrame
# -------------------------------
def load_json_to_df(file_path: str) -> pd.DataFrame:
    """
    Loads data from a JSON file and converts it into a pandas DataFrame.
    Args:
        file_path (str): Path to the JSON file.
    Returns:
        pd.DataFrame: DataFrame containing the JSON data.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)


# -------------------------------
#  function to print the first 5 rows of a dataframe
# -------------------------------
def print_df(df: pd.DataFrame):
    """
    Prints the first 5 rows of the given DataFrame.
    Args:
        df (pd.DataFrame): The DataFrame to print.
    """
    print(df.head())


# -------------------------------
#  function to print column names
# -------------------------------
def print_columns(df: pd.DataFrame):
    """
    Prints the column names of the DataFrame.
    """
    print(df.columns)


# -------------------------------
#  function to print column data types
# -------------------------------
def print_dtypes(df: pd.DataFrame):
    """
    Prints the data types of each column in the DataFrame.
    """
    print(df.dtypes)


# -------------------------------
#  function to print the first item in each column
# -------------------------------
def print_first_item_in_column(df: pd.DataFrame):
    """
    Iterates over each column in the DataFrame and prints the
    first item in that column, prefixed with the column name.
    """
    for column in df.columns:
        print(f"Column: {column}")
        print(df[column].iloc[0])


# -------------------------------
#  function to print the first 5 "title" entries
# -------------------------------
def print_first_5_title_entries(df: pd.DataFrame):
    """
    Prints the first 5 rows from the 'title' column in the DataFrame.
    Args:
        df (pd.DataFrame): The DataFrame containing a 'title' column.
    """
    print(df["title"].head())


# -------------------------------
#  pydantic model for classification responses
# -------------------------------
class Classifcations(BaseModel):
    """
    Pydantic model to parse and validate the classification response
    from the OpenAI API.
    """
    title: str
    classification: str
    classifications: list[str]


# -------------------------------
#  function to call the OpenAI API
# -------------------------------
def openai_api_call(prompt: str) -> Classifcations:
    """
    Sends a prompt to the OpenAI API using the provided prompt string.
    Args:
        prompt (str): The user-defined prompt to pass to OpenAI.
    Returns:
        Classifcations: A Pydantic model containing the parsed response.
    """
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


# -------------------------------
#  function to create the prompt and parse classification
# -------------------------------
def openai_prompt_creating(title: str, classifications: list[str], classification_dict: dict):
    """
    Prepares a prompt that asks the OpenAI API to determine if a given
    title matches any classification in 'classifications'.
    It updates 'classification_dict' with the classification returned
    by the API for that title.

    Args:
        title (str): The textual title to classify.
        classifications (list[str]): Predefined categories for classification.
        classification_dict (dict): Dictionary to store the classifications with keys as titles.
    """
    prompt = (
        f"Does the title '{title}' belong mostly in one of the following "
        f"classifications: {classifications}? If not, please provide a new "
        f"classification for the title"
    )
    print('Title:', title)
    print('Classifications:', classifications)

    response = openai_api_call(prompt)

    # The response from the OpenAI API is expected to be a parsed pydantic model
    title_classification = response.choices[0].message.parsed
    print("[0] response.choices from open ai:", title_classification)
    print("\nThe Type of the objects just printed:", type(title_classification))

    classification_list = title_classification.classifications
    # Clean up any potential whitespace
    classifications = [c.strip() for c in classification_list]

    # Store the classification for the title in the dictionary
    classification_dict[title] = title_classification.title


# -------------------------------
#  function to classify all titles in a DataFrame series
# -------------------------------
def classify_titles(df: pd.Series, classifications: list[str] = ["none"]):
    """
    Iterates over each title in a DataFrame series and uses the
    OpenAI API to classify each title into one of the specified
    classifications. If the default "none" classification is used,
    a default list of classifications is assigned.

    Args:
        df (pd.Series): A series containing titles.
        classifications (list[str]): A list of possible classifications.

    Returns:
        (list[str], dict): A tuple containing the (updated) list of
        classifications and a dictionary with (title -> classification).
    """

    # Provide defaults if 'classifications' is ["none"]
    if classifications[0] == "none":
        classifications = ["Software Project", "Writing Ideas", "Things You've Learned"]

    classification_dict = {}
    print(df.head())

    total = len(df)
    print(f"Beginning classification process for {total} titles...")

    # Loop through each title, pass it to OpenAI, and store the result
    for i, title in enumerate(df, start=1):
        print(f"Classifying {i}/{total} titles: {title}")
        openai_prompt_creating(title, classifications, classification_dict)

    print("All titles classified.")
    return classifications, classification_dict


# -------------------------------
#  main execution
# -------------------------------
if __name__ == "__main__":
    # 1. Load the JSON data into a DataFrame
    df = load_json_to_df(r"C:\Users\edens\Downloads\ChatGPTRawData_2024-08-03\conversations.json")

    # 2. Print the first 5 rows of the DataFrame (for verification)
    print_df(df)

    # 3. Drop all the columns except 'title'
    df = df["title"]

    # 4. Save the series of titles to a separate JSON (for backup/verification)
    df.to_json("titles.json")

    print("DF object shape:", df.shape)
    print("head before pass through:\n", df.head())

    # 5. Classify the titles
    classifications, classification_dict = classify_titles(df)

    # 6. Print the results
    print("Classifications:", classifications)
    print("Classification Dictionary:", classification_dict)

    # 7. Save the classification dictionary and classifications list to JSON files

    '''These are saved in the repo with the names "classification_dict.json" and "classifications.json" '''
    with open("classification_dict.json", "w") as f:
        json.dump(classification_dict, f)
    with open("classifications.json", "w") as f:
        json.dump(classifications, f)
