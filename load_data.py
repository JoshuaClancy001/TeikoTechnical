import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "db"))

from schema import DB_URL, create_schema
from load import load_csv, inspect, insert

if __name__ == "__main__":
    create_schema(drop_existing=True)
    df = load_csv()
    inspect(df)
    insert(df)
