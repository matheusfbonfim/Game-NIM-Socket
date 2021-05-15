import socket 
# Módulo implementa protocolos binários para serializar e desserializar uma estrutura de objeto Python
import pickle
import time
import random

# =========================================================================

# Criação de socket TCP (Escuta e conexão)
  # AF_INET -> Tipo de endereço IPv4
  # SOCK_STREAM -> Protocolo de transporte TCP
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# =========================================================================

# Configuração 

ip = ''         # Não é atribuido, pois é usado o localhost (127.0.0.1)
porta = 5100    # Numero da porta - Servidor responde nessa porta  
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
        print("\n====================================================================",end='\n')
        print("\n========== BEM-VINDO AO JOGO DO NIM! - SERVIDOR/JOGADOR 1 ========== ",end='\n')
        print("\n====================================================================",end='\n\n')

        print("Para iniciar a partida é preciso determinar alguns parâmetros:",end='\n\n')
        
        n = int(input("\nDigite quantas peças inicialmente estão dispostas: "))
        m = int(input("Digite o limite de peças por jogadas: "))

        # Verifica limite de número de peças 
        while m < 1:
          print("O limite de peças é inválido. O limite de peças deve ser menor ou igual a quantidade de peças")
          m = int(input("Digite um limite de peças por jogadas válido: "))

        self.numPecas = n
        self.limitePecas = m

    def imparPar(self,num):
      # [0] - Impar [1] - Par
      aleatorioImparPar = random.randint(0, 1)

      print("\n======================= START GAME ===============================  \n\n")

      if (aleatorioImparPar == num): 

          print(f"Resultado do impar ou par: {aleatorioImparPar}\n")
          print("O jogador 2 (client) ganhou o ímpar ou par e iniciará o jogo\n")
          return self.jogador2
      else:
          print(f"Resultado do impar ou par: {aleatorioImparPar}\n")
          print("O jogador 1 (server) ganhou o ímpar ou par e iniciará o jogo\n")
          return self.jogador1
    

    def sendDataString(self, info):
      tcp_dados.send(bytes(info, 'utf-8'))


    def escolhe_jogada(self):
      """
      - Solicita quantas peças o usuário irá tirar
      - Verifica a validade dos parâmetros
      - Retorna o valor de peças retiradas
      """
      numero = int(input('\nQuantas peças você vai tirar? '))

      while numero > self.numPecas or numero > self.limitePecas or numero <= 0:
          print("\nOops! Jogada inválida! Tente de novo.")
          numero = int(input("\nQuantas peças você vai tirar? "))

      return numero


    def theEnd(self, ganhador):
      if (ganhador):
        print("VOCÊ GANHOU!!")
      else: 
        print("VOCÊ PERDEU")
        
# =========================================================================


print(tcp_dados, end="\n\n")
print(cliente, end="\n\n")

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
  # Envia para o 1 jogador os parametros de jogo
tcp_dados.send(pickle.dumps(msg1))


## RECEIVING - CHOICE ODD OR EVEN
  # Recebendo a escolha entre impar ou par do cliente - jogador2
escolha = int.from_bytes(tcp_dados.recv(16), 'big')


## CONTROL - PLAYER START GAME
  # Quem iniciará o jogo
initial_player = server.imparPar(escolha)


## SEND TO PLAYER 2 - PLAYER START GAME
  # Enviando para o jogador quem começa o jogo 
server.sendDataString(initial_player)


# =========================================================================
primeirojoga = None
ganhador = None


## GAME
if initial_player == server.jogador1:
    
  retirada = server.escolhe_jogada()

  print(f"\nVocê tirou {retirada} peça(s).")
    
  server.numPecas = server.numPecas - retirada

  print(f"Numero de pecas: {server.numPecas}")

  tcp_dados.send(server.numPecas.to_bytes(16, 'big'))##


else:   
    primeirojoga = True; 



while ((server.numPecas > 0) or primeirojoga):
  primeirojoga = False

  numPecasRestantes = int.from_bytes(tcp_dados.recv(16), 'big') #recive

  if (numPecasRestantes == 0):
      server.theEnd(False)

  server.numPecas = numPecasRestantes

  print(f"Numero de pecas - RECEIVED: {numPecasRestantes}")

  if (server.numPecas == 0):
      print("Fim do jogo")  
       
  
  retirada = server.escolhe_jogada()

  print(f"\nVocê tirou {retirada} peça(s).")
    
  server.numPecas = server.numPecas - retirada


  if (server.numPecas == 0): 
    server.theEnd(True)

  print(f"Numero de pecas: {server.numPecas}")


  tcp_dados.send(server.numPecas.to_bytes(16, 'big')) #send
# =========================================================================



tcp_dados.close()

input("Aperte para encerrar")