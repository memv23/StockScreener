# StockScreener
Grabs some data and adds it to a PostgreSQL database (if it's not already there)

To choose your stock screener criteria:
1. Go to https://finviz.com/screener.ashx
2. Choose whatever criteria you like
3. Use the final url in your python script
4. Note: this tool is only set up to collect the first 20 stocks screened, so be highly selective in your filters (or modify the code to filter through different criteria)



To set up PostgreSQL server in Docker:

1. Install Docker
2. CMD: $docker pull postgres
3. CMD: $docker run --name database_name -d -p 2022:5432 -e POSTGRES_PASSWORD=abcd1234 postgres
4. Go to Docker, run your newly created container
5. Go to CLI in Docker
6. $psql -U postgres

I have this Python Script set up to run every morning at 8a (Windows Task Scheduler) so I can see if there are any stocks I should pay attention to when the market opens
