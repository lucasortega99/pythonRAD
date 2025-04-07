import os

def cria_arquivo():
    nome_do_arquivo = input('Por favor digite o nome do arquivo, ou enter para o default (arquivo.txt):')
    if nome_do_arquivo == '':
        nome_do_arquivo = 'arquivo.txt'

    with open(nome_do_arquivo, 'w') as arquivo:
        print(f'Arquivo {nome_do_arquivo} criado com sucesso!')
        arquivo.close()
        input('Pressione enter para continuar...')

    return

def adiciona_linhas():
    nome_do_arquivo = input('Por favor digite o nome do arquivo, ou enter para o default (arquivo.txt):')
    if nome_do_arquivo == '':
        nome_do_arquivo = 'arquivo.txt'

    with open(nome_do_arquivo, 'a') as arquivo:
        linha = input(f'Digite a linha a ser inserida no arquivo {nome_do_arquivo} (digite 0 para sair):')
        while linha != '0':
            arquivo.write(f'{linha}\n')
            linha = input(f'Digite a proxima linha a ser inserida no arquivo {nome_do_arquivo} (digite 0 para sair):')
        arquivo.close()
        input('Pressione enter para continuar...')
    return

def mostra_linhas():
    nome_do_arquivo = input('Por favor digite o nome do arquivo, ou enter para o default (arquivo.txt):')
    if nome_do_arquivo == '':
        nome_do_arquivo = 'arquivo.txt'

    with open(nome_do_arquivo, 'r') as arquivo:
        for linha in arquivo:
            print(linha)
        arquivo.close()
        input('Pressione enter para continuar...')

    return

option = 'start'
while option != 'x':

    _=os.system("cls")

    if option == '1':
        cria_arquivo()
        _=os.system("cls")
    elif option == '2':
        adiciona_linhas()
        _=os.system("cls")
    elif option == '3':
        mostra_linhas()
        _=os.system("cls")
    elif option.lower() == 'x':
        exit()
    elif option != 'start':
        print('Opcao invalida, digite novamente...')
    
    option = input("""Digite uma das opcoes:
          1 - Criar arquivo
          2 - Adicionar linhas ao arquivo
          3 - Mostrar arquivo
          x - Sair
          Opcao: """)
