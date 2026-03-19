#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
import uuid
from datetime import datetime, timedelta

import requests

ES_URL = "http://localhost:9200"
INDEX_NAME = "produtos_hipster"
TOTAL_PRODUTOS = 4000
BATCH_SIZE = 500
TIMEOUT = 30

random.seed()

CATEGORIAS = {
    "instrumentos": {
        "guitarras": [
            "Guitarra Stratocaster",
            "Guitarra Telecaster",
            "Guitarra Les Paul",
            "Guitarra Semi-Hollow",
            "Guitarra Offset",
            "Guitarra Superstrat",
        ],
        "baixos": [
            "Baixo Precision",
            "Baixo Jazz Bass",
            "Baixo Ativo 5 Cordas",
            "Baixo Short Scale",
            "Baixo Vintage",
        ],
        "violoes": [
            "Violão Folk",
            "Violão Jumbo",
            "Violão Clássico",
            "Violão Eletroacústico",
            "Violão Auditorium",
        ],
        "teclados": [
            "Stage Piano",
            "Sintetizador Analógico",
            "Controlador MIDI",
            "Teclado Arranjador",
            "Workstation",
        ],
        "bateria_percussao": [
            "Caixa de Bateria",
            "Prato Ride",
            "Prato Crash",
            "Cajón",
            "Pad Eletrônico",
            "Pedal de Bumbo",
        ],
    },
    "acessorios": {
        "pedais": [
            "Pedal Overdrive",
            "Pedal Distortion",
            "Pedal Delay",
            "Pedal Reverb",
            "Pedal Chorus",
            "Pedal Fuzz",
            "Pedal Compressor",
            "Pedal Wah",
        ],
        "audio": [
            "Interface de Áudio",
            "Monitor de Estúdio",
            "Fone de Referência",
            "Microfone Condensador",
            "Microfone Dinâmico",
            "Pré-Amplificador",
        ],
        "utilidades": [
            "Correia",
            "Cabo P10",
            "Suporte de Instrumento",
            "Afinador",
            "Case Premium",
            "Bag Acolchoada",
            "Pack de Palhetas",
            "Capotraste",
            "Banco para Teclado",
        ],
    },
    "roupas": {
        "camisetas": [
            "Camiseta Vintage Band",
            "Camiseta Oversized Studio",
            "Camiseta Minimal Sound",
            "Camiseta Washed Guitar Club",
            "Camiseta Analog Dreams",
        ],
        "moletons": [
            "Moletom Classic Amp",
            "Moletom Oversized Vinyl",
            "Moletom Heavy Cotton Session",
            "Moletom Midnight Rehearsal",
        ],
        "jaquetas": [
            "Jaqueta Denim Black",
            "Jaqueta Canvas Studio",
            "Jaqueta Bomber Midnight",
            "Jaqueta Workwear Session",
        ],
        "bones": [
            "Boné Dad Hat Records",
            "Boné Trucker Vintage Tone",
            "Boné Canvas Session",
            "Boné Studio Crew",
        ],
    },
}

MARCAS_INSTRUMENTOS = [
    "Fender",
    "Gibson",
    "Ibanez",
    "Yamaha",
    "Roland",
    "Boss",
    "Squier",
    "Epiphone",
    "PRS",
    "Tagima",
    "Condor",
    "Cort",
    "Jackson",
    "Gretsch",
    "Pearl",
    "Casio",
    "Korg",
]

MARCAS_ACESSORIOS = [
    "Boss",
    "MXR",
    "TC Electronic",
    "Focusrite",
    "Audio-Technica",
    "Shure",
    "AKG",
    "Hercules",
    "Ernie Ball",
    "D'Addario",
    "Planet Waves",
    "Behringer",
    "M-Audio",
]

MARCAS_ROUPAS = [
    "Studio North",
    "Midnight Noise",
    "Vinyl Supply",
    "Broken Strings Co.",
    "Analog Club",
    "Tape Echo Wear",
    "Loft Sessions",
    "Urban Tone",
    "Velvet Signal",
    "Late Night Label",
]

CORES = [
    "preto",
    "branco",
    "off_white",
    "sunburst",
    "natural",
    "walnut",
    "azul_marinho",
    "vermelho_vinho",
    "cinza",
    "verde_oliva",
    "creme",
    "rosa_claro",
    "prata",
    "dourado",
    "amber",
    "terracota",
]

TAGS_BASE = [
    "musica",
    "lifestyle",
    "vintage",
    "premium",
    "studio",
    "ao_vivo",
    "minimalista",
    "urbano",
    "artista",
    "indie",
    "retro",
    "essencial",
    "tour",
    "analogico",
    "palco",
    "ensaio",
]

MATERIAIS_INSTRUMENTOS = [
    "alder",
    "mahogany",
    "maple",
    "rosewood",
    "spruce",
    "basswood",
    "poplar",
    "ash",
]

MATERIAIS_ROUPAS = [
    "algodao",
    "algodao_premium",
    "moletom",
    "canvas",
    "denim",
    "fleece",
]

MATERIAIS_ACESSORIOS = [
    "aco",
    "aluminio",
    "couro",
    "nylon",
    "borracha",
    "latao",
    "silicone",
]

SERIES = [
    "Classic Series",
    "Studio Edition",
    "Vintage Line",
    "Midnight Collection",
    "Artist Choice",
    "Essential Series",
    "Road Session",
    "Modern Tone",
    "Heritage",
    "Signature Feel",
]

QUALIDADES = [
    "Premium",
    "Deluxe",
    "Custom",
    "Essential",
    "Pro",
    "Select",
    "Original",
]

VIBES = [
    "vintage",
    "minimalista",
    "indie",
    "urbana",
    "autoral",
    "moderna",
    "clássica",
    "lo-fi",
    "de estúdio",
    "de palco",
]

DESCRICOES_INSTRUMENTOS = [
    "Construção sólida, boa tocabilidade e um visual que conversa muito bem com estúdio, ensaio e palco.",
    "Modelo pensado para quem quer presença sonora, acabamento bonito e sensação confiável nas mãos.",
    "Entrega equilíbrio entre conforto, resposta dinâmica e uma estética inspirada em clássicos atemporais.",
    "Peça com personalidade forte, excelente para músicos que valorizam timbre, identidade visual e versatilidade.",
    "Combina inspiração tradicional com detalhes modernos, resultando em um instrumento expressivo e elegante.",
    "Foi desenvolvido para oferecer desempenho consistente, visual marcante e ótima adaptação a diferentes estilos.",
    "Tem pegada confortável, construção honesta e proposta sonora pronta para gravações, shows e estudos.",
    "Visual refinado e resposta musical muito equilibrada, com foco em tocabilidade e presença no mix.",
]

DESCRICOES_ACESSORIOS = [
    "Acessório confiável, com ótimo acabamento e proposta prática para rotina de estúdio, ensaio ou apresentação.",
    "Entrega uso simples, boa durabilidade e uma experiência consistente para quem vive o dia a dia musical.",
    "Foi pensado para resolver a rotina do músico sem complicação, mantendo visual limpo e construção segura.",
    "Une funcionalidade, resistência e estética discreta, ideal para setups modernos e organizados.",
    "Ótima escolha para quem procura desempenho estável, materiais sólidos e sensação profissional no uso diário.",
    "Tem proposta versátil, acabamento caprichado e encaixa muito bem em setups compactos ou mais completos.",
    "Ajuda a elevar a praticidade do setup com uma construção segura e foco real em uso recorrente.",
]

DESCRICOES_ROUPAS = [
    "Peça criada para quem gosta de vestir música também fora do palco, com caimento moderno e identidade forte.",
    "Visual casual com referência direta ao universo musical, ideal para rotina urbana, estúdio ou café depois do ensaio.",
    "Modelagem confortável, estética bem resolvida e clima autoral para quem prefere estilo com personalidade.",
    "Combina bem com looks criativos e discretos, trazendo uma energia de banda, fita cassete e noites de gravação.",
    "Tem proposta visual contemporânea, toque confortável e uma pegada artística que foge do óbvio.",
    "Foi pensada para unir conforto, presença e um imaginário musical mais indie, analógico e noturno.",
    "Roupa com personalidade, acabamento bonito e uma vibe perfeita para quem curte design, som e cidade.",
]

COMPLEMENTOS = [
    "É o tipo de produto que funciona muito bem tanto como peça principal quanto como parte de um setup mais completo.",
    "Conversa facilmente com uma estética retrô, sem perder praticidade no uso cotidiano.",
    "Tem aquele equilíbrio raro entre visual marcante e uso descomplicado.",
    "O resultado é um item expressivo, bonito e fácil de incorporar na rotina.",
    "A proposta aqui é entregar personalidade sem exagero, com um acabamento que chama atenção na medida certa.",
    "É uma opção que agrada tanto iniciantes exigentes quanto quem já tem um repertório visual e musical mais definido.",
    "Funciona especialmente bem para quem curte equipamentos e roupas com cara de curadoria, não só de catálogo.",
]

NARRATIVAS = [
    "Inspirado em sessões noturnas de gravação e no charme cru dos estúdios analógicos.",
    "Com referências de lojas de discos, amplificadores antigos e interiores industriais.",
    "Pensado para uma estética entre o palco pequeno, a cafeteria certa e o apartamento cheio de vinil.",
    "Uma leitura contemporânea do imaginário clássico de banda, turnê e fita demo.",
    "Com um pé no retrô e outro no uso moderno, sem cara de produto genérico.",
    "Feito para dialogar com uma cultura musical mais autoral, urbana e calorosa.",
]

ADJETIVOS_LOOK = [
    "elegante",
    "expressivo",
    "equilibrado",
    "discreto",
    "marcante",
    "versátil",
    "sofisticado",
    "autoral",
]

FAIXAS_PRECO = {
    "guitarras": (1800, 18000),
    "baixos": (1900, 15000),
    "violoes": (700, 10000),
    "teclados": (900, 17000),
    "bateria_percussao": (150, 6500),
    "pedais": (220, 2800),
    "audio": (280, 7800),
    "utilidades": (20, 1600),
    "camisetas": (69, 259),
    "moletons": (149, 499),
    "jaquetas": (219, 899),
    "bones": (79, 229),
}


def escolher_marca(grupo_principal: str) -> str:
    if grupo_principal == "instrumentos":
        return random.choice(MARCAS_INSTRUMENTOS)
    if grupo_principal == "acessorios":
        return random.choice(MARCAS_ACESSORIOS)
    return random.choice(MARCAS_ROUPAS)


def gerar_nome(tipo_produto: str, marca: str, cor: str) -> str:
    cor_fmt = cor.replace("_", " ").title()
    formato = random.choice(
        [
            "{tipo} {serie}",
            "{tipo} {qualidade} {serie}",
            "{tipo} {cor}",
            "{tipo} {qualidade}",
            "{tipo} {serie} {cor}",
        ]
    )
    return formato.format(
        tipo=tipo_produto,
        serie=random.choice(SERIES),
        qualidade=random.choice(QUALIDADES),
        cor=cor_fmt,
        marca=marca,
    )


def gerar_preco(subcategoria: str) -> float:
    minimo, maximo = FAIXAS_PRECO[subcategoria]
    return round(random.uniform(minimo, maximo), 2)


def gerar_rating() -> float:
    return round(random.uniform(3.6, 5.0), 1)


def gerar_created_at() -> str:
    dias_atras = random.randint(0, 900)
    horas_atras = random.randint(0, 23)
    minutos_atras = random.randint(0, 59)
    data = datetime.utcnow() - timedelta(
        days=dias_atras, hours=horas_atras, minutes=minutos_atras
    )
    return data.strftime("%Y-%m-%dT%H:%M:%S")


def gerar_tags(grupo_principal: str, subcategoria: str, cor: str) -> list[str]:
    tags = set(random.sample(TAGS_BASE, k=random.randint(3, 5)))
    tags.add(subcategoria)
    tags.add(grupo_principal)
    if cor in {"preto", "off_white", "branco", "sunburst", "natural"}:
        tags.add("best_seller")
    if grupo_principal == "roupas":
        tags.update(random.sample(["street", "casual", "band", "tour", "records"], k=2))
    elif grupo_principal == "instrumentos":
        tags.update(random.sample(["timbre", "palco", "gravação", "gear"], k=2))
    else:
        tags.update(random.sample(["setup", "cabo", "pedalboard", "acustica"], k=2))
    return sorted(tags)


def gerar_material(grupo_principal: str) -> str:
    if grupo_principal == "instrumentos":
        return random.choice(MATERIAIS_INSTRUMENTOS)
    if grupo_principal == "roupas":
        return random.choice(MATERIAIS_ROUPAS)
    return random.choice(MATERIAIS_ACESSORIOS)


def gerar_descricao(
    grupo_principal: str,
    tipo_produto: str,
    marca: str,
    cor: str,
    material: str,
) -> str:
    cor_txt = cor.replace("_", " ")
    material_txt = material.replace("_", " ")

    if grupo_principal == "instrumentos":
        base = random.choice(DESCRICOES_INSTRUMENTOS)
    elif grupo_principal == "acessorios":
        base = random.choice(DESCRICOES_ACESSORIOS)
    else:
        base = random.choice(DESCRICOES_ROUPAS)

    abertura = random.choice(
        [
            f"{tipo_produto} da {marca}",
            f"Produto {marca}",
            f"{tipo_produto} em destaque da {marca}",
            f"Peça da linha {marca}",
        ]
    )

    trecho_visual = random.choice(
        [
            f"Na cor {cor_txt}, tem visual {random.choice(ADJETIVOS_LOOK)} e acabamento em {material_txt}.",
            f"Com acabamento em {material_txt} e tonalidade {cor_txt}, transmite uma presença {random.choice(ADJETIVOS_LOOK)}.",
            f"O uso de {material_txt} combinado ao tom {cor_txt} reforça uma estética {random.choice(VIBES)}.",
        ]
    )

    narrativa = random.choice(NARRATIVAS)
    fechamento = random.choice(COMPLEMENTOS)

    return f"{abertura}. {trecho_visual} {base} {narrativa} {fechamento}"


def gerar_documento(seq: int) -> dict:
    grupo_principal = random.choice(list(CATEGORIAS.keys()))
    subcategoria = random.choice(list(CATEGORIAS[grupo_principal].keys()))
    tipo_produto = random.choice(CATEGORIAS[grupo_principal][subcategoria])

    marca = escolher_marca(grupo_principal)
    cor = random.choice(CORES)
    material = gerar_material(grupo_principal)
    nome = gerar_nome(tipo_produto, marca, cor)
    descricao = gerar_descricao(grupo_principal, tipo_produto, marca, cor, material)
    preco = gerar_preco(subcategoria)

    documento = {
        "id": f"P{seq:05d}-{uuid.uuid4().hex[:8].upper()}",
        "nome": nome,
        "descricao": descricao,
        "categoria": grupo_principal,
        "subcategoria": subcategoria,
        "marca": marca,
        "preco": preco,
        "emPromocao": random.random() < 0.28,
        "rating": gerar_rating(),
        "tags": gerar_tags(grupo_principal, subcategoria, cor),
        "cor": cor,
        "disponivel": random.random() < 0.93,
        "createdAt": gerar_created_at(),
    }
    return documento


def montar_bulk(docs: list[dict]) -> str:
    linhas = []
    for doc in docs:
        linhas.append(json.dumps({"index": {"_index": INDEX_NAME}}, ensure_ascii=False))
        linhas.append(json.dumps(doc, ensure_ascii=False))
    return "\n".join(linhas) + "\n"


def enviar_lote(sessao: requests.Session, docs: list[dict]) -> None:
    payload = montar_bulk(docs)
    response = sessao.post(
        f"{ES_URL}/_bulk",
        data=payload.encode("utf-8"),
        headers={"Content-Type": "application/x-ndjson"},
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    resultado = response.json()
    if resultado.get("errors"):
        erros = []
        for item in resultado.get("items", []):
            index_info = item.get("index", {})
            if "error" in index_info:
                erros.append(index_info["error"])
                if len(erros) >= 5:
                    break
        raise RuntimeError(f"Bulk retornou erros. Exemplos: {erros}")


def verificar_elasticsearch(sessao: requests.Session) -> None:
    response = sessao.get(ES_URL, timeout=TIMEOUT)
    response.raise_for_status()


def main() -> None:
    sessao = requests.Session()
    verificar_elasticsearch(sessao)

    enviados = 0
    lote = []

    for i in range(1, TOTAL_PRODUTOS + 1):
        lote.append(gerar_documento(i))

        if len(lote) >= BATCH_SIZE:
            enviar_lote(sessao, lote)
            enviados += len(lote)
            print(f"Lote enviado. Total acumulado: {enviados}/{TOTAL_PRODUTOS}")
            lote = []

    if lote:
        enviar_lote(sessao, lote)
        enviados += len(lote)
        print(f"Lote enviado. Total acumulado: {enviados}/{TOTAL_PRODUTOS}")

    print("Inserção concluída com sucesso.")


if __name__ == "__main__":
    main()