{{ config(materialized="table") }}

select 
    grandes_grupos_subgrupos_principais_subgrupos_e_grupos_de_base_,
    indicador,
    valor,
    (dt_ingest || '-03:00')::timestamptz as dt_ingest,
    nome_fonte
from {{ source("censo_demografico", "mulheres_tabela_6_tabela_base_do_sidra_10283_parte_2") }}