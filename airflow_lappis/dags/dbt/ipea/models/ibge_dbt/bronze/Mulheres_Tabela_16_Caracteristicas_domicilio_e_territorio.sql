{{ config(materialized="table") }}

SELECT
    brasil_grande_regiao_unidade_federacao_municipio,
    canalizacao_interna_agua_area_urbana,
    canalizacao_interna_agua_area_rural,
    canalizacao_interna_agua_terras_indigenas,
    canalizacao_interna_agua_territorios_quilobolas,
    canalizacao_interna_agua_favelas_comundades_urbanas,
    banheiro_sanitario_uso_exclusivo_area_urbana,
    banheiro_sanitario_uso_exclusivo_area_rural,
    banheiro_sanitario_uso_exclusivo_terras_indigenas,
    banheiro_sanitario_uso_exclusivo_territorios_quilobolas,
    banheiro_sanitario_uso_exclusivo_favelas_comundades_urbanas,
    esgotamento_sanitario_por_rede_coletora_area_urbana,
    esgotamento_sanitario_por_rede_coletora_area_rural,
    esgotamento_sanitario_por_rede_coletora_terras_indigenas,
    esgotamento_sanitario_por_rede_coletora_territorios_quilobolas,
    esgotamento_sanit_por_rede_colet_favel_comun_urbanas,
    coleta_direta_indireta_lixo_area_urbana,
    coleta_direta_indireta_lixo_area_rural,
    coleta_direta_indireta_lixo_terras_indigenas,
    coleta_direta_indireta_lixo_territorios_quilobolas,
    coleta_direta_indireta_lixo_favelas_comundades_urbanas,
    (dt_ingest || '-03:00')::timestamptz AS dt_ingest,
    nome_fonte
FROM {{ source("censo_demografico", "mulheres_tabela_16_br_gr_uf_mu") }}
