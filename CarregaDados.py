import psycopg2
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://user:pass1010@localhost:5553/db')


print('\nIniciando o Processo de Carga dos Dados\n')


def carrega_dados(csv_file, table_name, schema):

	try:
		df = pd.read_csv(csv_file)
		df.to_sql(table_name, engine, schema= schema, if_exists = 'append', index= False)
		print(f'Dados do arquivo {csv_file} foram inseridos na tabela {schema}.{table_name}.')
	except Exception as e:
		print(f'Erro ao inserir dados do arquivo {csv_file} na tabela {schema}.{table_name}: {e}')


carrega_dados('clientes.csv', 'clientes', 'projeto')
carrega_dados('imoveis.csv', 'imoveis', 'projeto')
carrega_dados('transacoes_financeiras.csv', 'transacoes_financeiras', 'projeto')
carrega_dados('historico_transacoes.csv', 'historico_transacoes', 'projeto')

print('\nCarga Executada com Sucesso! Use o pdAdmin para checar os dados se desejar!\n')
print('\nIniciando o Projeto de Análise de Daados com IA. Seja paciente e aguarde o resultado!\n')