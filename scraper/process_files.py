import os
import pandas as pd
from sqlalchemy import create_engine

class CSVProcessor:
    def __init__(self, root_folder):
        self.root_folder = root_folder
        self.df_list = []

    def process_files(self):
        # Walk through the directory tree and process each CSV file
        for dirpath, _, filenames in os.walk(self.root_folder):
            for filename in filenames:
                if filename.endswith('.csv'):
                    file_path = os.path.join(dirpath, filename)
                    country, port = self.extract_country_port(file_path)
                    print(f"Processing file: {filename} | Country: {country}, Port: {port}")
                    df = self.read_and_enrich_csv(file_path, country, port)
                    self.df_list.append(df)

    def extract_country_port(self, file_path):
        # Extract country and port from directory names
        parts = os.path.normpath(file_path).split(os.sep)
        country = parts[-3]
        port = parts[-2]
        return country, port

    def read_and_enrich_csv(self, file_path, country, port):
        # Read CSV file and add country and port columns
        df = pd.read_csv(file_path)
        df['country'] = country
        df['port'] = port
        return df

    def combine_data(self):
        # Combine all DataFrames into one
        return pd.concat(self.df_list, ignore_index=True)

    def save_to_postgresql(self, combined_df, table_name, db_url):
        # Create SQLAlchemy engine and upload to PostgreSQL
        engine = create_engine(db_url)
        combined_df.to_sql(table_name, engine, if_exists='replace', index=False)
        print("✅ Data uploaded to PostgreSQL automatically.")

class DataPipeline:
    def __init__(self, root_folder, table_name, db_url):
        self.csv_processor = CSVProcessor(root_folder)
        self.table_name = table_name
        self.db_url = db_url

    def run(self):
        self.csv_processor.process_files()
        combined_df = self.csv_processor.combine_data()
        print(f"✅ All CSVs combined with country and port columns. Combined DataFrame shape: {combined_df.shape}")
        self.csv_processor.save_to_postgresql(combined_df, self.table_name, self.db_url)

# Usage
if __name__ == "__main__":
    root_folder = 'downloads'  # Adjust this as needed
    table_name = 'exaqube_esl'
    db_url = 'postgresql+psycopg2://venkat:postgres@localhost:5432/postgres'
    
    pipeline = DataPipeline(root_folder, table_name, db_url)
    pipeline.run()
