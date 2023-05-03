from yahoofinancials import YahooFinancials
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

Stock = [
    {"symbol": "^IXIC", "name": "Nasdaq"},
    {"symbol": "^DJI", "name": " Dow Jones"},
    {"symbol": "AAPL", "name": "Apple"},
    {"symbol": "MSFT", "name": "Microsoft"},
    {"symbol": "GOOGL", "name": "Alphabet"},
    {"symbol": "AMZN", "name": "Amazon"},
    {"symbol": "META", "name": "Meta"},
    {"symbol": "TSLA", "name": "Tesla"},
    {"symbol": "JPM", "name": "JPMorgan"},
    {"symbol": "JNJ", "name": "Johnson & Johnson"},
    {"symbol": "V", "name": "Visa"},
    {"symbol": "PG", "name": "Procter & Gamble Company"}
]

def get_stock_data(symbol):
    stock = YahooFinancials(symbol)
    curr_price = stock.get_current_price()
    prev_price = stock.get_prev_close_price()
    perc_change = round(stock.get_current_percent_change()*100,2)
    return [curr_price,prev_price,perc_change]

for index,stock in enumerate(Stock):
    Stock[index]['data'] = get_stock_data(stock['symbol'])

Sorted_data = sorted(Stock[2:], key=lambda x: x["data"][-1], reverse=True)
Stock = Stock[:2] + Sorted_data

#Today date in format: 03 May 2023
today = datetime.datetime.today()
formatted_date = today.strftime("%d %B %Y")

#Decides color of % change text
def UpDown(perc):
    if perc < 0:
        return f' <span style="color: red">{perc}%</span>'
    else:
        return f' <span style="color: #339966">+{perc}%</span>'

#Add data to table
html_stock_text = ''

for i in range(2,len(Stock)):
    html_stock_text += f'<tr><td>{Stock[i]["name"]}</td><td>{Stock[i]["data"][0]}<br>{UpDown(Stock[i]["data"][2])}</td></tr>'

#Create Html format for email
html = """
<!DOCTYPE html>
<html>
<head>
	<title>Stock Digest</title>
	<style>
        body {
            font-family: Arial, Helvetica, sans-serif;
            background: #000;
            color: #fff;
        }
        h1,p,div {
            text-align: center;
        }
        div {
            
        }
		table {
			border-collapse: collapse;
			width: 100%;
			color: #000;
		}
        th {
            background-color: rgb(75, 128, 234);
            color: #fff;
        }
        tr:nth-child(odd) {
            background-color: rgb(241, 241, 241);
        }
        tr:nth-child(even) {
            background-color: #fff;
        }
		th, td {
			text-align: left;
			padding: 8px;
			border: 1px solid #ddd;
		}
		th {
		    text-align: center;
		}
	</style>
</head>
<body>
	<h1>Stock Digest</h1>
	<p>"""+formatted_date+"""</p>
	<div><span style='font-weight: bold;'>Nasdaq</span> $"""+ f"{Stock[0]['data'][0]} "+ f" {UpDown(Stock[0]['data'][2])}" + """</div>
	<div><span style='font-weight: bold;'>Dow Jones</span> $"""+ f"{Stock[1]['data'][0]} "+ f" {UpDown(Stock[1]['data'][2])}" + """</div>
	<br>
	<table>
		<thead>
			<tr>
				<th>Stocks</th>
				<th>Price($)</th>
			</tr>
		</thead>
		<tbody>
			"""+html_stock_text+"""
		</tbody>
	</table>
</body>
</html>
"""

sender_email = 'mediatv7051@gmail.com'
password = 'xxfznlnadwfjunuf'
receiver_email = ['ayushchandrapatel7051@gmail.com','ayushcp7051a@gmail.com']

def send_email(html):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    # Send the email
    try:
        for email in receiver_email:
            # Create the email message
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = email
            message['Subject'] = 'Stock Update'
            message.attach(MIMEText(html, 'html'))
            server.sendmail(sender_email, email, message.as_string())
            print(f'Email sent to {email}...')
    except Exception as e:
        print(e)
    finally:
        server.quit()

send_email(html)
