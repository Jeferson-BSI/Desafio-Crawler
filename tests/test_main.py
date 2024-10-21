import pytest

from diaries_crawler.crawler import DiaryCrawler
from diaries_crawler.hash_md5 import HashMd5Handle


def test_search_diaries_valid_date():
    publication_date = "2024-10-04"
    crawler = DiaryCrawler("https://www.tjro.jus.br/diario_oficial/")
    url = crawler.run(publication_date)
    
    print(url)

    assert url is not None, "A URL do PDF não deve ser None para uma data válida."
    assert url.startswith('https://www.tjro.jus.br/novodiario'), "A URL do PDF deve começar com o domínio correto."


def test_handle_hash_md5():
    publication_date = "2024-10-04"
    
    crawler = DiaryCrawler("https://www.tjro.jus.br/diario_oficial/")
    url = crawler.run(publication_date)

    md5 = HashMd5Handle()

    if url:
        hash_md5 = md5.run(url)

        assert hash_md5 is not None, "O hash MD5 não deve ser None após o download do PDF."
        assert len(hash_md5) == 32, "O hash MD5 deve ter 32 caracteres."
    else:
        pytest.fail("URL não encontrada para a data fornecida.")


def test_search_diaries_invalid_date():
    publication_date = "2024-01-01"

    crawler = DiaryCrawler("https://www.tjro.jus.br/diario_oficial/")
    url = crawler.run(publication_date)

    assert url is None, "A URL do PDF deve ser None para uma data inválida."
