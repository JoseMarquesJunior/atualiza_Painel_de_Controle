import pandas as pd

# ---------------------------------------------------------------------------
# Referências para restaurar a acentuação correta dos nomes, que no PAEBES
# vêm em caixa alta e sem acento (ex.: "AAcento FUNDAO", "SRE AFONSO CLAUDIO").
# ---------------------------------------------------------------------------

CAMINHO_REFERENCIA_MUNICIPIOS = (
    "dados/IDEB/2025/divulgacao_anos_iniciais_municipios_2025/"
    "divulgacao_anos_iniciais_municipios_2025/"
    "divulgacao_anos_iniciais_municipios_2025.xlsx"
)

REGIONAIS = {
    27: "SRE Carapina",
    28: "SRE Vila Velha",
    29: "SRE Cariacica",
    30: "SRE Linhares",
    31: "SRE São Mateus",
    32: "SRE Barra de São Francisco",
    33: "SRE Nova Venécia",
    34: "SRE Colatina",
    35: "SRE Cachoeiro de Itapemirim",
    36: "SRE Comendadora Jurema Moretz Sohn",
    37: "SRE Afonso Cláudio",
}

ETAPAS = {
    "ENSINO FUNDAMENTAL DE 9 ANOS - 1º ANO": "Ensino fundamental de 9 anos - 1º ano",
    "ENSINO FUNDAMENTAL DE 9 ANOS - 2º ANO": "Ensino fundamental de 9 anos - 2º ano",
    "ENSINO FUNDAMENTAL DE 9 ANOS - 3º ANO": "Ensino fundamental de 9 anos - 3º ano",
    "ENSINO FUNDAMENTAL DE 9 ANOS - 5º ANO": "Ensino fundamental de 9 anos - 5º ano",
    "ENSINO FUNDAMENTAL DE 9 ANOS - 9º ANO": "Ensino fundamental de 9 anos - 9º ano",
    "ENSINO MEDIO - 3ª SERIE": "Ensino médio - 3ª série",
    "ENSINO MÉDIO - 3ª SÉRIE": "Ensino médio - 3ª série",
    "ENSINO MEDIO - 4ª SERIE": "Ensino médio - 4ª série",
    "ENSINO MÉDIO - 4ª SÉRIE": "Ensino médio - 4ª série",
}

# "Ciências da Natureza" é o nome usado a partir de 2025 para a disciplina
# que nas edições anteriores do PAEBES aparecia como "Ciências".
COMPONENTES = {
    "Língua Portuguesa": "Língua portuguesa",
    "Matemática": "Matemática",
    "Geografia": "Geografia",
    "História": "História",
    "Biologia": "Biologia",
    "Física": "Física",
    "Química": "Química",
    "Ciências da Natureza": "Ciências",
}

# Cada tupla é (caminho do arquivo, lista de abas de "Resultados de
# Participação e Desempenho" a processar). As abas variam de edição para
# edição porque as disciplinas avaliadas no Ensino Médio mudaram (Geografia/
# História até 2024, Biologia/Física/Química/Ciências da Natureza a partir de
# 2025, seguindo o Novo Ensino Médio).
ARQUIVOS_PAEBES = [
    (
        "dados/paebes/paebes2024/paebes/resultados_Prg_1931_Paebes_2024_250404.xlsx",
        ["D_1", "D_2", "D_14", "D_15"],
    ),
    (
        "dados/paebes/paebes2025/paebes/resultados_Prg_2068_Paebes_2025_260323.xlsx",
        ["D_1", "D_2", "D_11", "D_12", "D_13", "D_29"],
    ),
]

CAMINHO_ARQUIVO_HISTORICO = "dados/Arquivos originais/PAEBES 1.csv"
NOME_NOVO_ARQUIVO = "PAEBES_2024_2025.xlsx"

COLUNAS_NECESSARIAS = [
    "Tipo",
    "Código da regional",
    "Regional",
    "Código do município",
    "Município",
    "Código da escola",
    "Escola",
    "Edição",
    "Rede",
    "Etapa",
    "DISCIPLINA",
    "Ensino",
    "Turno agregado",
    "Previsto",
    "Efetivo",
    "Participação %",
    "Proficiência",
    "Padrão de Desempenho",
    "Abaixo do Básico (TRI) %",
    "Básico (TRI) %",
    "Proficiente (TRI) %",
    "Avançado (TRI) %",
]


def carregar_referencia_municipios():
    """
    Carrega a relação Código do IBGE -> Nome do município (com acentuação
    correta) a partir da base do IDEB, já usada em outros scripts deste
    projeto.
    """

    ref = pd.read_excel(
        CAMINHO_REFERENCIA_MUNICIPIOS,
        skiprows=9,
        usecols=["SG_UF", "CO_MUNICIPIO", "NO_MUNICIPIO"],
    )
    ref = ref[ref["SG_UF"] == "ES"]

    return dict(zip(ref["CO_MUNICIPIO"].astype(int), ref["NO_MUNICIPIO"]))


def carregar_aba(caminho, aba):
    return pd.read_excel(caminho, sheet_name=aba, usecols=COLUNAS_NECESSARIAS)


def filtrar_e_deduplicar(df):
    """
    Reduz a planilha ao mesmo grão do arquivo histórico: uma linha por
    escola, rede e etapa.

    - Tipo == 'ESCOLA': descarta os agregados por município/regional/estado.
    - Rede em Estadual/Municipal: descarta 'Pública' (agregado de Estadual +
      Municipal) e 'Particular'.
    - Turno agregado == 'GERAL': descarta os recortes por turno (INTEGRAL,
      PARCIAL, INTERMEDIÁRIO), que duplicariam os registros.
    - Ensino: no Ensino Médio, a mesma etapa aparece dividida por itinerário
      (ENSINO MÉDIO / ENSINO MÉDIO INTEGRADO) e por um agregado 'TODOS'.
      Quando existe o agregado 'TODOS', ele é o único mantido.
    """

    df = df[df["Tipo"] == "ESCOLA"]
    df = df[df["Rede"].isin(["Estadual", "Municipal"])]
    df = df[df["Turno agregado"] == "GERAL"]

    tem_todos = df.groupby("Etapa")["Ensino"].transform(
        lambda serie: "TODOS" in serie.values
    )
    df = df[(~tem_todos) | (df["Ensino"] == "TODOS")]

    return df


def paebes_para_numero(serie):
    """
    Converte um valor numérico no formato bruto do PAEBES (vírgula como
    separador decimal) para float. '-' marca ausência de resultado (ex.:
    escola sem estudantes avaliados na etapa/rede) e vira nulo.
    """

    return (
        serie.astype(str)
        .str.replace(",", ".", regex=False)
        .replace({"-": pd.NA, "nan": pd.NA})
        .astype(float)
    )


def formatar_percentual(serie):
    """
    Converte percentuais do formato bruto do PAEBES ('33,33333333') para o
    padrão do arquivo histórico: 1 casa decimal, vírgula como separador
    decimal, e sem casa decimal quando o valor é inteiro (ex.: '0', '18',
    '14,3').
    """

    valores = paebes_para_numero(serie).round(1)

    def formatar_valor(valor):
        if pd.isna(valor):
            return pd.NA
        texto = f"{valor:.1f}".replace(".", ",")
        if texto.endswith(",0"):
            texto = texto[:-2]
        return texto

    return valores.apply(formatar_valor)


def renomear_e_traduzir(df, municipios):
    df = df.copy()

    etapas_nao_mapeadas = set(df["Etapa"].unique()) - set(ETAPAS)
    if etapas_nao_mapeadas:
        raise ValueError(f"Etapa(s) não mapeada(s): {etapas_nao_mapeadas}")

    componentes_nao_mapeados = set(df["DISCIPLINA"].unique()) - set(COMPONENTES)
    if componentes_nao_mapeados:
        raise ValueError(f"Componente(s) não mapeado(s): {componentes_nao_mapeados}")

    codigos_regionais = pd.to_numeric(df["Código da regional"]).astype(int)
    regionais_nao_mapeadas = set(codigos_regionais.unique()) - set(REGIONAIS)
    if regionais_nao_mapeadas:
        raise ValueError(f"Regional(is) não mapeada(s): {regionais_nao_mapeadas}")

    codigos_municipios = pd.to_numeric(df["Código do município"]).astype(int)
    municipios_nao_mapeados = set(codigos_municipios.unique()) - set(municipios)
    if municipios_nao_mapeados:
        raise ValueError(f"Município(s) não mapeado(s): {municipios_nao_mapeados}")

    df["Municipio"] = codigos_municipios.map(municipios)
    df["SuperintendenciaRegionalDeEducacao"] = codigos_regionais.map(REGIONAIS)
    df["Etapa"] = df["Etapa"].map(ETAPAS)
    df["ComponenteCurricular"] = df["DISCIPLINA"].map(COMPONENTES)

    df["ProficienciaMedia"] = paebes_para_numero(df["Proficiência"]).round(0)

    # O arquivo histórico grafa "Abaixo do básico" com b minúsculo (única
    # exceção às demais faixas, escritas com inicial maiúscula) e mantém o
    # marcador '-' quando a escola não teve estudantes avaliados.
    df["Padrão de Desempenho"] = df["Padrão de Desempenho"].replace(
        {"Abaixo do Básico": "Abaixo do básico"}
    )

    for origem, destino in [
        ("Abaixo do Básico (TRI) %", "AbaixoDoBasico"),
        ("Básico (TRI) %", "Basico"),
        ("Proficiente (TRI) %", "Proficiente"),
        ("Avançado (TRI) %", "Avancado"),
        ("Participação %", "PercentualDeParticipacao"),
    ]:
        df[destino] = formatar_percentual(df[origem])

    df = df.rename(columns={
        "Código da escola": "CodigoINEP",
        "Edição": "Edicao",
        "Rede": "DependenciaAdministrativa",
        "Previsto": "EstudantesPrevistos",
        "Efetivo": "EstudantesEfetivos",
        "Padrão de Desempenho": "PadraoDeDesempenho",
    })

    df["Edicao"] = df["Edicao"].astype(int)

    return df


def selecionar_colunas_finais(df):
    colunas = [
        "DependenciaAdministrativa",
        "ComponenteCurricular",
        "Etapa",
        "SuperintendenciaRegionalDeEducacao",
        "Municipio",
        "CodigoINEP",
        "Escola",
        "Edicao",
        "ProficienciaMedia",
        "PadraoDeDesempenho",
        "AbaixoDoBasico",
        "Basico",
        "Proficiente",
        "Avancado",
        "EstudantesPrevistos",
        "EstudantesEfetivos",
        "PercentualDeParticipacao",
    ]

    return df[colunas].copy()



print("Iniciando o tratamento do PAEBES 2024/2025...")

municipios = carregar_referencia_municipios()

partes = []

for caminho, abas in ARQUIVOS_PAEBES:
    for aba in abas:
        print(f"Lendo {caminho} / {aba}...")
        df = carregar_aba(caminho, aba)
        df = filtrar_e_deduplicar(df)
        df = renomear_e_traduzir(df, municipios)
        df = selecionar_colunas_finais(df)
        partes.append(df)
        print(f"  Registros após tratamento: {len(df):,}")

df_paebes = pd.concat(partes, ignore_index=True)


print(f"\nTotal de linhas: {len(df_paebes):,}")

# Salvando arquivo tratado em Excel
df_paebes.to_excel(NOME_NOVO_ARQUIVO, index=False)

print(f"\nArquivo '{NOME_NOVO_ARQUIVO}' salvo com sucesso.")
