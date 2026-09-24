# Excelência — Programa de Excelência das UREs

## Objetivo

Consolidar as tabelas de metas, glossário de indicadores e snapshot de matrículas do **Programa de Excelência das UREs** (Unidades Regionais de Ensino) da rede estadual de SP. Os dados são consumidos por um dashboard Power BI que monitora o desempenho das diretorias em 12 indicadores educacionais.

---

## Cliente / Política Pública

Secretaria da Educação do Estado de São Paulo — Programa de Excelência / Planejamento de Rede

---

## Regra de Negócio

* **Conceito**: o Programa de Excelência define metas anuais para cada URE em 12 indicadores (alunos pendentes, PEI, salas de aula, rendimento, etc.). O glossário documenta fórmulas e faixas de cores. O snapshot SED congelado permite comparação com Censo Escolar.
* **Fluxo do processo**: os dados de metas e glossário são enviados via arquivo Excel para volumes monitorados; jobs de File Arrival atualizam as tabelas automaticamente.
* **Critérios e filtros**:
  * `excelencia_objetivo`: MERGE por `chave` (ano_ref + diretoria), deduplicação por `file_modification_time`
  * `excelencia_glossario`: CREATE OR REPLACE, deduplicação por `Indicador` + `file_modification_time`
  * `sed_congelado_maio_26`: snapshot pontual de matrículas por escola e modalidade
* **Legislação / Referência**: regras operacionais do Programa de Excelência e planilha de glossário de indicadores.

---

## Estrutura do Repositório

```
├── DDL/
│   ├── excelencia_glossario.sql        -- CREATE TABLE (documentação)
│   ├── excelencia_objetivo.sql         -- CREATE TABLE (documentação)
│   └── sed_congelado.sql               -- CREATE TABLE (documentação)
├── DML/
│   ├── [tabela] Glossário.py           -- Notebook: CREATE OR REPLACE (glossário)
│   ├── [tabela] Objetivos 2026-2027.py -- Notebook: MERGE INTO (metas por URE)
│   └── [Tabela] SED - Congelado.py     -- Notebook: CREATE OR REPLACE (snapshot SED)
├── PBIP/                               -- Projeto Power BI versionado no Git (a ser incluído)
├── CONTRIBUTING.md
└── README.md
```

---

## Localização

* **Produção**: `/Shared/COIN/clientes/Excelencia/DML/`
* **Dev**: `DML/`
* **DDL**: `DDL/`
* **Tabelas destino**:
  * `citem.power_bi.excelencia_glossario`
  * `citem.power_bi.excelencia_objetivo`
  * `citem.sandbox.sed_congelado_maio_26`

---

## Fontes de Dados

| Origem | Tabela Databricks | Atualização |
| --- | --- | --- |
| Excel `Glossario_Indicadores*.xlsx` (volume `/Volumes/citem/power_bi/pex/`) | `citem.power_bi.excelencia_glossario` | File Arrival |
| Excel `*.xlsx` (volume `/Volumes/citem/power_bi/objetivos_pex/`) | `citem.power_bi.excelencia_objetivo` | File Arrival |
| `deinf.bronze.tb_escola_sed`, `deinf.bronze.tb_turma_sed`, `deinf.bronze.tb_aluno_sed` | `citem.sandbox.sed_congelado_maio_26` | Sob demanda |

---

## Job

| Job | ID | Trigger | Notebook | Descrição |
| --- | --- | --- | --- | --- |
| `programa_de_excelencia_glossario` | `20074708928939` | File Arrival (`/Volumes/citem/power_bi/pex/`) | `[tabela] Glossário` | Atualiza glossário |
| `programa_de_excelencia_objetivo` | `1120001018845630` | File Arrival (`/Volumes/citem/power_bi/objetivos_pex/`) | `[tabela] Objetivos 2026-2027` | Atualiza metas |

* **Notificações**: lucas.ferro@apoioeducacao.sp.gov.br

---

## Histórico de Alterações

| Data | Autor | Descrição da Alteração |
| --- | --- | --- |
| 24/09/2026 | Lucas Ferro | Criação do repositório Git com estrutura DDL/DML/PBIP. Notebooks migrados para DML/. DDLs documentais criados para as 3 tabelas. README e CONTRIBUTING padronizados. |

---

## Limitações Conhecidas

* `sed_congelado_maio_26` é um snapshot pontual (maio/2026) e não é atualizado automaticamente.
* A tabela `citem.power_bi.excelencia` (base principal do dashboard) é gerida fora deste repositório.
* O notebook `[Tabela] SED - Congelado` contém células de análise de divergência SED vs Censo que não fazem parte do pipeline automatizado.
