# utilities.py
from fasthtml.common import *
import os
import pandas as pd

def list_files():
    path = 'data'  # Path to your data folder
    return os.listdir(path)

def file_to_table(filename):
    path = os.path.join('data', filename)
    with open(path, 'r') as file:
        lines = file.readlines()
        header = lines[0].strip().split(',')
        body = [line.strip().split(',') for line in lines[1:]]
    return Table(
        Tr(*[Th(h) for h in header]),
        *[Tr(*[Td(cell) for cell in row]) for row in body]
    )

def load_csv_to_dataframe(filename):
    path = os.path.join('data', filename)
    return pd.read_csv(path)

def dataframe_to_table(df):
    header = df.columns.tolist()
    body = df.values.tolist()
    return Table(
        Tr(*[Th(h) for h in header]),
        *[Tr(*[Td(cell) for cell in row]) for row in body]
    )