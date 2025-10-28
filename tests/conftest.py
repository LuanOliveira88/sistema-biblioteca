import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base
from src.services import BibliotecaService, DatabaseService


@pytest.fixture
def session():
    """Cria uma sessão de teste com SQLite em memória para cada teste."""
    engine = create_engine('sqlite:///:memory:', echo=False)

    # Agora todas as classes já estão carregadas, Base conhece os mapeamentos
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    db_session = Session()

    yield db_session

    try:
        db_session.rollback()
    except Exception:
        pass
    finally:
        db_session.close()


@pytest.fixture
def db_service(session):
    """Fornece um DatabaseService configurado para testes."""
    service = DatabaseService(engine=session.bind)
    return service


@pytest.fixture
def biblioteca_service(db_service):
    """Retorna uma instância de BibliotecaService com dependência injetada."""
    return BibliotecaService(db_service)
