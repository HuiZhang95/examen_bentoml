# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pathlib import Path
import click
import logging
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from check_structure import check_existing_file, check_existing_folder
import os

@click.command()
@click.argument('input_filepath', type=click.Path(exists=False), required=0)
@click.argument('output_filepath', type=click.Path(exists=False), required=0)

def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../preprocessed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    # Prompt the user for input file paths
    # input_filepath= click.prompt('Enter the file path for the input data', type=click.Path(exists=True))
    input_filepath = './data/raw'
    output_filepath = './data/processed'
    input_file = f"{input_filepath}/admission.csv"
    # output_filepath = click.prompt('Enter the file path for the output preprocessed data (e.g., output/preprocessed_data.csv)', type=click.Path())
    
    # Call the main data processing function with the provided file paths
    process_data(input_file, output_filepath)

def process_data(input_file, output_folderpath):
 
    #--Importing dataset
    df = pd.read_csv(input_file, index_col = 0)
    df.rename(columns = {'GRE Score':'GRE_Score', 'TOEFL Score':'TOEFL_Score', 'University Rating':'University_Rating', 'Chance of Admit ':'Chance_of_Admit'}, inplace = True)

    #--train test split
    target = df['Chance_of_Admit']
    data = df.drop(columns = ['Chance_of_Admit'])
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size = 0.2)

    #--rescale data
    scaler = preprocessing.MinMaxScaler()
    scaler.fit(X_train)
    X_train_scaled = pd.DataFrame(scaler.transform(X_train), index=X_train.index, columns=X_train.columns)
    X_test_scaled = pd.DataFrame(scaler.transform(X_test), index=X_test.index, columns=X_test.columns)

    
    #--Saving the dataframes to their respective output file paths
    for file, filename in zip([X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test], ['X_train', 'X_test', 'X_train_scaled', 'X_test_scaled', 'y_train', 'y_test']):
        output_filepath = os.path.join(output_folderpath, f'{filename}.csv')
        if check_existing_file(output_filepath):
            file.to_csv(output_filepath, index=False)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]


    main()
