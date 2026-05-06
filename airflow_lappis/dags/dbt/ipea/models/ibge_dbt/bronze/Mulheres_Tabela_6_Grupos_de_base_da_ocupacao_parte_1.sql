{{ config(materialized="table") }}

SELECT
    grandes_grupos_subgr_princ_subgr_grupos_base_ocupa_tr_principal,
    sexo_total,
    sexo_homens,
    sexo_mulheres,
    (dt_ingest || '-03:00')::timestamptz AS dt_ingest,
    nome_fonte
FROM {{ source("censo_demografico", "mulheres_tabela_6_tabela_base_do_sidra_10283_parte_1") }}
