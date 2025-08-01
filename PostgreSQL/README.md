# **PostgreSQL Partitioning & Performance Lab**

## **Prerequisites**

- Docker installed and running

- Terminal/Command Line access

- PostgreSQL client (psql) installed (use Homebrew on Mac: `brew install libpq && brew link --force libpq`)

- No GUI required


## **Step 1: Start PostgreSQL with Docker**

docker run --name pg-partition-lab -e POSTGRES\_PASSWORD=postgres -p 5432:5432 -d postgres:16

docker start pg-lab        

docker exec -it pg-lab psql -U postgres

\
\


**Step 3: Create a Base Table (Non-partitioned)**

We’ll create a simple e-commerce-style `orders` table.

CREATE TABLE orders (

  order\_id SERIAL PRIMARY KEY,

  customer\_id INT NOT NULL,

  order\_date DATE NOT NULL,

  region TEXT NOT NULL,

  amount NUMERIC(10, 2)

);


### **Insert Sample Data (\~500K rows)**

INSERT INTO orders (customer\_id, order\_date, region, amount)

SELECT

  (RANDOM() \* 5000)::INT,

  DATE '2021-01-01' + (RANDOM() \* 1095)::INT, -- \~3 years

  CASE

    WHEN RANDOM() < 0.25 THEN 'North'

    WHEN RANDOM() < 0.5 THEN 'South'

    WHEN RANDOM() < 0.75 THEN 'East'

    ELSE 'West'

  END,

  ROUND((RANDOM() \* 10000)::NUMERIC, 2)

FROM generate\_series(1, 500000);

\


**Step 4: Visualize the Data**


### **Check sample data:**

SELECT \* FROM orders LIMIT 10;


### **Group by region:**

SELECT region, COUNT(\*) FROM orders GROUP BY region;

\


**Step 5: Create Range Partitioned Table**

CREATE TABLE orders\_range (

  order\_id INT,

  customer\_id INT NOT NULL,

  order\_date DATE NOT NULL,

  region TEXT NOT NULL,

  amount NUMERIC(10,2),

  PRIMARY KEY (order\_id, order\_date)

) PARTITION BY RANGE (order\_date);


### **Create child partitions by year:**

CREATE TABLE orders\_range\_2021 PARTITION OF orders\_range

FOR VALUES FROM ('2021-01-01') TO ('2022-01-01');

CREATE TABLE orders\_range\_2022 PARTITION OF orders\_range

FOR VALUES FROM ('2022-01-01') TO ('2023-01-01');

CREATE TABLE orders\_range\_2023 PARTITION OF orders\_range

FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');

\


**Step 6: Create List Partitioned Table (on** `region`**)**

CREATE TABLE orders\_list (

  order\_id INT,

  customer\_id INT NOT NULL,

  order\_date DATE NOT NULL,

  region TEXT NOT NULL,

  amount NUMERIC(10,2),

  PRIMARY KEY (order\_id, region)

) PARTITION BY LIST (region);

CREATE TABLE orders\_list\_north PARTITION OF orders\_list

FOR VALUES IN ('North');

CREATE TABLE orders\_list\_south PARTITION OF orders\_list

FOR VALUES IN ('South');

CREATE TABLE orders\_list\_east PARTITION OF orders\_list

FOR VALUES IN ('East');

CREATE TABLE orders\_list\_west PARTITION OF orders\_list

FOR VALUES IN ('West');

\


**Step 7: Populate Partitioned Tables**


### **Copy data from** `orders`**:**

INSERT INTO orders\_range

SELECT \* FROM orders WHERE order\_date BETWEEN '2021-01-01' AND '2023-12-31';

INSERT INTO orders\_list

SELECT \* FROM orders;

\
\
\
\


**Step 8: Query Analysis with EXPLAIN ANALYZE**


### **Non-partitioned:**

EXPLAIN ANALYZE

SELECT \* FROM orders WHERE order\_date BETWEEN '2022-01-01' AND '2022-12-31';


### **Partitioned (Range):**

EXPLAIN ANALYZE

SELECT \* FROM orders\_range WHERE order\_date BETWEEN '2022-01-01' AND '2022-12-31';


### **Partitioned (List):**

EXPLAIN ANALYZE

SELECT \* FROM orders\_list WHERE region = 'South';

Look for:

- Bitmap Heap Scan vs Sequential Scan

- Partition Pruning in partitioned queries

**Step 9: VACUUM & AUTOVACUUM**


### **Manual Vacuum:**

VACUUM ANALYZE orders\_range;

VACUUM ANALYZE orders\_list;


### **Enable autovacuum logging:**

SHOW autovacuum;

(Enable logging in `postgresql.conf` if needed — not required in this lab.)

\
\


**Step 10: Index Testing**


### **Without Index:**

EXPLAIN ANALYZE SELECT \* FROM orders\_list WHERE customer\_id = 42;


### **Add Index:**

CREATE INDEX idx\_orders\_list\_customer ON orders\_list (customer\_id);

EXPLAIN ANALYZE SELECT \* FROM orders\_list WHERE customer\_id = 42;

Notice the speed difference.

**Step 11: Clean Up (Optional)**

docker stop pg-partition-lab

docker rm pg-partition-lab

\


**Bonus: View Partition Structure**

SELECT

  inhrelid::regclass AS child,

  inhparent::regclass AS parent

FROM pg\_inherits

WHERE inhparent::regclass::text LIKE 'orders\_%';
