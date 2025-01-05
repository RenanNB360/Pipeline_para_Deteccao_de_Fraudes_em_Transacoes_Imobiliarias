import psycopg2

def executa_script_sql(filename):
    try:
        conn = psycopg2.connect(
            dbname='db',
            user='user',
            password='pass1010',
            host='localhost',
            port='5553'
        )
        print('A conexão com o banco de dados foi estabelecida com sucesso.')
        
        cur = conn.cursor()

        with open(filename, 'r') as file:
            sql_script = file.read()

        try:
            cur.execute(sql_script)
            conn.commit()
            print('\nScript executado com sucesso!\n')
        except Exception as e:
            conn.rollback()
            print(f'Erro ao executar o script: {e}')
        finally:
            cur.close()
            conn.close()
    except psycopg2.OperationalError as e:
        print(f'Erro ao conectar ao banco de dados: {e}')

executa_script_sql('Tabelas.sql')
