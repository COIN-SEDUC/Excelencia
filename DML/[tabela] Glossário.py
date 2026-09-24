-- Databricks notebook source
-- DBTITLE 1,Criar tabela a partir de Excel
CREATE OR REPLACE TABLE citem.power_bi.excelencia_glossario AS
WITH raw AS (
  SELECT
    *,
    _metadata.file_modification_time AS _file_mod_time
  FROM read_files(
    '/Volumes/citem/power_bi/pex/Glossario_Indicadores*.xlsx',
    format => 'excel',
    headerRows => 1,
    dataAddress => 'Glossario'
  )
),
deduped AS (
  SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY Indicador ORDER BY _file_mod_time DESC) AS _rn
  FROM raw
)
SELECT * EXCEPT (_file_mod_time, _rn)
FROM deduped
WHERE _rn = 1