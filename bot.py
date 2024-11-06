import yfinance as yf
import time
import threading
import telebot 
import jsonhttps://github.com/sous4vfx/Investiment-Tracker/blob/main/bot.py
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)
group_id = None

acoes_configuradas = []
metas = []
notificacoes = []

data_file_path = "DATA.json"

def carregar_dados():
    if os.path.exists(data_file_path):
        with open(data_file_path, 'r') as file:
            return json.load(file)
    return {}

def salvar_dados(data):
    with open(data_file_path, 'w') as file:
        json.dump(data, file, indent=4)

def atualizar_estado():
    global group_id, acoes_configuradas, metas, notificacoes
    
    dados = carregar_dados()
    
    group_id = dados.get('group_id', None)
    acoes_configuradas = dados.get('acoes_configuradas', [])
    metas = dados.get('metas', [])
    notificacoes = dados.get('notificacoes', [])

atualizar_estado()

def obter_preco_acao(simbolo_acao, bolsa):
    if not bolsa or bolsa == "NASDAQ":
        ticker = simbolo_acao
    else:
        ticker = f"{simbolo_acao}.{bolsa}"

    acao = yf.Ticker(ticker)

    try:
        historico = acao.history(period="1d")
        if not historico.empty:
            preco_acao = historico['Close'].iloc[0]
            return preco_acao
        else:
            print(f"\n[ ! ] Nenhum dado encontrado para {ticker}. Verifique o símbolo e a bolsa.")
            return None
    except Exception as e:
        print(f"\n[ ! ] Erro ao obter preço para {ticker}: {e}")
        return None

def calculo(preco_total_pago, preco_total):
    variacao_valor = preco_total - preco_total_pago
    variacao_percentual = (variacao_valor / preco_total_pago) * 100 if preco_total_pago != 0 else 0
    return variacao_valor, variacao_percentual

def exibir_notificacoes(simbolo_acao, bolsa, preco_total_pago, quantidade, intervalo):
    bot.send_message(group_id, '``` 🔔 • Notificação Ativada - para acompanhamento de ações!```', parse_mode="Markdown")

    while True:
        preco_atual = obter_preco_acao(simbolo_acao, bolsa)
        if preco_atual is None:
            bot.send_message(group_id, "``` ⚠️ • Notificação interrompida: Não foi possível obter dados de preço para a ação.```", parse_mode="Markdown")
            break

        preco_total = quantidade * preco_atual
        variacao_valor, variacao_percentual = calculo(preco_total_pago, preco_total)

        mensagem = (
            f"*📊 • Atualização de Preço*: `{simbolo_acao}` na `{bolsa}`\n\n"
            f"*💲 • Preço Atual*: `$ {preco_atual:.2f}`\n\n"
            f"*💼 • Valor Total Atual*: `$ {preco_total:.2f}`\n"
            f"*💸 • Valor Total Pago*: `$ {preco_total_pago:.2f}`\n"
        )

        if preco_total_pago < preco_total:
            mensagem += f"\n*📈 Lucro*: `$ {variacao_valor:.2f}` (+{variacao_percentual:.2f}%) 🟢\n"
        elif preco_total_pago > preco_total:
            mensagem += f"\n*📉 Perda*: `$ {abs(variacao_valor):.2f}` (-{abs(variacao_percentual):.2f}%) 🔻\n"
        else:
            mensagem += f"\n*➖ Sem variação*: O valor das suas ações permanece o mesmo.\n"

        mensagem += '―――――――――――――――'

        bot.send_message(group_id, mensagem, parse_mode="Markdown")
        time.sleep(intervalo)


    
def configurar_grupo():
    global group_id
    while True:
        try:
            group_id = int(input("[ + ] Digite o ID do grupo do Telegram onde as notificações devem ser enviadas: "))
            print("[ + ] ID do grupo configurado com sucesso.")

            salvar_dados({"group_id": group_id, "acoes_configuradas": acoes_configuradas, "metas": metas, "notificacoes": notificacoes})
            break
        except ValueError:
            print("[ ! ] Insira um valor numérico válido para o ID do grupo.")


def agendar_notf():
    global group_id, acoes_configuradas
    while group_id is None:
        print("\n[ ! ] Nenhum Grupo configurado! Por favor, configure o ID do grupo.")
        print("""
[ + ] Como Obter o ID do Chat do Telegram

    1. Abra o Telegram e inicie o bot - [ @myidbot ].
    2. Clique em "Iniciar" e envie o comando /getgroupid.
    3. Crie um grupo e adicione o bot - [ @myidbot ].
    4. Volte ao bot e anote o ID do grupo que ele fornecer.
    5. Adicione o bot [ InvestimentTracker_Bot ] ao grupo.
    """)

        configurar_grupo()

    print('\n--------------------------')
    print('[ ⬐ ] (Func) - Adicionar Ação')

    simbolo_acao = input("\n[ $ ] Digite o símbolo da ação: ").upper()
    bolsa = input("[ + ] Digite o código da bolsa (deixe vazio para NASDAQ): ").upper()

    preco_atual = obter_preco_acao(simbolo_acao, bolsa)
    if preco_atual is None:
        print("\n[ ! ] Falha ao adicionar a ação. Verifique os dados e tente novamente.")
        return None, None, None, None, None

    while True:
        try:
            preco_pago = float(input('[ $ ] Qual o valor que você pagou pela ação? $'))
            break
        except ValueError:
            print("\n[ ! ] Por favor, insira um valor numérico válido.")

    while True:
        try:
            quantidade = int(input('[ X ] Quantidade de ações comprada: '))
            break
        except ValueError:
            print("\n[ ! ] Por favor, insira um número inteiro válido.")

    preco_total_pago = quantidade * preco_pago

    if not bolsa:
        bolsa = 'NASDAQ'

    print(f"\n[ ! ] O preço atual de {simbolo_acao} na bolsa {bolsa} é: $ {preco_atual:.2f}\n")

    while True:
        try:
            intervalo = int(input('[ i ] Defina o intervalo de notificações em segundos (ex: 120s = 2min): '))
            break
        except ValueError:
            print("\n[ ! ] Por favor, insira um número inteiro válido.")

    nova_acao = {
        "id": len(acoes_configuradas) + 1,
        "simbolo_acao": simbolo_acao,
        "bolsa": bolsa,
        "preco_total_pago": preco_total_pago,
        "quantidade": quantidade,
        "intervalo": intervalo
    }
    
    acoes_configuradas.append(nova_acao)
    salvar_dados({"group_id": group_id, "acoes_configuradas": acoes_configuradas, "metas": metas, "notificacoes": notificacoes})

    notificacao_thread = threading.Thread(
        target=exibir_notificacoes,
        args=(simbolo_acao, bolsa, preco_total_pago, quantidade, intervalo)
    )
    notificacao_thread.daemon = True
    notificacao_thread.start()

    print(f"[ + ] Notificações para {simbolo_acao} iniciadas com sucesso!")

def iniciar_notificacoes_automaticas():
    global acoes_configuradas
    if acoes_configuradas:
        print("\n[ + ] Iniciando notificações automáticas para ações configuradas...")
        for acao in acoes_configuradas:
            exibir_notificacoes(
                simbolo_acao=acao['simbolo_acao'],
                bolsa=acao['bolsa'],
                preco_total_pago=acao['preco_total_pago'],
                quantidade=acao['quantidade'],
                intervalo=acao['intervalo']
            )
    else:
        print("\n[ ! ] Nenhuma notificação configurada para iniciar automaticamente.")

def agendar_metas():
    simbolo_acao = input("\n[ $ ] Digite o símbolo da ação: ").upper()
    bolsa = input("[ + ] Digite o código da bolsa (deixe vazio para NASDAQ): ").upper()

    aviso = input("[ + ] Digite o aviso desejado para sua Meta (Ex 'Vender Ação'): ")

    preco_atual = obter_preco_acao(simbolo_acao, bolsa)
    if preco_atual is None:
        print("\n[ ! ] Falha ao adicionar a meta. Verifique os dados e tente novamente.")
        return

    while True:
        try:
            valor_meta = float(input('[ $ ] Qual valor você deseja para a meta? $'))
            break
        except ValueError:
            print("\n[ ! ] Por favor, insira um valor numérico válido.")

    nova_meta = {
        "id": len(metas) + 1,
        "simbolo_acao": simbolo_acao,
        "bolsa": bolsa,
        "valor_meta": valor_meta,
        "aviso": aviso,
        "preco_atual": preco_atual
    }

    metas.append(nova_meta)
    salvar_dados({"group_id": group_id, "acoes_configuradas": acoes_configuradas, "metas": metas, "notificacoes": notificacoes})

def listar_notificacoes():
    global acoes_configuradas
    print('\n[ ⬐ ] (Func) - Listar Notificações')
    if not acoes_configuradas:
        print("\n[ ! ] Nenhuma notificação configurada.")
    else:
        print("\n[ Listando Notificações ]")
        for acao in acoes_configuradas:
            print(f"ID: {acao['id']} | Ação: {acao['simbolo_acao']} | Bolsa: {acao['bolsa']} | Preço Pago: $ {acao['preco_total_pago']:.2f} | Quantidade: {acao['quantidade']}")


def remover_notificacoes():
    global acoes_configuradas
    print('\n[ ⬐ ] (Func) - Remover Notificações')
    if not acoes_configuradas:
        print("\n[ ! ] Nenhuma notificação configurada para remover.")
        return

    listar_notificacoes()
    while True:
        try:
            id_remover = int(input("\n[ - ] Insira o ID da notificação a ser removida: "))
            acao_remover = next((acao for acao in acoes_configuradas if acao['id'] == id_remover), None)
            if acao_remover:
                acoes_configuradas.remove(acao_remover)
                print(f"[ - ] Notificação para {acao_remover['simbolo_acao']} removida com sucesso.")
                salvar_dados({"group_id": group_id, "acoes_configuradas": acoes_configuradas, "metas": metas, "notificacoes": notificacoes})
                break
            else:
                print("[ ! ] ID não encontrado. Tente novamente.")
        except ValueError:
            print("[ ! ] Por favor, insira um valor numérico válido.")

def listar_metas():
    if not metas:
        print("[ ! ] Não há metas cadastradas.")
        return

    print("\n[ * ] Metas Cadastradas:")
    for meta in metas:
        print(f"ID: {meta['id']}, Ação: {meta['simbolo_acao']}, Bolsa: {meta['bolsa']}, Valor da Meta: $ {meta['valor_meta']}, Aviso: {meta['aviso']}")

def remover_meta():
    listar_metas()
    while True:
        try:
            id_meta = int(input("[ - ] Digite o ID da meta que deseja remover: "))
            break
        except ValueError:
            print("\n[ ! ] Por favor, insira um ID válido.")

    metas[:] = [meta for meta in metas if meta["id"] != id_meta]
    salvar_dados({"group_id": group_id, "acoes_configuradas": acoes_configuradas, "metas": metas, "notificacoes": notificacoes})
    print(f"[ - ] Meta de ID {id_meta} removida com sucesso.")


def verificar_e_enviar_metas():
    global metas, group_id

    while True:
        for meta in metas:
            preco_atual = obter_preco_acao(meta['simbolo_acao'], meta['bolsa'])
            if preco_atual is not None:
                if preco_atual == meta['valor_meta']:
                    mensagem_meta = (
                        "🚨 • *Alerta de Meta Atingida* 🚨\n"
                        f"*📈 • Ação*: `{meta['simbolo_acao']}` | *Bolsa*: `{meta['bolsa']}`\n"
                        f"*🎯 • Meta*: `$ {meta['valor_meta']:.2f}` atingida!\n"
                        f"*💲 • Preço Atual*: `$ {preco_atual:.2f}`\n"
                        f"*📝 • Aviso*: {meta['aviso']}\n"
                        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                    )
                    bot.send_message(group_id, mensagem_meta, parse_mode="Markdown")

        break


def main():

    if acoes_configuradas:
        notificacoes_thread = threading.Thread(target=iniciar_notificacoes_automaticas)
        notificacoes_thread.daemon = True 
        notificacoes_thread.start()

    metas_thread = threading.Thread(target=verificar_e_enviar_metas)
    metas_thread.daemon = True
    metas_thread.start()

    while True:
        print("\n[ Painel Principal ]\n")
        print("[ 1 ] Adicionar Acao")
        print("[ 2 ] Notificações")
        print("[ 3 ] Metas")
        print("[ 4 ] Configuracoes")
        print("[ 0 ] Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            agendar_notf() 
        elif opcao == '2':
            print("\n[ Painel Notificacoes ]\n")
            print("[ 1 ] Listar Notificações")
            print("[ 2 ] Configurar Notificacoes")
            secopcao = input("\nEscolha uma opção: ")
            if secopcao == '1':
                listar_notificacoes()
            elif secopcao == '2':
                print("\n[ Painel Configuracoes Notificacoes ]\n")
                print("[ 1 ] Adicionar Acao")
                print("[ 2 ] Remover Acao")
                print("[ 0 ] Sair")
                subopcao = input("\nEscolha uma opção: ")
                if subopcao == "1":
                    agendar_notf()
                elif subopcao == "2":
                   remover_notificacoes()
                elif subopcao == '0':
                   print("[ + ] Saindo...")
                break
            else:
                print("[ ! ] Opção inválida. Tente novamente.")
            
        elif opcao == '3':
            print("\n[ Painel Metas ]\n")
            print("[ 1 ] Listar Metas")
            print("[ 2 ] Agendar Metas")
            print("[ 3 ] Configurar Metas")
            secopcao = input("\nEscolha uma opção: ")
            if secopcao == '1':
                listar_metas()
            elif secopcao == '2':
                agendar_metas()
            elif secopcao == '3':
                print("\n[ Painel Configuracoes Metas ]\n")
                print("[ 1 ] Adicionar Meta")
                print("[ 2 ] Remover Meta")
                print("[ 0 ] Sair")
                ubopcao = input("\nEscolha uma opção: ")
                if subopcao == "1":
                    agendar_metas()
                elif subopcao == "2":
                    remover_meta()
                elif subopcao == '0':
                    print("[ + ] Saindo...")
                    break
                else:
                    print("[ ! ] Opção inválida. Tente novamente.")
        elif opcao == '4':
            print("\n[ Painel Configuracoes ]\n")
            print("[ 1 ] Definir Chat ID")
            print("[ 0 ] Sair")
            subopcao = input("\nEscolha uma opção: ")
            if subopcao == '1':
                configurar_grupo()
            elif subopcao == '0':
                print("[ + ] Saindo...")
                break
            else:
                print("[ ! ] Opção inválida. Tente novamente.")
                
        elif opcao == '0':
            print("[ + ] Saindo...")
            break
        else:
            print("[ ! ] Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
