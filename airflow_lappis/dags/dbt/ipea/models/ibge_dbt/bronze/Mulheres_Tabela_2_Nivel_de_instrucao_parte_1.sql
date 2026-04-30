{{ config(materialized="table") }}

select 
    brasil_grande_regiao_unidade_da_federacao_e_municipio,
    indicador,
    valor,
    (dt_ingest || '-03:00')::timestamptz as dt_ingest,
    nome_fonte
from {{ source("censo_demografico", "mulheres_tabela_2_tabela_base_do_sidra_10061_parte_1") }}