# Tratamento dos Microdados do Censo Escolar 2024

Script em Python para leitura, filtragem e organização dos microdados do **Censo Escolar 2024**, com geração de um arquivo Excel contendo as informações de interesse.

## Objetivo

O projeto tem como objetivo facilitar o tratamento dos microdados do Censo Escolar, permitindo selecionar:

* uma unidade da federação;
* um município;
* determinadas dependências administrativas;
* um conjunto específico de variáveis.

Atualmente, o código está em **fase de desenvolvimento e testes**, utilizando como município de referência **Divino de São Lourenço (ES)**.

## Fonte dos dados

Os dados utilizados são os **Microdados do Censo Escolar 2024**, disponibilizados pelo Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP).

O arquivo utilizado pelo script é:

```text
microdados_ed_basica_2024.csv
```

O arquivo original deve ser colocado no seguinte caminho:

```text
dados/
└── Censo_escolar/
    └── 2024/
        └── microdados_censo_escolar_2024_defeso/
            └── dados/
                └── microdados_ed_basica_2024.csv
```

> Os microdados não devem ser versionados no GitHub. O arquivo deve ser obtido diretamente da fonte oficial e colocado localmente na estrutura indicada acima.

## Requisitos

* Python 3.x
* pandas
* openpyxl

Para instalar as dependências:

```bash
pip install pandas openpyxl
```

## Execução

Na raiz do projeto, execute:

```bash
python tratamento_Censo_2024.py
```

O script irá:

1. carregar os microdados do Censo Escolar 2024;
2. filtrar as escolas do Espírito Santo;
3. filtrar o município de Divino de São Lourenço;
4. selecionar escolas estaduais e municipais;
5. selecionar as variáveis de interesse;
6. gerar um arquivo Excel com os dados tratados.

## Filtros aplicados

### Unidade da Federação

São mantidos apenas registros do:

```text
Espírito Santo
```

### Município

Durante a fase atual de testes, são mantidos apenas registros de:

```text
Divino de São Lourenço
```

Esse filtro deverá ser posteriormente parametrizado para permitir a seleção de diferentes municípios.

### Dependência administrativa

São mantidas apenas escolas:

| Código | Dependência |
| -----: | ----------- |
|      2 | Estadual    |
|      3 | Municipal   |

As categorias disponíveis no Censo são:

| Código | Dependência |
| -----: | ----------- |
|      1 | Federal     |
|      2 | Estadual    |
|      3 | Municipal   |
|      4 | Privada     |

## Variáveis selecionadas

O arquivo final contém atualmente as seguintes variáveis:

| Variável                      | Descrição                             |
| ----------------------------- | ------------------------------------- |
| `NO_MUNICIPIO`                | Nome do município                     |
| `NO_ENTIDADE`                 | Nome da escola                        |
| `CO_ENTIDADE`                 | Código da escola                      |
| `TP_DEPENDENCIA`              | Dependência administrativa            |
| `TP_LOCALIZACAO`              | Localização da escola                 |
| `TP_LOCALIZACAO_DIFERENCIADA` | Localização diferenciada              |
| `TP_AEE`                      | Atendimento Educacional Especializado |
| `IN_EJA_FUND`                 | Oferta de EJA – Ensino Fundamental    |
| `IN_EJA_MED`                  | Oferta de EJA – Ensino Médio          |

## Arquivo de saída

Após a execução, será gerado:

```text
CensoEscolarMicrodados2024.xlsx
```

O arquivo contém apenas os registros e variáveis selecionados pelo tratamento.

## Estrutura do projeto

```text
.
├── dados/
│   └── Censo_escolar/
│       └── 2024/
│           └── ...
│
├── tratamento_Censo_2024.py
├── CensoEscolarMicrodados2024.xlsx
└── README.md
```

## Próximos passos

O projeto ainda está em desenvolvimento. Entre as próximas etapas previstas estão:

* parametrizar o município;
* permitir o processamento de vários municípios;
* ampliar o conjunto de variáveis selecionadas;
* criar tratamentos e recodificações das variáveis;
* gerar arquivos padronizados para utilização em análises;
* automatizar o processamento dos microdados;
* avaliar a possibilidade de processamento de outros anos do Censo Escolar.

## Observação

Os microdados utilizados neste projeto são disponibilizados pelo INEP. Este repositório contém o código de tratamento e organização dos dados, não sendo necessário versionar os arquivos brutos do Censo Escolar.
