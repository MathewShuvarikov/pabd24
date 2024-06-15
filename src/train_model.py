import argparse
import logging
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error as mape, mean_absolute_error as mae
from joblib import dump
import numpy as np
from lightgbm import LGBMRegressor

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='log/train_model.log',
    encoding='utf-8',
    level=logging.DEBUG,
    format='%(asctime)s %(message)s')

TRAIN_DATA = 'data/proc/train.csv'
VAL_DATA = 'data/proc/val.csv'
MODEL_SAVE_PATH = 'models/lgbm.joblib'


def main(args):
    df_train = pd.read_csv(TRAIN_DATA)
    x_train = df_train.drop(columns='price')
    y_train = np.log(df_train['price'])

    # linear_model = LinearRegression()
    # linear_model.fit(x_train, y_train)
    # dump(linear_model, args.model)
    # logger.info(f'Saved to {args.model}')
    # r2 = linear_model.score(x_train, y_train)

    # rf = RandomForestRegressor(random_state=0, n_jobs=-1,
    #                            ** {'max_depth': 9, 'max_features': 'sqrt', 'min_samples_leaf': 1, 'min_samples_split': 2})
    # rf.fit(x_train, y_train)
    # r2 = rf.score(x_train, y_train)
    # dump(rf, args.model)
    # logger.info(f'Saved to {args.model}')

    lgbm = LGBMRegressor(random_state=0, n_jobs=-1,**{'n_estimators': 73, 'max_depth': 4, 'learning_rate': 0.2333555765304363,
                                                      'num_leaves': 18, 'reg_alpha': 0.6191071061084727, 'reg_lambda': 4.299778245226726})

    lgbm.fit(x_train, y_train)
    r2 = lgbm.score(x_train, y_train)
    mape1 = mape(np.exp(y_train), np.exp(lgbm.predict(x_train)))
    mae1 = mae(np.exp(y_train), np.exp(lgbm.predict(x_train)))
    dump(lgbm, args.model)
    logger.info(f'Saved to {args.model}')

    # c = int(linear_model.coef_[0])
    # inter = int(linear_model.intercept_)

    logger.info(f'R2 = {r2:.3f}  MAE = {mae1:,.0f} MAPE = {mape1:.3f}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model',
                        help='Model save path',
                        default=MODEL_SAVE_PATH)
    args = parser.parse_args()
    main(args)