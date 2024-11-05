```markdown
# 📈 Bot de Notificação de Ações para Telegram

Bem-vindo ao **Bot de Notificação de Ações**! Esse bot fornece atualizações em tempo real sobre preços de ações, ajudando você a manter-se informado sobre seus investimentos diretamente no Telegram.

---

## 📋 Funcionalidades
- **Monitoramento de Ações**: Configure o bot para acompanhar ações específicas e receba atualizações de preço em intervalos definidos.
- **Notificações de Lucro e Prejuízo**: Veja seus ganhos ou perdas potenciais calculados com base no preço de compra.
- **Metas de Preço**: Defina metas de preço para ações e receba notificações quando forem atingidas.
- **Persistência de Dados**: As configurações são salvas localmente para referência futura.

---

## 🚀 Começando

### Pré-requisitos
Certifique-se de ter o Python 3.x instalado junto com as seguintes bibliotecas:
- `yfinance`
- `telebot`
- `json`
- `os`

Para instalar as dependências, execute:
```bash
pip install yfinance pyTelegramBotAPI
```

### Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/seuusuario/bot-notificacao-acoes.git
   cd bot-notificacao-acoes
   ```

2. Salve o **Token do Bot do Telegram** na variável `TOKEN` do script:
   ```python
   TOKEN = 'SEU_TOKEN_DO_BOT_TELEGRAM'
   ```

3. Execute o script:
   ```bash
   python bot.py
   ```

---

## 🛠 Configurando o ID do Grupo no Telegram

Para começar a receber notificações, é necessário configurar o bot em seu grupo do Telegram.

1. **Obtenha o ID do Chat**:
   - Use [MyIDBot](https://t.me/myidbot). Inicie o bot e envie o comando `/getgroupid` para obter o ID do grupo.

2. **Adicione Nosso Bot ao Grupo**:
   - Adicione [NTFInvestHelp_bot](https://t.me/NTFInvestHelp_bot) ao grupo onde você deseja receber notificações.

3. **Insira o ID do Grupo no Script**:
   - Quando solicitado, insira o ID do grupo ou defina manualmente modificando a variável `group_id` no arquivo `DATA.json`.

---

## 💡 Como Usar

### Painel Principal

- Execute `python bot.py` e utilize o menu da interface:
  - **Opção 1**: Adicionar notificações de ações.
  - **Opção 2**: Gerenciar notificações (listar, adicionar, remover).
  - **Opção 3**: Configurar e acompanhar metas de preço.
  - **Opção 4**: Configurar ou atualizar o ID do grupo do Telegram.

### Gerenciando Notificações

1. **Adicionando uma Notificação**:
   - Insira o símbolo da ação, bolsa, preço pago, quantidade e intervalo de notificações.

2. **Removendo Notificações**:
   - Liste as notificações existentes e remova pelo ID.

### Gerenciando Metas

1. **Configurar Meta**:
   - Insira o símbolo da ação, valor desejado e uma nota de alerta.

2. **Remover Meta**:
   - Liste as metas atuais e exclua pelo ID.

---

## 👥 Créditos

Este projeto foi desenvolvido e mantido por:

- [Seu Perfil do GitHub](https://github.com/seuusuario)
- [Nome do Colaborador](https://github.com/colaboradorusuario)

Sinta-se à vontade para contribuir ou relatar problemas no GitHub!

---

## 📌 Versão Atual

- **Versão**: 1.0
```
