import cianparser
import pandas as pd
import datetime
from dotenv import dotenv_values

# using now() to get current time
configs = dotenv_values('.env')

moscow_parser = cianparser.CianParser(location="Москва")

def main():
    rooms = 3
    data = moscow_parser.get_flats(
        deal_type="sale",
        rooms=(rooms,),
        with_saving_csv=False,
        additional_settings={
            "start_page": 1,
            "end_page": 50,
            "object_type": "secondary"
        })
    data = pd.DataFrame(data)
    t = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    data.to_csv(f'../data/raw/rooms_{rooms}_{t}.csv', index=0)

if __name__ == '__main__':
    main()
