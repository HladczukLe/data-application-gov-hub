{{ config(materialized="table") }}

SELECT
    brasil_grande_regiao_unidade_federacao_municipio,
    sexo_local_exercicio_trabalho_principal_total_total,
    sexo_local_exerc_traba_princ_total_domic_residencia,
    sexo_local_exerc_traba_princ_total_fora_domic_residencia,
    sexo_local_exercicio_trabalho_principal_total_outro_municipio,
    sexo_local_exercicio_trabalho_principal_homens_total,
    sexo_local_exerc_traba_princ_homens_domic_residencia,
    sexo_local_exerc_traba_princ_homens_fora_domic_residencia,
    sexo_local_exercicio_trabalho_principal_homens_outro_municipio,
    sexo_local_exercicio_trabalho_principal_mulheres_total,
    sexo_local_exerc_traba_princ_mulhe_domic_residencia,
    sexo_local_exerc_traba_princ_mulhe_fora_domic_residencia,
    sexo_local_exerc_traba_princ_mulhe_outro_municipio,
    (dt_ingest || '-03:00')::timestamptz AS dt_ingest,
    nome_fonte
FROM {{ source("censo_demografico", "mulheres_tabela_8_tabela_base_do_sidra_10329_parte_1") }}
