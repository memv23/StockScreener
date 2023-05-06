# Import necessary modules

from bs4 import BeautifulSoup
import urllib
import psycopg2


# Initialize variables
# Note: Use your own info here, I'm not publishing the keys to my server

user = ''
password = ''
host = ''
port = ''
dbname = ''


# Connect to PostgreSQL database

connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
cursor = connection.cursor()


# Go to https://finviz.com/screener.ashx and filter to your heart's desire. Copy that url and paste here:

url = ""


# Scrape finviz website

req = urllib.request.Request(url)
req.add_header('User-Agent','Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0')
response = urllib.request.urlopen(req)
data = response.read()
html = data.decode('utf-8')

soup = BeautifulSoup(html, 'html5lib')


# Find the list of screner-link items
results = soup.find_all('a', class_='screener-link')

# Group the items into chunks representing each stock
chunk_size = 10
chunks = [results[i:i + chunk_size] for i in range(0, len(results), chunk_size)]

# Process the chunks and collect the data
data_rows = []
for chunk in chunks:
    data_row = [
        chunk[0].get_text(strip=True),
        str(chunk[1])[str(chunk[1]).find('?t=')+3:str(chunk[1]).find('&amp')],
        chunk[1].get_text(strip=True),
        chunk[2].get_text(strip=True),
        chunk[3].get_text(strip=True),
        chunk[4].get_text(strip=True),
        chunk[5].get_text(strip=True),
        chunk[6].get_text(strip=True),
        chunk[7].get_text(strip=True),
        chunk[8].get_text(strip=True),
        chunk[9].get_text(strip=True)
    ]
    data_rows.append(data_row)

tickerlist = []


# Initialize url for data scraping p. II

urla = 'https://finviz.com/screener.ashx?v=152&t='
urlb = '&c=0,1,2,3,4,5,79,6,7,8,9,10,11,12,13,73,74,75,14,15,16,77,17,18,19,20,21,23,22,82,78,24,25,26,27,28,29,30,31,84,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,68,70,80,83,76,60,61,62,63,64,67,69,81,65,66,71,72'

for tickers in data_rows:
    tickerlist.append(tickers[1])

tickerdict = {}

for j in tickerlist:
    urlx = urla+j+urlb
    jreq = urllib.request.Request(urlx)
    jreq.add_header('User-Agent','Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0')
    jresponse = urllib.request.urlopen(jreq)
    jdata = jresponse.read()
    jhtml = jdata.decode('utf-8')
    jsoup = BeautifulSoup(jhtml, 'html5lib')
    jresults = jsoup.find_all('a', class_='screener-link')
    results2 = []
    for i in jresults:
            i = str(i)
            if i.find('</span>') != -1:
                a_span = i.find('<span')
                b_span = i.find('">', a_span)
                g = i.replace(i[a_span:b_span+2],'')
                results2.append(g[75:g.find('<',75)])
            else:
                results2.append(i[75:i.find('<',75)])
            tickerdict[j] = results2


for k in tickerdict:
    select_query = 'SELECT ticker FROM finviz_data WHERE ticker=\''+str(k)+'\''
    tik = k
    k = tickerdict[k]
    k[0] = tik
    print(k)
    try:
        print("1")
        cursor.execute(select_query)
        result = cursor.fetchall()
        if result == []:
            try:
                print("7")
                k = str(k)
                k = k.replace('[','')
                k = k.replace(']','')
                k_values = k.split(', ')
                insert_query ='INSERT INTO finviz_data (ticker, company, sector, industry, country, index, market_cap, p_e, fwd_p_e, peg, p_s, p_b, p_c, p_fcf, book_sh, cash_sh, dividend, dividend_yield, payout_ratio, eps, eps_next_q, eps_this_yr, eps_next_yr, eps_past_5y, eps_next_5y, sales_past_5y, sales_q_q, eps_q_q, sales, income, shares_outstanding, shares_float, insider_ownership, insider_transactions, institutional_ownership, institutional_transactions, float_short, short_ratio, short_interest, roa, roe, roi, current_ratio, quick_ratio, ltdebt_equity, debt_equity, gross_margin, operating_margin, net_profit_margin, performance_week, performance_month, performance_quarter, performance_half_year, performance_year, performance_ytd, beta, average_true_range, volatility_week, volatility_month, twenty_day_simple_moving_avg, fifty_day_simple_moving_avg, two_hundred_day_simple_moving_avg, fifty_day_high, fifty_day_low, fifty_two_week_high, fifty_two_week_low, rsi, earnings_date, ipo_date, optionable, shortable, employees, change_from_open, gap, analyst_rec, avg_volume, relative_volume, volume, target_price, previous_close, price, change, ah_close, ah_change) VALUES ({})'.format(', '.join(k_values))
                cursor = connection.cursor()
                cursor.execute(insert_query)
                connection.commit()

            except Exception as e3:
                print("Error - Inner#1: ", e3)
                print("8")
                connection.rollback()
    except Exception as e1:
        print("2")
        print("Error - Outer: ", e1)
        try:
            print("3")
            k = str(k)
            k = k.replace('[','')
            k = k.replace(']','')
            insert_query ='INSERT INTO finviz_data (ticker, company, sector, industry, country, index, market_cap, p_e, fwd_p_e, peg, p_s, p_b, p_c, p_fcf, book_sh, cash_sh, dividend, dividend_yield, payout_ratio, eps, eps_next_q, eps_this_yr, eps_next_yr, eps_past_5y, eps_next_5y, sales_past_5y, sales_q_q, eps_q_q, sales, income, shares_outstanding, shares_float, insider_ownership, insider_transactions, institutional_ownership, institutional_transactions, float_short, short_ratio, short_interest, roa, roe, roi, current_ratio, quick_ratio, ltdebt_equity, debt_equity, gross_margin, operating_margin, net_profit_margin, performance_week, performance_month, performance_quarter, performance_half_year, performance_year, performance_ytd, beta, average_true_range, volatility_week, volatility_month, twenty_day_simple_moving_avg, fifty_day_simple_moving_avg, two_hundred_day_simple_moving_avg, fifty_day_high, fifty_day_low, fifty_two_week_high, fifty_two_week_low, rsi, earnings_date, ipo_date, optionable, shortable, employees, change_from_open, gap, analyst_rec, avg_volume, relative_volume, volume, target_price, previous_close, price, change, ah_close, ah_change) VALUES ({})'.format(', '.join(k_values))
            cursor = connection.cursor()
            cursor.execute(insert_query)
            connection.commit()

        except Exception as e2:
            print("Error - Inner#2: ", e2)
            connection.rollback()
