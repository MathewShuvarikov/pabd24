import argparse
import logging
import pandas as pd
from joblib import load
from sklearn.metrics import mean_absolute_error as mae, mean_absolute_percentage_error as mape
import numpy as np

MODEL_SAVE_PATH = 'models/lgbm.joblib'
TEST_DATA = 'data/proc/val.csv'

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='log/test_model.log',
    encoding='utf-8',
    level=logging.DEBUG,
    format='%(asctime)s %(message)s')


def main(args):
    df_test = pd.read_csv(TEST_DATA)
    print(TEST_DATA)
    x_test = df_test.drop(columns='price')
    y_test = df_test['price']
    model = load(MODEL_SAVE_PATH)
    y_pred = np.exp(model.predict(x_test))
    mae1 = mae(y_pred, y_test)
    mape1 = mape(y_pred, y_test)
    logger.info(f'Test model {MODEL_SAVE_PATH} on {TEST_DATA}, MAE = {mae1:,.0f}, MAPE = {mape1:.3f}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model',
                        help='Model save path',
                        default=MODEL_SAVE_PATH)
    parser.add_argument("-p", "--TEST_DATA", type=int, required=False, help="TEST_DATA_PATH")
    args = parser.parse_args()
    main(args)