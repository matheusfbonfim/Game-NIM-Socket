"""
No TCP é necessário pedir conexão ao servidor
"""
import time
import socket
import pickle

# Criação de um socket TCP usado para comunicação de dados
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Configuração

ip_serv = '127.0.0.1' # Endereço IP do servidor - localhost

porta_serv = 35000 # Porta do servidor

dest = (ip_serv, porta_serv) # IP e porta do servidor em um tupla

tcp.connect(dest) # Manda um SYN para conectar com o servidor 
                  # Só terminar quando receber o ACK 
                  # Fica travado até conectar ao servidor - Timeout

# ==========================================================

# FUNÇÕES

def imprimiParametros(n, m):
    print("\n====================================================================",end='\n')
    print("\n========== BEM-VINDO AO JOGO DO NIM! - JOGADOR 2 =================== ",end='\n')
    print("\n====================================================================",end='\n\n')

    print("A partida está configurada com os seguintes parâmetros:", end='\n\n')
    
    print(f"1- Número de peças: {n} peças\n")
    print(f"2- Peças por jogada: 1 a {m} peças\n")


def decisionOddOrEven():
    print("\n========== QUEM COMEÇA O JOGO? ==========  \n")
    print("Vamos decidir por impar ou par:\n")
    print("\t [0] - Ímpar\n")
    print("\t [1] - PAR\n\n")

    decision = int(input("Digite a opção [0 ou 1]: "))

    # Verifica se foi escrito uma opção válida
    while (decision != 0) & (decision != 1):
        print("\n !!! A opção escolhida é inválida !!!\n")
        print("\t [0] - Ímpar\n")
        print("\t [1] - PAR\n")
        decision = int(input("Digite novamente [0 ou 1]: "))

    return decision

def infoPlayerStartGame(player):
    print("\n========== START GAME ==========  \n\n")

    if (player == 'player2'):
        print("O jogador 2 (client) ganhou o ímpar ou par e iniciará o jogo\n")
    else:
        print("O jogador 1 (server) ganhou o ímpar ou par e iniciará o jogo\n")


def usuario_escolhe_jogada():
      """
      - Solicita quantas peças o usuário irá tirar
      - Verifica a validade dos parâmetros
      - Retorna o valor de peças retiradas
      """
      numero = int(input('\nQuantas peças você vai tirar? '))

      while numero > numPecas or numero > limitePecas or numero <= 0:
          print("\nOops! Jogada inválida! Tente de novo.")
          numero = int(input("\nQuantas peças você vai tirar? "))

      return numero

def theEnd(ganhador):
      if (ganhador):
        print("VOCÊ GANHOU!!")
      else: 
        print("VOCÊ PERDEU")


# ==========================================================
    #print(f"Tipo: {type(odd_or_even)} / Valor: {odd_or_even}")

# ÍNICIO

## RECEIVING GAME PARAMETERS 
    # Parametros do jogo
numPecas, limitePecas = pickle.loads(tcp.recv(2048))


## INFORMATION GAME
    # Imprime parametros
imprimiParametros(numPecas, limitePecas)


## ODD OR EVEN
    # Decisão de quem começa o jogo - Impar ou par
odd_or_even = decisionOddOrEven()

    # Envia um inteiro para indicar a escolha do impar ou par
tcp.send(odd_or_even.to_bytes(16,'big'))


## INFORMATION PLAYER START GAME
    # Recebendo a decisão de quem começa o jogo
resp1 = tcp.recv(1024)

initial_player = resp1.decode()

    # Emite informação de quem começa o jogo
infoPlayerStartGame(initial_player) 

# =========================================================================

firstTime = None

if initial_player == 'player2':

    retirada = usuario_escolhe_jogada()

    print(f"\nVocê tirou {retirada} peça(s).")
    
    numPecas = numPecas - retirada

    print(f"Agora restam {numPecas} peças no tabuleiro.")

    tcp.send(numPecas.to_bytes(16, 'big'))
   
else:
    # Primeira vez do jogador 1 (Caso não jogue primeiro)
    firstTime = True

while ((numPecas > 0) or firstTime):

    firstTime = False
    numPecas_server = int.from_bytes(tcp.recv(16), 'big') 
    
    jogada_anterior_restantes = numPecas - numPecas_server

    numPecas = numPecas_server

    if (numPecas == 0):
        theEnd(False)
        break

    print(f"\nO player 1 tirou {jogada_anterior_restantes} peça(s).")
    print(f"\nAgora restam {numPecas} peças no tabuleiro.")
    

    if (numPecas == 0):
    
        print("Fim do jogo")
    
    retirada = usuario_escolhe_jogada()

    print(f"\nVocê tirou {retirada} peça(s).")
    
    numPecas = numPecas - retirada

    if (numPecas == 0):
        theEnd(True)

    print(f"Numero de pecas: {numPecas}")

    tcp.send(numPecas.to_bytes(16, 'big'))
    
      


tcp.close()

input("aperte enter para encerrar")