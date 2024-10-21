import pytest
from main import search_diaries, handle_hash_md5

def test_search_diaries_valid_date():
    publication_date = "2024-10-04"
    
    url = search_diaries(publication_date, "https://www.tjro.jus.br/diario_oficial/")
    print(url)

    assert url is not None, "A URL do PDF não deve ser None para uma data válida."
    assert url.startswith('https://www.tjro.jus.br/novodiario'), "A URL do PDF deve começar com o domínio correto."


def test_handle_hash_md5():
    publication_date = "2024-10-04"
    
    url = search_diaries(publication_date, "https://www.tjro.jus.br/diario_oficial/")

    if url:
        hash_md5 = handle_hash_md5(url)
        assert hash_md5 is not None, "O hash MD5 não deve ser None após o download do PDF."
        assert len(hash_md5) == 32, "O hash MD5 deve ter 32 caracteres."
    else:
        pytest.fail("URL não encontrada para a data fornecida.")


def test_search_diaries_invalid_date():
    publication_date = "2024-01-01"
    url = search_diaries(publication_date, "https://www.tjro.jus.br/diario_oficial/")

    assert url is None, "A URL do PDF deve ser None para uma data inválida."
