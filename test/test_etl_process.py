import pytest
import pandas as pd
import os
from etl_process.etl_process import extrair_dados, transformar_dados, carregar_dados

@pytest.fixture
def dados_exemplo():
    return pd.DataFrame({
        'data': ['2023-01-01', '2023-02-01', '2023-03-01'],
        'produto': ['A', 'B', 'A'],
        'quantidade': [2, None, 3],
        'valor_unitario': [10.0, 15.0, 12.0],
        'valor_total': [20.0, None, 36.0]
    })

def test_extrair_dados(tmp_path):
    # Criar um arquivo CSV temporário para testar
    arquivo_teste = tmp_path / "teste_vendas.csv"
    pd.DataFrame({'coluna1': [1, 2, 3]}).to_csv(arquivo_teste, index=False)
    
    resultado = extrair_dados(arquivo_teste)
    assert isinstance(resultado, pd.DataFrame)
    assert len(resultado) == 3

def test_transformar_dados(dados_exemplo):
    resultado = transformar_dados(dados_exemplo)
    
    assert 'mes' in resultado.columns
    assert 'total_vendas' in resultado.columns
    assert resultado['quantidade'].isnull().sum() == 0
    assert resultado['valor_total'].isnull().sum() == 0
    assert len(resultado) == len(dados_exemplo.drop_duplicates())

def test_carregar_dados(tmp_path, dados_exemplo):
    caminho_saida_csv = tmp_path / "teste_saida.csv"
    caminho_saida_parquet = tmp_path / "teste_saida.parquet"
    
    carregar_dados(dados_exemplo, caminho_saida_csv, caminho_saida_parquet)
    
    assert os.path.exists(caminho_saida_csv)
    assert os.path.exists(caminho_saida_parquet)
    
    df_csv = pd.read_csv(caminho_saida_csv)
    df_parquet = pd.read_parquet(caminho_saida_parquet)
    
    assert df_csv.equals(dados_exemplo)
    assert df_parquet.equals(dados_exemplo)
