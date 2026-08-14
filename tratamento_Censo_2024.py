import pandas as pd

CAMINHO_ARQUIVO = "dados/Censo_escolar/2024/microdados_censo_escolar_2024_defeso/dados/microdados_ed_basica_2024.csv"
NOME_NOVO_ARQUIVO = "CensoEscolarMicrodados2024.xlsx"

print("Iniciando o tratamento do Censo 2024...")

df_censo = pd.read_csv(CAMINHO_ARQUIVO, encoding="latin1", sep=";")
#dados\Censo_escolar\2024\microdados_censo_escolar_2024_defeso\dados\microdados_ed_basica_2024.csv

print("Dados do Censo 2024 carregados com sucesso!")
print(df_censo.head())


# Filtrando dados do Espírto Santo
df_censo = df_censo[df_censo['NO_UF'] == 'Espírito Santo']

# Em fase de teste, será utilizado o municipio de NO_MUNICIPIO = Divino de São Lourenço
df_censo = df_censo[df_censo['NO_MUNICIPIO'] == 'Divino de São Lourenço']

# Filtrando apenas escolas estaduais e municipais (1 - Federal, 2 - Estadual, 3 - Municipal, 4 - Privada)
df_censo = df_censo[df_censo["TP_DEPENDENCIA"].isin([2, 3])]

# Selecionando apenas as colunas de interesse
colunas = [
    "NO_MUNICIPIO", "NO_ENTIDADE", "CO_ENTIDADE", "TP_DEPENDENCIA", "TP_LOCALIZACAO", 
    "TP_LOCALIZACAO_DIFERENCIADA", "TP_AEE", "IN_EJA_FUND", "IN_EJA_MED", 
    "IN_INF", "IN_INF_CRE", "IN_INF_PRE", "IN_FUND", "IN_FUND_AI", "IN_FUND_AF",
    "IN_MED", "IN_ESP"
    ]
df_censo = df_censo[colunas].copy()

# Salvando arquivo tratado em Excel
df_censo.to_excel(NOME_NOVO_ARQUIVO, index=False)