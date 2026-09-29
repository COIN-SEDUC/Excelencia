-- Databricks notebook source
create or replace table citem.sandbox.sed_congelado_maio_26

SELECT
  es.COD_ESC,
  es.ANO_MES,
  COUNT(DISTINCT tu.CLASSE)                           AS total_turmas,
  COUNT(DISTINCT al.CD_MATRICULA_ALUNO)               AS total_matriculas,
 
  -- EDUCAÇÃO INFANTIL (agrupada: Creche + Pré-Escola + Multi)
  COUNT(DISTINCT CASE WHEN tu.GRAU_TBTURMA = 6
    THEN al.CD_MATRICULA_ALUNO END)                   AS ed_infantil,
 
  -- FUND. ANOS INICIAIS
  COUNT(DISTINCT CASE
    WHEN tu.GRAU_TBTURMA = 30
      AND CASE WHEN al.SERIE = 0 AND al.SERIE_NIVEL_TBMATR = 0 THEN al.SERIE_TBMATR
               WHEN al.SERIE = 0 THEN al.SERIE_NIVEL_TBMATR
               ELSE al.SERIE END <> 0
    THEN al.CD_MATRICULA_ALUNO
    WHEN tu.GRAU_TBTURMA IN (14,78,80)
      AND CASE WHEN al.SERIE = 0 AND al.SERIE_NIVEL_TBMATR = 0 THEN al.SERIE_TBMATR
               WHEN al.SERIE = 0 THEN al.SERIE_NIVEL_TBMATR
               ELSE al.SERIE END IN (1,2,3,4,5)
    THEN al.CD_MATRICULA_ALUNO
  END)                                                AS fund_ai,
 
  -- FUND. ANOS FINAIS
  COUNT(DISTINCT CASE
    WHEN tu.GRAU_TBTURMA = 40
      AND CASE WHEN al.SERIE = 0 AND al.SERIE_NIVEL_TBMATR = 0 THEN al.SERIE_TBMATR
               WHEN al.SERIE = 0 THEN al.SERIE_NIVEL_TBMATR
               ELSE al.SERIE END <> 0
    THEN al.CD_MATRICULA_ALUNO
    WHEN tu.GRAU_TBTURMA IN (14,81,82,83,84)
      AND CASE WHEN al.SERIE = 0 AND al.SERIE_NIVEL_TBMATR = 0 THEN al.SERIE_TBMATR
               WHEN al.SERIE = 0 THEN al.SERIE_NIVEL_TBMATR
               ELSE al.SERIE END IN (6,7,8,9)
    THEN al.CD_MATRICULA_ALUNO
  END)                                                AS fund_af,
 
  -- ENSINO MÉDIO
  COUNT(DISTINCT CASE
    WHEN tu.GRAU_TBTURMA IN (2,25,50,76,93,98,101,104,105)
    THEN al.CD_MATRICULA_ALUNO
  END)                                                AS ensino_medio,
 
  -- EJA (total agrupado: CEEJA + EJA todas sub-categorias)
  COUNT(DISTINCT CASE
    WHEN tu.GRAU_TBTURMA IN (3,4,5,61,62,63,87,88,107,56)
    THEN al.CD_MATRICULA_ALUNO
  END)                                                AS eja_total,
 
  --   CEEJA (TIPOCLASSE IN 75,76,77,78)
  COUNT(DISTINCT CASE
    WHEN tu.GRAU_TBTURMA IN (3,61) AND tu.TIPOCLASSE IN (75,76,77,78)
    THEN al.CD_MATRICULA_ALUNO
  END)                                                AS ceeja_ai,
 
  COUNT(DISTINCT CASE
    WHEN tu.GRAU_TBTURMA IN (4,62,87) AND tu.TIPOCLASSE IN (75,76,77,78)
    THEN al.CD_MATRICULA_ALUNO
  END)                                                AS ceeja_af,
 
  COUNT(DISTINCT CASE
    WHEN tu.GRAU_TBTURMA IN (5,63,88,107,56) AND tu.TIPOCLASSE IN (75,76,77,78)
    THEN al.CD_MATRICULA_ALUNO
  END)                                                AS ceeja_em,
 
  -- EJA (nova regra 2026: TIPOCLASSE NOT IN 75,76,77,78)
  COUNT(DISTINCT CASE
    WHEN tu.GRAU_TBTURMA IN (3,61) AND tu.TIPOCLASSE NOT IN (75,76,77,78)
    THEN al.CD_MATRICULA_ALUNO
  END)                                                AS eja_ai,
 
  COUNT(DISTINCT CASE
    WHEN tu.GRAU_TBTURMA IN (4,62,87) AND tu.TIPOCLASSE NOT IN (75,76,77,78)
    THEN al.CD_MATRICULA_ALUNO
  END)                                                AS eja_af,
 
  COUNT(DISTINCT CASE
    WHEN tu.GRAU_TBTURMA IN (5,63,88,107,56) AND tu.TIPOCLASSE NOT IN (75,76,77,78)
    THEN al.CD_MATRICULA_ALUNO
  END)                                                AS eja_em,
 
  -- PROFISSIONALIZANTE
  COUNT(DISTINCT CASE
    WHEN tu.GRAU_TBTURMA IN (46,99,22,21,104,97,92,94,100,91,23,24,95,90,57,25,108,93,98,107,35)
    THEN al.CD_MATRICULA_ALUNO
  END)                                                AS profissionalizante
 
FROM deinf.bronze.escola es
INNER JOIN deinf.bronze.classe tu
  ON tu.COD_ESC = es.COD_ESC AND tu.ANO_MES = '202605'
INNER JOIN deinf.bronze.aluno al
  ON al.NUMCLASSE = tu.CLASSE AND al.ANO_MES = '202605'
WHERE es.ANO_MES = '202605'
  -- AND es.DEPADM = 1
  AND es.CODSIT = 1
  AND al.FLAG_SIT_ALUNO = 0
  AND tu.DURCLASSE IN (0, 1)  -- turmas ativas 1° semestre
  AND tu.GRAU_TBTURMA IN (
    2,3,4,5,6,13,14,25,30,36,37,40,46,47,50,54,55,56,
    61,62,63,74,75,76,78,80,81,82,83,84,87,88,89,90,
    91,92,93,97,98,99,101,102,103,104,105,107,35
  )
GROUP BY es.COD_ESC, es.ANO_MES

-- COMMAND ----------

select * from citem.sandbox.sed_congelado_maio_26

-- COMMAND ----------

-- DBTITLE 1,Análise de Divergência SED vs Censo Escolar
-- Divergência por escola: SED Congelado (maio/2026) vs Censo Escolar — filtrado pelas escolas da base Excelência
WITH excelencia AS (
  SELECT ESCOLA_CD_ESCOLA, ds_rede_ensino, DIRETORIA_NM_DIRETORIA
  FROM citem.power_bi.excelencia
),
sed AS (
  SELECT * FROM citem.sandbox.sed_congelado_maio_26
),
censo AS (
  SELECT *
  FROM citem.sandbox.tb_censo_escolar_coleta_historico
  WHERE dt_referencia = (SELECT MAX(dt_referencia) FROM citem.sandbox.tb_censo_escolar_coleta_historico)
    AND total_matriculas_curricular > 0
),
comparativo AS (
  SELECT
    s.COD_ESC,
    ex.ds_rede_ensino                           AS rede_ensino,
    ex.DIRETORIA_NM_DIRETORIA                   AS diretoria,
    c.nm_escola,
    c.municipio,
    c.forma_coleta,
    -- TOTAL
    s.total_matriculas                          AS sed_total,
    c.total_matriculas_curricular               AS censo_total,
    s.total_matriculas - c.total_matriculas_curricular AS diff_total,
    -- EDUCAÇÃO INFANTIL
    s.ed_infantil                               AS sed_ei,
    (c.mat_presencial_creche + c.mat_presencial_pre_escola) AS censo_ei,
    s.ed_infantil - (c.mat_presencial_creche + c.mat_presencial_pre_escola) AS diff_ei,
    -- FUND. ANOS INICIAIS
    s.fund_ai                                   AS sed_ai,
    c.mat_presencial_ensino_fundamental_anos_iniciais AS censo_ai,
    s.fund_ai - c.mat_presencial_ensino_fundamental_anos_iniciais AS diff_ai,
    -- FUND. ANOS FINAIS
    s.fund_af                                   AS sed_af,
    c.mat_presencial_ensino_fundamental_anos_finais AS censo_af,
    s.fund_af - c.mat_presencial_ensino_fundamental_anos_finais AS diff_af,
    -- ENSINO MÉDIO
    s.ensino_medio                              AS sed_em,
    (c.mat_presencial_ensino_medio + c.mat_presencial_ensino_medio_normal_magisterio) AS censo_em,
    s.ensino_medio - (c.mat_presencial_ensino_medio + c.mat_presencial_ensino_medio_normal_magisterio) AS diff_em,
    -- EJA
    s.eja_total                                 AS sed_eja,
    (c.mat_presencial_eja_fundamental_e_fic_integrado
     + c.mat_presencial_eja_medio_fic_integrado_e_tecnico_integrado
     + c.mat_semipresencial_eja_curricular
     + c.mat_ead_eja_fundamental
     + c.mat_ead_eja_medio)                     AS censo_eja,
    s.eja_total - (c.mat_presencial_eja_fundamental_e_fic_integrado
     + c.mat_presencial_eja_medio_fic_integrado_e_tecnico_integrado
     + c.mat_semipresencial_eja_curricular
     + c.mat_ead_eja_fundamental
     + c.mat_ead_eja_medio)                     AS diff_eja,
    -- PROFISSIONALIZANTE
    s.profissionalizante                        AS sed_prof,
    (c.mat_presencial_curso_tecnico_concomitante_subsequente
     + c.mat_ead_educacao_profissional_tecnica_de_nivel_medio_concomitante_subsequente) AS censo_prof,
    s.profissionalizante - (c.mat_presencial_curso_tecnico_concomitante_subsequente
     + c.mat_ead_educacao_profissional_tecnica_de_nivel_medio_concomitante_subsequente) AS diff_prof
  FROM sed s
  INNER JOIN excelencia ex ON s.COD_ESC = ex.ESCOLA_CD_ESCOLA
  INNER JOIN censo c ON s.COD_ESC = c.cd_cie
)
SELECT
  COD_ESC,
  rede_ensino,
  diretoria,
  nm_escola,
  municipio,
  forma_coleta,
  sed_total,
  censo_total,
  diff_total,
  ROUND(diff_total * 100.0 / NULLIF(sed_total, 0), 1) AS pct_diff_total,
  -- Percentual por modalidade: (SED - Censo) / SED
  diff_ei,
  ROUND(diff_ei * 100.0 / NULLIF(sed_ei, 0), 1)   AS pct_diff_ei,
  diff_ai,
  ROUND(diff_ai * 100.0 / NULLIF(sed_ai, 0), 1)   AS pct_diff_ai,
  diff_af,
  ROUND(diff_af * 100.0 / NULLIF(sed_af, 0), 1)   AS pct_diff_af,
  diff_em,
  ROUND(diff_em * 100.0 / NULLIF(sed_em, 0), 1)   AS pct_diff_em,
  diff_eja,
  ROUND(diff_eja * 100.0 / NULLIF(sed_eja, 0), 1) AS pct_diff_eja,
  diff_prof,
  ROUND(diff_prof * 100.0 / NULLIF(sed_prof, 0), 1) AS pct_diff_prof
FROM comparativo
where 1 = 1
and rede_ensino like 'Federal'
---group by diretoria
ORDER BY ABS(pct_diff_total) DESC

-- COMMAND ----------

SELECT
  COD_ESC,
  rede_ensino,
  diretoria,
  nm_escola,
  municipio,
  forma_coleta,
  sed_total,
  censo_total,
  diff_total,
  ROUND(diff_total * 100.0 / NULLIF(sed_total, 0), 1) AS pct_diff_total,
  -- Percentual por modalidade: (SED - Censo) / SED
  diff_ei,
  ROUND(diff_ei * 100.0 / NULLIF(sed_ei, 0), 1)   AS pct_diff_ei,
  diff_ai,
  ROUND(diff_ai * 100.0 / NULLIF(sed_ai, 0), 1)   AS pct_diff_ai,
  diff_af,
  ROUND(diff_af * 100.0 / NULLIF(sed_af, 0), 1)   AS pct_diff_af,
  diff_em,
  ROUND(diff_em * 100.0 / NULLIF(sed_em, 0), 1)   AS pct_diff_em,
  diff_eja,
  ROUND(diff_eja * 100.0 / NULLIF(sed_eja, 0), 1) AS pct_diff_eja,
  diff_prof,
  ROUND(diff_prof * 100.0 / NULLIF(sed_prof, 0), 1) AS pct_diff_prof
FROM comparativo
where 1 = 1
and rede_ensino = 'Pública'
ORDER BY ABS(pct_diff_total) DESC