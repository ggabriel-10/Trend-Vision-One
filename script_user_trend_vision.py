import csv
import re

# Arquivo CSV a ser lido e o arquivo CSV de saída
csv_file = 'base.csv'
output_file = 'resultados.csv'

# Função para extrair informações do campo Detail info
def extract_info(detail_info):
    info = {}
    try:
        info['assetCriticality'] = re.search(r'assetCriticality:\s*(\d+)', detail_info).group(1)
        info['logonFailCount'] = re.search(r'logonFailCount:\s*(\d+)', detail_info).group(1)
        info['firstSeen'] = re.search(r'firstSeen:\s*([\d\-\s:]+)', detail_info).group(1)
        info['lastSeen'] = re.search(r'lastSeen:\s*([\d\-\s:]+)', detail_info).group(1)
        info['logonAttempts'] = re.search(r'logonAttempts:\s*(\d+)', detail_info).group(1)
        info['ips'] = ', '.join(re.findall(r'ips:\s*([\d.]+)', detail_info))
        info['locations'] = ', '.join(re.findall(r'locations:\s*([\w-]+)', detail_info))
        info['countries'] = ', '.join(re.findall(r'location country:\s*([\w\s]+)', detail_info))
    except AttributeError:
        # Caso alguma informação não seja encontrada
        pass
    return info

# Lendo o arquivo CSV e extraindo as informações
with open(csv_file, 'r', newline='', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    
    # Campos para o CSV de saída
    fieldnames = ['Usuário', 'Incidente', 'Criticidade', 'Indice Criticidade', 'Quantidade de Falhas', 'Primeira Detecção', 'Última Detecção', 'IP', 'País']
    
    # Abrindo o arquivo de saída para escrita
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            usuario = row['Asset']
            risk_event = row['Risk event']
            risk_asset = row['Risk level']
            detail_info = row['Detail info']
            
            extracted_info = extract_info(detail_info)
            
            # Criando um dicionário para a linha a ser escrita no CSV de saída
            output_row = {
                'Usuário': usuario,
                'Incidente': risk_event,
                'Criticidade': risk_asset,
                'Indice Criticidade': extracted_info.get('assetCriticality'),
                'Quantidade de Falhas': extracted_info.get('logonFailCount'),
                'Primeira Detecção': extracted_info.get('firstSeen'),
                'Última Detecção': extracted_info.get('lastSeen'),
                'IP': extracted_info.get('ips'),
                'País': extracted_info.get('locations'),
            }
            
            writer.writerow(output_row)
            
            # Também exibe os resultados no console (opcional)
            print(f"Usuário: {usuario}")
            print(f"Incidente: {risk_event}")
            print(f"Criticidade: {risk_asset}")
            print(f"Indice Criticidade: {extracted_info.get('assetCriticality')}")
            print(f"Quantidade de Falhas: {extracted_info.get('logonFailCount')}")
            print(f"Primeira Detecção: {extracted_info.get('firstSeen')}")
            print(f"Última Detecção: {extracted_info.get('lastSeen')}")
            print(f"IP: {extracted_info.get('ips')}")
            print(f"País: {extracted_info.get('locations')}")
            print("-" * 40)

print(f"Os resultados foram salvos em '{output_file}'.")
