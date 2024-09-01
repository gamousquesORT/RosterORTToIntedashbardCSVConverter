from math import isnan

import pandas
import pandas as pd
import re
import sys
import os

from numpy.f2py.auxfuncs import l_not

#user_file_name = ""
output_file_name = ""

def request_file_name() -> str:
    user_typed_filename = ""
    while True:
        user_typed_filename = input("Please enter the Excel file name: ")
        if user_typed_filename == "":
           return ""

        if not user_typed_filename.endswith('.xlsx'):
            print('Please provide an Excel file (.xlsx) as input.')
            continue
        else:
            break

    return user_typed_filename

def split_name(full_name):
    # Regex to match the name format "Fathername MotherName, FirstName SecondaName (ID)"
    match = re.match(r'[^,]*,\s*(\S+)\s+(\S+)\s+\((\d+)\)', full_name)
    if match:
        return match.group(1), match.group(2), match.group(3)
    return None, None, None

# Function to extract lastname
def extract_lastname(text):
    if pandas.isna(text):
        return "-- "
    return text.split(',')[0].strip()

# Function to extract firstname
def extract_firstname(text):
    if pandas.isna(text):
        return "-- "
    return text.split(',')[1].strip()

# Function to extract id
def extract_id(text):
    if pandas.isna(text):
        return "-- "
    return text.split(',')[2].strip()

def split_name(full_name):
    first_name = None
    last_name = None
    number = None

    # Regex to match the name format "FirstName, LastName (Number)"
    if pandas.isna(full_name):
        return first_name, last_name, number

    match = re.match(r'([^,]+),\s*([^()]+)\s*\((\d+)\)', full_name)
    if match:
        first_name = match.group(1).strip()
        last_name = match.group(2).strip()
        number = match.group(3).strip()
        return first_name, last_name, number
    return first_name , last_name , number

def convert_ORT_roster_to_intedashboard(file_name, output_file_name):

    df_original = pd.read_excel(file_name)

    if 'Nombre' not in df_original.columns:
        print("Error: 'Nombres' column not found in the Excel file.")
        exit(1)

    output_dict = {}


    output_dict['First Name'],output_dict["Last Name"], output_dict['Student ID']   =  df_original['Nombre'].apply(split_name)


    df_new = df_original.DataFrame(output_dict)


    print(df_new)

    df_new.to_csv(output_file_name, index=False)

    print('CSV file has been created successfully.')


def get_filepath(file_name):
    # Construct the full file path
    file_path = os.path.join('./data' , file_name)
    return file_path

def get_executing_folder():
    return os.path.abspath(os.path.dirname(__file__))


if __name__ == '__main__':
    user_file_name = request_file_name()
    if user_file_name == "":
        print("Thank you for using the program.")
        sys.exit(0)
    else:
        file_name = get_executing_folder() + "/data/" + user_file_name
        output_file_name = get_executing_folder() + "/data/" + user_file_name + "_output.csv"
        convert_ORT_roster_to_intedashboard(file_name, output_file_name)