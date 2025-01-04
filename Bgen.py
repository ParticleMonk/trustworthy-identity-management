import json
from openai import OpenAI
from openai.types.chat import ChatCompletion
from pydantic import BaseModel, Field
from typing import List, Optional
import pandas as pd
import os
import datetime

import sys
import string


# Pydantic model for structured output from the API
class GroupedTitles(BaseModel):
    group_name: str = Field(description="The name of the group the titles belong to.")
    titles: List[str] = Field(description="List of titles belonging to the group.")


class Classifications(BaseModel):
    list_of_groups: List[GroupedTitles] = Field(description="A list of the group names.")
    # classifications: List[str]


def group_conversation_titles(json_file_path):
    """
    Groups conversation titles from a ChatGPT JSON file based on implied meaning.

    Args:
        json_file_path: Path to the JSON file.

    Returns:
        A completion from the API
    """

    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)
        titles = [v for v in data.values()]
    except IOError:
        print('Could not load Titles JSON, check the filename/location.')
        return None

        # Construct the prompt for the OpenAI API
        # Call the OpenAI API
    prompt = f"Group the following conversation titles into meaningful categories based on their content:\n\n{', '.join(titles)}"
    return client.chat.completions.create(
        model="gpt-4o-mini",  # Or gpt-3.5-turbo, depending on your access
        messages=[
            {"role": "developer", "content": "You are a helpful assistant that groups items into categories."},
            {"role": "user", "content": prompt}
        ],
        functions=[
            {
                "name": "group_titles",
                "description": "Groups conversation titles into categories.",
                "parameters": Classifications.schema()
            }
        ],
        function_call={"name": "group_titles"}
    )


def check_for_saved_arguments_file(filename):
    dt = datetime.datetime
    temp: bool = (os.path.exists(filename)
                  and os.stat(filename).st_size > 0
                  and os.stat(filename).st_mtime >= int(dt.combine(dt.utcnow().date(), datetime.time()).timestamp()))
    return temp


def save_response_file(args, filename):
    print('Saving response file.. .. ..')
    try:
        with open(filename, "w") as fout:
            json.dump(args, fout, indent=4)
        print('Response file saved.')
    except IOError:
        print('Error while saving file!!')


def load_response_file(filename: str) -> dict:
    with open(filename, "r") as fin:
        print("Reading saved response.. .. ..")
        print("Response file successfully loaded.")
        return json.load(fin)


if __name__ == "__main__":
    client = OpenAI()
    OpenAI.api_key = os.environ['OPENAI_API_KEY']

    response_file: str = 'response.json'
    arguments: dict = {}

    'If there is an appropriate response file, load it'
    if check_for_saved_arguments_file(filename=response_file):
        arguments = load_response_file(filename=response_file)
    else:
        'Otherwise get a chat completion response from the API ($$)'
        response_full: ChatCompletion = group_conversation_titles(json_file_path='titles.json')
        arguments = json.loads(response_full.choices[0].message.function_call.arguments)
        save_response_file(arguments, response_file)

    'Format response through Classifications Class'
    # grouped_data = Classifications(**arguments)

    'Put into a DataFrame'
    df1: pd.DataFrame = pd.json_normalize(arguments['list_of_groups'])
    df2: pd.DataFrame = pd.json_normalize(arguments['list_of_groups']).explode('titles')

    'Print from DataFrame'
    print(df1)
    print('\n\n')
    print(df2)


# Notes for working with JSON -> DataFrame
# Extract and parse the structured output

# Create a Pandas DataFrame from the structured output
# df = pd.DataFrame(
#    {"group_name": [grouped_data.group_name] * len(grouped_data.titles), "title": grouped_data.titles})
# return df

# # Example print statements to inspect output
# print(df.groupby('group_name')['title'].apply(list))
# print(df['group_name'].unique())
