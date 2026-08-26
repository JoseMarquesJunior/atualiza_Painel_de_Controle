import pandas as pd

CAMINHO_ARQUIVO_PAEBES = (
    "dados/paebes_2015_2024_2025/Paebes/2024/"
    "resultados_Prg_1931_Paebes_2024_250428.xlsx"
)

nomes_colunas = [
    "Tipo",
    "Código do país",
    "País",
    "Código do estado",
    "Estado",
    "Código da regional",
    "Regional",
    "Código do município",
    "Município",
    "Código da escola",
    "Escola",
    "Código da turma",
    "Turma",
    "Documento",
    "Programa",
    "Edição",
    "Rede",
    "Etapa",
    "DISCIPLINA",
    "Código do ensino",
    "Ensino",
    "Turno agregado",
    "Código do turno agregado",
    "Habilidade - Código",
    "Habilidade - Posição",
    "Habilidade - Nome",
    "Habilidade - Descricao",
    "Previsto",
    "Efetivo",
    "Participação %",
    "Habilidade - Acerto %",
    "Habilidade - Faixa",
    "Acertos no Teste %"
]

# Abre o arquivo uma única vez
xls = pd.ExcelFile(CAMINHO_ARQUIVO_PAEBES)

# Identifica as abas H_
abas_h = [
    aba for aba in xls.sheet_names
    if aba.startswith("H_") and aba != "H_0"
]

print("Abas que serão processadas:")
print(abas_h)

dfs = []

for aba in abas_h:

    print(f"Lendo: {aba}")

    # Usa o ExcelFile já aberto
    df = pd.read_excel(
        xls,
        sheet_name=aba
    )
    df.columns = nomes_colunas
    # Filtro Espírito Santo
    # A coluna no arquivo é "Estado"
    if "Estado" in df.columns:
        df = df[
            df["Estado"]
            .astype("string")
            .str.strip()
            .str.upper()
            == "ESPÍRITO SANTO"
        ]

    # Identifica a aba de origem
    df["AbaOrigem"] = aba

    dfs.append(df)

    print(f"  Registros após filtro: {len(df):,}")

# Consolida
df_final = pd.concat(
    dfs,
    ignore_index=True
)

print("\nResultado final:")
print(f"Linhas: {len(df_final):,}")
print(f"Colunas: {len(df_final.columns)}")

print("\nAmostra:")
print(df_final.head())

# Salva
df_final.to_excel(
    "PAEBES 2024.xlsx",
    index=False
)

print("\nArquivo 'PAEBES 2024.xlsx' salvo com sucesso.")