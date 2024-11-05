
---

# 📈 Stock Notification Bot - Telegram Integration

## Description
A robust Python application designed for real-time stock tracking and notification through Telegram. This bot provides updates on stock prices, manages customized goals, and alerts users when set targets are reached. It leverages the `yfinance` library for obtaining live market data and the `telebot` library for Telegram notifications.

## Features
- **Real-time stock price monitoring** 📊
- **Configurable interval notifications** ⏰
- **User-defined investment goals** 🎯
- **Automated alerts on goal achievement** 🚨
- **Flexible stock exchange options** 🌎

## Technologies Used
- Python 🐍
- `yfinance` for stock data
- `telebot` for Telegram integration
- JSON for data storage

## Prerequisites
Before running the project, ensure you have:

- **Python 3.x** installed
- The following Python libraries:
  - `yfinance`
  - `pyTelegramBotAPI`
  - `json`
  - `threading`
  - `os`

You can install the required libraries using:
```bash
pip install yfinance pyTelegramBotAPI
```

## How to Run the Bot
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/stock-notification-bot.git
   cd stock-notification-bot
   ```

2. Open `main.py` and replace the placeholder `TOKEN` with your **Telegram bot token**.

3. Run the script:
   ```bash
   python main.py
   ```

4. Follow the on-screen instructions to configure your **Telegram group ID** and set up stock notifications.

## Configuration Details
### Configuring Telegram Group ID
- Obtain your group ID using the `@myidbot` on Telegram:
  1. Add `@myidbot` to your group.
  2. Send `/getgroupid` to retrieve the group ID.
  3. Add the bot to your group and use this ID for setting up notifications.

### Adding a Stock for Monitoring
- Enter the stock symbol (e.g., `AAPL`) and specify the exchange if necessary (e.g., `NASDAQ`).
- Provide the price you paid for the stock and the quantity.
- Set an interval (in seconds) for update notifications.

### Setting Investment Goals
- Specify the stock and a target price.
- Add a custom alert message (e.g., "Sell Stock").
- The bot will notify you when the target price is reached.

## Main Functions
### `main()`
- Displays the main user interface.
- Handles navigation through options like configuring notifications, setting goals, and more.

### `exibir_notificacoes()`
- Monitors and sends real-time stock updates to the configured Telegram group.

### `agendar_metas()`
- Allows users to set and track stock price goals.

### `carregar_dados()` and `salvar_dados()`
- Load and save data persistently in `DATA.json`.

---

## Screenshots
📸 *Screenshots of the Telegram interface and the command-line interface in action could be included here for better visualization.*

## License
This project is licensed under the MIT License.

---

# 📝 Bot de Notificações de Ações - Integração com Telegram

## Descrição
Um aplicativo robusto em Python para monitoramento de ações em tempo real e envio de notificações pelo Telegram. O bot fornece atualizações de preços de ações, gerencia metas personalizadas e alerta os usuários quando essas metas são atingidas. Utiliza a biblioteca `yfinance` para obter dados do mercado e `telebot` para integração com o Telegram.

## Funcionalidades
- **Monitoramento em tempo real de preços de ações** 📊
- **Notificações em intervalos configuráveis** ⏰
- **Metas de investimento definidas pelo usuário** 🎯
- **Alertas automáticos ao atingir as metas** 🚨
- **Opções flexíveis para diferentes bolsas de valores** 🌎

## Tecnologias Utilizadas
- Python 🐍
- `yfinance` para dados de ações
- `telebot` para integração com Telegram
- JSON para armazenamento de dados

## Pré-requisitos
Antes de executar o projeto, certifique-se de ter:

- **Python 3.x** instalado
- As seguintes bibliotecas Python:
  - `yfinance`
  - `pyTelegramBotAPI`
  - `json`
  - `threading`
  - `os`

Você pode instalar as bibliotecas necessárias com:
```bash
pip install yfinance pyTelegramBotAPI
```

## Como Executar o Bot
1. Clone o repositório:
   ```bash
   git clone https://github.com/yourusername/stock-notification-bot.git
   cd stock-notification-bot
   ```

2. Abra o arquivo `main.py` e substitua o `TOKEN` pelo **token do seu bot** no Telegram.

3. Execute o script:
   ```bash
   python main.py
   ```

4. Siga as instruções na tela para configurar o **ID do grupo do Telegram** e configurar as notificações de ações.

## Detalhes de Configuração
### Configurando o ID do Grupo no Telegram
- Obtenha o ID do grupo usando o `@myidbot` no Telegram:
  1. Adicione `@myidbot` ao seu grupo.
  2. Envie `/getgroupid` para receber o ID do grupo.
  3. Adicione o bot ao grupo e use este ID para configurar as notificações.

### Adicionando uma Ação para Monitoramento
- Digite o símbolo da ação (ex: `AAPL`) e especifique a bolsa, se necessário (ex: `NASDAQ`).
- Informe o preço pago pela ação e a quantidade.
- Defina um intervalo (em segundos) para as notificações de atualização.

### Definindo Metas de Investimento
- Especifique a ação e um preço-alvo.
- Adicione uma mensagem de alerta personalizada (ex: "Vender Ação").
- O bot notificará quando o preço-alvo for atingido.

## Principais Funções
### `main()`
- Exibe a interface principal do usuário.
- Gerencia a navegação por opções como configuração de notificações, metas, e mais.

### `exibir_notificacoes()`
- Monitora e envia atualizações de ações em tempo real para o grupo do Telegram configurado.

### `agendar_metas()`
- Permite ao usuário definir e acompanhar metas de preços de ações.

### `carregar_dados()` e `salvar_dados()`
- Carregam e salvam os dados de forma persistente em `DATA.json`.

---

## Capturas de Tela
📸 *Inclua capturas de tela da interface no Telegram e da interface de linha de comando em funcionamento para melhor visualização.*

## Licença
Este projeto está licenciado sob a Licença MIT.

---

Feel free to include more details or personalize further according to your project's needs!
