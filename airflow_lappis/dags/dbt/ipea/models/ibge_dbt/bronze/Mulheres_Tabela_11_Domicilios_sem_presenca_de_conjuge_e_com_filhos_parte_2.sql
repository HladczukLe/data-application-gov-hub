{{ config(materialized="table") }}

SELECT
    brasil_grande_regiao_unidade_federacao_municipio,
    sexo_pessoa_responsavel_pelo_domicilio_total,
    sexo_pessoa_responsavel_pelo_domicilio_homens,
    sexo_pessoa_responsavel_pelo_domicilio_mulheres,
    (dt_ingest || '-03:00')::timestamptz AS dt_ingest,
    nome_fonte
FROM {{ source("censo_demografico", "mulheres_tabela_11_tabela_base_do_sidra_9882_parte_2") }}
