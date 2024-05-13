import argparse
import logging
import pandas as pd
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='log/preprocess_data.log',
    encoding='utf-8',
    level=logging.DEBUG,
    format='%(asctime)s %(message)s')


IN_FILES = ['data/raw/1_2024-05-09_23-01.csv',
            'data/raw/2_2024-05-09_23-16.csv',
            'data/raw/3_2024-05-09_23-24.csv']

OUT_TRAIN = 'data/processed/train.csv'
OUT_VAL = 'data/processed/val.csv'

TRAIN_SIZE = 0.9

def main(args):
    main_dataframe = pd.read_csv(args.input[0], delimiter=',')
    for i in range(1, len(args.input)):
        data = pd.read_csv(args.input[i], delimiter=',')
        df = pd.DataFrame(data)
        main_dataframe = pd.concat([main_dataframe, df], axis=0)

    main_dataframe['url_id'] = main_dataframe['url'].map(lambda x: x.split('/')[-2])
    new_dataframe = main_dataframe[['url_id', 'total_meters', 'price', 'district']].set_index('url_id')

    new_df = new_dataframe[new_dataframe['price'] < 30_000_000]

    # border = int(args.split * len(new_df))
    # train_df, val_df = new_df[0:border], new_df[border:-1]
    train_df, val_df = train_test_split(new_df, train_size=TRAIN_SIZE, random_state=1)
    train_df.to_csv(OUT_TRAIN)
    val_df.to_csv(OUT_VAL)
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