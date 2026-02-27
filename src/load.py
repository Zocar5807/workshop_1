import pandas as pd
from sqlalchemy import create_engine
import logging

def load_data_to_postgres(transformed_data: dict, db_connection_string: str):
    """
    Loads transformed DataFrames into a PostgreSQL Data Warehouse.
    Order is crucial to maintain referential integrity.
    """
    logging.info("Starting data loading process to Data Warehouse...")
    
    try:
        # Create SQLAlchemy engine
        engine = create_engine(db_connection_string)
        
        # Define the strict loading order: Dimensions first, Fact table last [cite: 175-176]
        tables_to_load = [
            'dim_candidate',
            'dim_technology',
            'dim_seniority',
            'dim_date',
            'fact_application'
        ]
        
        with engine.begin() as connection:
            for table_name in tables_to_load:
                df = transformed_data[table_name]
                logging.info(f"Loading table: {table_name} ({len(df)} rows)")
                
                # if_exists='append' assumes tables are already created via the SQL script
                # index=False ensures pandas doesn't insert its own row index
                df.to_sql(
                    name=table_name,
                    con=connection,
                    if_exists='append',
                    index=False
                )
                logging.info(f"Successfully loaded {table_name}.")
                
        logging.info("All data successfully loaded into the Data Warehouse.")
        
    except Exception as e:
        logging.error(f"Failed to load data into the Data Warehouse: {e}")
        raise