package br.com.infnet.produtosbackend.service.elastic;

import br.com.infnet.produtosbackend.dto.ProdutoHighlightResponse;
import br.com.infnet.produtosbackend.model.elasticsearch.ProdutoDocument;
import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.elasticsearch.core.SearchResponse;
import co.elastic.clients.elasticsearch.core.search.HighlightField;
import co.elastic.clients.util.NamedValue;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;

@Service
@RequiredArgsConstructor
public class GoogleLikeService {
    private final ElasticsearchClient client;

    public List<ProdutoHighlightResponse> buscarComHighlight(String term) throws IOException {
        SearchResponse<ProdutoDocument> response = client.search(s -> s
                .index("produtos_hipster")
                .query(q ->
                        q.multiMatch(mm -> mm
                                .fields("nome^3", "descricao")
                                .query(term)
                        )
                ).highlight(h -> h
                        .preTags("<strong>")
                        .postTags("</strong>")
                        .fields(highlightFields("nome", "descricao"))

                ), ProdutoDocument.class
        );
        return response.hits().hits().stream().map(
                ProdutoHighlightResponse::from
        ).toList();
    }
    private List<NamedValue<HighlightField>> highlightFields(String ... fields){
        return Arrays.stream(fields)
                .map(name ->
                        NamedValue.of(name, new HighlightField.Builder().build())).toList();


    }





}
