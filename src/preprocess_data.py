#
import argparse
import logging
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='log/preprocess_data.log',
    encoding='utf-8',
    level=logging.DEBUG,
    format='%(asctime)s %(message)s')


IN_FILES = ['data/raw/agg_data.csv']

OUT_TRAIN = 'data/proc/train.csv'
OUT_VAL = 'data/proc/val.csv'

TRAIN_SIZE = 0.9

def main(args):
    df = pd.DataFrame()
    for i in range(len(args.input)):
        df1 = pd.read_csv(args.input[i], delimiter=',')
        df = pd.concat([df, df1], axis=0, ignore_index=True)

    mapping = pd.read_csv('mapping/county.txt', sep='|')
    df = df.merge(mapping, left_on = 'district', right_on = 'district_name',how='left')
    df['county_short'] = np.where( df['county_short'].isna(), 'unknown', df['county_short'])
    df['county_short'] = np.where(df['county_short'] == 'Марьина роща', 'СВАО', df['county_short'])
    df['top_bottom_floor'] =  np.where((df.floor == df.floors_count) | (df.floor == 1), 1, 0)
    df.dropna(inplace=True, subset='district')

    df = pd.get_dummies(df, columns=['county_short', 'object_type'], drop_first=True, dtype='int')
    df = df.select_dtypes(['int', 'float'])
    df.dropna(inplace=True)
    df.drop(columns=['price_per_month', 'commissions'], inplace=True)
    print('dataframe shape', df.shape)
    df = df.loc[df.price<=30_000_000,:]
    train_df, val_df = train_test_split(df, train_size=TRAIN_SIZE, random_state=1, shuffle=True)
    train_df.to_csv(OUT_TRAIN, index=0)
    val_df.to_csv(OUT_VAL, index=0)
    print('train shape', train_df.shape, 'val shape', val_df.shape)
    logger.info(f'Write {args.input} to train.csv and val.csv. Train set size: {args.split}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--split', type=float,
                        help='Split test size',
                        default=TRAIN_SIZE)
    parser.add_argument('-i', '--input', nargs='+',
                        help='List of input files',
                        default=IN_FILES)
    args = parser.parse_args()
    main(args)