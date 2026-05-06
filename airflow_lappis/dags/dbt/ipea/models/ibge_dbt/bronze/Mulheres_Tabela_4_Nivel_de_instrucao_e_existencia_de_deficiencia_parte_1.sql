{{ config(materialized="table") }}

SELECT
    brasil_grande_regiao_unidade_federacao_municipio,
    sexo_exist_defic_nivel_instr_homens_pessoa_defic_total,
    sexo_exist_defic_nivel_instr_homens_pessoa_defic_sem_incompleto,
    sexo_exist_defic_nivel_instr_homens_pessoa_defic_fun_incompleto,
    sexo_exist_defic_nivel_instr_homens_pessoa_defic_med_incompleto,
    sexo_exist_defic_nivel_instr_homens_pessoa_defic_super_completo,
    sexo_exist_defic_nivel_instr_homens_pessoa_sem_defic_total,
    sexo_exist_defic_nivel_instr_homens_pessoa_sem_defic_incompleto,
    sexo_exist_defic_nivel_instr_homens_pessoa_sem_defic_incomple_1,
    sexo_exist_defic_nivel_instr_homens_pessoa_sem_defic_incomple_2,
    sexo_exist_defic_nivel_instr_homens_pessoa_sem_defic_s_completo,
    sexo_exist_defic_nivel_instr_mulhe_pessoa_defic_total,
    sexo_exist_defic_nivel_instr_mulhe_pessoa_defic_sem__incompleto,
    sexo_exist_defic_nivel_instr_mulhe_pessoa_defic_fund_incompleto,
    sexo_exist_defic_nivel_instr_mulhe_pessoa_defic_medi_incompleto,
    sexo_exist_defic_nivel_instr_mulhe_pessoa_defic_super_completo,
    sexo_exist_defic_nivel_instr_mulhe_pessoa_sem_defic_total,
    sexo_exist_defic_nivel_instr_mulhe_pessoa_sem_defic__incompleto,
    sexo_exist_defic_nivel_instr_mulhe_pessoa_sem_defic__incomple_1,
    sexo_exist_defic_nivel_instr_mulhe_pessoa_sem_defic__incomple_2,
    sexo_exist_defic_nivel_instr_mulhe_pessoa_sem_defic_su_completo,
    (dt_ingest || '-03:00')::timestamptz AS dt_ingest,
    nome_fonte
FROM {{ source("censo_demografico", "mulheres_tabela_4_tabela_base_do_sidra_10141_parte_1") }}
