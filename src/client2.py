"""
No TCP é necessário pedir conexão ao servidor
"""

import socket
import pickle

# Criação de um socket TCP usado para comunicação de dados
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Configuração

ip_serv = '127.0.0.1' # Endereço IP do servidor - localhost

porta_serv = 6400 # Porta do servidor

dest = (ip_serv, porta_serv) # IP e porta do servidor em um tupla

tcp.connect(dest) # Manda um SYN para conectar com o servidor 
                  # Só terminar quando receber o ACK 
                  # Fica travado até conectar ao servidor - Timeout

# ==========================================================

def imprimiParametros(list_params):

    print("\n========== BEM-VINDO AO JOGO DO NIM! - Jogador 2 ========== ",end='\n\n')

    print("A partida está configurada com os seguintes parâmetros:", end='\n\n')
    print(f"1- Número de peças: {list_params[0]} peças\n")
    print(f"2- Peças por jogada: 1 a {list_params[1]} peças\n\n")

# ==========================================================

# Parametros do jogo
parametros_recebidos = pickle.loads(tcp.recv(2048))

# Imprime parametros
imprimiParametros(parametros_recebidos)




# # Usuário entra com a mensagem 
# msg = input()

# # Tamanho da mensagem convertida para bytes
# tam = (len(msg)).to_bytes(16, 'big')

# # Mandar o tamanho da mensagem, gastando sempre 16 bytes 
# # E na sequência a mensagem em si
# tcp.send(tam + msg.encode())


# Ao chegar resposta 

# Tamanho da resposta - Recebendo 16 Bytes
#tam_resp = int.from_bytes(tcp.recv(4), 'big')

# Lê a mensagem
#resp = tcp.recv(tam_resp)


#tam_resp = int.from_bytes(tcp.recv(4), 'big')



tcp.close()

input("aperte enter para encerrar")