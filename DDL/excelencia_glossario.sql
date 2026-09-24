-- ============================================================================
-- DDL: citem.power_bi.excelencia_glossario
-- Descrição: Glossário dos indicadores do Programa de Excelência,
--            com fórmulas, interpretação e faixas de cores.
-- Gerado por: DML/[tabela] Glossário (notebook)
-- Modo de escrita: CREATE OR REPLACE TABLE (recriação a cada execução)
-- ============================================================================

CREATE TABLE IF NOT EXISTS citem.power_bi.excelencia_glossario (
  OrdemCategoria    BIGINT   COMMENT 'Ordem da categoria para exibição',
  Categoria         STRING   COMMENT 'Escopo | Indicador | Regra',
  OrdemIndicador    BIGINT   COMMENT 'Ordem do indicador para exibição',
  Indicador         STRING   COMMENT 'Nome do indicador ou escopo',
  Unidade           STRING   COMMENT '# (contagem) ou % (percentual)',
  Status            STRING   COMMENT 'Implementado ou Em construção',
  Descricao         STRING   COMMENT 'Texto descritivo do indicador',
  Calculo           STRING   COMMENT 'Fórmula de cálculo',
  LeituraSubida     STRING   COMMENT 'Interpretação quando o valor sobe',
  LeituraDescida    STRING   COMMENT 'Interpretação quando o valor desce',
  CorRegra          STRING   COMMENT 'Faixas verde / amarela / vermelha',
  Cuidado           STRING   COMMENT 'Observações e ressalvas'
)
USING DELTA;
