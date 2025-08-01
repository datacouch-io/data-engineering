# PostgreSQL Partitioning & Performance Lab


This hands-on lab explores PostgreSQL's **partitioning** capabilities (range & list) and performance tuning techniques like `EXPLAIN ANALYZE`, `VACUUM`, and indexing. It is designed for benchmarking and educational use.

---
## Prerequisites
````
- Docker installed and running
- Terminal or command-line access
- No GUI required
````
## Step 1: Start PostgreSQL with Docker

```bash
docker run --name pg-partition-lab -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:16

docker start pg-partition-lab        

docker exec -it pg-partition-lab psql -U postgres
````

## Step 2: Create a Base Table (Non-Partitioned)

```sql
CREATE TABLE orders (
  order_id SERIAL PRIMARY KEY,
  customer_id INT NOT NULL,
  order_date DATE NOT NULL,
  region TEXT NOT NULL,
  amount NUMERIC(10, 2)
);
```

### Insert Sample Data (\~500K Rows)

```sql
INSERT INTO orders (customer_id, order_date, region, amount)
SELECT
  (RANDOM() * 5000)::INT,
  DATE '2021-01-01' + (RANDOM() * 1095)::INT,  -- ~3 years
  CASE
    WHEN RANDOM() < 0.25 THEN 'North'
    WHEN RANDOM() < 0.5 THEN 'South'
    WHEN RANDOM() < 0.75 THEN 'East'
    ELSE 'West'
  END,
  ROUND((RANDOM() * 10000)::NUMERIC, 2)
FROM generate_series(1, 500000);
```

---

## Step 3: Visualize the Data

```sql
-- Sample rows
SELECT * FROM orders LIMIT 10;

-- Region-wise distribution
SELECT region, COUNT(*) FROM orders GROUP BY region;
```

---

## Step 4: Create a Range Partitioned Table (By Order Date)

```sql
CREATE TABLE orders_range (
  order_id INT,
  customer_id INT NOT NULL,
  order_date DATE NOT NULL,
  region TEXT NOT NULL,
  amount NUMERIC(10,2),
  PRIMARY KEY (order_id, order_date)
) PARTITION BY RANGE (order_date);
```

### Create Yearly Partitions

```sql
CREATE TABLE orders_range_2021 PARTITION OF orders_range
FOR VALUES FROM ('2021-01-01') TO ('2022-01-01');

CREATE TABLE orders_range_2022 PARTITION OF orders_range
FOR VALUES FROM ('2022-01-01') TO ('2023-01-01');

CREATE TABLE orders_range_2023 PARTITION OF orders_range
FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');
```

---

## Step 5: Create a List Partitioned Table (By Region)

```sql
CREATE TABLE orders_list (
  order_id INT,
  customer_id INT NOT NULL,
  order_date DATE NOT NULL,
  region TEXT NOT NULL,
  amount NUMERIC(10,2),
  PRIMARY KEY (order_id, region)
) PARTITION BY LIST (region);
```

### Create Regional Partitions

```sql
CREATE TABLE orders_list_north PARTITION OF orders_list FOR VALUES IN ('North');
CREATE TABLE orders_list_south PARTITION OF orders_list FOR VALUES IN ('South');
CREATE TABLE orders_list_east  PARTITION OF orders_list FOR VALUES IN ('East');
CREATE TABLE orders_list_west  PARTITION OF orders_list FOR VALUES IN ('West');
```

---

## Step 6: Populate the Partitioned Tables

```sql
-- Range partition
INSERT INTO orders_range
SELECT * FROM orders
WHERE order_date BETWEEN '2021-01-01' AND '2023-12-31';

-- List partition
INSERT INTO orders_list
SELECT * FROM orders;
```

---

## Step 7: Performance Testing with EXPLAIN ANALYZE

### Non-partitioned Query

```sql
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE order_date BETWEEN '2022-01-01' AND '2022-12-31';
```

### Range Partitioned Query

```sql
EXPLAIN ANALYZE
SELECT * FROM orders_range
WHERE order_date BETWEEN '2022-01-01' AND '2022-12-31';
```

### List Partitioned Query

```sql
EXPLAIN ANALYZE
SELECT * FROM orders_list
WHERE region = 'South';
```

### Key Observations

* Look for **Bitmap Heap Scan** vs **Sequential Scan**
* Partition pruning should occur on partitioned queries

---

## Step 8: Vacuum & Autovacuum

### Manual Vacuuming

```sql
VACUUM ANALYZE orders_range;
VACUUM ANALYZE orders_list;
```

### View Autovacuum Status

```sql
SHOW autovacuum;
```
---

## Step 9: Indexing Performance Test

### Without Index

```sql
EXPLAIN ANALYZE
SELECT * FROM orders_list WHERE customer_id = 42;
```

### Add Index

```sql
CREATE INDEX idx_orders_list_customer ON orders_list (customer_id);

EXPLAIN ANALYZE
SELECT * FROM orders_list WHERE customer_id = 42;
```

> Compare query speed before and after adding the index.

---

## Step 10: Clean Up (Optional)

```bash
docker stop pg-partition-lab
docker rm pg-partition-lab
```

---

## Bonus: View Partition Structure

```sql
SELECT
  inhrelid::regclass AS child,
  inhparent::regclass AS parent
FROM pg_inherits
WHERE inhparent::regclass::text LIKE 'orders_%';
```
