-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS etl_workshop;
USE etl_workshop;

-- ==========================================
-- 1. CREACIÓN DE TABLAS DE DIMENSIONES
-- ==========================================

-- Dimensión: Candidato
CREATE TABLE IF NOT EXISTS dim_candidate (
    candidate_sk INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(150),
    country VARCHAR(100)
);

-- Dimensión: Tecnología
CREATE TABLE IF NOT EXISTS dim_technology (
    technology_sk INT AUTO_INCREMENT PRIMARY KEY,
    technology_name VARCHAR(100)
);

-- Dimensión: Seniority
CREATE TABLE IF NOT EXISTS dim_seniority (
    seniority_sk INT AUTO_INCREMENT PRIMARY KEY,
    seniority_level VARCHAR(50),
    yoe INT -- Years of experience
);

-- Dimensión: Fecha (Date)
-- Buena práctica: Usar un entero YYYYMMDD como SK en lugar de Auto Increment
CREATE TABLE IF NOT EXISTS dim_date (
    date_sk INT PRIMARY KEY, 
    full_date DATE,
    year INT,
    month INT,
    day INT
);

-- ==========================================
-- 2. CREACIÓN DE LA TABLA DE HECHOS
-- ==========================================

CREATE TABLE IF NOT EXISTS fact_application (
    application_id INT AUTO_INCREMENT PRIMARY KEY, -- Identificador único del grano
    candidate_sk INT,
    technology_sk INT,
    seniority_sk INT,
    date_sk INT,
    code_challenge_score INT,
    technical_interview_score INT,
    is_hired BOOLEAN, -- 1 si es contratado, 0 si no (Regla de negocio)
    
    -- Restricciones de Integridad Referencial
    FOREIGN KEY (candidate_sk) REFERENCES dim_candidate(candidate_sk),
    FOREIGN KEY (technology_sk) REFERENCES dim_technology(technology_sk),
    FOREIGN KEY (seniority_sk) REFERENCES dim_seniority(seniority_sk),
    FOREIGN KEY (date_sk) REFERENCES dim_date(date_sk)
);