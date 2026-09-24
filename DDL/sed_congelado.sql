-- ============================================================================
-- DDL: citem.sandbox.sed_congelado_maio_26
-- Descrição: Snapshot congelado do SED (maio/2026) com contagem de matrículas
--            por escola e modalidade de ensino.
-- Gerado por: DML/[Tabela] SED - Congelado (notebook)
-- Modo de escrita: CREATE OR REPLACE TABLE (snapshot pontual)
-- ============================================================================

CREATE TABLE IF NOT EXISTS citem.sandbox.sed_congelado_maio_26 (
  COD_ESC              INT      COMMENT 'Código da escola',
  ANO_MES              STRING   COMMENT 'Ano/mês de referência',
  total_turmas         BIGINT   COMMENT 'Total de turmas',
  total_matriculas     BIGINT   COMMENT 'Total de matrículas',
  ed_infantil          BIGINT   COMMENT 'Matrículas Educação Infantil',
  fund_ai              BIGINT   COMMENT 'Matrículas Fundamental Anos Iniciais',
  fund_af              BIGINT   COMMENT 'Matrículas Fundamental Anos Finais',
  ensino_medio         BIGINT   COMMENT 'Matrículas Ensino Médio',
  eja_total            BIGINT   COMMENT 'Matrículas EJA Total',
  ceeja_ai             BIGINT   COMMENT 'Matrículas CEEJA Anos Iniciais',
  ceeja_af             BIGINT   COMMENT 'Matrículas CEEJA Anos Finais',
  ceeja_em             BIGINT   COMMENT 'Matrículas CEEJA Ensino Médio',
  eja_ai               BIGINT   COMMENT 'Matrículas EJA Anos Iniciais',
  eja_af               BIGINT   COMMENT 'Matrículas EJA Anos Finais',
  eja_em               BIGINT   COMMENT 'Matrículas EJA Ensino Médio',
  profissionalizante   BIGINT   COMMENT 'Matrículas Profissionalizante'
)
USING DELTA;
