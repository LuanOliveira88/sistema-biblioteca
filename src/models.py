from datetime import date
from enum import Enum

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase, MappedAsDataclass):
    """
    Class base para o tipo de mapeamento dos atributos pelo ORM
    """


class StatusExemplar(Enum):
    DISPONIVEL = 'disponivel'
    EMPRESTADO = 'emprestado'
    ATRASADO = 'atrasado'


class Livro(Base):
    __tablename__ = 'livros'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    titulo: Mapped[str]
    autor: Mapped[str]
    isbn: Mapped[str]
    ano_publicacao: Mapped[int]

    def to_dict(self):
        return {
            'titulo': self.titulo,
            'autor': self.autor,
            'isbn': self.isbn,
            'ano_publicacao': self.ano_publicacao,
        }


class Exemplar(Base):
    __tablename__ = 'exemplares'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    livro_id: Mapped[int] = mapped_column(ForeignKey('livros.id'))
    livro: Mapped[Livro] = relationship('Livro', backref='exemplares', init=False)
    status: Mapped[StatusExemplar] = mapped_column(
        SQLEnum(StatusExemplar), default=StatusExemplar.DISPONIVEL
    )


class TipoUsuario(Enum):
    ESTUDANTE = 'estudante'
    PROFESSOR = 'professor'


class Usuario(Base):
    __tablename__ = 'usuarios'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    nome: Mapped[str]
    email: Mapped[str]
    tipo: Mapped[TipoUsuario] = mapped_column(SQLEnum(TipoUsuario))


class StatusEmprestimo(Enum):
    PENDENTE = 'pendente'
    DEVOLVIDO = 'devolvido'
    ATRASADO = 'atrasado'


class Emprestimo(Base):
    __tablename__ = 'emprestimos'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    data_inicio: Mapped[date]
    data_devolucao: Mapped[date]
    status: Mapped[StatusEmprestimo] = mapped_column(
        SQLEnum(StatusEmprestimo), default=StatusEmprestimo.PENDENTE, init=False
    )
    usuario_id: Mapped[int] = mapped_column(ForeignKey('usuarios.id'), init=False)
    usuario: Mapped[Usuario] = relationship('Usuario', backref='emprestimo')

    exemplares: Mapped[list[Exemplar]] = relationship(
        'Exemplar', secondary='emprestimo_exemplares', backref='emprestimos', init=False
    )

    def __post_init__(self):
        if self.data_inicio == self.data_devolucao:
            raise ValueError(
                'A data de empréstimo deve ser diferente da data de devolução.'
            )

        if self.data_devolucao < self.data_inicio:
            raise ValueError(
                'A data de empréstimo deve ser anterior a data de devolução.'
            )

        if self.usuario.tipo == TipoUsuario.ESTUDANTE and len(self.exemplares) > 3:
            raise ValueError(
                'Estudantes só podem pegar no máximo 3 livros emprestados '
                'simultaneamente.'
            )

        if self.usuario.tipo == TipoUsuario.PROFESSOR and len(self.exemplares) > 5:
            raise ValueError(
                'Professores só podem pegar no máximo 5 livros emprestados '
                'simultaneamente.'
            )


class EmprestimoExemplar(Base):
    __tablename__ = 'emprestimo_exemplares'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    emprestimo_id: Mapped[int] = mapped_column(ForeignKey('emprestimos.id'))
    exemplar_id: Mapped[int] = mapped_column(ForeignKey('exemplares.id'))
