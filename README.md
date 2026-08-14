# Tratamento dos Microdados do Censo Escolar

## Objetivo

Este repositório tem como objetivo realizar a leitura, seleção, transformação e padronização dos microdados do **Censo Escolar da Educação Básica**, disponibilizados pelo Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP).

Os dados tratados serão utilizados posteriormente na geração de arquivos destinados à carga do **Painel de Controle - Educação do Tribunal de Contas do Estado do Espírito Santo (TCE-ES)**.

O projeto inicialmente contempla os dados dos anos de **2024 e 2025**, podendo ser posteriormente ampliado para outros anos.

---

## Fluxo de tratamento

O processamento dos dados segue as seguintes etapas:

1. Leitura dos microdados do Censo Escolar;
2. Seleção do estado do Espírito Santo;
3. Seleção das dependências administrativas estadual e municipal;
4. Seleção apenas das escolas em funcionamento;
5. Seleção das variáveis de interesse;
6. Transformação dos dados para o formato analítico por etapa de ensino;
7. Inclusão das informações de matrículas em tempo integral;
8. Inclusão do ano de referência;
9. Padronização dos nomes das colunas;
10. Exportação dos dados tratados para arquivo Excel.

---

## Fonte dos dados

Os dados utilizados são os **Microdados do Censo Escolar da Educação Básica**, disponibilizados pelo INEP.

Os arquivos brutos não são alterados. O código realiza o processamento diretamente sobre os arquivos armazenados no diretório de dados.

Para o Censo Escolar 2024, é utilizado o arquivo:

```text
dados/Censo_escolar/2024/
└── microdados_censo_escolar_2024_defeso/
    └── dados/
        └── microdados_ed_basica_2024.csv