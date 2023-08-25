import contextlib

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


# db 세션 객체를 리턴하는 제너레이터 함수 추가
# @contextlib.contextmanager # 해당 어노테이션을 적용했기 때문에 사용 시 with 문과 함께 사용할 수 있다.
# -> fastapi의 Depends 적용 시 이미 해당 어노테이션이 구성되어 있기 때문에 삭제해야 오류가 안남
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()