package br.com.infnet.produtosbackend.dto;

import br.com.infnet.produtosbackend.model.elasticsearch.ProdutoDocument;
import co.elastic.clients.elasticsearch.core.search.Hit;
import org.springframework.data.elasticsearch.core.SearchHit;

import java.util.List;
import java.util.Map;

public record ProdutoHighlightResponse(String id,
                                       String nome,
                                       String descricao,
                                       String categoria,
                                       String marca,
                                       Float preco,
                                       Float rating,
                                       Boolean emPromocao,
                                       Boolean disponivel,
                                       List<String> highlightsNome,
                                       List<String> highlightsDescricao) {
    public static ProdutoHighlightResponse from(Hit<ProdutoDocument> hit) {
        ProdutoDocument produto = hit.source();

        Map<String, List<String>> highlight =
                hit.highlight();
        List<String> highlightsNome =
                highlight != null ? highlight.getOrDefault("nome", List.of()) : List.of();
        List<String> highlightsDescricao =
                highlight != null ? highlight.getOrDefault("descricao", List.of()) : List.of();

        return new ProdutoHighlightResponse(
                produto.getId(),
                produto.getNome(),
                produto.getDescricao(),
                produto.getCategoria(),
                produto.getMarca(),
                produto.getPreco(),
                produto.getRating(),
                produto.getEmPromocao(),
                produto.getDisponivel(),
                highlightsNome,
                highlightsDescricao
        );
    }
}
