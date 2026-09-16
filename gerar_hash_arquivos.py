import csv
import hashlib
import zipfile
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Registra o hash SHA-256 dos arquivos .xlsx gerados na raiz do projeto (os
# que alimentam o Painel de Controle), para permitir conferir depois qual
# versão exata de cada arquivo foi enviada e quando.
#
# O registro é append-only em CSV: cada linha é uma "foto" do arquivo em um
# momento. Só é gravada uma linha nova quando o hash muda em relação ao
# último registro daquele arquivo, então o histórico mostra só os envios que
# de fato alteraram o conteúdo.
# ---------------------------------------------------------------------------

PASTA_RAIZ = Path(__file__).parent
ARQUIVO_REGISTRO = PASTA_RAIZ / "hash_arquivos.csv"
ARQUIVO_ZIP_ENVIO = PASTA_RAIZ / "arquivos_para_envio.zip"
COLUNAS_REGISTRO = ["Arquivo", "HashSHA256", "TamanhoBytes", "DataHora"]


def listar_arquivos_xlsx():
    """
    Lista os .xlsx gerados na raiz do projeto, ignorando arquivos de trava
    do Excel/LibreOffice (~$...).
    """

    return sorted(
        arquivo
        for arquivo in PASTA_RAIZ.glob("*.xlsx")
        if not arquivo.name.startswith("~$")
    )


def calcular_hash(arquivo, tamanho_bloco=1024 * 1024):
    sha256 = hashlib.sha256()
    with open(arquivo, "rb") as f:
        for bloco in iter(lambda: f.read(tamanho_bloco), b""):
            sha256.update(bloco)
    return sha256.hexdigest()


def carregar_ultimo_hash_registrado():
    """
    O registro é append-only, então a última linha de cada arquivo no CSV
    é o hash mais recente conhecido para ele.
    """

    if not ARQUIVO_REGISTRO.exists():
        return {}

    with open(ARQUIVO_REGISTRO, newline="", encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))

    return {linha["Arquivo"]: linha["HashSHA256"] for linha in linhas}


def registrar_novas_linhas(novas_linhas):
    arquivo_ja_existe = ARQUIVO_REGISTRO.exists()
    with open(ARQUIVO_REGISTRO, "a", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=COLUNAS_REGISTRO)
        if not arquivo_ja_existe:
            escritor.writeheader()
        escritor.writerows(novas_linhas)


def gerar_zip_para_envio(arquivos):
    """
    Empacota os .xlsx atuais junto com o registro de hashes num único .zip,
    pronto para anexar no e-mail de envio à TI. O .zip é sempre recriado do
    zero, refletindo o estado atual dos arquivos.
    """

    with zipfile.ZipFile(ARQUIVO_ZIP_ENVIO, "w", zipfile.ZIP_DEFLATED) as zip_arquivo:
        for arquivo in arquivos:
            zip_arquivo.write(arquivo, arcname=arquivo.name)
        if ARQUIVO_REGISTRO.exists():
            zip_arquivo.write(ARQUIVO_REGISTRO, arcname=ARQUIVO_REGISTRO.name)


print("Verificando hash dos arquivos .xlsx da raiz do projeto...\n")

arquivos = listar_arquivos_xlsx()
if not arquivos:
    print("Nenhum arquivo .xlsx encontrado na raiz do projeto.")
    raise SystemExit(0)

ultimo_hash_registrado = carregar_ultimo_hash_registrado()
agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

novas_linhas = []
for arquivo in arquivos:
    hash_atual = calcular_hash(arquivo)
    hash_anterior = ultimo_hash_registrado.get(arquivo.name)

    if hash_atual == hash_anterior:
        print(f"{arquivo.name}: sem alteração desde o último registro.")
        continue

    situacao = "novo arquivo" if hash_anterior is None else "conteúdo alterado"
    print(f"{arquivo.name}: {situacao} -> {hash_atual}")

    novas_linhas.append(
        {
            "Arquivo": arquivo.name,
            "HashSHA256": hash_atual,
            "TamanhoBytes": arquivo.stat().st_size,
            "DataHora": agora,
        }
    )

if novas_linhas:
    registrar_novas_linhas(novas_linhas)
    print(
        f"\n{len(novas_linhas)} novo(s) registro(s) adicionado(s) em "
        f"'{ARQUIVO_REGISTRO.name}'."
    )
else:
    print("\nNenhum arquivo mudou desde o último registro.")

gerar_zip_para_envio(arquivos)
print(f"'{ARQUIVO_ZIP_ENVIO.name}' gerado com {len(arquivos)} arquivo(s) para envio.")
