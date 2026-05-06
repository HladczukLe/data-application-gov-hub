{{ config(materialized="table") }}

SELECT
    brasil_grande_regiao_unidade_federacao_municipio,
    total_total,
    total_sem_instrucao_fundamental_incompleto,
    total_fundamental_completo_medio_incompleto,
    total_medio_completo_superior_incompleto,
    total_superior_completo,
    homens_total,
    homens_sem_instrucao_fundamental_incompleto,
    homens_fundamental_completo_medio_incompleto,
    homens_medio_completo_superior_incompleto,
    homens_superior_completo,
    mulheres_total,
    mulheres_sem_instrucao_fundamental_incompleto,
    mulheres_fundamental_completo_medio_incompleto,
    mulheres_medio_completo_superior_incompleto,
    mulheres_superior_completo,
    (dt_ingest || '-03:00')::timestamptz AS dt_ingest,
    nome_fonte
FROM {{ source("censo_demografico", "mulheres_tabela_2_tabela_base_do_sidra_10061_parte_2") }}
