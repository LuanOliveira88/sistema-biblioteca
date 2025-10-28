from contextlib import contextmanager
from typing import Optional

from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import Session

from src.dtos import LivroDTO, ResponseDTO
from src.errors import BusinessRuleError
from src.models import (
    Base,
    Exemplar,
    Livro,
)
from src.utils import get_current_args


class DatabaseService:
    def __init__(self, engine: Optional[Engine] = None):
        self.engine = engine or create_engine('sqlite:///biblioteca.db')

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    @contextmanager
    def session_scope(self):
        session = Session(self.engine)

        try:
            yield session
            session.commit()

        except:
            session.rollback()
            raise
        finally:
            session.close()


class BibliotecaService:
    def __init__(self, db_service: DatabaseService):
        self.db = db_service
        self.db.create_tables()

    def cadastrar_livro(
        self,
        titulo: str,
        autor: str,
        isbn: str,
        ano_publicacao: int,
        n_exemplares: int = 1,
    ) -> ResponseDTO:
        """
        Cadastra novo livro no sistema.

        Atende ao requisito funcional RF01.

        Args:
            titulo: Título do livro
            autor: Autor do livro
            isbn: Código ISBN
            ano_publicacao: Ano de publicação da obra
            n_exemplares: Número de exemplares que serão cadastrados (o default é 1)

        Return:
            livro: objeto
        """

        # validação de quantidade de exemplares
        if n_exemplares <= 0:
            raise BusinessRuleError(
                'A quantidade de exemplares deve ser um número inteiro positivo não '
                'nulo.'
            )

        with self.db.session_scope() as session:
            livro = session.query(Livro).filter(Livro.isbn == isbn).first()

            if not livro:
                dict_args = get_current_args()
                dict_args.pop('self')
                dict_args.pop('n_exemplares')
                livro = Livro(**dict_args)
                session.add(livro)
                session.flush()
                message = 'Livro cadastrado com sucesso'

            else:
                message = 'Livro já existente.'

            exemplares_lista = [
                Exemplar(livro_id=livro.id) for _ in range(n_exemplares)
            ]
            session.add_all(exemplares_lista)

            livro_dto = LivroDTO.model_validate(livro)

            return ResponseDTO(success=True, message=message, data=livro_dto)
