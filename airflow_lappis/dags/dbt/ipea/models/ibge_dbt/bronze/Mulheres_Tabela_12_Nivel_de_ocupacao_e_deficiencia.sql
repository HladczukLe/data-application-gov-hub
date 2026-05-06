{{ config(materialized="table") }}

SELECT
    brasil_grande_regiao_unidade_federacao_municipio,
    homens_14_a_17_sem_deficiencia,
    homens_14_a_17_deficiencia,
    homens_18_a_59_sem_deficiencia,
    homens_18_a_59_deficiencia,
    homens_60_mais_sem_deficiencia,
    homens_60_mais_deficiencia,
    mulheres_14_a_17_sem_deficiencia,
    mulheres_14_a_17_deficiencia,
    mulheres_18_a_59_sem_deficiencia,
    mulheres_18_a_59_deficiencia,
    mulheres_60_mais_sem_deficiencia,
    mulheres_60_mais_deficiencia,
    (dt_ingest || '-03:00')::timestamptz AS dt_ingest,
    nome_fonte
FROM {{ source("censo_demografico", "mulheres_tabela_12_br_gr_uf_mu") }}
