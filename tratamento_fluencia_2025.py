import pandas as pd

def realizar_filtragem(df):
    """
    Filtra os dados da Avaliação de Fluência em Leitura para o estado do
    Espírito Santo e para as redes estadual e municipal.

    A base traz também linhas agregadas com Rede = 'PÚBLICA', que somam
    Estadual + Municipal e duplicariam os registros caso não fossem
    descartadas.
    """

    # Filtrando dados do Espírito Santo
    df = df[df['Estado'] == 'ESPÍRITO SANTO']

    # Filtrando apenas rede estadual e municipal
    df = df[df["Rede"].isin(["ESTADUAL", "MUNICIPAL"])]

    df = df[df["Tipo"] != "TURMA"]

    return df

def selecionar_colunas(df):

    colunas = [
        "Tipo",
        "Regional",
        "Município",
        "Código da escola",
        "Escola",
        "Edição",
        "Rede",
        "Etapa",

        "Pré-leitor - Total %",
        "Leitor iniciante %",
        "Leitor fluente %",
    ]

    return df[colunas].copy()

def renomear_colunas(df):
    """
    Renomeia as colunas de identificação e dos indicadores
    de Fluência em Leitura.
    """

    nomes_colunas = {
        "Regional": "SuperintendenciaRegionalDeEducacao",
        "Município": "Municipio",
        "Código da escola": "CodigoINEP",
        "Edição": "Edicao",
        "Rede": "DependenciaAdministrativa",

        "Pré-leitor - Total %": "PreLeitor_Total_Percentual",
        "Leitor iniciante %": "LeitorIniciante_Percentual",
        "Leitor fluente %": "LeitorFluente_Percentual",
    }

    return df.rename(columns=nomes_colunas)

def tratar_valores_ausentes(df):
    """
    Converte o marcador '-' (utilizado quando o campo não se aplica ao
    nível de agregação da linha, ex.: Escola em uma linha do tipo
    MUNICIPIO) em valores nulos.
    """

    return df.replace("-", pd.NA)

def ordenar_colunas(df):
    """
    Reordena as colunas do DataFrame para a estrutura
    utilizada no banco analítico do Painel de Controle - Educação.
    """

    colunas = [
        "Tipo",
        "SuperintendenciaRegionalDeEducacao",
        "Municipio",
        "CodigoINEP",
        "Escola",
        "Edicao",
        "DependenciaAdministrativa",
        "Etapa",

        "PreLeitor_Total_Percentual",
        "LeitorIniciante_Percentual",
        "LeitorFluente_Percentual",
    ]

    return df[colunas].copy()

CAMINHO_ARQUIVO = "dados/Fluência/2025/1º ed. 2025 - Rede estadual e Redes Municipais de Ensino.xlsx"

NOME_NOVO_ARQUIVO = 'Fluencia2025.xlsx'

print("Iniciando o tratamento da Avaliação de Fluência em Leitura 2025...")

df_fluencia = pd.read_excel(CAMINHO_ARQUIVO, sheet_name="F_3")

print("Dados de Fluência carregados com sucesso!")

df_fluencia = realizar_filtragem(df_fluencia)
df_fluencia = selecionar_colunas(df_fluencia)
df_fluencia = renomear_colunas(df_fluencia)
df_fluencia = tratar_valores_ausentes(df_fluencia)
df_fluencia = ordenar_colunas(df_fluencia)

# Salvando arquivo tratado em Excel
df_fluencia.to_excel(NOME_NOVO_ARQUIVO, index=False)
