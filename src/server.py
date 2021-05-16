import socket 
# Módulo implementa protocolos binários para serializar e desserializar uma estrutura de objeto Python
import pickle
import random

# =========================================================================

# Criação de socket TCP (Escuta e conexão)
  # AF_INET -> Tipo de endereço IPv4
  # SOCK_STREAM -> Protocolo de transporte TCP
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# =========================================================================

# Configuração 

ip = ''         # Não é atribuido, pois é usado o localhost (127.0.0.1)
porta = 5200    # Numero da porta - Servidor responde nessa porta  
                # Port to listen on (non-privileged ports are > 1023)

orig = (ip, porta)  # ip e porta do servidor em uma tupla

tcp.bind(orig)      # Vinculando/ligar o socket TCP com as configurações (Socket para conexão)
                    # Socket para escutar conexões

tcp.listen(1)   # Comece a escutar o pedido de conexões/espera de dados
                # (1) Quantas conexões posso escutar ao mesmo tempo nessa espera


# =========================================================================

# Conexão do primeiro cliente

tcp_dados, cliente = tcp.accept() # Dado a conexão, aceita a conexão 
                                  # tcp_dados -> socket de comunicação
                                  # tcp_dados -> socket exclusivo para conectar com quem pediu
                                  # cliente -> informações dele       

# =========================================================================

class Server():
    def __init__(self):
        self.numPecas = None
        self.limitePecas = None
        self.jogador1 = 'player1'
        self.jogador2 = 'player2'

    def definindoParametros(self):
        print("\n=============================================================",end='\n')
        print("\n==== ♦️  BEM-VINDO AO JOGO DO NIM! - SERVIDOR/JOGADOR 1 ♦️ ==== ",end='\n')
        print("\n=============================================================",end='\n\n')

        print("Para iniciar a partida é preciso determinar alguns parâmetros:",end='\n\n')
        
        n = int(input("\n➔  Digite quantas peças inicialmente estão dispostas: "))
        m = int(input("\n➔  Digite o limite de peças por jogadas: "))

        # Verifica limite de número de peças 
        while m < 1:
            print("O limite de peças é inválido. O limite de peças deve ser menor ou igual a quantidade de peças")
            m = int(input("➔  Digite um limite de peças por jogadas válido: "))

        print("\n\nO jogador 2 está decidindo entre ímpar ou par, para iniciar o jogo.....",end='\n')

        self.numPecas = n
        self.limitePecas = m

    def imparPar(self,num):
      # [0] - Impar [1] - Par
      aleatorioImparPar = random.randint(0, 1)

      print("\n\n========== START GAME ==========\n")

      if (aleatorioImparPar == num): 
          odd_or_even_text = 'PAR' if aleatorioImparPar == 1 else 'IMPAR'

          print(f"Resultado do impar ou par: {odd_or_even_text}\n")
          print("O jogador 2 (client) ganhou o ímpar ou par e iniciará o jogo.\n")
          return self.jogador2
      else:
          odd_or_even_text = 'PAR' if aleatorioImparPar == 1 else 'IMPAR'

          print(f"Resultado do impar ou par: {odd_or_even_text}\n")
          print("O jogador 1 (server) ganhou o ímpar ou par e iniciará o jogo.")
          return self.jogador1
    

    def sendDataString(self, info):
      tcp_dados.send(bytes(info, 'utf-8'))


    def escolhe_jogada(self):
      """
      - Solicita quantas peças o usuário irá tirar
      - Verifica a validade dos parâmetros
      - Retorna o valor de peças retiradas
      """
      numero = int(input('\n\n➔ Quantas peças você vai tirar? '))

      while numero > self.numPecas or numero > self.limitePecas or numero <= 0:
          print("\nOops! Jogada inválida! Tente de novo.")
          numero = int(input("\n\n➔ Quantas peças você vai tirar? "))

      return numero


    def theEnd(self, ganhador):
      if (ganhador):
        print("\n\n================================\n")
        print("🏆🏆🏆 VOCÊ GANHOU!!🏆🏆🏆")
        print("\n================================\n")
      else: 
        print("\n================================\n")
        print("❌❌❌ VOCÊ PERDEU! ❌❌❌")
        print("\n================================\n")
# =========================================================================


print(f"**** CLIENTE: {cliente} se conectou ****", end="\n\n")

## DEFINE SERVER
  # Definindo server
server = Server()


## DEFINE GAME PARAMETERS 
  # Definindo parametros do jogo
server.definindoParametros()


## LIST WITH GAME PARAMETERS
  # Lista com numPecas e limite peca - Montar pacote de saída 
msg1 = [int(server.numPecas), int(server.limitePecas)]


## SEND - PLAYER 2 - PARAMETERS
  # Envia para o 2 jogador os parametros de jogo
tcp_dados.send(pickle.dumps(msg1))


## RECEIVING - CHOICE ODD OR EVEN
  # Recebendo a escolha entre impar ou par do cliente - Jogador2
option = int.from_bytes(tcp_dados.recv(16), 'big')


## CONTROL - PLAYER START GAME
  # Quem iniciará o jogo
initial_player = server.imparPar(option)


## SEND TO PLAYER 2 - PLAYER START GAME
  # Enviando para o jogador 2 quem começa o jogo 
server.sendDataString(initial_player)


# =========================================================================
## GAME

primeirojoga = None
ganhador = None

if initial_player == server.jogador1:
    
    retirada = server.escolhe_jogada()

    print(f"\n\tVocê tirou {retirada} peça(s).")
    
    server.numPecas = server.numPecas - retirada

    print(f"\n\tAgora restam {server.numPecas} peças no tabuleiro.")

    tcp_dados.send(server.numPecas.to_bytes(16, 'big'))##

else:   
    primeirojoga = True; 

while ((server.numPecas > 0) or primeirojoga):
  
    primeirojoga = False

    numPecasRestantes = int.from_bytes(tcp_dados.recv(16), 'big') #recive

    jogada_anterior_restantes = server.numPecas - numPecasRestantes

    if (numPecasRestantes == 0):
        server.theEnd(False)
        break

    server.numPecas = numPecasRestantes

    print("\n================================")
    print(f"\n\tO player 2 tirou {jogada_anterior_restantes} peça(s).")
    
    print(f"\n\tAgora restam {server.numPecas} peças no tabuleiro.")


    if (server.numPecas == 0):
        server.theEnd(False)
        break 
        
    
    retirada = server.escolhe_jogada()

    print(f"\n\tVocê tirou {retirada} peça(s).")
      
    server.numPecas = server.numPecas - retirada


    if (server.numPecas == 0): 
        server.theEnd(True)
        break

    print(f"\n\tAgora restam {server.numPecas} peças no tabuleiro.")

      
    tcp_dados.send(server.numPecas.to_bytes(16, 'big')) #send
# =========================================================================


tcp_dados.close()

input("Aperte para encerrar")