import argparse
import logging
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from joblib import dump

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='log/train_model.log',
    encoding='utf-8',
    level=logging.DEBUG,
    format='%(asctime)s %(message)s')

TRAIN_DATA = 'data/processed/train.csv'
VAL_DATA = 'data/processed/val.csv'
MODEL_SAVE_PATH = 'models/linear_regression_v01.joblib'
MAPPING = 'data/mapping/county.txt'

def main(args):
    df_train = pd.read_csv(TRAIN_DATA, index_col='url_id')
    df_val = pd.read_csv(VAL_DATA, index_col='url_id')
    df = pd.concat([df_train, df_val])
    mapping = pd.read_csv(MAPPING, sep='|')
    df = df.merge(mapping, how='left', left_on='district', right_on='district_name')
    df = pd.get_dummies(df, columns=['county_short'], drop_first=True, dtype=int)
    df_train, df_val = train_test_split(df, test_size=0.1, random_state=0)

    x_train = df_train.select_dtypes(include='number').drop(columns='price')
    y_train = df_train['price']

    x_val = df_val.select_dtypes(include='number').drop(columns='price')
    y_val = df_val['price']

    linear_model = LinearRegression()
    linear_model.fit(x_train, y_train)
    dump(linear_model, args.model)
    logger.info(f'Saved to {args.model}')

    r2 = linear_model.score(x_train, y_train)

    y_pred = linear_model.predict(x_val)
    mae = mean_absolute_error(y_pred, y_val)
    c = int(linear_model.coef_[0])
    inter = int(linear_model.intercept_)

    logger.info(f'R2 = {r2:.3f}     MAE = {mae:.0f}     Price = {c} * area + {inter}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model',
                        help='Model save path',
                        default=MODEL_SAVE_PATH)
    args = parser.parse_args()
    main(args)