# Tratamento dos Microdados do Censo Escolar

## Objetivo

Este repositório tem como objetivo realizar a **leitura e o tratamento dos microdados do Censo Escolar**, inicialmente referentes aos anos de **2024 e 2025**.

Após o tratamento, os dados serão utilizados para gerar arquivos estruturados que servirão de entrada para a **carga do Painel de Controle - Educação do TCE-ES**.

## Fluxo

O processo previsto para o projeto é:

1. Leitura dos microdados oficiais do Censo Escolar.
2. Filtragem dos dados de acordo com os critérios definidos.
3. Seleção e organização das variáveis necessárias.
4. Geração dos arquivos tratados.
5. Utilização dos arquivos tratados na carga do Painel de Controle - Educação do TCE-ES.

## Estrutura do projeto

```text
.
├── dados/
│   └── Censo_escolar/
│       ├── 2024/
│       └── 2025/
│
├── tratamento/
│   ├── tratamento_Censo_2024.py
│   └── tratamento_Censo_2025.py
│
├── .gitignore
└── README.md
```

Os microdados originais do Censo Escolar não devem, preferencialmente, ser versionados no GitHub. O `README` poderá informar posteriormente a fonte e as instruções para obtenção desses arquivos.

## Censo Escolar 2024

O tratamento dos dados de 2024 contempla, inicialmente:

* seleção do estado do Espírito Santo;
* seleção de município para testes;
* seleção das escolas estaduais e municipais;
* seleção das variáveis necessárias ao Painel de Controle;
* geração de arquivo Excel com os dados tratados.

O município utilizado atualmente na fase de testes é **Divino de São Lourenço/ES**.

### Variáveis selecionadas atualmente

* `NO_MUNICIPIO` — Município
* `NO_ENTIDADE` — Nome da escola
* `CO_ENTIDADE` — Código da escola
* `TP_DEPENDENCIA` — Dependência administrativa
* `TP_LOCALIZACAO` — Localização
* `TP_LOCALIZACAO_DIFERENCIADA` — Localização diferenciada
* `TP_AEE` — Atendimento Educacional Especializado
* `IN_EJA_FUND` — Oferta de EJA - Ensino Fundamental
* `IN_EJA_MED` — Oferta de EJA - Ensino Médio

Essa seleção poderá ser ampliada ou alterada conforme as necessidades do Painel de Controle.

## Censo Escolar 2025

O tratamento dos microdados de 2025 será incorporado posteriormente, seguindo a mesma lógica geral do processamento de 2024, com as adaptações necessárias em função das alterações nas variáveis e na estrutura dos microdados entre as diferentes edições do Censo Escolar.

## Saída

Os scripts de tratamento gerarão arquivos estruturados, inicialmente em formato `.xlsx`, que posteriormente serão utilizados como fonte para a carga dos dados no **Painel de Controle - Educação do TCE-ES**.

## Requisitos

O projeto utiliza Python e, inicialmente, as seguintes bibliotecas:

```text
pandas
openpyxl
```

A instalação das dependências pode ser realizada com:

```bash
pip install pandas openpyxl
```

## Execução

Para executar o tratamento de 2024:

```bash
python tratamento/tratamento_Censo_2024.py
```

O arquivo resultante será gerado no diretório definido no script.

## Fonte dos dados

Os microdados utilizados neste projeto são os **Microdados do Censo Escolar da Educação Básica**, disponibilizados pelo Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP).

## Observações

A estrutura dos microdados do Censo Escolar pode sofrer alterações entre diferentes anos. Dessa forma, os scripts de tratamento devem considerar as diferenças de variáveis e estrutura existentes entre as edições de 2024 e 2025.

O projeto está em desenvolvimento e a estrutura de processamento poderá ser reorganizada conforme a evolução das necessidades de carga e manutenção do **Painel de Controle - Educação do TCE-ES**.
