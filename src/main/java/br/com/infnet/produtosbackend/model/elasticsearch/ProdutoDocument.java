package br.com.infnet.produtosbackend.model.elasticsearch;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.*;
import org.springframework.data.annotation.Id;
import org.springframework.data.elasticsearch.annotations.DateFormat;
import org.springframework.data.elasticsearch.annotations.Document;
import org.springframework.data.elasticsearch.annotations.Field;
import org.springframework.data.elasticsearch.annotations.FieldType;

import java.time.Instant;
import java.time.LocalDateTime;
import java.util.List;


@Document(indexName = "produtos_hipster", createIndex = false)
@Getter@Setter@AllArgsConstructor@NoArgsConstructor@ToString
public class ProdutoDocument {
    @Id
    private String id;

    @Field(type = FieldType.Text, name = "nome")
    private String nome;

    @Field(type = FieldType.Text, name = "descricao")
    private String descricao;

    @Field(type = FieldType.Keyword, name = "categoria")
    private String categoria;

    @Field(type = FieldType.Keyword, name = "subcategoria")
    private String subcategoria;

    @Field(type = FieldType.Keyword, name = "marca")
    private String marca;

    @Field(type = FieldType.Float, name = "preco")
    private Float preco;

    @Field(type = FieldType.Boolean, name = "emPromocao")
    private Boolean emPromocao;

    @Field(type = FieldType.Float, name = "rating")
    private Float rating;

    @Field(type = FieldType.Keyword, name = "tags")
    private List<String> tags;

    @Field(type = FieldType.Keyword, name = "cor")
    private String cor;

    @Field(type = FieldType.Boolean, name = "disponivel")
    private Boolean disponivel;

    @Field(type = FieldType.Date, name = "createdAt")
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime createdAt;

}
