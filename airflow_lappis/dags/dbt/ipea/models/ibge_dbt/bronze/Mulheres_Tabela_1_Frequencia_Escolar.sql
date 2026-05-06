{{ config(materialized="table") }}

SELECT
    brasil_grande_regiao_unidade_federacao_municipio,
    sexo_grupo_idade_homens_0_a_3_anos,
    sexo_grupo_idade_homens_4_a_5_anos,
    sexo_grupo_idade_homens_6_a_14_anos,
    sexo_grupo_idade_homens_15_a_17_anos,
    sexo_grupo_idade_homens_18_a_24_anos,
    sexo_grupo_idade_homens_25_anos_mais,
    sexo_grupo_idade_mulheres_0_a_3_anos,
    sexo_grupo_idade_mulheres_4_a_5_anos,
    sexo_grupo_idade_mulheres_6_a_14_anos,
    sexo_grupo_idade_mulheres_15_a_17_anos,
    sexo_grupo_idade_mulheres_18_a_24_anos,
    sexo_grupo_idade_mulheres_25_anos_mais,
    (dt_ingest || '-03:00')::timestamptz AS dt_ingest,
    nome_fonte
FROM {{ source("censo_demografico", "mulheres_tabela_1_tabela_base_do_sidra_10056") }}
