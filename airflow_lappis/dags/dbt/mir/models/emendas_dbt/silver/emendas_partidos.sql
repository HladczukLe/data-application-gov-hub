{{ config(materialized='table') }}

WITH tg_emendas AS (
	SELECT *
	FROM {{ ref('tg_emendas') }}
),

parlamentares AS (
	SELECT *
	FROM {{ ref('parlamentares') }}
),

tg_emendas_tratado AS (
	SELECT
		*,
		TRIM(UPPER(autor_emendas_orcamento_nome)) AS chave_join_nome
	FROM tg_emendas
),

final AS (
	SELECT
		e.emissao_mes,
		e.emissao_dia,
		e.programa_governo AS codigo_programa,
		e.programa_governo_descricao AS programa,
		e.acao_governo AS codigo_acao_ajustada,
		e.acao_governo_descricao AS acao_ajustada,
		e.autor_emendas_orcamento_descricao,
		e.uf_pt AS uf,
		e.uf_pt_descricao AS uf_descricao,
		e.municipio_pt AS municipio,
		'Brasil' AS pais,
		e.ne_ccor,
		e.ne_num_processo,
		e.ne_info_complementar,
		e.ne_ccor_descricao,
		e.doc_observacao,
		e.grupo_despesa AS codigo_gnd,
		e.grupo_despesa_descricao AS gnd,
		e.natureza_despesa,
		e.natureza_despesa_descricao,
		e.modalidade_aplicacao AS codigo_modalidade,
		e.modalidade_aplicacao_descricao AS modalidade,
		e.ne_ccor_favorecido,
		e.ne_ccor_favorecido_descricao,
		e.ne_ccor_ano_emissao,
		e.ptres,
		e.item_informacao,
		e.item_informacao_descricao,
		e.despesas_empenhadas,
		e.despesas_liquidadas,
		e.despesas_pagas,

		p.id_parlamentar as id_autor,
		p.cargo_parlamentar as cargo_autor,
		p.nome_parlamentar as autor,
		p.sigla_partido as partido,
		p.uf_parlamentar as uf_autor,
		p.url_foto as url_foto_autor,
		p.email as email_autor,
		p.url_logo_partido as url_foto_partido,

		e.dt_ingest

	FROM tg_emendas_tratado e
	LEFT JOIN parlamentares p
		ON e.chave_join_nome = p.chave_join_nome
)

SELECT *
FROM final
