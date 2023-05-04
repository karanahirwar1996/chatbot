# -*- coding: utf-8 -*-
"""StockAnalysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZkWfxqb2ttVg-Vgcj4EyLeAQpynr-7wv
"""

import pandas as pd
import time
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
def short_link(link):
    import urllib.parse
    import urllib.request

# Define the URL shortening service endpoint and long URL to be shortened
    endpoint = 'http://tinyurl.com/api-create.php'
    long_url = link
# Encode the long URL as a query parameter for the API call
    params = {'url': long_url}
    encoded_params = urllib.parse.urlencode(params).encode('utf-8')

# Make the API call and check the response status code
    response = urllib.request.urlopen(endpoint + '?' + encoded_params.decode('utf-8'))
    if response.status == 200:
        short_url = response.read().decode('utf-8')
        return short_url
    else:
        return 'Error: HTTP'
def stock_details(url):
    import smtplib
    from email.mime.text import MIMEText
    import datetime
    import requests
    from bs4 import BeautifulSoup
    import json
    import pandas as pd
    
    res=requests.get(url)
    soup=BeautifulSoup(res.content,features="html.parser")
    script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
    if script_tag is None:
        print(f"No script tag with id '__NEXT_DATA__' found on {url}")
        return None
    json_data = json.loads(script_tag.string)
    security_info = json_data['props']['pageProps']['securityInfo']
    info = security_info.get('info', {})
    isin = security_info.get('isin', None)
    name = info.get('name', None)
    sector = info.get('sector', None) 
    exchange = info.get('exchange', None)
    value = security_info.get('ratios', {})
    change=json_data['props']['pageProps']['securityQuote'].get('dyChange',None)
    _52whigh = value.get('52wHigh', None)
    _52wlow = value.get('52wLow', None)
    mc = value.get('marketCap', None)
    label = value.get('marketCapLabel', None)
    pe = value.get('pe', None)
    roe = value.get('roe', None)
    details = json_data['props']['pageProps']['securityQuote']
    price = details.get('price', None)
    l = details.get('l', None)
    h = details.get('h', None)
    date_today = datetime.date.today().strftime('%Y-%m-%d')
    data = {'Date': date_today, 'Name': name, 'ISIN': isin, 'Sector': sector, 'Exchange': exchange, '52 Week High': _52whigh, '52 Week Low': _52wlow, 'Market Cap': mc,\
            'Market Cap Label': label, 'P/E Ratio': pe, 'Day Return': change, 'Return on Equity': roe, 'Price': price, 'Low': l, 'High': h,"URL":url}
    df = pd.DataFrame(data, index=[0])
    Plus_5=df.loc[(df['Day Return']>5)&(df['Price']<2000)]
    Plus_5['New_URL']=Plus_5['URL'].apply(short_link)
    if len(Plus_5)>0:
    # send email
        res=requests.get(Plus_5['URL'][0])
        soup=BeautifulSoup(res.content,features="html.parser")
        script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
        json_data = json.loads(script_tag.string)
        news = json_data['props']['pageProps']['securitySummary'].get('news', None)
        financial=pd.DataFrame(json_data['props']['pageProps']['securitySummary']['financialSummary']['fiscalYearToData'])
        if news:
            news_df = pd.DataFrame(news, columns=['headline', 'date', 'link'])
        else:
            news_df = pd.DataFrame(columns=['headline', 'date', 'link'])
        sender_email = "karan.ahirwar1996@gmail.com"
        receiver_email = "anitaahirwar2112@gmail.com"
        password = "uccrgtqdnusrpmnk"

        table_html = Plus_5[['Name','Price','Day Return','New_URL']].to_html(index=False)

        message = MIMEText(f"I hope this email finds you well. I am writing to inform you about a recent development regarding stocks. \
        As of today, the day change for some of stocks has exceeded 5%. The details are as follows: \
        <br><br>{table_html} \
        <br>In addition to this, I would like to bring your attention to some relevant news articles related to these stocks: \
        <br><br>{news_df.to_html(index=False) if news is not None else 'No news available'} \
        <br><br>Here are the fiscal year details for the security: \
        <br><br>{financial.to_html(index=False)} \
        <br><br>Best regards:<br>Karan Ahirwar", "html")

        message["Subject"] = "Stock Details"
        message["From"] = sender_email
        message["To"] = receiver_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

    
    return df
def create_url(name, tag):
    name_slug = name.lower().replace(' ', '-')
    url = f"https://www.tickertape.in/stocks/{name_slug}-{tag}?ref=screener-table_int-asset-widget"
    return url
url_df=pd.read_csv("./tickertape_data.csv")
url_df['URL'] = url_df.apply(lambda row: create_url(row['Name'], row['Tag']), axis=1)
url_list =list(url_df['URL'][500:510])
df_list = []
for url in url_list:
    df1 = stock_details(url)
    df_list.append(df1)
    time.sleep(random.randint(0,3))
result_df = pd.concat(df_list, ignore_index=True)


scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# specify the path to your service account JSON file
creds = ServiceAccountCredentials.from_json_keyfile_name('./original-advice-385307-e221975bf7db.json', scope)
# authenticate with Google
client = gspread.authorize(creds)
# open the Google Sheets file by its name
gs = client.open('StockAnalysis')
sheet=gs.worksheet('Main')
sheet.clear()
sheet.update([result_df.columns.values.tolist()]+result_df.values.tolist())
print("Data Updated Successfully.....")
