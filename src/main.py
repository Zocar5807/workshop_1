import logging
from extract import extract_from_csv
from transform import transform_data
from load import load_data_to_postgres

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Configuration paths and connection strings
    # In a real project, this connection string comes from a secure .env file
    csv_file_path = r'data\raw\candidates.csv'
    
    # Replace user, password, host, and dbname with your local PostgreSQL credentials
    # Format: postgresql+psycopg2://user:password@host:port/dbname
    # Reemplaza 'TU_CONTRASEÑA' por la real.
    postgres_connection_string = 'postgresql+psycopg2://postgres:WHITE5807@localhost:5432/etl_workshop'
    
    try:
        # Phase 1: Extract [cite: 160-162]
        raw_df = extract_from_csv(csv_file_path)
        
        # Phase 2: Transform [cite: 163-169]
        transformed_data_dict = transform_data(raw_df)
        
        # Phase 3: Load [cite: 174-177]
        load_data_to_postgres(transformed_data_dict, postgres_connection_string)
        
        logging.info("ETL Pipeline executed successfully.")
        
    except Exception as e:
        logging.critical(f"ETL Pipeline failed: {e}")

if __name__ == "__main__":
    main()