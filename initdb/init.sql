CREATE TABLE company (
    id SERIAL PRIMARY KEY,
    company_ko TEXT DEFAULT NULL,
    company_en TEXT DEFAULT NULL,
    company_ja TEXT DEFAULT NULL,
    tag_ko TEXT DEFAULT NULL,
    tag_en TEXT DEFAULT NULL,
    tag_ja TEXT DEFAULT NULL
);

COPY company(
    company_ko,
    company_en,
    company_ja,
    tag_ko,
    tag_en,
    tag_ja)
FROM '/docker-entrypoint-initdb.d/company_tag_sample.csv'
DELIMITER ','
CSV HEADER;