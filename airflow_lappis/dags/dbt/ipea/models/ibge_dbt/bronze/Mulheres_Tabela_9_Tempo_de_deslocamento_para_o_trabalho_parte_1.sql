{{ config(materialized="table") }}

SELECT
    brasil_grande_regiao_unidade_federacao_municipio,
    homens_total,
    homens_ate_cinco_minutos,
    homens_seis_minutos_ate_quinze_minutos,
    homens_mais_quinze_minutos_ate_meia_hora,
    homens_mais_meia_hora_ate_uma_hora,
    homens_mais_uma_hora_ate_duas_horas,
    homens_mais_duas_horas_ate_quatro_horas,
    homens_mais_quatro_horas,
    mulheres_total,
    mulheres_ate_cinco_minutos,
    mulheres_seis_minutos_ate_quinze_minutos,
    mulheres_mais_quinze_minutos_ate_meia_hora,
    mulheres_mais_meia_hora_ate_uma_hora,
    mulheres_mais_uma_hora_ate_duas_horas,
    mulheres_mais_duas_horas_ate_quatro_horas,
    mulheres_mais_quatro_horas,
    (dt_ingest || '-03:00')::timestamptz AS dt_ingest,
    nome_fonte
FROM {{ source("censo_demografico", "mulheres_tabela_9_tabela_base_do_sidra_10331_parte_1") }}
