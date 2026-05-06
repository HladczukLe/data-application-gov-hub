{{ config(materialized="table") }}

SELECT
    brasil_grande_regiao_unidade_federacao,
    total_total,
    total_homens,
    total_mulheres,
    educacao_total,
    educacao_homens,
    educacao_mulheres,
    ciencias_naturais_matematica_estatistica_total,
    ciencias_naturais_matematica_estatistica_homens,
    ciencias_naturais_matematica_estatistica_mulheres,
    computacao_tecnologias_informacao_comunicacao_tic_total,
    computacao_tecnologias_informacao_comunicacao_tic_homens,
    computacao_tecnologias_informacao_comunicacao_tic_mulheres,
    engenharia_producao_construcao_total,
    engenharia_producao_construcao_homens,
    engenharia_producao_construcao_mulheres,
    saude_bem_estar_total,
    saude_bem_estar_homens,
    saude_bem_estar_mulheres,
    servicos_pessoais_total,
    servicos_pessoais_homens,
    servicos_pessoais_mulheres,
    (dt_ingest || '-03:00')::timestamptz AS dt_ingest,
    nome_fonte
FROM {{ source("censo_demografico", "mulheres_tabela_3_tabela_base_do_sidra_10063_parte_1") }}
