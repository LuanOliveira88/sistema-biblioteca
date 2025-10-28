"""Módulo de testes dos modelos"""

from datetime import date

import pytest

from src.models import Emprestimo, Exemplar, Livro, TipoUsuario, Usuario


@pytest.mark.models
class TestModels:
    """Testes para os modelos do banco de dados: Livro, Exemplar e Emprestimo."""

    def test_livro_criacao(self, session):
        """Testa a criação de um objeto Livro e sua persistência no banco."""
        livro = Livro(
            titulo='Dom Casmurro',
            autor='Machado de Assis',
            isbn='12345',
            ano_publicacao=1899,
        )
        session.add(livro)
        session.commit()
        assert livro.id is not None

    def test_exemplar_criacao(self, session):
        """Testa a criação de um objeto Exemplar vinculado a um Livro."""
        livro = Livro(
            titulo='Dom Casmurro',
            autor='Machado de Assis',
            isbn='12345',
            ano_publicacao=1899,
        )
        session.add(livro)
        session.commit()
        exemplar = Exemplar(livro_id=livro.id)
        session.add(exemplar)
        session.commit()
        assert exemplar.id is not None
        assert exemplar.livro_id == livro.id

    def test_emprestimo_criacao(self, session):
        """Testa a criação de um objeto Emprestimo com Exemplares associados."""

        with session.no_autoflush:
            livro = Livro(
                titulo='Dom Casmurro',
                autor='Machado de Assis',
                isbn='12345',
                ano_publicacao=1899,
            )
            session.add(livro)
            session.commit()
            exemplar = Exemplar(livro_id=livro.id)
            session.add(exemplar)
            session.commit()
            usuario = Usuario(
                nome='José', email='jose@email.com', tipo=TipoUsuario.ESTUDANTE
            )
            session.add(usuario)
            session.commit()
            emprestimo = Emprestimo(
                data_inicio=date(2025, 11, 20),
                data_devolucao=date(2025, 12, 20),
                usuario=usuario,
            )
            emprestimo.exemplares.append(exemplar)
            session.add(emprestimo)
            session.commit()
            assert exemplar in emprestimo.exemplares

    def test_livro_to_dict(self):
        livro = Livro(
            titulo='Dom Casmurro',
            autor='Machado de Assis',
            isbn='12345',
            ano_publicacao=1899,
        )

        livro_dict = livro.to_dict()

        assert isinstance(livro_dict, dict)

        chaves_esperadas = {'titulo', 'autor', 'ano_publicacao', 'isbn'}

        assert set(livro_dict.keys()) == chaves_esperadas

        assert livro_dict['titulo'] == 'Dom Casmurro'
        assert livro_dict['autor'] == 'Machado de Assis'
        assert livro_dict['isbn'] == '12345'
        assert livro_dict['ano_publicacao'] == 1899
