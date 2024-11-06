import yfinance as yf
import time
import threading
import telebot 
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv('token')

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
group_id = None


configured_stocks = []
goals = []
notifications = []

data_file_path = "DATA.json"

def load_data():
    if os.path.exists(data_file_path):
        with open(data_file_path, 'r') as file:
            return json.load(file)
    return {}

def save_data(data):
    with open(data_file_path, 'w') as file:
        json.dump(data, file, indent=4)

def update_state():
    global group_id, configured_stocks, goals, notifications
    
    data = load_data()
    
    group_id = data.get('group_id', None)
    configured_stocks = data.get('configured_stocks', [])
    goals = data.get('goals', [])
    notifications = data.get('notifications', [])

update_state()

def get_stock_price(stock_symbol, exchange):
    if not exchange or exchange == "NASDAQ":
        ticker = stock_symbol
    else:
        ticker = f"{stock_symbol}.{exchange}"

    stock = yf.Ticker(ticker)

    try:
        history = stock.history(period="1d")
        if not history.empty:
            stock_price = history['Close'].iloc[0]
            return stock_price
        else:
            print(f"\n[ ! ] No data found for {ticker}. Check the symbol and exchange.")
            return None
    except Exception as e:
        print(f"\n[ ! ] Error retrieving price for {ticker}: {e}")
        return None

def calculate(total_paid_price, total_price):
    value_variation = total_price - total_paid_price
    percent_variation = (value_variation / total_paid_price) * 100 if total_paid_price != 0 else 0
    return value_variation, percent_variation

def display_notifications(stock_symbol, exchange, total_paid_price, quantity, interval):
    bot.send_message(group_id, '``` 🔔 • Notification Activated - for stock tracking!```', parse_mode="Markdown")

    while True:
        current_price = get_stock_price(stock_symbol, exchange)
        if current_price is None:
            bot.send_message(group_id, "``` ⚠️ • Notification stopped: Unable to retrieve price data for the stock.```", parse_mode="Markdown")
            break

        total_price = quantity * current_price
        value_variation, percent_variation = calculate(total_paid_price, total_price)

        message = (
            f"*📊 • Price Update*: `{stock_symbol}` on `{exchange}`\n\n"
            f"*💲 • Current Price*: `$ {current_price:.2f}`\n\n"
            f"*💼 • Current Total Value*: `$ {total_price:.2f}`\n"
            f"*💸 • Total Paid Value*: `$ {total_paid_price:.2f}`\n"
        )

        if total_paid_price < total_price:
            message += f"\n*📈 Profit*: `$ {value_variation:.2f}` (+{percent_variation:.2f}%) 🟢\n"
        elif total_paid_price > total_price:
            message += f"\n*📉 Loss*: `$ {abs(value_variation):.2f}` (-{abs(percent_variation):.2f}%) 🔻\n"
        else:
            message += f"\n*➖ No variation*: The value of your stocks remains the same.\n"

        message += '―――――――――――――――'

        bot.send_message(group_id, message, parse_mode="Markdown")
        time.sleep(interval)

def configure_group():
    global group_id
    while True:
        try:
            group_id = int(input("[ + ] Enter the Telegram group ID where notifications should be sent: "))
            print("[ + ] Group ID successfully configured.")

            save_data({"group_id": group_id, "configured_stocks": configured_stocks, "goals": goals, "notifications": notifications})
            break
        except ValueError:
            print("[ ! ] Please enter a valid numeric value for the group ID.")

def schedule_notification():
    global group_id, configured_stocks
    while group_id is None:
        print("\n[ ! ] No Group configured! Please set up the group ID.")
        print("""
[ + ] How to Obtain the Telegram Chat ID

    1. Open Telegram and start the bot - [ @myidbot ].
    2. Click "Start" and send the command /getgroupid.
    3. Create a group and add the bot - [ @myidbot ].
    4. Return to the bot and note the group ID it provides.
    5. Add the bot [ InvestimentTracker_Bot ] to the group.
    """)

        configure_group()

    print('\n--------------------------')
    print('[ ⬐ ] (Func) - Add Stock')

    stock_symbol = input("\n[ $ ] Enter the stock symbol: ").upper()
    exchange = input("[ + ] Enter the exchange code (leave empty for NASDAQ): ").upper()

    current_price = get_stock_price(stock_symbol, exchange)
    if current_price is None:
        print("\n[ ! ] Failed to add the stock. Check the data and try again.")
        return None, None, None, None, None

    while True:
        try:
            paid_price = float(input('[ $ ] What is the price you paid for the stock? $'))
            break
        except ValueError:
            print("\n[ ! ] Please enter a valid numeric value.")

    while True:
        try:
            quantity = int(input('[ X ] Quantity of stocks purchased: '))
            break
        except ValueError:
            print("\n[ ! ] Please enter a valid integer value.")

    total_paid_price = quantity * paid_price

    if not exchange:
        exchange = 'NASDAQ'

    print(f"\n[ ! ] The current price of {stock_symbol} on the {exchange} exchange is: $ {current_price:.2f}\n")

    while True:
        try:
            interval = int(input('[ i ] Set the notification interval in seconds (e.g., 120s = 2min): '))
            break
        except ValueError:
            print("\n[ ! ] Please enter a valid integer value.")

    new_stock = {
        "id": len(configured_stocks) + 1,
        "stock_symbol": stock_symbol,
        "exchange": exchange,
        "total_paid_price": total_paid_price,
        "quantity": quantity,
        "interval": interval
    }
    
    configured_stocks.append(new_stock)
    save_data({"group_id": group_id, "configured_stocks": configured_stocks, "goals": goals, "notifications": notifications})

    notification_thread = threading.Thread(
        target=display_notifications,
        args=(stock_symbol, exchange, total_paid_price, quantity, interval)
    )
    notification_thread.daemon = True
    notification_thread.start()

    print(f"[ + ] Notifications for {stock_symbol} successfully started!")

def start_automatic_notifications():
    global configured_stocks
    if configured_stocks:
        print("\n[ + ] Starting automatic notifications for configured stocks...")
        for stock in configured_stocks:
            display_notifications(
                stock_symbol=stock['stock_symbol'],
                exchange=stock['exchange'],
                total_paid_price=stock['total_paid_price'],
                quantity=stock['quantity'],
                interval=stock['interval']
            )
    else:
        print("\n[ ! ] No notifications configured to start automatically.")

def schedule_goals():
    stock_symbol = input("\n[ $ ] Enter the stock symbol: ").upper()
    exchange = input("[ + ] Enter the exchange code (leave empty for NASDAQ): ").upper()

    alert = input("[ + ] Enter the desired alert for your Goal (e.g., 'Sell Stock'): ")

    current_price = get_stock_price(stock_symbol, exchange)
    if current_price is None:
        print("\n[ ! ] Failed to add the goal. Check the data and try again.")
        return

    while True:
        try:
            goal_value = float(input('[ $ ] What value do you want for the goal? $'))
            break
        except ValueError:
            print("\n[ ! ] Please enter a valid numeric value.")

    new_goal = {
        "id": len(goals) + 1,
        "stock_symbol": stock_symbol,
        "exchange": exchange,
        "goal_value": goal_value,
        "alert": alert,
        "current_price": current_price
    }

    goals.append(new_goal)
    save_data({"group_id": group_id, "configured_stocks": configured_stocks, "goals": goals, "notifications": notifications})

def list_notifications():
    global configured_stocks
    print('\n[ ⬐ ] (Func) - List Notifications')
    if not configured_stocks:
        print("\n[ ! ] No notifications configured.")
    else:
        print("\n[ Listing Notifications ]")
        for stock in configured_stocks:
            print(f"ID: {stock['id']} | Stock: {stock['stock_symbol']} | Exchange: {stock['exchange']} | Paid Price: $ {stock['total_paid_price']:.2f} | Quantity: {stock['quantity']}")

def remove_notifications():
    global configured_stocks
    print('\n[ ⬐ ] (Func) - Remove Notifications')
    if not configured_stocks:
        print("\n[ ! ] No notifications configured to remove.")
        return

    list_notifications()
    while True:
        try:
            id_to_remove = int(input("\n[ - ] Enter the ID of the notification to remove: "))
            break
        except ValueError:
            print("\n[ ! ] Please enter a valid integer value.")

    for stock in configured_stocks:
        if stock['id'] == id_to_remove:
            configured_stocks.remove(stock)
            print(f"\n[ + ] The notification for {stock['stock_symbol']} has been removed successfully.")
            save_data({"group_id": group_id, "configured_stocks": configured_stocks, "goals": goals, "notifications": notifications})
            return

    print("\n[ ! ] No notification found with the specified ID.")

def main():
    update_state()

    while True:
        print("""
[ + ] Main Menu
 1. Configure Group ID
 2. Schedule Notification
 3. Start Automatic Notifications
 4. Schedule Goals
 5. List Notifications
 6. Remove Notifications
 0. Exit""")

        choice = input("\n[ ? ] Select an option: ")
        if choice == '1':
            configure_group()
        elif choice == '2':
            schedule_notification()
        elif choice == '3':
            start_automatic_notifications()
        elif choice == '4':
            schedule_goals()
        elif choice == '5':
            list_notifications()
        elif choice == '6':
            remove_notifications()
        elif choice == '0':
            break
        else:
            print("\n[ ! ] Invalid choice. Try again.")

if __name__ == "__main__":
    main()
