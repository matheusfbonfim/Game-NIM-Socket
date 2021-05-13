par = None

import random

def funcao():
  global par
  
  decision = 5

  if (decision == 1):
    par = True
  else:
    par = False


def main():
  funcao()
  print(f"Resposta é {random.randint(0,1)}")


main()