# Atualiza Painel de Controle — Documentação do Projeto

Resumo
- Scripts para limpeza e preparação dos microdados do Censo Escolar (2024/2025) e arquivos IDEB, gerando arquivos analíticos para o Painel de Controle.

Arquivos principais
- `tratamento_Censo_2024.py` — leitura e verificação do CSV do Censo 2024.
- `tratamento_Censo_2025.py` — pipeline que junta Tabela_Escola, Tabela_Docente e Tabela_Matricula e produz o arquivo analítico por etapa.
- `tratamento_IDEB_Escola.py` — função utilitária de leitura e pré-processamento de planilhas IDEB (.xlsx).

Estrutura de dados
- Dados brutos: `dados/` (subpastas por ano e tipo). Exemplo:
  - `dados/Censo_escolar/2025/microdados_censo_escolar_2025/dados/Tabela_Escola_2025.csv`
  - `dados/IDEB/2025/.../divulgacao_anos_finais_escolas_2025.xlsx`

Dependências e instalação
- Recomendado Python 3.10+.
- Instalação mínima:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip
pip install pandas openpyxl pyarrow
```

Como rodar
- Executar qualquer script diretamente:
```powershell
python .\tratamento_Censo_2025.py
python .\tratamento_Censo_2024.py
python .\tratamento_IDEB_Escola.py
```

Notas sobre encoding
- Se aparecer `UnicodeDecodeError`, tente ler com `encoding='latin-1'` ou `encoding='cp1252'`.
- Recomenda-se adicionar uma função utilitária para tentar múltiplos encodings automaticamente.

Boas práticas sugeridas
- Encapsular leituras em funções reutilizáveis (ver `tratamento_IDEB_Escola.py`).
- Usar `logging` em vez de `print` para pipelines.
- Converter CSV limpos para `parquet` para acesso mais rápido.
- Validar colunas e tipos após a leitura.

Próximos passos que posso aplicar
- Adicionar função utilitária de leitura robusta para CSV/Excel.
- Padronizar scripts com `if __name__ == '__main__'` e `logging`.

Se preferir, posso substituir o `README.md` existente com este conteúdo ou mesclá-lo.