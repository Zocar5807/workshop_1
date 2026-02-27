import pandas as pd
import logging

# Configure logging to see the process in the terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_from_csv(file_path: str) -> pd.DataFrame:
    """
    Extracts data from a CSV file into a pandas DataFrame.
    """
    try:
        logging.info(f"Starting data extraction from: {file_path}")
        # Read the CSV. Assuming comma separation.
        df = pd.read_csv(file_path, sep=';')
        logging.info(f"Successfully extracted {len(df)} rows.")
        return df
    except FileNotFoundError:
        logging.error(f"The file {file_path} was not found. Please check the path.")
        raise
    except Exception as e:
        logging.error(f"An error occurred during extraction: {e}")
        raise