import socket 
import pickle

class Server():
    def __init__(self):
        self.numPecas = None
        self.limitePecas = None
        self.jogador1 = None
        self.jogador2 = None  

    

    def definindoParametros(self):
        print("\n==========================================================",end='\n')
        print("\n========== BEM-VINDO AO JOGO DO NIM! - SERVIDOR ========== ",end='\n')
        print("\n==========================================================",end='\n\n')

        print("Para iniciar a partida é preciso determinar alguns parâmetros:",end='\n\n')
        
        n = int(input("\nDigite quantas peças inicialmente estão dispostas: "))
        m = int(input("Digite o limite de peças por jogadas: "))

        # Verifica limite de número de peças 
        while m < 1:
          print("O limite de peças é inválido. O limite de peças deve ser menor ou igual a quantidade de peças")
          m = int(input("Digite um limite de peças por jogadas válido: "))

        self.numPecas = n
        self.limitePecas = m

# =========================================================================

# Criação de socket TCP (Escuta e conexão)
  # AF_INET -> Tipo de endereço IPv4
  # SOCK_STREAM -> Protocolo de transporte TCP
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# =========================================================================

# Configuração 

ip = ''         # Não é atribuido, pois é usado o localhost (127.0.0.1)
porta = 6400    # Numero da porta - Servidor responde nessa porta  
                # Port to listen on (non-privileged ports are > 1023)

orig = (ip, porta)  # ip e porta do servidor em uma tupla

tcp.bind(orig)      # Vinculando/ligar o socket TCP com as configurações (Socket para conexão)
                    # Socket para escutar conexões

tcp.listen(2)   # Comece a escutar o pedido de conexões/espera de dados
                # (1) Quantas conexões posso escutar ao mesmo tempo nessa espera


# =========================================================================

# Conexão do primeiro cliente

tcp_dados, cliente = tcp.accept() # Dado a conexão, aceita a conexão 
                                  # tcp_dados -> socket de comunicação
                                  # tcp_dados -> socket exclusivo para conectar com quem pediu
                                  # cliente -> informações dele       

# =========================================================================

print(tcp_dados, end="\n\n")
print(cliente, end="\n\n")

# Definindo server
server = Server()

# Define o primeiro jogador
server.jogador1 = cliente

# Definindo parametros do jogo
server.definindoParametros()

# Montar pacote de saída 
msg1 = [int(server.numPecas), int(server.limitePecas)]

# Envia para o 1 jogador os parametros de jogo
tcp_dados.send(pickle.dumps(msg1))

# Envia para o 1 jogador os parametros de jogo
tcp_dados.send(pickle.dumps(msg1))

# =========================================================================

# Conexão do segundo cliente

tcp_dados2, cliente2 = tcp.accept() # Dado a conexão, aceita a conexão 
                                    # tcp_dados -> socket de comunicação
                                    # tcp_dados -> socket exclusivo para conectar com quem pediu
                                    # cliente -> informações dele       

# =========================================================================

# Define o segundo jogador
server.jogador2 = cliente2

# Envia para o 2 jogador os parametros de jogo
tcp_dados2.send(pickle.dumps(msg1))

# Envia para o 2 jogador os parametros de jogo
tcp_dados2.send(pickle.dumps(msg1))


# Tamanho da mensagem e codifica em bytes
#tam_resp = (len(msg1)).to_bytes(4, 'big')

# Manda para o cliente o tamanho da frase e a frase codificada
#tcp_dados.send(data)


# tcp_dados1, cliente2 = tcp.accept()

# print(tcp_dados1, end="\n\n")
# print(cliente2)



# # Obtendo o tamanho da mensagem que será recebida
# tam_bytes = tcp_dados.recv(16) # Tamando da mensagem que o client está enviando

# # Conversão para inteiro
# tam_msg = int.from_bytes(tam_bytes, 'big')

# # Obter a mensagem 
# msg = tcp_dados.recv(tam_msg) # Faz a leitura da mensagem (com base no tamanho)

# # Impressão para ver a mensagem
# print(msg.decode()) # Tem que decodificar




# # Montar pacote de saída 
# resp = "Olá, seja bem vindo ao server TCP"

# # Tamanho da mensagem e codifica em bytes
# tam_resp = (len(resp)).to_bytes(16, 'big')

# # Manda para o cliente o tamanho da frase e a frase codificada
# tcp_dados.send(tam_resp + resp.encode())

tcp_dados.close()

input("Aperte para encerrar")