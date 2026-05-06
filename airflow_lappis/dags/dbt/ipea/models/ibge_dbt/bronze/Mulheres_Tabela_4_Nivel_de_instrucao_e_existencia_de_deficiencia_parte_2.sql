{{ config(materialized="table") }}

SELECT
    brasil_grande_regiao_unidade_federacao_municipio,
    homens_pessoa_deficiencia_total,
    homens_pessoa_deficiencia_sem_instrucao_fundamental_incompleto,
    homens_pessoa_deficiencia_fundamental_completo_medio_incompleto,
    homens_pessoa_deficiencia_medio_completo_superior_incompleto,
    homens_pessoa_deficiencia_superior_completo,
    homens_pessoa_sem_deficiencia_total,
    homens_pessoa_sem_defic_sem_instr_funda_incompleto,
    homens_pessoa_sem_defic_funda_compl_medio_incompleto,
    homens_pessoa_sem_defic_medio_compl_super_incompleto,
    homens_pessoa_sem_deficiencia_superior_completo,
    mulheres_pessoa_deficiencia_total,
    mulheres_pessoa_defic_sem_instr_funda_incompleto,
    mulheres_pessoa_defic_funda_compl_medio_incompleto,
    mulheres_pessoa_deficiencia_medio_completo_superior_incompleto,
    mulheres_pessoa_deficiencia_superior_completo,
    mulheres_pessoa_sem_deficiencia_total,
    mulheres_pessoa_sem_defic_sem_instr_funda_incompleto,
    mulheres_pessoa_sem_defic_funda_compl_medio_incompleto,
    mulheres_pessoa_sem_defic_medio_compl_super_incompleto,
    mulheres_pessoa_sem_deficiencia_superior_completo,
    (dt_ingest || '-03:00')::timestamptz AS dt_ingest,
    nome_fonte
FROM {{ source("censo_demografico", "mulheres_tabela_4_tabela_base_do_sidra_10141_parte_2") }}
