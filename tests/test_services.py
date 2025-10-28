import pytest

from src.errors import BusinessRuleError
from src.models import Exemplar, Livro


@pytest.mark.services
class TestBibliotecaService:
    """Testes para a camada de serviço da biblioteca."""

    def test_cadastrar_livro_cria_livro_e_exemplar(self, biblioteca_service, session):
        """Deve cadastrar um novo livro e criar exemplares associados."""
        response = biblioteca_service.cadastrar_livro(
            titulo='Dom Casmurro',
            autor='Machado de Assis',
            isbn='12345',
            ano_publicacao=1899,
            n_exemplares=2,
        )

        assert response.success is True
        assert response.message == 'Livro cadastrado com sucesso'
        assert response.data.titulo == 'Dom Casmurro'

        livros = session.query(Livro).all()
        exemplares = session.query(Exemplar).all()
        assert len(livros) == 1
        assert len(exemplares) == 2

    def test_cadastrar_livro_existente(self, biblioteca_service):
        """Deve retornar mensagem de livro já existente ao cadastrar ISBN repetido."""
        biblioteca_service.cadastrar_livro(
            titulo='Dom Casmurro',
            autor='Machado de Assis',
            isbn='12345',
            ano_publicacao=1899,
        )

        response = biblioteca_service.cadastrar_livro(
            titulo='Dom Casmurro',
            autor='Machado de Assis',
            isbn='12345',
            ano_publicacao=1899,
        )

        assert response.success is True
        assert response.message == 'Livro já existente.'

    def test_cadastrar_livro_quantidade_invalida(self, biblioteca_service):
        """Deve levantar BusinessRuleError se n_exemplares <= 0."""
        with pytest.raises(BusinessRuleError) as exc_info:
            biblioteca_service.cadastrar_livro(
                titulo='Memórias Póstumas',
                autor='Machado de Assis',
                isbn='987654321',
                ano_publicacao=1881,
                n_exemplares=0,
            )

        assert 'quantidade de exemplares' in str(exc_info.value).lower()
