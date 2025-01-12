import json
from openai import OpenAI
from openai.types.chat import ChatCompletion
from pydantic import BaseModel, Field
from typing import List
import pandas as pd
import os
import datetime


# Pydantic models for structured output from the API
class GroupedTitles(BaseModel):
    group_name: str = Field(description="The name of the group the titles belong to.")
    titles: List[str] = Field(description="List of titles belonging to the group.")


class Classifications(BaseModel):
    list_of_groups: List[GroupedTitles] = Field(description="A list of the group names.")

    # dict_of_grouped_titles: {str, List[str]} =
    # (Field(description="A dict where keys are group names and values are lists of titles that belong in the group."))

    # classifications: List[str]


def group_conversation_titles(json_file_path):
    """
    Groups conversation titles from a ChatGPT JSON file based on implied meaning.

    Args:
        json_file_path: Path to the JSON file.

    Returns:
        A completion from the API
    """
    # FIXME: Send titles in smaller groups via a callback (yet to be written) and put in loop to auto-call till end
    try:
        with open(json_file_path, "r") as f:
            data: dict = json.load(f)
        titles = [v for k, v in data.items() if int(k) < 1000]
    except IOError:
        print('Could not load Titles JSON, check the filename/location.')
        return None

    # Construct the prompt for the OpenAI API
    prompt = (f"Titles:"
              f"\n\n'''{', '.join(titles)}'''***END OF TITLES***")
    dev_message = (f"You are a helpful assistant that iterates thru a list of titles and groups them into "
                   f"meaningful categories. ")

    # Call the OpenAI API
    return client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "developer", "content": dev_message},
            {"role": "user", "content": prompt}
        ],
        response_format=Classifications,
        #temperature=.25
    )


def check_for_saved_arguments_file(filename):
    # FIXME: Mod_time/Midnight comparison needs to be tested
    dt = datetime.datetime
    return (os.path.exists(filename)
            and os.stat(filename).st_size > 0)
    # and os.stat(filename).st_mtime >= int(dt.combine(dt.utcnow().date(), datetime.time()).timestamp()))


def save_response_file(args, filename):
    print('Saving response file.. .. ..')
    try:
        with open(filename, "w") as fout:
            json.dump(args, fout, indent=4)
        print('Response file saved.')
    except IOError:
        print('Error while saving file!!')


def load_response_file(filename: str) -> dict:
    print("Opening saved response file.. .. ..")
    try:
        with open(filename, "r") as fin:
            print("Reading saved response.. .. ..")
            return json.load(fin)
    except IOError or UnboundLocalError:
        fin = False
        print('Error while loading file!!')
    finally:
        if fin:
            print("Response file successfully loaded.")


if __name__ == "__main__":
    client = OpenAI()
    OpenAI.api_key = os.environ['OPENAI_API_KEY']

    response_file: str = 'response.json'
    arguments: dict = {}

    # If there is an appropriate response file, load it
    if check_for_saved_arguments_file(filename=response_file) and True: #FIXME: flag to run API call every time
        arguments = load_response_file(filename=response_file)
    else:
        # Otherwise get a chat completion response from the API ($$)
        response_full: ChatCompletion = group_conversation_titles(json_file_path='titles.json')

        # Debugging FIXME: Remove after debugging
        # print(response_full)
        for i in response_full.usage:
            print(i)
        print(response_full.choices[0].finish_reason)

        arguments = json.loads(response_full.choices[0].message.content)

        save_response_file(arguments, response_file)

    # removed - # Format response through Classifications Class
    # removed - grouped_data = Classifications(**arguments)

    # Put into a DataFrame
    df1: pd.DataFrame = pd.json_normalize(arguments['list_of_groups'])
    df2: pd.DataFrame = pd.json_normalize(arguments['list_of_groups']).explode('titles')

    # Playing with Classifications with a dict
    # df1: pd.DataFrame = pd.json_normalize(arguments)
    # df2: pd.DataFrame = pd.json_normalize(arguments).explode('titles')

    # Print from DataFrame
    if False:
        print(df1)
        print('\n\n')
        print(df2)

# NOTES FOR WORKING WITH JSON -> DATAFRAME
# Extract and parse the structured output

# Create a Pandas DataFrame from the structured output
# df = pd.DataFrame(
#    {"group_name": [grouped_data.group_name] * len(grouped_data.titles), "title": grouped_data.titles})
# return df

# # Example print statements to inspect output
# print(df.groupby('group_name')['title'].apply(list))
# print(df['group_name'].unique())
