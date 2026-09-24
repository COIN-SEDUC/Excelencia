-- ============================================================================
-- DDL: citem.power_bi.excelencia_objetivo
-- Descrição: Metas de desempenho por URE (diretoria) e ano de referência
--            para o Programa de Excelência.
-- Gerado por: DML/[tabela] Objetivos 2026-2027 (notebook)
-- Modo de escrita: MERGE INTO (upsert pela chave ano_diretoria)
-- ============================================================================

CREATE TABLE IF NOT EXISTS citem.power_bi.excelencia_objetivo (
  chave                        STRING        COMMENT 'Identificador único: ano_ref + _ + diretoria',
  ano_ref                      INT           COMMENT 'Ano de referência',
  diretoria                    STRING        COMMENT 'Nome da URE',
  escolas                      INT           COMMENT 'Quantidade de escolas',
  alunos_noturnos              DECIMAL(6,4)  COMMENT 'Meta — Ensino Médio Noturno',
  alunos_pei                   DECIMAL(6,4)  COMMENT 'Meta — PEI',
  salas_aula                   INT           COMMENT 'Meta — Salas de Aula',
  alunos_pendentes             DECIMAL(6,4)  COMMENT 'Meta — Alunos Pendentes',
  qualidade_entur              DECIMAL(6,4)  COMMENT 'Meta — Qualidade de Enturmamento',
  rendimento                   DECIMAL(6,4)  COMMENT 'Meta — Rendimento',
  fechamento                   DECIMAL(6,4)  COMMENT 'Meta — Fechamento',
  bolsa_percent_nao_informado  DECIMAL(6,4)  COMMENT 'Meta — Bolsa Família (% não informados)',
  diverg_matricula             DECIMAL(6,4)  COMMENT 'Meta — Censo: Divergência de Matrícula',
  diverg_rendimento            DECIMAL(6,4)  COMMENT 'Meta — Censo: Divergência de Rendimento',
  cadastro_escola              DECIMAL(6,4)  COMMENT 'Meta — Cadastro Escolas',
  cadastro_aluno               DECIMAL(6,4)  COMMENT 'Meta — Cadastro Alunos'
)
USING DELTA
COMMENT 'Metas de desempenho e qualidade das escolas por URE e ano de referência';
