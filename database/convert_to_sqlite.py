import sqlite3
import pandas as pd


def convert_now():
        df = pd.read_csv('database/db.csv')

        df.drop(columns=df.columns[:1], 
                axis=1, 
                inplace=True)

        df.columns = df.columns.str.strip()

        con = sqlite3.connect("database/threatfinder.db")

        # drop data into database
        df.to_sql("SocialThreatFinder", con)

        con.close()
