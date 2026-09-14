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
    "ENSINO FUNDAMENTAL DE 9 ANOS - 2º ANO": "Ensino fundamental de 9 anos - 2º ano",
}

# No PAEBES Alfa, cada arquivo/aba resulta de uma combinação de itens
# diferente (D_1/D_2 = itens objetivos, Leitura + Matemática; D_3/D_60 = só
# itens de resposta construída, Escrita; D_4/D_61 = itens construída +
# objetiva, consolidado). A partir de 2025 o CAEd renomeou esses conceitos
# para IRS (Item de Resposta Selecionada) e IRC (Item de Resposta
# Construída), mas o conteúdo avaliado é o mesmo — por isso o nome de 2024 e
# o de 2025 caem no mesmo ComponenteCurricular.
COMPONENTES = {
    "Língua Portuguesa - Leitura": "Língua portuguesa",
    "Matemática": "Matemática",
    "Língua Portuguesa - Escrita": "Língua portuguesa - Escrita",
    "Língua Portuguesa - Itens de Resposta Construída": "Língua portuguesa - Escrita",
    "Língua Portuguesa - Escrita e Leitura": "Língua portuguesa - Escrita e leitura",
    "Língua Portuguesa - IRC e IRS": "Língua portuguesa - Escrita e leitura",
}

# Cada tupla é (caminho do arquivo, lista de abas de "Resultados de
# Participação e Desempenho" a processar, nome da coluna de edição naquele
# arquivo). A coluna de edição vem grafada de formas diferentes conforme o
# arquivo ("Edição" ou, só no arquivo-base de 2025, "Edicao" sem acento).
ARQUIVOS_PAEBES_ALFA = [
    (
        "dados/paebes/paebes2024/paebes_alfa/resultados_Prg_1930_Paebes_Alfa_2024_250220/"
        "resultados_Prg_1930_Paebes_Alfa_2024_250221.xlsx",
        ["D_1", "D_2"],
        "Edição",
    ),
    (
        "dados/paebes/paebes2024/paebes_alfa/resultados_Prg_1930_Paebes_Alfa_Escrita_2024_250221/"
        "resultados_Prg_1930_Paebes_Alfa_Escrita_2024_250221.xlsx",
        ["D_3"],
        "Edição",
    ),
    (
        "dados/paebes/paebes2024/paebes_alfa/resultados_Prg_1930_Paebes_Alfa_Escrita_e_Leitura_2024_250221/"
        "resultados_Prg_1930_Paebes_Alfa_Escrita_e_Leitura_2024_250223.xlsx",
        ["D_4"],
        "Edição",
    ),
    (
        "dados/paebes/paebes2025/paebes_alfa/resultados_Prg_2067_Paebes_Alfa_2025_260325/"
        "resultados_Prg_2067_Paebes_Alfa_2025_260325.xlsx",
        ["D_1", "D_2"],
        "Edicao",
    ),
    (
        "dados/paebes/paebes2025/paebes_alfa/resultados_Prg_2067_Paebes_Alfa_2025_IRC_260410/"
        "resultados_Prg_2067_Paebes_Alfa_2025_IRC_260410.xlsx",
        ["D_60"],
        "Edição",
    ),
    (
        "dados/paebes/paebes2025/paebes_alfa/resultados_Prg_2067_Paebes_Alfa_2025_IRC_e_IRS_260410/"
        "resultados_Prg_2067_Paebes_Alfa_2025_IRC_e_IRS_260410.xlsx",
        ["D_61"],
        "Edição",
    ),
]

NOME_NOVO_ARQUIVO = "PAEBES_ALFA_2024_2025.xlsx"

COLUNAS_NECESSARIAS = [
    "Tipo",
    "Código da regional",
    "Regional",
    "Código do município",
    "Município",
    "Código da escola",
    "Escola",
    "Rede",
    "Etapa",
    "Disciplina",
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


def carregar_aba(caminho, aba, coluna_edicao):
    """
    Lê a aba e seleciona as colunas de COLUNAS_NECESSARIAS + a coluna de
    edição, resolvendo os nomes de forma insensível a maiúsculas/minúsculas.
    Isso é necessário porque, entre os arquivos do PAEBES Alfa, colunas como
    "Abaixo do Básico (TRI) %" aparecem ora com "B" maiúsculo, ora com "b"
    minúsculo.
    """

    bruto = pd.read_excel(caminho, sheet_name=aba)
    colunas_disponiveis = {coluna.strip().lower(): coluna for coluna in bruto.columns}

    nomes_alvo = COLUNAS_NECESSARIAS + [coluna_edicao]
    colunas_resolvidas = []
    colunas_nao_encontradas = []
    for nome in nomes_alvo:
        coluna_real = colunas_disponiveis.get(nome.strip().lower())
        if coluna_real is None:
            colunas_nao_encontradas.append(nome)
        else:
            colunas_resolvidas.append(coluna_real)

    if colunas_nao_encontradas:
        raise ValueError(
            f"Coluna(s) não encontrada(s) em {caminho} / {aba}: {colunas_nao_encontradas}"
        )

    df = bruto[colunas_resolvidas].copy()
    df.columns = COLUNAS_NECESSARIAS + ["Edição"]
    return df


def filtrar_e_deduplicar(df):
    """
    Reduz a planilha ao mesmo grão do arquivo histórico: uma linha por
    escola, rede e etapa.

    - Tipo == 'ESCOLA': descarta os agregados por município/regional/estado.
    - Rede em Estadual/Municipal: descarta 'Pública' (agregado de Estadual +
      Municipal) e 'Particular'.
    - Turno agregado == 'GERAL': descarta os recortes por turno (INTEGRAL,
      PARCIAL, INTERMEDIÁRIO), que duplicariam os registros.
    """

    df = df[df["Tipo"] == "ESCOLA"]
    df = df[df["Rede"].isin(["Estadual", "Municipal"])]
    df = df[df["Turno agregado"] == "GERAL"]

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

    componentes_nao_mapeados = set(df["Disciplina"].unique()) - set(COMPONENTES)
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
    df["ComponenteCurricular"] = df["Disciplina"].map(COMPONENTES)

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


print("Iniciando o tratamento do PAEBES Alfa 2024/2025...")

municipios = carregar_referencia_municipios()

partes = []

for caminho, abas, coluna_edicao in ARQUIVOS_PAEBES_ALFA:
    for aba in abas:
        print(f"Lendo {caminho} / {aba}...")
        df = carregar_aba(caminho, aba, coluna_edicao)
        df = filtrar_e_deduplicar(df)
        df = renomear_e_traduzir(df, municipios)
        df = selecionar_colunas_finais(df)
        partes.append(df)
        print(f"  Registros após tratamento: {len(df):,}")

df_paebes_alfa = pd.concat(partes, ignore_index=True)

print(f"\nTotal de linhas: {len(df_paebes_alfa):,}")

# Salvando arquivo tratado em Excel
df_paebes_alfa.to_excel(NOME_NOVO_ARQUIVO, index=False)

print(f"\nArquivo '{NOME_NOVO_ARQUIVO}' salvo com sucesso.")
