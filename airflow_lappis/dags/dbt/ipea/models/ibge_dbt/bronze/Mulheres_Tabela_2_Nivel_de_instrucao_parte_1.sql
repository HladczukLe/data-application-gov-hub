{{ config(materialized="table") }}

SELECT
    brasil_grande_regiao_unidade_federacao_municipio,
    sexo_nivel_instrucao_total_total,
    sexo_nivel_instrucao_total_sem_instrucao_fundamental_incompleto,
    sexo_nivel_instr_total_funda_compl_medio_incompleto,
    sexo_nivel_instrucao_total_medio_completo_superior_incompleto,
    sexo_nivel_instrucao_total_superior_completo,
    sexo_nivel_instrucao_homens_total,
    sexo_nivel_instr_homens_sem_instr_funda_incompleto,
    sexo_nivel_instr_homens_funda_compl_medio_incompleto,
    sexo_nivel_instrucao_homens_medio_completo_superior_incompleto,
    sexo_nivel_instrucao_homens_superior_completo,
    sexo_nivel_instrucao_mulheres_total,
    sexo_nivel_instr_mulhe_sem_instr_funda_incompleto,
    sexo_nivel_instr_mulhe_funda_compl_medio_incompleto,
    sexo_nivel_instr_mulhe_medio_compl_super_incompleto,
    sexo_nivel_instrucao_mulheres_superior_completo,
    (dt_ingest || '-03:00')::timestamptz AS dt_ingest,
    nome_fonte
FROM {{ source("censo_demografico", "mulheres_tabela_2_tabela_base_do_sidra_10061_parte_1") }}
