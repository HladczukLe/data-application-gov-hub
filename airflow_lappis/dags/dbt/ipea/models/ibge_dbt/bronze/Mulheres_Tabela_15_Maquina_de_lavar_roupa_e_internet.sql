{{ config(materialized="table") }}

SELECT
    brasil_grande_regiao_unidade_federacao_municipio,
    maquina_lavar_roupas_branca,
    maquina_lavar_roupas_preta_parda,
    maquina_lavar_roupas_indigena,
    conexao_domiciliar_a_internet_branca,
    conexao_domiciliar_a_internet_preta_parda,
    conexao_domiciliar_a_internet_indigena,
    (dt_ingest || '-03:00')::timestamptz AS dt_ingest,
    nome_fonte
FROM {{ source("censo_demografico", "mulheres_tabela_15_br_gr_uf_mu") }}
