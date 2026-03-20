package br.com.infnet.produtosbackend;

import br.com.infnet.produtosbackend.service.elastic.GoogleLikeService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.io.IOException;

@SpringBootTest
class ProdutosBackendApplicationTests {
    @Autowired
    GoogleLikeService google;
	@Test
	void contextLoads() throws IOException {
        var result = google.buscarComHighlight("guitarra");
        System.out.println(result);
	}

}
