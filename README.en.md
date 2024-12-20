
# 📈 Stock Notification Bot for Telegram

Welcome to the **Stock Notification Bot**! This bot provides real-time updates on stock prices, helping you stay informed about your investments directly through Telegram.

![ezgif com-crop](https://github.com/user-attachments/assets/2a240e2a-17b2-4352-bd25-3bb15816e4ba)

---

## 📋 Features
- **Stock Monitoring**: Configure the bot to track specific stocks, and receive price updates at set intervals.
- **Profit and Loss Notifications**: See your potential gains or losses calculated based on your input price.
- **Price Targets**: Set specific price goals for stocks, and receive notifications when these are met.
- **Persistent Data**: Configurations are saved locally for future reference.

---

## 🚀 Getting Started

### Prerequisites
Ensure you have Python 3.x installed along with the following libraries:
- `yfinance`
- `telebot`
- `json`
- `os`
- `dotenv`

To install the dependencies, run:
```bash
pip install yfinance pyTelegramBotAPI python-dotenv
```

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/sous4vfx/Investiment-Tracker
   cd Investiment-Tracker
   ```
2. Run the script:
   ```bash
   python bot.py
   ```
   
---

## 🛠 Configuring the ID for Telegram Group

To start receiving notifications, you need to configure the bot in your Telegram group.

1. **Get the Chat ID**:
   - Use [MyIDBot](https://t.me/myidbot). Start the bot and send the command `/getgroupid` to get your group ID.

2. **Add Our Bot to Your Group**:
   - Add [InvestimentTracker_Bot](https://t.me/InvestimentTracker_Bot) to the group where you want to receive notifications.

3. **Input the Group ID in the Script**:
   - When prompted, input the group ID or set it manually by modifying the `group_id` variable in the `DATA.json` file.

---

## 💡 How to Use

### Main Panel

- Run `python bot.py` and use the console menu:
  - **Option 1**: Add stock notifications.
  - **Option 2**: Manage notifications (list, add, remove).
  - **Option 3**: Configure and track price targets.
  - **Option 4**: Set up or update the Telegram group ID.

### Managing Notifications

1. **Adding a Notification**:
   - Enter the stock symbol, exchange, paid price, quantity, and notification interval.

2. **Removing Notifications**:
   - List existing notifications and remove by ID.

### Managing Targets

1. **Set Up a Target**:
   - Input a stock symbol, desired price, and a note for the alert.

2. **Remove a Target**:
   - List current targets and delete by ID.

---

## 👥 Credits

This project was developed and maintained by:

- [Sousa](https://github.com/sous4vfx)
- [Marcus](https://github.com/MarcusLopesDEV)

Feel free to contribute or report issues on GitHub!

---

## 📌 Current Version
```
- Version: 1.0
```
