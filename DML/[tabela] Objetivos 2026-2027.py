-- Databricks notebook source
-- DBTITLE 1,⚠️ AVISO — Não modificar sem autorização
-- MAGIC %md
-- MAGIC ## ⚠️ ATENÇÃO — Notebook em produção
-- MAGIC
-- MAGIC **Este notebook é executado automaticamente por um job (ID: `1140001018845630`) via trigger de File Arrival.**
-- MAGIC
-- MAGIC > **Não delete, renomeie ou modifique este notebook sem antes conversar com o responsável.**
-- MAGIC >
-- MAGIC > Contato: `lucas.ferro@apoioeducacao.sp.gov.br`
-- MAGIC
-- MAGIC Alterações indevidas podem quebrar a atualização automática da tabela `citem.power_bi.excelencia_objetivo`.

-- COMMAND ----------

-- DBTITLE 1,Atualização da tabela de metas - excelência URE
--atualizando a tabela excelencia_objetivo com os dados do excel

--validar se as colunas no excel correspondem as colunas do select

merge into citem.power_bi.excelencia_objetivo as d --d = destino
using (
    select * from(
        select 
            `chave` as chave,
            try_cast( `ano_ref` as int) as ano_ref,
            `URE` as diretoria,
            try_cast(`Ensino Médio Noturno` as decimal(6,4)) as alunos_noturnos,
            try_cast(`PEI` as decimal(6,4)) as alunos_pei, 
            try_cast(`Salas de Aula` as int) as salas_aula,
            try_cast(`Pendentes` as decimal(6,4)) as alunos_pendentes, 
            try_cast(`Qualid. Enturmamento` as decimal(6,4)) as qualidade_entur, 
            try_cast(`Fechamento` as decimal(6,4)) as fechamento,
            try_cast(`Rendimento` as decimal(6,4)) as rendimento,
            try_cast(`Bolsa Família: % não informados` as decimal(6,4)) as bolsa_percent_nao_informado,
            try_cast(`Censo: Div. Matrícula` as decimal(6,4)) as diverg_matricula,
            try_cast(`Censo: Div. Rendimento` as decimal(6,4)) as diverg_rendimento,
            try_cast(`Cadastro Escolas` as decimal(6,4)) as cadastro_escola, 
            try_cast(`Cadastro Alunos` as decimal(6,4)) as cadastro_aluno,
            row_number() over(
                partition by `chave`
                order by _metadata.file_modification_time desc
            ) as rn --garante registro mais recente em caso de duplicatas
        from read_files(
        '/Volumes/citem/power_bi/objetivos_pex/*.xlsx', --todos os arquivos excel do volume
        format =>  'excel',
        headerRows => 1,
        dataAddress =>  'Objetivos'
        )
    )
    where rn = 1
      and chave is not null
      and trim(chave) != ''
) as o --o = origem
on d.chave = o.chave
when matched then
    update set
    d.chave = concat(o.ano_ref,'_',o.diretoria),
    d.ano_ref	 = 	o.ano_ref,
    d.diretoria	 = 	o.diretoria,
    d.alunos_noturnos	 = 	o.alunos_noturnos,
    d.alunos_pei	 = 	o.alunos_pei,
    d.salas_aula	 = 	o.salas_aula,
    d.alunos_pendentes	 = 	o.alunos_pendentes,
    d.qualidade_entur	 = 	o.qualidade_entur,
    d.fechamento	 = 	o.fechamento,
    d.rendimento	 = 	o.rendimento,
    d.bolsa_percent_nao_informado	 = 	o.bolsa_percent_nao_informado,
    d.diverg_matricula	 = 	o.diverg_matricula,
    d.diverg_rendimento	 = 	o.diverg_rendimento,
    d.cadastro_escola	 = 	o.cadastro_escola,
    d.cadastro_aluno	 = 	o.cadastro_aluno
when not matched then
    insert (
        d.chave,
        d.ano_ref,
        d.diretoria,
        d.alunos_noturnos,
        d.alunos_pei,
        d.salas_aula,
        d.alunos_pendentes,
        d.qualidade_entur,
        d.fechamento,
        d.rendimento,
        d.bolsa_percent_nao_informado,
        d.diverg_matricula,
        d.diverg_rendimento,
        d.cadastro_escola,
        d.cadastro_aluno
    )
    values (
        concat(o.ano_ref,'_',o.diretoria),
        o.ano_ref,
        o.diretoria,
        o.alunos_noturnos,
        o.alunos_pei,
        o.salas_aula,
        o.alunos_pendentes,
        o.qualidade_entur,
        o.fechamento,
        o.rendimento,
        o.bolsa_percent_nao_informado,
        o.diverg_matricula,
        o.diverg_rendimento,
        o.cadastro_escola,
        o.cadastro_aluno
    )



-- COMMAND ----------

-- DBTITLE 1,Célula de parada do job
-- MAGIC %python
-- MAGIC dbutils.notebook.exit("Ok")
-- MAGIC
-- MAGIC

-- COMMAND ----------

select * from citem.power_bi.excelencia_objetivo