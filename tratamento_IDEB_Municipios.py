import pandas as pd

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
    df = df[df["REDE"].isin(["Municipal", "Estadual", "Pública"])]

    return df

def selecionar_colunas(df):

    df = df.copy()
    df["Ano"] = 2025

    colunas = [
        "Ano",
        "NO_MUNICIPIO",
        "CO_MUNICIPIO",
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
        "CO_MUNICIPIO": "CodigoDoMunicipio",
        "REDE": "DependenciaAdministrativa"
    })
    print(df.columns)
    
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
        "CodigoDoMunicipio",
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
        '-'  : sem resultado para a rede
        'ND' : resultado não divulgado

    Mantidos como texto, esses marcadores levavam a limpezas manuais
    com localizar/substituir de 'ND', que também apagavam o 'nd' dos
    nomes dos municípios (ex.: 'Baixo Guandu' -> 'Baixo Guau').
    """

    df = df.copy()

    colunas_indicadores = [
        coluna for coluna in df.columns
        if coluna.startswith(("NotaSAEB_", "IDEB_"))
    ]

    df[colunas_indicadores] = (
        df[colunas_indicadores]
        .replace(["-", "ND"], pd.NA)
        .apply(pd.to_numeric)
    )

    return df

def consolidar_por_municipio(df):
    """
    Consolida os registros por município e dependência administrativa,
    juntando os indicadores das diferentes etapas em uma única linha.
    """

    colunas_grupo = [
        "Ano",
        "Municipio",
        "CodigoDoMunicipio",
        "DependenciaAdministrativa"
    ]

    df = df.copy()

    # Trata células vazias como valores ausentes
    df = df.replace(r"^\s*$", pd.NA, regex=True)

    # Consolida os indicadores, mantendo o primeiro valor não nulo.
    # dropna=False é necessário porque as linhas do "Estado do Espírito
    # Santo" não têm CodigoDoMunicipio (fica nulo por não se tratar de um
    # município) — sem isso, o groupby descartaria essas linhas.
    df = (
        df.groupby(colunas_grupo, as_index=False, sort=False, dropna=False)
        .first()
    )

    return df

def carregar_dados_estado(etapa):
    """
    Carrega, para a etapa informada, as linhas do agregado "Estado do
    Espírito Santo" nas redes Pública e Estadual, a partir do arquivo de
    divulgação por UF/regiões do IDEB (divulgacao_regioes_ufs_ideb_2025).

    CodigoDoMunicipio fica nulo nessas linhas, já que não se trata de um
    município.

    O IDEB do Ensino Médio não tem, na fonte, um agregado "Pública" para o
    Espírito Santo (só há Total, Privada e Estadual) — nesse caso a linha
    "Pública" simplesmente não recebe indicadores de Ensino Médio, o mesmo
    que já acontece com municípios sem dados divulgados para alguma
    etapa/rede.
    """

    df = pd.read_excel(
        CAMINHO_ARQUIVO_UF,
        sheet_name=ABAS_ARQUIVO_UF[etapa],
        skiprows=9,
    )
    df = df.rename(columns={
        df.columns[0]: "NO_MUNICIPIO",
        df.columns[1]: "REDE",
    })

    df = df[df["NO_MUNICIPIO"] == "Espírito Santo"]
    df = df[df["REDE"].isin(REDES_ESTADO_DESEJADAS)]
    df = df.copy()

    df["REDE"] = df["REDE"].map(REDES_ESTADO_DESEJADAS)
    df["NO_MUNICIPIO"] = "Estado do Espírito Santo"
    df["CO_MUNICIPIO"] = pd.NA

    return df

CAMINHO_ARQUIVO_AI = "dados/IDEB/2025/divulgacao_anos_iniciais_municipios_2025/divulgacao_anos_iniciais_municipios_2025/divulgacao_anos_iniciais_municipios_2025.xlsx"
CAMINHO_ARQUIVO_AF = "dados/IDEB/2025/divulgacao_anos_finais_municipios_2025/divulgacao_anos_finais_municipios_2025/divulgacao_anos_finais_municipios_2025.xlsx"
CAMINHO_ARQUIVO_EM = "dados/IDEB/2025/divulgacao_ensino_medio_municipios_2025/divulgacao_ensino_medio_municipios_2025/divulgacao_ensino_medio_municipios_2025.xlsx"

CAMINHO_ARQUIVO_UF = (
    "dados/IDEB/2025/divulgacao_regioes_ufs_ideb_2025/"
    "divulgacao_regioes_ufs_ideb_2025/divulgacao_regioes_ufs_ideb_2025.xlsx"
)

# O arquivo por UF/regiões tem uma aba por etapa, nesta ordem (os nomes das
# abas têm acentuação, por isso identificamos pela posição).
ABAS_ARQUIVO_UF = {"AI": 0, "AF": 1, "EM": 2}

# No arquivo por UF/regiões a coluna Rede vem com marcadores de nota de
# rodapé (ex.: "Pública (4)"), que aqui são normalizados para o mesmo texto
# usado no restante do arquivo final ("Pública", "Estadual").
REDES_ESTADO_DESEJADAS = {
    "Pública (4)": "Pública",
    "Estadual": "Estadual",
}

NOME_NOVO_ARQUIVO = 'IDEB_Municipios2025.xlsx'

print("Iniciando o tratamento do IDEB Municipios 2025...")

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

print("Carregando linhas do Estado do Espírito Santo (Pública/Estadual)...")

estado_AI = carregar_dados_estado("AI")
estado_AI = selecionar_colunas(estado_AI)
estado_AI = renomear_colunas(estado_AI, "AI")
ideb_AI = pd.concat([ideb_AI, estado_AI], ignore_index=True)

estado_AF = carregar_dados_estado("AF")
estado_AF = selecionar_colunas(estado_AF)
estado_AF = renomear_colunas(estado_AF, "AF")
ideb_AF = pd.concat([ideb_AF, estado_AF], ignore_index=True)

estado_EM = carregar_dados_estado("EM")
estado_EM = selecionar_colunas(estado_EM)
estado_EM = renomear_colunas(estado_EM, "EM")
ideb_EM = pd.concat([ideb_EM, estado_EM], ignore_index=True)

df_ideb = concatenar_ideb(ideb_AI, ideb_AF, ideb_EM)
df_ideb = ordenar_colunas(df_ideb)
df_ideb = tratar_valores_ausentes(df_ideb)
df_ideb = consolidar_por_municipio(df_ideb)
df_ideb = df_ideb.sort_values("Municipio")

# Salvando arquivo tratado em Excel
df_ideb.to_excel(NOME_NOVO_ARQUIVO, index=False)
print(ideb_AI.head(10))