{{ config(materialized="table") }}

SELECT
    brasil_grande_regiao_unidade_federacao_municipio,
    branca_a_pe,
    branca_bicicleta,
    branca_motocicleta_mototaxi,
    branca_automovel_taxi_assemelhados,
    branca_transporte_coletivo,
    branca_outros,
    preta_parda_a_pe,
    preta_parda_bicicleta,
    preta_parda_motocicleta_mototaxi,
    preta_parda_automovel_taxi_assemelhados,
    preta_parda_transporte_coletivo,
    preta_parda_outros,
    indigena_a_pe,
    indigena_bicicleta,
    indigena_motocicleta_mototaxi,
    indigena_automovel_taxi_assemelhados,
    indigena_transporte_coletivo,
    indigena_outros,
    (dt_ingest || '-03:00')::timestamptz AS dt_ingest,
    nome_fonte
FROM {{ source("censo_demografico", "mulheres_tabela_13_br_gr_uf_mu") }}
