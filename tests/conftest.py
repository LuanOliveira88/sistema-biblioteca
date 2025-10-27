import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base


@pytest.fixture(scope="function")
def session():
    """Cria uma sessão de teste com SQLite em memória para cada teste."""
    engine = create_engine("sqlite:///:memory:", echo=False)

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
