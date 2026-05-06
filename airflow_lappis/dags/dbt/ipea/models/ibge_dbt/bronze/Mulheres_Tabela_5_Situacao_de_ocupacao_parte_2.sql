{{ config(materialized="table") }}

SELECT
    brasil_grande_regiao_unidade_federacao_municipio,
    sexo_situacao_ocupacao_semana_referencia_total_total,
    sexo_situacao_ocupacao_semana_referencia_total_ocupadas,
    sexo_situacao_ocupacao_semana_referencia_total_nao_ocupadas,
    sexo_situacao_ocupacao_semana_referencia_homens_total,
    sexo_situacao_ocupacao_semana_referencia_homens_ocupadas,
    sexo_situacao_ocupacao_semana_referencia_homens_nao_ocupadas,
    sexo_situacao_ocupacao_semana_referencia_mulheres_total,
    sexo_situacao_ocupacao_semana_referencia_mulheres_ocupadas,
    sexo_situacao_ocupacao_semana_referencia_mulheres_nao_ocupadas,
    (dt_ingest || '-03:00')::timestamptz AS dt_ingest,
    nome_fonte
FROM {{ source("censo_demografico", "mulheres_tabela_5_tabela_base_do_sidra_10253_parte_2") }}
