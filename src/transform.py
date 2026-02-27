import pandas as pd
import logging

def transform_data(df: pd.DataFrame) -> dict:
    """
    Cleans data, applies business rules, and models it into a Star Schema.
    """
    logging.info("Starting data transformation...")
    
    # 1. Clean column names (lowercase and replace spaces with underscores)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # 2. Apply Business Rule: Candidate is HIRED if both scores are >= 7
    # This creates a boolean column (True/False) and converts it to integer (1/0)
    df['is_hired'] = (
        (df['code_challenge_score'] >= 7) & 
        (df['technical_interview_score'] >= 7)
    ).astype(int)
    
    # 3. Create Dimensions
    logging.info("Building dimension tables...")
    
    # --- Dim_Date ---
    df['application_date'] = pd.to_datetime(df['application_date'])
    dim_date = pd.DataFrame({'full_date': df['application_date'].unique()})
    # Generate integer Date SK: YYYYMMDD
    dim_date['date_sk'] = dim_date['full_date'].dt.strftime('%Y%m%d').astype(int)
    dim_date['year'] = dim_date['full_date'].dt.year
    dim_date['month'] = dim_date['full_date'].dt.month
    dim_date['day'] = dim_date['full_date'].dt.day
    
    # --- Dim_Technology ---
    dim_technology = pd.DataFrame({'technology_name': df['technology'].unique()})
    dim_technology.insert(0, 'technology_sk', range(1, 1 + len(dim_technology)))
    
    # --- Dim_Seniority ---
    # Grouping unique combinations of seniority level and years of experience
    dim_seniority = df[['seniority', 'yoe']].drop_duplicates().reset_index(drop=True)
    dim_seniority.rename(columns={'seniority': 'seniority_level'}, inplace=True)
    dim_seniority.insert(0, 'seniority_sk', range(1, 1 + len(dim_seniority)))
    
    # --- Dim_Candidate ---
    # Assuming email is the unique natural key for candidates
    dim_candidate = df[['first_name', 'last_name', 'email', 'country']].drop_duplicates(subset=['email']).reset_index(drop=True)
    dim_candidate.insert(0, 'candidate_sk', range(1, 1 + len(dim_candidate)))
    
    # 4. Create Fact Table
    logging.info("Building fact table...")
    fact_df = df.copy()
    
    # Map Date SK
    fact_df['date_sk'] = fact_df['application_date'].dt.strftime('%Y%m%d').astype(int)
    
    # Map Candidate SK
    fact_df = fact_df.merge(dim_candidate[['email', 'candidate_sk']], on='email', how='left')
    
    # Map Technology SK
    fact_df = fact_df.merge(dim_technology, left_on='technology', right_on='technology_name', how='left')
    
    # Map Seniority SK
    fact_df = fact_df.merge(dim_seniority, left_on=['seniority', 'yoe'], right_on=['seniority_level', 'yoe'], how='left')
    
    # Select only the specific columns for the final Fact Table
    fact_application = fact_df[[
        'candidate_sk', 'technology_sk', 'seniority_sk', 'date_sk',
        'code_challenge_score', 'technical_interview_score', 'is_hired'
    ]]
    
    # Insert application_id as Surrogate Key for the Fact Table
    fact_application.insert(0, 'application_id', range(1, 1 + len(fact_application)))
    
    logging.info("Transformation completed successfully.")
    
    # Return a dictionary containing all tables
    return {
        'dim_candidate': dim_candidate,
        'dim_technology': dim_technology,
        'dim_seniority': dim_seniority,
        'dim_date': dim_date,
        'fact_application': fact_application
    }