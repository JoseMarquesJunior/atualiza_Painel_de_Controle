import pandas as pd

def selecionar_colunas(df):
    """
    Função para selecionar apenas as colunas de interesse do DataFrame.
    
    Parâmetros:
    df (DataFrame): O DataFrame original.    
    Retorna:
    DataFrame: Um novo DataFrame contendo apenas as colunas especificadas.
    """
    # Selecionando apenas as colunas de interesse
    colunas = [
        "NO_MUNICIPIO", "NO_ENTIDADE", "CO_ENTIDADE", 
        "TP_DEPENDENCIA",                                               # 1 - Federal, 2 - Estadual, 3 - Municipal, 4 - Privada
        "TP_LOCALIZACAO",                                               # 1 - Urbana, 2 - Rural

        "TP_LOCALIZACAO_DIFERENCIADA",                                  # 0 - A escola não está em área de localização diferenciada
                                                                        # 1 - Área de assentamento
                                                                        # 2 - Terra indígena
                                                                        # 3 - Comunidade quilombola
                                                                        # 8 - Área onde se localizam povos e comunidades tradicionais

        "TP_AEE",                                                       # Atendimento Educacional Especializado (AEE)
                                                                        # 0 - Não oferece
                                                                        # 1 - Não exclusivamente
                                                                        # 2 - Exclusivamente

        # colunas que indicam etapa escolar
        "IN_EJA_FUND", "IN_EJA_MED", "IN_INF_CRE", "IN_INF_PRE", "IN_FUND_AI", "IN_FUND_AF", "IN_MED", "IN_ESP",    

        # colunas que indicam quantidade de docentes por etapa escolar
        "QT_DOC_EJA_FUND", "QT_DOC_EJA_MED", "QT_DOC_INF_CRE", "QT_DOC_INF_PRE", "QT_DOC_FUND_AI", "QT_DOC_FUND_AF", "QT_DOC_MED", "QT_DOC_ESP",

        # colunas que indicam quantidade de matrículas por etapa escolar
        "QT_MAT_EJA_FUND", "QT_MAT_EJA_MED", "QT_MAT_INF_CRE", "QT_MAT_INF_PRE", "QT_MAT_FUND_AI", "QT_MAT_FUND_AF", "QT_MAT_MED", "QT_MAT_ESP",

        # colunas de matrículas em tempo integral
        "QT_MAT_INF_CRE_INT", "QT_MAT_INF_PRE_INT", "QT_MAT_FUND_AI_INT", "QT_MAT_FUND_AF_INT", "QT_MAT_MED_INT",

        ]
    return df[colunas].copy()

def transformar_por_etapa(df):
    """
    Cria uma linha para cada etapa de ensino ofertada pela escola.

    As colunas IN_* indicam se a escola oferece determinada etapa:
    1 = oferece
    0 = não oferece
    """

    etapas = {
        "IN_EJA_FUND": "Educação de Jovens e Adultos (EJA) - Ensino Fundamental",
        "IN_EJA_MED": "Educação de Jovens e Adultos (EJA) - Ensino Médio",
        "IN_INF_CRE": "Educação Infantil - Creche",
        "IN_INF_PRE": "Educação Infantil - Pré-Escola",
        "IN_FUND_AI": "Ensino Fundamental - Anos Iniciais",
        "IN_FUND_AF": "Ensino Fundamental - Anos Finais",
        "IN_MED": "Ensino Médio",
        "IN_ESP": "Educação Especial",
    }

    # Etapas que possuem dados específicos de matrículas em tempo integral
    etapas_tempo_integral = {
        "IN_INF_CRE": "Educação Infantil - Creche - Tempo Integral",
        "IN_INF_PRE": "Educação Infantil - Pré-Escola - Tempo Integral",
        "IN_FUND_AI": "Ensino Fundamental - Anos Iniciais - Tempo Integral",
        "IN_FUND_AF": "Ensino Fundamental - Anos Finais - Tempo Integral",
        "IN_MED": "Ensino Médio - Tempo Integral",
    }

    linhas = []

    for _, escola in df.iterrows():

        # ---------------------------------------------------------
        # Etapas regulares
        # ---------------------------------------------------------
        for coluna, etapa in etapas.items():

            nova_linha = escola.drop(
                list(etapas.keys())
            ).to_dict()

            nova_linha["EtapaDeEnsinoOfertadaPelaEscola"] = etapa

            # Quantidade de docentes correspondente à etapa
            coluna_docentes = coluna.replace("IN_", "QT_DOC_")
            nova_linha["QuantidadeDeDocentesPorEtapa"] = escola[coluna_docentes]

            # Quantidade de matrículas correspondente à etapa
            coluna_matriculas = coluna.replace("IN_", "QT_MAT_")
            nova_linha["QuantidadeDeMatriculasPorEtapa"] = escola[coluna_matriculas]

            linhas.append(nova_linha)

        # ---------------------------------------------------------
        # Etapas em tempo integral
        # ---------------------------------------------------------
        for coluna, etapa in etapas_tempo_integral.items():

            nova_linha = escola.drop(
                list(etapas.keys())
            ).to_dict()

            nova_linha["EtapaDeEnsinoOfertadaPelaEscola"] = etapa

            # Docentes: permanece a quantidade de docentes da etapa
            coluna_docentes = coluna.replace("IN_", "QT_DOC_")
            nova_linha["QuantidadeDeDocentesPorEtapa"] = escola[coluna_docentes]

            # Matrículas: utiliza a coluna específica de tempo integral
            coluna_matriculas = coluna.replace(
                "IN_",
                "QT_MAT_"
            ) + "_INT"

            nova_linha["QuantidadeDeMatriculasPorEtapa"] = escola[coluna_matriculas]

            linhas.append(nova_linha)

    return pd.DataFrame(linhas)

def formatar_dataframe(df):
    """
    Mantém apenas as colunas necessárias para o arquivo analítico.
    """
    df["Ano"] = 2024

    colunas = [
        "Ano",
        "NO_MUNICIPIO",
        "NO_ENTIDADE",
        "CO_ENTIDADE",
        "TP_DEPENDENCIA",
        "TP_LOCALIZACAO",
        "TP_LOCALIZACAO_DIFERENCIADA",
        "TP_AEE",
        "EtapaDeEnsinoOfertadaPelaEscola",
        "QuantidadeDeDocentesPorEtapa",
        "QuantidadeDeMatriculasPorEtapa",
    ]

    df = df[colunas].copy()

    return df

def renomear_colunas(df):
    """
    Renomeia as colunas do DataFrame para os nomes utilizados
    no banco analítico do Painel de Controle - Educação.
    """

    nomes_colunas = {
        "NO_MUNICIPIO": "Municipio",
        "NO_ENTIDADE": "Escola",
        "CO_ENTIDADE": "CodigoINEP",
        "TP_DEPENDENCIA": "DependenciaAdministrativa",
        "TP_LOCALIZACAO": "Localizacao",
        "TP_LOCALIZACAO_DIFERENCIADA": "LocalizacaoDiferenciada",
        "TP_AEE": "AtendimentoEducacionalEspecializado",
    }

    return df.rename(columns=nomes_colunas)

def mapear_valores(df):
    """
    Converte códigos numéricos das variáveis categóricas
    para suas respectivas descrições.
    """

    # Dependência administrativa
    mapa_dependencia = {
        1: "Federal",
        2: "Estadual",
        3: "Municipal",
        4: "Privada",
    }

    mapa_localizacao = {
        1: "Urbana",    
        2: "Rural",
    }

    # Localização diferenciada
    mapa_localizacao_diferenciada = {
        1: "Assentamento",
        2: "Terra indígena",
        3: "Comunidade quilombola",
        8: "Comunidades tradicionais",
    }

    # Atendimento Educacional Especializado
    mapa_aee = {
        0: "Não",
        1: "Sim",
        2: "Sim",
    }

    df["TP_DEPENDENCIA"] = df["TP_DEPENDENCIA"].map(mapa_dependencia)

    df["TP_LOCALIZACAO"] = df["TP_LOCALIZACAO"].map(mapa_localizacao)

    df["TP_LOCALIZACAO_DIFERENCIADA"] = df["TP_LOCALIZACAO_DIFERENCIADA"].map(mapa_localizacao_diferenciada)

    df["TP_AEE"] = df["TP_AEE"].map(mapa_aee)

    return df

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
#df_censo = df_censo[df_censo['NO_MUNICIPIO'] == 'Divino de São Lourenço']

# Filtrando apenas escolas estaduais e municipais (1 - Federal, 2 - Estadual, 3 - Municipal, 4 - Privada)
df_censo = df_censo[df_censo["TP_DEPENDENCIA"].isin([2, 3])]

# Filtrando apenas escolas em funcionamento (# 1 - Em Atividade, 2 - Paralisada, 3 - Extinta (ano do Censo), 4 - Extinta em Anos Anteriores)
df_censo = df_censo[df_censo["TP_SITUACAO_FUNCIONAMENTO"] == 1]     

df_censo = selecionar_colunas(df_censo)
df_censo = transformar_por_etapa(df_censo)
df_censo = formatar_dataframe(df_censo)
df_censo = mapear_valores(df_censo)
df_censo = renomear_colunas(df_censo)

# Salvando arquivo tratado em Excel
df_censo.to_excel(NOME_NOVO_ARQUIVO, index=False)
print(df_censo.head(10))