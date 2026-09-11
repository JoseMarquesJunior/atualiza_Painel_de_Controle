import pandas as pd

def selecionar_colunas(df):

    df = df.copy()
    df["Ano"] = 2025

    colunas = [
        "Ano",
        "NO_MUNICIPIO",
        "ID_ESCOLA",
        "NO_ESCOLA",
        "REDE",
        "VL_NOTA_MATEMATICA_2025",
        "VL_NOTA_PORTUGUES_2025",
        "VL_OBSERVADO_2025"
    ]

    return df[colunas].copy()

def renomear_colunas(df, etapa):
    """
    Renomeia as colunas dos indicadores do SAEB/IDEB
    de acordo com a etapa de ensino.

    Parâmetros:
        df (DataFrame): DataFrame contendo as colunas originais.
        etapa (str): Etapa de ensino:
            - "AI": Ensino Fundamental - Anos Iniciais
            - "AF": Ensino Fundamental - Anos Finais
            - "EM": Ensino Médio

    Retorna:
        DataFrame: DataFrame com as colunas renomeadas.
    """

    nomes_colunas = {
        "AI": {
            "VL_NOTA_MATEMATICA_2025":
                "NotaSAEB_Matematica_EnsinoFundamental_AnosIniciais",

            "VL_NOTA_PORTUGUES_2025":
                "NotaSAEB_LinguaPortuguesa_EnsinoFundamental_AnosIniciais",

            "VL_OBSERVADO_2025":
                "IDEB_EnsinoFundamental_AnosIniciais",
        },

        "AF": {
            "VL_NOTA_MATEMATICA_2025":
                "NotaSAEB_Matematica_EnsinoFundamental_AnosFinais",

            "VL_NOTA_PORTUGUES_2025":
                "NotaSAEB_LinguaPortuguesa_EnsinoFundamental_AnosFinais",

            "VL_OBSERVADO_2025":
                "IDEB_EnsinoFundamental_AnosFinais",
        },

        "EM": {
            "VL_NOTA_MATEMATICA_2025":
                "NotaSAEB_Matematica_EnsinoMedio",

            "VL_NOTA_PORTUGUES_2025":
                "NotaSAEB_LinguaPortuguesa_EnsinoMedio",

            "VL_OBSERVADO_2025":
                "IDEB_EnsinoMedio",
        }
    }
    print(df.columns)

    if etapa not in nomes_colunas:
        raise ValueError(
            f"Etapa inválida: '{etapa}'. "
            "Use 'AI', 'AF' ou 'EM'."
        )
    df = df.rename(columns=nomes_colunas[etapa])

    df = df.rename(columns={
        "NO_MUNICIPIO": "Municipio",
        "NO_ESCOLA": "Escola",
        "ID_ESCOLA": "CodigoINEP",
        "REDE": "DependenciaAdministrativa"
    })
    print(df.columns)
    
    return df

def realizar_filtragem(df):
    """
    Filtra os dados do Censo Escolar para o estado do Espírito Santo
    e para escolas estaduais e municipais.
    """

    # Filtrando dados do Espírto Santo
    df = df[df['SG_UF'] == 'ES']

    # Em fase de teste, será utilizado o municipio de NO_MUNICIPIO = Divino de São Lourenço
    #df = df[df['NO_MUNICIPIO'] == 'Vitória']

    # Filtrando apenas escolas estaduais e municipais 
    df = df[df["REDE"].isin(["Municipal", "Estadual"])]

    return df

def concatenar_ideb(ideb_AI, ideb_AF, ideb_EM):
    """
    Concatena os DataFrames de IDEB dos Anos Iniciais,
    Anos Finais e Ensino Médio.

    Mantém todas as colunas existentes nos três DataFrames.
    """

    df_ideb = pd.concat(
        [ideb_AI, ideb_AF, ideb_EM],
        ignore_index=True,
        sort=False
    )

    return df_ideb

def ordenar_colunas(df):
    """
    Reordena as colunas do DataFrame para a estrutura
    utilizada no banco analítico do Painel de Controle - Educação.
    """

    colunas = [
        "Ano",
        "Municipio",
        "CodigoINEP",
        "Escola",
        "DependenciaAdministrativa",

        "NotaSAEB_Matematica_EnsinoFundamental_AnosIniciais",
        "NotaSAEB_Matematica_EnsinoFundamental_AnosFinais",
        "NotaSAEB_Matematica_EnsinoMedio",

        "NotaSAEB_LinguaPortuguesa_EnsinoFundamental_AnosIniciais",
        "NotaSAEB_LinguaPortuguesa_EnsinoFundamental_AnosFinais",
        "NotaSAEB_LinguaPortuguesa_EnsinoMedio",

        "IDEB_EnsinoFundamental_AnosIniciais",
        "IDEB_EnsinoFundamental_AnosFinais",
        "IDEB_EnsinoMedio",
    ]

    return df[colunas].copy()

def tratar_valores_ausentes(df):
    """
    Converte os marcadores do INEP em valores nulos e deixa as colunas
    de indicadores numéricas:
        '-'    : sem resultado para a rede
        'ND'   : resultado não divulgado
        'ND***': resultado não divulgado (com nota de rodapé do INEP)

    Qualquer outro marcador de texto não mapeado faz o pd.to_numeric
    falhar, evitando que um símbolo desconhecido passe despercebido.
    """

    df = df.copy()

    colunas_indicadores = [
        coluna for coluna in df.columns
        if coluna.startswith(("NotaSAEB_", "IDEB_"))
    ]

    df[colunas_indicadores] = (
        df[colunas_indicadores]
        .replace(r"^-$|^ND\**$", pd.NA, regex=True)
        .apply(pd.to_numeric)
    )

    return df

def consolidar_por_escola(df):
    """
    Consolida os registros por escola, juntando os indicadores das
    diferentes etapas (Anos Iniciais, Anos Finais e Ensino Médio) em
    uma única linha por escola.

    Sem essa consolidação, cada escola aparece em até três linhas
    (uma por etapa), cada uma com apenas um grupo de colunas
    preenchido e o restante vazio.
    """

    colunas_grupo = [
        "Ano",
        "Municipio",
        "CodigoINEP",
        "Escola",
        "DependenciaAdministrativa",
    ]

    df = df.copy()

    # Consolida os indicadores, mantendo o primeiro valor não nulo
    df = (
        df.groupby(colunas_grupo, as_index=False, sort=False)
        .first()
    )

    return df

CAMINHO_ARQUIVO_AI = "dados/IDEB/2025/divulgacao_anos_iniciais_escolas_2025/divulgacao_anos_iniciais_escolas_2025/divulgacao_anos_iniciais_escolas_2025.xlsx"
CAMINHO_ARQUIVO_AF = "dados/IDEB/2025/divulgacao_anos_finais_escolas_2025/divulgacao_anos_finais_escolas_2025/divulgacao_anos_finais_escolas_2025.xlsx"
CAMINHO_ARQUIVO_EM = "dados/IDEB/2025/divulgacao_ensino_medio_escolas_2025/divulgacao_ensino_medio_escolas_2025/divulgacao_ensino_medio_escolas_2025.xlsx"

NOME_NOVO_ARQUIVO = 'IDEB_Escolas2025.xlsx'

print("Iniciando o tratamento do IDEB Escolas 2025...")

ideb_AI = pd.read_excel(CAMINHO_ARQUIVO_AI, skiprows=9)
ideb_AF = pd.read_excel(CAMINHO_ARQUIVO_AF, skiprows=9)
ideb_EM = pd.read_excel(CAMINHO_ARQUIVO_EM, skiprows=9)

print("Dados do IDEB carregados com sucesso!")


ideb_AI = realizar_filtragem(ideb_AI)
ideb_AI = selecionar_colunas(ideb_AI)
ideb_AI = renomear_colunas(ideb_AI, "AI")

ideb_AF = realizar_filtragem(ideb_AF)
ideb_AF = selecionar_colunas(ideb_AF)
ideb_AF = renomear_colunas(ideb_AF, "AF")

ideb_EM = realizar_filtragem(ideb_EM)
ideb_EM = selecionar_colunas(ideb_EM)
ideb_EM = renomear_colunas(ideb_EM, "EM")

df_ideb = concatenar_ideb(ideb_AI, ideb_AF, ideb_EM)
df_ideb = ordenar_colunas(df_ideb)
df_ideb = tratar_valores_ausentes(df_ideb)
df_ideb = consolidar_por_escola(df_ideb)
df_ideb = df_ideb.sort_values("Municipio")

# Salvando arquivo tratado em Excel
df_ideb.to_excel(NOME_NOVO_ARQUIVO, index=False)

