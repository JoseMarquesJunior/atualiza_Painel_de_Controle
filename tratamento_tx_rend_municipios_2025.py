import pandas as pd

def realizar_filtragem(df):
    """
    Filtra os dados da Taxa de Rendimento Escolar para o estado do
    Espírito Santo e para as redes estadual e municipal.
    """

    # Filtrando dados do Espírito Santo
    df = df[df['SG_UF'] == 'ES']

    # Em fase de teste, será utilizado o municipio de NO_MUNICIPIO = Divino de São Lourenço
    #df = df[df['NO_MUNICIPIO'] == 'Divino de São Lourenço']

    # Filtrando apenas rede estadual e municipal
    df = df[df["NO_DEPENDENCIA"].isin(["Municipal", "Estadual"])]

    return df

def selecionar_colunas(df):

    colunas = [
        "NU_ANO_CENSO",
        "NO_MUNICIPIO",
        "CO_MUNICIPIO",
        "NO_CATEGORIA",
        "NO_DEPENDENCIA",

        "1_CAT_FUN_AI",
        "1_CAT_FUN_AF",
        "1_CAT_FUN",
        "1_CAT_MED",

        "3_CAT_FUN_AI",
        "3_CAT_FUN_AF",
        "3_CAT_FUN",
        "3_CAT_MED",
    ]

    return df[colunas].copy()

def renomear_colunas(df):
    """
    Renomeia as colunas de identificação do município e dos indicadores
    de Taxa de Rendimento Escolar (Aprovação e Abandono).
    """

    nomes_colunas = {
        "NU_ANO_CENSO": "Ano",
        "NO_MUNICIPIO": "Municipio",
        "CO_MUNICIPIO": "CodigoDoMunicipio",
        "NO_CATEGORIA": "Localizacao",
        "NO_DEPENDENCIA": "DependenciaAdministrativa",

        "1_CAT_FUN_AI": "TaxaDeAprovacao_EnsinoFundamental_AnosIniciais",
        "1_CAT_FUN_AF": "TaxaDeAprovacao_EnsinoFundamental_AnosFinais",
        "1_CAT_FUN": "TaxaDeAprovacao_EnsinoFundamental_Total",
        "1_CAT_MED": "TaxaDeAprovacao_EnsinoMedio_Total",

        "3_CAT_FUN_AI": "TaxaDeAbandono_EnsinoFundamental_AnosIniciais",
        "3_CAT_FUN_AF": "TaxaDeAbandono_EnsinoFundamental_AnosFinais",
        "3_CAT_FUN": "TaxaDeAbandono_EnsinoFundamental_Total",
        "3_CAT_MED": "TaxaDeAbandono_EnsinoMedio_Total",
    }

    return df.rename(columns=nomes_colunas)

def tratar_valores_ausentes(df):
    """
    Converte o marcador '--' (utilizado pelo INEP quando não há dados
    suficientes para o cálculo da taxa) em valores nulos e garante que
    as colunas de taxa fiquem no tipo numérico.
    """

    colunas_taxas = [coluna for coluna in df.columns if coluna.startswith("Taxa")]

    df[colunas_taxas] = df[colunas_taxas].replace("--", pd.NA)

    for coluna in colunas_taxas:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    return df

def ordenar_colunas(df):
    """
    Reordena as colunas do DataFrame para a estrutura
    utilizada no banco analítico do Painel de Controle - Educação.
    """

    colunas = [
        "Ano",
        "Municipio",
        "CodigoDoMunicipio",
        "Localizacao",
        "DependenciaAdministrativa",

        "TaxaDeAprovacao_EnsinoFundamental_AnosIniciais",
        "TaxaDeAprovacao_EnsinoFundamental_AnosFinais",
        "TaxaDeAprovacao_EnsinoFundamental_Total",
        "TaxaDeAprovacao_EnsinoMedio_Total",

        "TaxaDeAbandono_EnsinoFundamental_AnosIniciais",
        "TaxaDeAbandono_EnsinoFundamental_AnosFinais",
        "TaxaDeAbandono_EnsinoFundamental_Total",
        "TaxaDeAbandono_EnsinoMedio_Total",
    ]

    return df[colunas].copy()

CAMINHO_ARQUIVO = "dados/Taxa de Rendimento/tx_rend_municipios_2025/tx_rend_municipios_2025.xlsx"

NOME_NOVO_ARQUIVO = 'TaxaRendimento_Municipios2025.xlsx'

print("Iniciando o tratamento da Taxa de Rendimento Municípios 2025...")

df_tx_rend = pd.read_excel(CAMINHO_ARQUIVO, sheet_name="MUNICIPIOS ", skiprows=8)

print("Dados da Taxa de Rendimento Municípios carregados com sucesso!")

df_tx_rend = realizar_filtragem(df_tx_rend)
df_tx_rend = selecionar_colunas(df_tx_rend)
df_tx_rend = renomear_colunas(df_tx_rend)
df_tx_rend = tratar_valores_ausentes(df_tx_rend)
df_tx_rend = ordenar_colunas(df_tx_rend)

# Salvando arquivo tratado em Excel
df_tx_rend.to_excel(NOME_NOVO_ARQUIVO, index=False)
