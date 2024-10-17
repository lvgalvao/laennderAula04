import pandas as pd
import os

def extrair_dados(caminho_arquivo):
    print("Extraindo dados...")
    df = pd.read_csv(caminho_arquivo)
    return df

def transformar_dados(df):
    print("Transformando dados...")
    # Remover duplicatas
    df = df.drop_duplicates()
    
    # Tratar valores nulos
    df['quantidade'] = df['quantidade'].fillna(0)
    df['valor_total'] = df['valor_total'].fillna(df['quantidade'] * df['valor_unitario'])
    
    # Adicionar coluna de mês
    df['mes'] = pd.to_datetime(df['data']).dt.strftime('%B')
    
    # Calcular total de vendas por produto
    df['total_vendas'] = df['quantidade'] * df['valor_unitario']
    
    return df

def carregar_dados(df, caminho_saida_csv, caminho_saida_parquet):
    print("Carregando dados...")
    # Salvar em CSV
    df.to_csv(caminho_saida_csv, index=False)
    print(f"Dados salvos em CSV: {caminho_saida_csv}")
    
    # Salvar em Parquet
    df.to_parquet(caminho_saida_parquet, index=False)
    print(f"Dados salvos em Parquet: {caminho_saida_parquet}")

def processo_etl():
    # Definir caminhos
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_entrada = os.path.join(diretorio_atual, '..', 'data', 'input', 'vendas.csv')
    caminho_saida_csv = os.path.join(diretorio_atual, '..', 'data', 'output', 'vendas_processadas.csv')
    caminho_saida_parquet = os.path.join(diretorio_atual, '..', 'data', 'output', 'vendas_processadas.parquet')
    
    # Executar ETL
    dados_brutos = extrair_dados(caminho_entrada)
    dados_transformados = transformar_dados(dados_brutos)
    carregar_dados(dados_transformados, caminho_saida_csv, caminho_saida_parquet)
    
    print("Processo ETL concluído com sucesso!")

if __name__ == "__main__":
    processo_etl()
