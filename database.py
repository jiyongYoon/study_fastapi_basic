from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./fastapi.db"

# 커넥션 풀 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# db에 접속하기 위해 필요한 클래스
SessionLocal = sessionmaker(
    # autocommit 사용 안함.
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 데이터베이스 모델을 구성할 때 사용할 클래스
Base = declarative_base()