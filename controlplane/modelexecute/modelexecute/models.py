from sqlalchemy import Column, String, DateTime, Enum, BigInteger, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()


class Model(Base):
    __tablename__ = 'model'
    id = Column('id', UUID(as_uuid=True),
                primary_key=True, default=uuid.uuid4, unique=True)
    name = Column('name', String(150), unique=True, nullable=False)
    artifacts = Column('artifacts', String(250), nullable=False)
    file_name = Column('file_name', String(75), nullable=False)
    predict_method = Column('predict_method', String(50), nullable=False)
    status = Column('status', Enum('ONLINE', 'OFFLINE',
                                   name='model_status'), nullable=False)
    created_at = Column('created_at', DateTime(
        timezone=False), server_default=func.now())
    udpated_at = Column('updated_at', DateTime(
        timezone=False), onupdate=func.now())


class Run(Base):
    __tablename__ = 'run'
    id = Column(UUID(as_uuid=True),
                primary_key=True, default=uuid.uuid4, unique=True)
    model_name = Column(String(250), nullable=False)
    input = Column(String(500), nullable=False)
    tasks = relationship(
        'RunTask', back_populates="run", cascade="all, delete-orphan")
    created_at = Column(DateTime(
        timezone=False), server_default=func.now())
    status = Column(Enum('STARTED', 'RUNNING', 'FAILED',
                         'SUCCESS', name='run_status'), nullable=True)
    updated_at = Column(DateTime(
        timezone=False), onupdate=func.now())


class RunTask(Base):
    __tablename__ = 'run_task'
    id = Column(UUID(as_uuid=True),
                primary_key=True, default=uuid.uuid4, unique=True)
    run_id = Column(UUID(as_uuid=True), ForeignKey(
        'run.id'), nullable=False)
    run = relationship('Run', back_populates='tasks')
    offset = Column(BigInteger, nullable=False)
    length = Column(BigInteger, nullable=False)
    output = Column(String(500), nullable=True)
    status = Column(Enum('SCHEDULED', 'RUNNING', 'FAILED',
                         'SUCCESS', name='task_status'), nullable=True)
    created_at = Column(DateTime(
        timezone=False), server_default=func.now())
    updated_at = Column(DateTime(
        timezone=False), onupdate=func.now())
