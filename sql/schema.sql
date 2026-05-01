-- =============================================================
-- Data Insights Pipeline — Schema
-- =============================================================

CREATE TABLE IF NOT EXISTS sales (
    id          SERIAL PRIMARY KEY,
    product     VARCHAR(200)   NOT NULL,
    category    VARCHAR(100),
    price       NUMERIC(10, 2) NOT NULL,
    quantity    INT            NOT NULL DEFAULT 1,
    rating      NUMERIC(3, 2),
    sale_date   TIMESTAMP      NOT NULL DEFAULT NOW(),
    source_api  VARCHAR(100)   DEFAULT 'fakestoreapi'
);

CREATE INDEX IF NOT EXISTS idx_sales_category  ON sales(category);
CREATE INDEX IF NOT EXISTS idx_sales_sale_date ON sales(sale_date);
