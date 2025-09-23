
import datetime
import schedule
import time
from Sah_Yang_image import save_sah_df_img 
from Sah_Yang_Schedule import Sah_filtered_dataframe 

def generate_image():
    try:
        df = Sah_filtered_dataframe()
        save_sah_df_img(df, filename="2509.png")
    except Exception as e:
        pass

schedule.every().monday.at("09:00").do(generate_image)
schedule.every().tuesday.at("09:00").do(generate_image)
schedule.every().friday.at("09:00").do(generate_image)
schedule.every().saturday.at("09:00").do(generate_image)
schedule.every().sunday.at("09:00").do(generate_image)

if __name__ == "__main__":
    pass
    while True:
        schedule.run_pending()
        time.sleep(60)
