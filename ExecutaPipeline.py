import subprocess
import time

def executa_comando(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f'\nComando "{command}" executado com sucesso!')
        print('\nSaida:\n', result.stdout)
    except subprocess.CalledProcessError as e:
        print(f'\nErro ao executar o comando "{command}".')
        print('\nErro:\n', e.stderr)

def executa_pipeline(script_name):
    try:
        result = subprocess.run(['python', script_name], check=True, capture_output=True, text=True)
        print(f'\nScript {script_name} executado com sucesso!')
        print('\nSaida:\n', result.stdout)
    except subprocess.CalledProcessError as e:
        print(f'\nErro ao executar o script {script_name}.')
        print('\nErro:\n', e.stderr)

docker_command = 'docker run --name projeto_docker -p 5553:5432 -e POSTGRES_USER=user -e POSTGRES_PASSWORD=pass1010 -e POSTGRES_DB=db -d postgres:16.1'
pip_command = 'pip install -r requirements.txt'

start_time = time.time()

executa_comando(docker_command)
executa_comando(pip_command)

scripts = [
    'CriaTabelas.py',
    'CarregaDados.py',
    'ExecutaLLM.py'
]

for script in scripts:
    executa_pipeline(script)

destroy_docker_command = 'docker rm -f projeto_docker'
executa_comando(destroy_docker_command)

end_time = time.time()
total_time = end_time - start_time

print(f'\nPipeline executado com sucesso.')
print(f'Tempo total de execução: {total_time:.2f} segundos.\n')