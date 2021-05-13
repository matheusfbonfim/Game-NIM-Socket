# Bibliotecas 
import random

# VARIAVEIS GLOBAIS

n = None                    # Quantidade de peças
m = None                    # Limite de peças por jogada
option_client = None        # Atribui [0] - Impar [1] - Par
vez = None
retirada = 0

# ===================================================================

def computador_escolhe_jogada(n,m):
    """
    - Solicita quantas peças o usuário irá tirar
    - Verifica a validade dos parâmetros
    - Retorna o valor de peças retiradas
    """
    print("\nSERVIDOR\n")
    numero = int(input('\nQuantas peças você vai tirar? '))

    while numero > n or numero > m or numero <= 0:
        print("\nOops! Jogada inválida! Tente de novo.")
        numero = int(input("\nQuantas peças você vai tirar? "))
    return numero

# ===================================================================

def usuario_escolhe_jogada(n,m):
    """
    - Solicita quantas peças o usuário irá tirar
    - Verifica a validade dos parâmetros
    - Retorna o valor de peças retiradas
    """
    print("\nUSUARIO\n")
    numero = int(input('\nQuantas peças você vai tirar? '))

    while numero > n or numero > m or numero <= 0:
        print("\nOops! Jogada inválida! Tente de novo.")
        numero = int(input("\nQuantas peças você vai tirar? "))
    return numero

# ===================================================================

def partida():
    n = int(input("\nQuantas peças? "))
    m = int(input("Limite de peças por jogada? "))

    vez = None
    retirada = 0

    while m < 1:
        print("O limite de peças é inválido. O limite de peças deve ser menor ou igual a quantidade de peças")
        m = int(input("Limite de peças por jogada? "))

    if (n % (m + 1)) == 0:

        print("\nVocê começa!")
        vez = False

        while n > 0:
            if not(vez):
                retirada = usuario_escolhe_jogada(n, m)
                print(f"\nVocê tirou {retirada} peça(s).")
                n = n - retirada
                if n == 0:
                    vez = False
                else:
                    print(f"Agora restam {n} peças no tabuleiro.")
                    vez = True
            else:
                retirada = computador_escolhe_jogada(n, m)
                print(f"\nO computador tirou {retirada} peça(s).")
                n = n - retirada
                if n == 0:
                    vez = True
                else:
                    print(f"Agora restam {n} peças no tabuleiro.")
                    vez = False

        if vez:
            print("Fim do jogo! O computador ganhou!")
            return True
        else:
            print("Fim do jogo! O você ganhou!")
            return False

    else:
        print("\nComputador começa!")
        vez = True # Vez do computador

        while n > 0:
            if vez:
                retirada = computador_escolhe_jogada(n,m)
                print(f"\nO computador tirou {retirada} peça(s).")
                n = n - retirada
                if n == 0:
                    vez = True
                else:
                    vez = False
                    print(f"Agora restam {n} peças no tabuleiro.")
            else:
                retirada = usuario_escolhe_jogada(n, m)
                print(f"\nVocê tirou {retirada} peça(s).")
                n = n - retirada

                if n == 0:
                    vez = False
                else:
                    print(f"Agora restam {n} peças no tabuleiro.")
                    vez = True

        if vez:
            print("Fim do jogo! O computador ganhou!")
            return True
        else:
            print("Fim do jogo! O você ganhou!")
            return False
# ===================================================================

def step1_server():
    print("\nSERVIDOR\n")


    print("Bem-vindo ao jogo do NIM! - Jogador 1",end='\n')
    print("Para iniciar a partida é preciso determinar alguns parâmetros:",end='\n')

    global n    # Referência a variavel global - Quantidade de peças
    global m    # Referência a variavel global - Limite de peças por jogada

    n = int(input("\nQuantas peças? "))
    m = int(input("Limite de peças por jogada? "))

    # Verifica limite de número de peças 
    while m < 1:
        print("O limite de peças é inválido. O limite de peças deve ser menor ou igual a quantidade de peças")
        m = int(input("Limite de peças por jogada? "))
    
    # Enviar informações para o cliente

# ===================================================================

def step2_client():
    print("\n\nCLIENTE\n")
    
    print("BEM-VINDO AO JOGO DO NIM! - Jogador 2",end='\n')

    # Informação vinda do servidor 
    print("A partida está configurada com os seguintes parâmetros:", end='\n')
    print(f"\t 1- Número de peças: {n} peças\n")
    print(f"\t 2- Peças por jogada: 1 a {m} peças\n\n")

    # Decisão de quem começa o jogo
    print("ÍNICIO DO GAME NIM \n")
    print("Quem começa o jogo? Vamos decidir por impar ou par\n")
    print("\t [0] - Ímpar\n")
    print("\t [1] - PAR\n\n")

    decision = int(input("Digite a opção [0 ou 1]: "))

    # Verifica se foi escrito uma opção válida
    while (decision != 0) & (decision != 1):
        print("A opção escolhida é inválida\n")
        print("\t [0] - Ímpar\n")
        print("\t [1] - PAR\n")
        decision = int(input("Limite de peças por jogada? "))

    # Caso seja [0] - Impar ou [1] - Par
    if decision == 1:
        global option_client
        option_client = 1
    else:
        option_client = 0

# ===================================================================

def step3_server():
    print("\n\nSERVIDOR\n")

    # [0] - Impar [1] - Par
    if (random.randint(0, 1) == option_client):
        print("O jogador 2 (client) ganhou o ímpar ou par e iniciará o jogo\n")
        step4_client()
    else:
        print("Está com sorte! Você ganhou o impar ou par e iniciará o jogo\n")
        step4_server()

# ===================================================================

def step4_client():
    print("Está com sorte! Você ganhou o impar ou par e iniciará o jogo\n")

    global n
    global retirada
    global vez

    vez = False

    while n > 0:
        if not(vez):
            retirada = usuario_escolhe_jogada(n, m)
            print(f"\nVocê tirou {retirada} peça(s).")
            n = n - retirada

            if n == 0:
                vez = False
            else:
                print(f"Agora restam {n} peças no tabuleiro.")
                vez = True
        else:
            retirada = computador_escolhe_jogada(n, m)
            print(f"\nO computador tirou {retirada} peça(s).")
            n = n - retirada
            if n == 0:
                vez = True
            else:
                print(f"Agora restam {n} peças no tabuleiro.")
                vez = False

    end()


# ===================================================================
def step4_server():
    global vez
    global n
    global retirada

    vez = False

    while n > 0:
        if not(vez):
            retirada = usuario_escolhe_jogada(n, m)
            print(f"\nVocê tirou {retirada} peça(s).")
            n = n - retirada

            if n == 0:
                vez = False
            else:
                print(f"Agora restam {n} peças no tabuleiro.")
                vez = True
        else:
            retirada = computador_escolhe_jogada(n, m)
            print(f"\nO computador tirou {retirada} peça(s).")
            n = n - retirada
            if n == 0:
                vez = True
            else:
                print(f"Agora restam {n} peças no tabuleiro.")
                vez = False

    end()

# ===================================================================

def end():

    global vez
   
    if vez:
        print("Fim do jogo! O server ganhou!")
        return True
    else:
        print("Fim do jogo! O jogador monstro ganhou!")
        return False



def main():
    step1_server()
    step2_client()
    step3_server()

    

main()