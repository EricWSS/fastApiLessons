from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnector://u274908554_710A:INbd710A@sql812.main-hosting.eu/u274908554_710A"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Testa conexões antes de usá-las.
    pool_recycle=1800,   # Fecha conexões inativas após 30 minutos.
    pool_size=5,         # Número máximo de conexões no pool.
    max_overflow=10      # Conexões extras além do pool.
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        db.rollback()  # Garante que não haja transações pendentes
        raise e
    finally:
        db.close()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
