import pymysql
import subprocess
import os
from dotenv import load_dotenv

subprocess.run('cls', shell=True)
load_dotenv()

conexao = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD", ""), 
    database=os.getenv("DB_NAME")
)


def insert_compras(tabela,colunas_lista, *args):
    item_tratado = []
    colunas_formatadas = ", ".join(colunas_lista)
    placeholders = ", ".join(["%s"] * len(args))
    print(item_tratado)
    comando_sql = f"INSERT INTO {tabela} ({colunas_formatadas}) VALUES ({placeholders})"
    cursor.execute(comando_sql, args)
    conexao.commit()
    print("Compra inserida com sucesso!")
def selecionar(tabela, coluna_filtro= None, valor_filtro = None):
    if coluna_filtro is None: #dps puxar o datetime.date como só data ou aparecer somente o números
        comando_selecionar = f"SELECT * FROM {tabela}"
        print(f"\nNa tabela {tabela} temos: {tabela} tabela(s)")
        cursor.execute(comando_selecionar)
    else:
        comando_selecionar = f"SELECT * FROM {tabela} WHERE {coluna_filtro} = %s"
        
        print(f"\nNa tabela {tabela} temos: {cursor.execute(comando_selecionar,(valor_filtro))} tabela(s)")

    compras = cursor.fetchall()
    # print(f"Aqui estão os dados da sua tabela {tabela}: ")
    for linha in compras:
        print("\n",linha)
    return 
def deletar(tabela, coluna_filtro, valor_deletar):
    comando_selecionar = f"DELETE FROM {tabela} WHERE {coluna_filtro} = %s;"
    cursor.execute(comando_selecionar, (valor_deletar))
    print(f"A coluna do filtro {valor_deletar} foi deletada")
    conexao.commit()
    return


def mostrar_tabelas():
    i=0
    cursor.execute("SHOW TABLES;")
    global tabelas
    tabelas = cursor.fetchall()
    for tabela in tabelas:
                print(i,tabela[0])
                i += 1
    return
def mostrar_colunas():
    global collumns
    global table 
    global pacote
    i= 0 
    table = tabelas[resposta][0]
    comando_selecionar = f"SHOW COLUMNS FROM {table};"
    cursor.execute(comando_selecionar)
    collumns = cursor.fetchall()
    pacote = []
    for coluna in collumns:
        print("\n",i, coluna[0])
        i += 1
        pacote.append(coluna[0])
     

print("Conexão bem sucedida com o MySQL do XAMPP")

cursor = conexao.cursor()


while True:
    i= 0 
    pergunta = int(input('\nO que você quer fazer?\n [1]SELECT\t [2]INSERT\t [3]DELETE\n'))
    print("\n")
    if pergunta == 1:
        mostrar_tabelas()
        resposta = int(input("\nDe qual tabela você quer as informações?:\t"))
        pergunta = input("\nvocê vai querer uma informação especifica?[S]im[N]ão: \t").lower()
        if pergunta.startswith('n'):
            selecionar(tabelas[resposta][0])
        else:
            mostrar_colunas()
            pergunta_2 = int(input("\nvocê quer filtrar por qual informação?: \t"))
            pergunta_3 = input(f"\nSELECT * FROM {table} WHERE {collumns[pergunta_2][0]} =:\t")

            selecionar(table,collumns[pergunta_2][0],pergunta_3)     
            
            
    elif pergunta == 2:
        mostrar_tabelas()
    
        resposta = int(input("\nDe qual tabela você quer inserir as informações?:\t"))
        mostrar_colunas()

        colunas = ", ".join(pacote)#para aparecer bonitinho ali na linha 104
       
        pacote_valores = []
        for item in pacote:
            item_resposta = input(f"Para o item: {item} qual seria o valor?:")
            i+=1
            pacote_valores.append(item_resposta)
        item = ", ".join(pacote_valores)
        pergunta_insert = input(f"INSERT INTO {tabelas[resposta][0]} ({colunas}) VALUES ({item}) pode commitar?:").lower()
        if pergunta_insert.startswith('s'):
            insert_compras(tabelas[resposta][0], pacote, *pacote_valores)
        else:
            continue
    elif pergunta == 3:
        mostrar_tabelas()
        resposta = int(input("\nDe qual tabela você quer deletar as informações?:\t"))
        mostrar_colunas()
        pergunta_2 = int(input("\nvocê quer filtrar por qual informação?: \t"))
        pergunta_3 = input(f"DELETE FROM {table} WHERE {collumns[pergunta_2][0]} = ")
        deletar(table, collumns[pergunta_2][0],pergunta_3)


        # deletar()
#PROXIMA ETAPA, CONCLUIR O [3] DELETE, para deletar as colunas.
#FALTA:TELA DE LOGIN, TRATAMENTO DOS DADOS, ADIÇÃO DE FUNÇÕES
# conexao.commit() isso é para atualizar as informações do bdd

