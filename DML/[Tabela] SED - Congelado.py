# Databricks notebook source
# MAGIC %sql
# MAGIC create or replace table citem.sandbox.sed_congelado_maio_26
# MAGIC
# MAGIC SELECT
# MAGIC   es.COD_ESC,
# MAGIC   es.ANO_MES,
# MAGIC   COUNT(DISTINCT tu.CLASSE)                           AS total_turmas,
# MAGIC   COUNT(DISTINCT al.CD_MATRICULA_ALUNO)               AS total_matriculas,
# MAGIC  
# MAGIC   -- EDUCAÇÃO INFANTIL (agrupada: Creche + Pré-Escola + Multi)
# MAGIC   COUNT(DISTINCT CASE WHEN tu.GRAU_TBTURMA = 6
# MAGIC     THEN al.CD_MATRICULA_ALUNO END)                   AS ed_infantil,
# MAGIC  
# MAGIC   -- FUND. ANOS INICIAIS
# MAGIC   COUNT(DISTINCT CASE
# MAGIC     WHEN tu.GRAU_TBTURMA = 30
# MAGIC       AND CASE WHEN al.SERIE = 0 AND al.SERIE_NIVEL_TBMATR = 0 THEN al.SERIE_TBMATR
# MAGIC                WHEN al.SERIE = 0 THEN al.SERIE_NIVEL_TBMATR
# MAGIC                ELSE al.SERIE END <> 0
# MAGIC     THEN al.CD_MATRICULA_ALUNO
# MAGIC     WHEN tu.GRAU_TBTURMA IN (14,78,80)
# MAGIC       AND CASE WHEN al.SERIE = 0 AND al.SERIE_NIVEL_TBMATR = 0 THEN al.SERIE_TBMATR
# MAGIC                WHEN al.SERIE = 0 THEN al.SERIE_NIVEL_TBMATR
# MAGIC                ELSE al.SERIE END IN (1,2,3,4,5)
# MAGIC     THEN al.CD_MATRICULA_ALUNO
# MAGIC   END)                                                AS fund_ai,
# MAGIC  
# MAGIC   -- FUND. ANOS FINAIS
# MAGIC   COUNT(DISTINCT CASE
# MAGIC     WHEN tu.GRAU_TBTURMA = 40
# MAGIC       AND CASE WHEN al.SERIE = 0 AND al.SERIE_NIVEL_TBMATR = 0 THEN al.SERIE_TBMATR
# MAGIC                WHEN al.SERIE = 0 THEN al.SERIE_NIVEL_TBMATR
# MAGIC                ELSE al.SERIE END <> 0
# MAGIC     THEN al.CD_MATRICULA_ALUNO
# MAGIC     WHEN tu.GRAU_TBTURMA IN (14,81,82,83,84)
# MAGIC       AND CASE WHEN al.SERIE = 0 AND al.SERIE_NIVEL_TBMATR = 0 THEN al.SERIE_TBMATR
# MAGIC                WHEN al.SERIE = 0 THEN al.SERIE_NIVEL_TBMATR
# MAGIC                ELSE al.SERIE END IN (6,7,8,9)
# MAGIC     THEN al.CD_MATRICULA_ALUNO
# MAGIC   END)                                                AS fund_af,
# MAGIC  
# MAGIC   -- ENSINO MÉDIO
# MAGIC   COUNT(DISTINCT CASE
# MAGIC     WHEN tu.GRAU_TBTURMA IN (2,25,50,76,93,98,101,104,105)
# MAGIC     THEN al.CD_MATRICULA_ALUNO
# MAGIC   END)                                                AS ensino_medio,
# MAGIC  
# MAGIC   -- EJA (total agrupado: CEEJA + EJA todas sub-categorias)
# MAGIC   COUNT(DISTINCT CASE
# MAGIC     WHEN tu.GRAU_TBTURMA IN (3,4,5,61,62,63,87,88,107,56)
# MAGIC     THEN al.CD_MATRICULA_ALUNO
# MAGIC   END)                                                AS eja_total,
# MAGIC  
# MAGIC   --   CEEJA (TIPOCLASSE IN 75,76,77,78)
# MAGIC   COUNT(DISTINCT CASE
# MAGIC     WHEN tu.GRAU_TBTURMA IN (3,61) AND tu.TIPOCLASSE IN (75,76,77,78)
# MAGIC     THEN al.CD_MATRICULA_ALUNO
# MAGIC   END)                                                AS ceeja_ai,
# MAGIC  
# MAGIC   COUNT(DISTINCT CASE
# MAGIC     WHEN tu.GRAU_TBTURMA IN (4,62,87) AND tu.TIPOCLASSE IN (75,76,77,78)
# MAGIC     THEN al.CD_MATRICULA_ALUNO
# MAGIC   END)                                                AS ceeja_af,
# MAGIC  
# MAGIC   COUNT(DISTINCT CASE
# MAGIC     WHEN tu.GRAU_TBTURMA IN (5,63,88,107,56) AND tu.TIPOCLASSE IN (75,76,77,78)
# MAGIC     THEN al.CD_MATRICULA_ALUNO
# MAGIC   END)                                                AS ceeja_em,
# MAGIC  
# MAGIC   -- EJA (nova regra 2026: TIPOCLASSE NOT IN 75,76,77,78)
# MAGIC   COUNT(DISTINCT CASE
# MAGIC     WHEN tu.GRAU_TBTURMA IN (3,61) AND tu.TIPOCLASSE NOT IN (75,76,77,78)
# MAGIC     THEN al.CD_MATRICULA_ALUNO
# MAGIC   END)                                                AS eja_ai,
# MAGIC  
# MAGIC   COUNT(DISTINCT CASE
# MAGIC     WHEN tu.GRAU_TBTURMA IN (4,62,87) AND tu.TIPOCLASSE NOT IN (75,76,77,78)
# MAGIC     THEN al.CD_MATRICULA_ALUNO
# MAGIC   END)                                                AS eja_af,
# MAGIC  
# MAGIC   COUNT(DISTINCT CASE
# MAGIC     WHEN tu.GRAU_TBTURMA IN (5,63,88,107,56) AND tu.TIPOCLASSE NOT IN (75,76,77,78)
# MAGIC     THEN al.CD_MATRICULA_ALUNO
# MAGIC   END)                                                AS eja_em,
# MAGIC  
# MAGIC   -- PROFISSIONALIZANTE
# MAGIC   COUNT(DISTINCT CASE
# MAGIC     WHEN tu.GRAU_TBTURMA IN (46,99,22,21,104,97,92,94,100,91,23,24,95,90,57,25,108,93,98,107,35)
# MAGIC     THEN al.CD_MATRICULA_ALUNO
# MAGIC   END)                                                AS profissionalizante
# MAGIC  
# MAGIC FROM deinf.bronze.escola es
# MAGIC INNER JOIN deinf.bronze.classe tu
# MAGIC   ON tu.COD_ESC = es.COD_ESC AND tu.ANO_MES = '202605'
# MAGIC INNER JOIN deinf.bronze.aluno al
# MAGIC   ON al.NUMCLASSE = tu.CLASSE AND al.ANO_MES = '202605'
# MAGIC WHERE es.ANO_MES = '202605'
# MAGIC   -- AND es.DEPADM = 1
# MAGIC   AND es.CODSIT = 1
# MAGIC   AND al.FLAG_SIT_ALUNO = 0
# MAGIC   AND tu.DURCLASSE IN (0, 1)  -- turmas ativas 1° semestre
# MAGIC   AND tu.GRAU_TBTURMA IN (
# MAGIC     2,3,4,5,6,13,14,25,30,36,37,40,46,47,50,54,55,56,
# MAGIC     61,62,63,74,75,76,78,80,81,82,83,84,87,88,89,90,
# MAGIC     91,92,93,97,98,99,101,102,103,104,105,107,35
# MAGIC   )
# MAGIC GROUP BY es.COD_ESC, es.ANO_MES

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from citem.sandbox.sed_congelado_maio_26

# COMMAND ----------

# DBTITLE 1,Análise de Divergência SED vs Censo Escolar
# MAGIC %sql
# MAGIC -- Divergência por escola: SED Congelado (maio/2026) vs Censo Escolar — filtrado pelas escolas da base Excelência
# MAGIC WITH excelencia AS (
# MAGIC   SELECT ESCOLA_CD_ESCOLA, ds_rede_ensino, DIRETORIA_NM_DIRETORIA
# MAGIC   FROM citem.power_bi.excelencia
# MAGIC ),
# MAGIC sed AS (
# MAGIC   SELECT * FROM citem.sandbox.sed_congelado_maio_26
# MAGIC ),
# MAGIC censo AS (
# MAGIC   SELECT *
# MAGIC   FROM citem.sandbox.tb_censo_escolar_coleta_historico
# MAGIC   WHERE dt_referencia = (SELECT MAX(dt_referencia) FROM citem.sandbox.tb_censo_escolar_coleta_historico)
# MAGIC     AND total_matriculas_curricular > 0
# MAGIC ),
# MAGIC comparativo AS (
# MAGIC   SELECT
# MAGIC     s.COD_ESC,
# MAGIC     ex.ds_rede_ensino                           AS rede_ensino,
# MAGIC     ex.DIRETORIA_NM_DIRETORIA                   AS diretoria,
# MAGIC     c.nm_escola,
# MAGIC     c.municipio,
# MAGIC     c.forma_coleta,
# MAGIC     -- TOTAL
# MAGIC     s.total_matriculas                          AS sed_total,
# MAGIC     c.total_matriculas_curricular               AS censo_total,
# MAGIC     s.total_matriculas - c.total_matriculas_curricular AS diff_total,
# MAGIC     -- EDUCAÇÃO INFANTIL
# MAGIC     s.ed_infantil                               AS sed_ei,
# MAGIC     (c.mat_presencial_creche + c.mat_presencial_pre_escola) AS censo_ei,
# MAGIC     s.ed_infantil - (c.mat_presencial_creche + c.mat_presencial_pre_escola) AS diff_ei,
# MAGIC     -- FUND. ANOS INICIAIS
# MAGIC     s.fund_ai                                   AS sed_ai,
# MAGIC     c.mat_presencial_ensino_fundamental_anos_iniciais AS censo_ai,
# MAGIC     s.fund_ai - c.mat_presencial_ensino_fundamental_anos_iniciais AS diff_ai,
# MAGIC     -- FUND. ANOS FINAIS
# MAGIC     s.fund_af                                   AS sed_af,
# MAGIC     c.mat_presencial_ensino_fundamental_anos_finais AS censo_af,
# MAGIC     s.fund_af - c.mat_presencial_ensino_fundamental_anos_finais AS diff_af,
# MAGIC     -- ENSINO MÉDIO
# MAGIC     s.ensino_medio                              AS sed_em,
# MAGIC     (c.mat_presencial_ensino_medio + c.mat_presencial_ensino_medio_normal_magisterio) AS censo_em,
# MAGIC     s.ensino_medio - (c.mat_presencial_ensino_medio + c.mat_presencial_ensino_medio_normal_magisterio) AS diff_em,
# MAGIC     -- EJA
# MAGIC     s.eja_total                                 AS sed_eja,
# MAGIC     (c.mat_presencial_eja_fundamental_e_fic_integrado
# MAGIC      + c.mat_presencial_eja_medio_fic_integrado_e_tecnico_integrado
# MAGIC      + c.mat_semipresencial_eja_curricular
# MAGIC      + c.mat_ead_eja_fundamental
# MAGIC      + c.mat_ead_eja_medio)                     AS censo_eja,
# MAGIC     s.eja_total - (c.mat_presencial_eja_fundamental_e_fic_integrado
# MAGIC      + c.mat_presencial_eja_medio_fic_integrado_e_tecnico_integrado
# MAGIC      + c.mat_semipresencial_eja_curricular
# MAGIC      + c.mat_ead_eja_fundamental
# MAGIC      + c.mat_ead_eja_medio)                     AS diff_eja,
# MAGIC     -- PROFISSIONALIZANTE
# MAGIC     s.profissionalizante                        AS sed_prof,
# MAGIC     (c.mat_presencial_curso_tecnico_concomitante_subsequente
# MAGIC      + c.mat_ead_educacao_profissional_tecnica_de_nivel_medio_concomitante_subsequente) AS censo_prof,
# MAGIC     s.profissionalizante - (c.mat_presencial_curso_tecnico_concomitante_subsequente
# MAGIC      + c.mat_ead_educacao_profissional_tecnica_de_nivel_medio_concomitante_subsequente) AS diff_prof
# MAGIC   FROM sed s
# MAGIC   INNER JOIN excelencia ex ON s.COD_ESC = ex.ESCOLA_CD_ESCOLA
# MAGIC   INNER JOIN censo c ON s.COD_ESC = c.cd_cie
# MAGIC )
# MAGIC SELECT
# MAGIC   COD_ESC,
# MAGIC   rede_ensino,
# MAGIC   diretoria,
# MAGIC   nm_escola,
# MAGIC   municipio,
# MAGIC   forma_coleta,
# MAGIC   sed_total,
# MAGIC   censo_total,
# MAGIC   diff_total,
# MAGIC   ROUND(diff_total * 100.0 / NULLIF(sed_total, 0), 1) AS pct_diff_total,
# MAGIC   -- Percentual por modalidade: (SED - Censo) / SED
# MAGIC   diff_ei,
# MAGIC   ROUND(diff_ei * 100.0 / NULLIF(sed_ei, 0), 1)   AS pct_diff_ei,
# MAGIC   diff_ai,
# MAGIC   ROUND(diff_ai * 100.0 / NULLIF(sed_ai, 0), 1)   AS pct_diff_ai,
# MAGIC   diff_af,
# MAGIC   ROUND(diff_af * 100.0 / NULLIF(sed_af, 0), 1)   AS pct_diff_af,
# MAGIC   diff_em,
# MAGIC   ROUND(diff_em * 100.0 / NULLIF(sed_em, 0), 1)   AS pct_diff_em,
# MAGIC   diff_eja,
# MAGIC   ROUND(diff_eja * 100.0 / NULLIF(sed_eja, 0), 1) AS pct_diff_eja,
# MAGIC   diff_prof,
# MAGIC   ROUND(diff_prof * 100.0 / NULLIF(sed_prof, 0), 1) AS pct_diff_prof
# MAGIC FROM comparativo
# MAGIC where 1 = 1
# MAGIC and rede_ensino like 'Federal'
# MAGIC ---group by diretoria
# MAGIC ORDER BY ABS(pct_diff_total) DESC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   COD_ESC,
# MAGIC   rede_ensino,
# MAGIC   diretoria,
# MAGIC   nm_escola,
# MAGIC   municipio,
# MAGIC   forma_coleta,
# MAGIC   sed_total,
# MAGIC   censo_total,
# MAGIC   diff_total,
# MAGIC   ROUND(diff_total * 100.0 / NULLIF(sed_total, 0), 1) AS pct_diff_total,
# MAGIC   -- Percentual por modalidade: (SED - Censo) / SED
# MAGIC   diff_ei,
# MAGIC   ROUND(diff_ei * 100.0 / NULLIF(sed_ei, 0), 1)   AS pct_diff_ei,
# MAGIC   diff_ai,
# MAGIC   ROUND(diff_ai * 100.0 / NULLIF(sed_ai, 0), 1)   AS pct_diff_ai,
# MAGIC   diff_af,
# MAGIC   ROUND(diff_af * 100.0 / NULLIF(sed_af, 0), 1)   AS pct_diff_af,
# MAGIC   diff_em,
# MAGIC   ROUND(diff_em * 100.0 / NULLIF(sed_em, 0), 1)   AS pct_diff_em,
# MAGIC   diff_eja,
# MAGIC   ROUND(diff_eja * 100.0 / NULLIF(sed_eja, 0), 1) AS pct_diff_eja,
# MAGIC   diff_prof,
# MAGIC   ROUND(diff_prof * 100.0 / NULLIF(sed_prof, 0), 1) AS pct_diff_prof
# MAGIC FROM comparativo
# MAGIC where 1 = 1
# MAGIC and rede_ensino = 'Pública'
# MAGIC ORDER BY ABS(pct_diff_total) DESC