import csv
import psycopg2
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama.llms import OllamaLLM


llm = OllamaLLM(model = 'llama3.1:8b')

output_parser = StrOutputParser()

def gera_insights():

	conn = psycopg2.connect(
		dbname= 'db',
		user= 'user',
		password= 'pass1010',
		host= 'localhost',
		port= '5553'
	)

	cursor = conn.cursor()

	query = """
		SELECT 	t.id_transacao AS id_transacao,
				c.nome AS cliente,
				i.descricao AS imovel_descricao,
				t.valor AS valor_imovel,
				t.data_transacao AS data_transaacao,
				t.tipo_transacao AS tipo_transacao,
				t.status AS status,
				h.data_modificacao AS data_modificacao,
				h.descricao AS historico_descricao
			FROM projeto.transacoes_financeiras t
			JOIN projeto.clientes c ON t.id_cliente = c.id_cliente
			JOIN projeto.imoveis i ON t.id_imovel = i.id_imovel
			JOIN projeto.historico_transacoes h ON t.id_transacao = h.id_transacao
			WHERE t.valor > 1000000
			   OR (t.status = 'Concluida' AND h.descricao LIKE '%Cancelamento%')
			   OR EXISTS (SELECT 1 FROM projeto.transacoes_financeiras t2
			   			   WHERE t2.id_imovel = t.id_imovel
			   			     AND t2.id_transacao != t.id_transacao
			   			     AND ABS(EXTRACT(DAY FROM AGE(t2.data_transacao, t.data_transacao))) < 30)
			ORDER BY t.data_transacao DESC;
	"""
	cursor.execute(query)

	rows = cursor.fetchall()

	insights = []

	prompt = ChatPromptTemplate.from_messages(
		[
			('system', 'Você é um analista imobiliário especializado. Analise os dados e forneça feedback em português do Brasil sobre a detecção de fraudes em transaações financeiras imobiliárias'),
			('user', 'question {question}')
		]
	)

	chain = prompt | llm | output_parser

	for row in rows:

		id_transacao, cliente, imovel_descricao, valor_imovel, data_transacao, tipo_transacao, status, data_modificacao, historico_descricao = row
		consulta = f'ID_TRANSAÇÃO: {id_transacao} NOME DO CLIENTE: {cliente} DESCRIÇÃO DO IMOVEL: {imovel_descricao} VALOR DO IMOVEL ${valor_imovel:.2f} DATA DA TRANSAÇÃO: {data_transacao} TIPO DA TRANSAÇÃO: {tipo_transacao} STATUS: {status} DATA MODIFICAÇÃO: {data_modificacao} DESCRIÇÃO DO HISTORICO: {historico_descricao}.'
		response = chain.invoke({'question': consulta})
		insights.append(response)
	
	conn.close()

	with open('projeto_analise.csv', mode='w', newline='', encoding='utf8') as file:
		writer = csv.writer(file)
		writer.writerow(['Insight'])
		for insight in insights:
			writer.writerow([insight])

	return insights

insights = gera_insights()

for insight in insights:
	print(insight)