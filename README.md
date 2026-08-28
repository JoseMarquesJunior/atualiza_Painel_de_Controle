# Atualiza Painel de Controle — Documentação do Projeto

Scripts em Python (pandas) para tratar microdados públicos de educação (INEP) — Censo Escolar, IDEB, Taxa de Rendimento Escolar e PAEBES — e gerar planilhas analíticas prontas para alimentar o Painel de Controle de Educação, filtradas para o estado do Espírito Santo (redes Estadual e Municipal).

## Scripts e arquivos gerados

| Script | Fonte (`dados/`) | Arquivo gerado |
|---|---|---|
| `tratamento_Censo_2024.py` | `Censo_escolar/2024/microdados_censo_escolar_2024_defeso/dados/microdados_ed_basica_2024.csv` | `CensoEscolarMicrodados2024.xlsx` |
| `tratamento_Censo_2025.py` | Tabela_Escola / Tabela_Docente / Tabela_Matricula 2025 | `CensoEscolarMicrodados2025.xlsx` |
| `tratamento_IDEB_Escola.py` | `IDEB/2025/divulgacao_{anos_iniciais,anos_finais,ensino_medio}_escolas_2025/...xlsx` | `IDEB_Escolas2025.xlsx` |
| `tratamento_IDEB_Municipios.py` | `IDEB/2025/divulgacao_{anos_iniciais,anos_finais,ensino_medio}_municipios_2025/...xlsx` | `IDEB_Municipios2025.xlsx` |
| `tratamento_tx_rend_escolas_2024.py` | `Taxa de Rendimento/tx_rend_escolas_2024/tx_rend_escolas_2024.xlsx` | `TaxaRendimento_Escola2024.xlsx` |
| `tratamento_tx_rend_escolas_2025.py` | `Taxa de Rendimento/tx_rend_escolas_2025/tx_rend_escolas_2025.xlsx` | `TaxaRendimento_Escola2025.xlsx` |
| `tratamento_tx_rend_municipios_2024.py` | `Taxa de Rendimento/tx_rend_municipios_2024/tx_rend_municipios_2024.xlsx` | `TaxaRendimento_Municipios2024.xlsx` |
| `tratamento_tx_rend_municipios_2025.py` | `Taxa de Rendimento/tx_rend_municipios_2025/tx_rend_municipios_2025.xlsx` | `TaxaRendimento_Municipios2025.xlsx` |
| `tratamento_PAEBES.py` | `paebes_2015_2024_2025/Paebes/2024/resultados_Prg_1931_Paebes_2024_250428.xlsx` | `PAEBES 2024.xlsx` |

## Estrutura de dados

Dados brutos ficam em `dados/`, organizados por indicador e ano:

```
dados/
├── Censo_escolar/{2024,2025}/...
├── IDEB/2025/divulgacao_{anos_iniciais,anos_finais,ensino_medio}_{escolas,municipios}_2025/...
├── Taxa de Rendimento/tx_rend_{escolas,municipios}_{2024,2025}/tx_rend_....xlsx
└── paebes_2015_2024_2025/Paebes/2024/...
```

Os arquivos `.xlsx` de IDEB e Taxa de Rendimento vêm do INEP com linhas de cabeçalho/rodapé institucional antes da tabela de dados — os scripts pulam essas linhas com `skiprows` (9 para IDEB, 8 para Taxa de Rendimento).

## Padrões seguidos pelos scripts

- **Filtro geográfico/rede**: todos os tratamentos filtram `SG_UF == 'ES'` e dependência administrativa em `["Municipal", "Estadual"]`.
- **Pipeline em funções**: `realizar_filtragem` → `selecionar_colunas` → `renomear_colunas` → (`tratar_valores_ausentes` quando aplicável) → `ordenar_colunas`.
- **Valores ausentes**: o INEP usa `'--'` para indicar taxa não calculável (poucos alunos); os scripts de Taxa de Rendimento convertem esse marcador para nulo e a coluna para numérico.
- **Nomenclatura de colunas** no arquivo final: `Ano`, `Municipio`, `CodigoINEP`/`CodigoDoMunicipio`, `Escola` (quando por escola), `Localizacao`, `DependenciaAdministrativa`, seguidas dos indicadores nomeados por etapa de ensino (`EnsinoFundamental_AnosIniciais`, `EnsinoFundamental_AnosFinais`, `EnsinoFundamental_Total`, `EnsinoMedio_Total`).
- **IDEB por escola**: como os três arquivos fonte (AI/AF/EM) não têm exatamente as mesmas escolas, o script concatena as três bases (uma linha por escola+etapa) em vez de fazer merge.
- **IDEB por município**: já concatenado por etapa e depois consolidado (`consolidar_por_municipio`) em uma única linha por município+dependência.

## Dependências e instalação

Recomendado Python 3.10+.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip
pip install pandas openpyxl
```

## Como rodar

Executar qualquer script diretamente a partir da raiz do projeto (os caminhos dos dados são relativos):

```powershell
python .\tratamento_Censo_2024.py
python .\tratamento_Censo_2025.py
python .\tratamento_IDEB_Escola.py
python .\tratamento_IDEB_Municipios.py
python .\tratamento_tx_rend_escolas_2024.py
python .\tratamento_tx_rend_escolas_2025.py
python .\tratamento_tx_rend_municipios_2024.py
python .\tratamento_tx_rend_municipios_2025.py
python .\tratamento_PAEBES.py
```

> Se um arquivo `.xlsx` de origem estiver aberto no Excel/LibreOffice (arquivo `.~lock.*`), feche-o antes de rodar o script correspondente.

## Notas sobre encoding

- CSVs do Censo Escolar costumam vir em `latin-1`/`cp1252`. Se aparecer `UnicodeDecodeError`, ajuste o `encoding` na leitura (`tratamento_Censo_2024.py` já usa `encoding="latin1"`).
