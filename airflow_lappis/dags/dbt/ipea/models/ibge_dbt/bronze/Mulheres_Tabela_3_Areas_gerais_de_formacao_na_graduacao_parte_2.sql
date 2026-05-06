{{ config(materialized="table") }}

SELECT
    brasil_grande_regiao_unidade_federacao,
    total_total,
    total_homens,
    total_mulheres,
    ciencia_tecnologia_engenharias_matematica_total,
    ciencia_tecnologia_engenharias_matematica_homens,
    ciencia_tecnologia_engenharias_matematica_mulheres,
    educacao_servicos_pessoais_saude_bem_estar_total,
    educacao_servicos_pessoais_saude_bem_estar_homens,
    educacao_servicos_pessoais_saude_bem_estar_mulheres,
    (dt_ingest || '-03:00')::timestamptz AS dt_ingest,
    nome_fonte
FROM {{ source("censo_demografico", "mulheres_tabela_3_tabela_base_do_sidra_10063_parte_2") }}
