{{ config(materialized="table") }}

SELECT
    brasil_grande_regiao_unidade_federacao,
    grandes_grupos_ocupacao_trabalho_principal_sexo_total,
    diretores_gerentes,
    profissionais_ciencias_intelectuais,
    tecnicos_profissionais_nivel_medio,
    trabalhadores_apoio_administrativo,
    trabalhadores_dos_servicos_vendedores_dos_comercios_mercados,
    trabalhadores_qualificados_agropecuaria_florestais_caca_pesca,
    trabalhadores_quali_opera_artes_const_artes_mecan_outro_oficios,
    operadores_instalacoes_maquinas_montadores,
    ocupacoes_elementares,
    membros_forcas_armadas_policiais_bombeiros_militares,
    ocupacoes_mal_definidas,
    (dt_ingest || '-03:00')::timestamptz AS dt_ingest,
    nome_fonte
FROM {{ source("censo_demografico", "mulheres_tabela_7_tabela_base_do_sidra_10282_parte_2") }}
