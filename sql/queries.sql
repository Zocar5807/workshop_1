SELECT 
    t.technology_name, 
    SUM(f.is_hired) AS total_hires 
FROM fact_application f
JOIN dim_technology t ON f.technology_sk = t.technology_sk
WHERE f.is_hired = 1
GROUP BY t.technology_name
ORDER BY total_hires DESC;
SELECT 
    d.year, 
    SUM(f.is_hired) AS total_hires 
FROM fact_application f
JOIN dim_date d ON f.date_sk = d.date_sk
WHERE f.is_hired = 1
GROUP BY d.year
ORDER BY d.year ASC;
SELECT 
    s.seniority_level, 
    SUM(f.is_hired) AS total_hires 
FROM fact_application f
JOIN dim_seniority s ON f.seniority_sk = s.seniority_sk
WHERE f.is_hired = 1
GROUP BY s.seniority_level
ORDER BY total_hires DESC;
SELECT 
    c.country, 
    d.year, 
    SUM(f.is_hired) AS total_hires 
FROM fact_application f
JOIN dim_candidate c ON f.candidate_sk = c.candidate_sk
JOIN dim_date d ON f.date_sk = d.date_sk
WHERE f.is_hired = 1 
  AND c.country IN ('United States of America', 'Brazil', 'Colombia', 'Ecuador') -- Ajusta el nombre exacto según el CSV
GROUP BY c.country, d.year
ORDER BY c.country, d.year ASC;
SELECT 
    (SUM(is_hired) * 100.0 / COUNT(*)) AS hire_rate_percentage
FROM fact_application;
SELECT 
    is_hired,
    AVG(code_challenge_score) AS avg_code_score,
    AVG(technical_interview_score) AS avg_interview_score
FROM fact_application
GROUP BY is_hired;