import datetime
import os
import cianparser
import pandas as pd
import argparse

moscow_parser = cianparser.CianParser(location="Москва")

os.makedirs("data/raw/", exist_ok=True)

def main(n_rooms=1, start_page=1, end_page=2, object_type="secondary"):
    """Function docstring"""
    t = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    csv_path = f'data/raw/{n_rooms}_pages{start_page}_{end_page}_{t}.csv'
    data = moscow_parser.get_flats(
        deal_type="sale",
        rooms=(n_rooms,),
        with_saving_csv=False,
        with_extra_data=False,
        additional_settings={
            "start_page": start_page,
            "end_page": end_page,
            "object_type": object_type
        })
    df = pd.DataFrame(data)
    df['object_type'] = object_type
    df.to_csv(csv_path,
              encoding='utf-8',
              index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--n_rooms", type=int, required=False, help="Number of rooms")
    parser.add_argument("-s", "--start_page", type=int, required=False, help="Start page")
    parser.add_argument("-e", "--end_page", type=int, required=False, help="End page")
    parser.add_argument("-ot", "--object_type", type=str, required=False, help="Type of estate")
    args = parser.parse_args()

    main(args.n_rooms, args.start_page, args.end_page, args.object_type)