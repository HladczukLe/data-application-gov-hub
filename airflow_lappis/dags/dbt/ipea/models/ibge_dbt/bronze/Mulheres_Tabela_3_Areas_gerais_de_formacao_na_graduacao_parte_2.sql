{{ config(materialized="table") }}

select 
    brasil_grande_regiao_e_unidade_da_federacao,
    indicador,
    valor,
    (dt_ingest || '-03:00')::timestamptz as dt_ingest,
    nome_fonte
from {{ source("censo_demografico", "mulheres_tabela_3_tabela_base_do_sidra_10063_parte_2") }}