{{ config(materialized="table") }}

SELECT
    brasil_grande_regiao_unidade_federacao_municipio,
    homens_sem_deficiencia,
    homens_deficiencia,
    mulheres_sem_deficiencia,
    mulheres_deficiencia,
    (dt_ingest || '-03:00')::timestamptz AS dt_ingest,
    nome_fonte
FROM {{ source("censo_demografico", "mulheres_tabela_14_br_gr_uf_mu") }}
