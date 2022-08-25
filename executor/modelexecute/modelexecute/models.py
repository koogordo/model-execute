from sqlalchemy import Column, String, DateTime, Enum, BigInteger, ForeignKey, Integer
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()


class Model(Base):
    __tablename__ = 'model'
    id = Column(UUID(as_uuid=True),
                primary_key=True, default=uuid.uuid4, unique=True)
    name = Column(String(150), unique=True, nullable=False)
    artifacts = Column(String(250), nullable=False)
    file_name = Column(String(75), nullable=False)
    predict_method = Column(String(50), nullable=False)
    status = Column(Enum('ONLINE', 'OFFLINE',
                                   name='model_status'), nullable=False)
    created_at = Column(DateTime(
        timezone=False), server_default=func.now())
    updated_at = Column(DateTime(
        timezone=False), onupdate=func.now())


class Run(Base):
    __tablename__ = 'run'
    id = Column(UUID(as_uuid=True),
                primary_key=True, default=uuid.uuid4, unique=True)
    model_name = Column(String(250), nullable=False)
    input = Column(String(500), nullable=False)
    max_partition_size = Column(BigInteger, nullable=False)
    tasks = relationship(
        'RunTask', back_populates="run", cascade="all, delete-orphan", order_by=lambda: RunTask.partition_num)
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
    beginning_offset = Column(BigInteger, nullable=True)
    ending_offset = Column(BigInteger, nullable=True)
    output = Column(String(500), nullable=True)
    partition_num = Column(Integer, nullable=False)
    status = Column(Enum('SCHEDULED', 'RUNNING', 'FAILED',
                         'SUCCESS', 'PARTITIONING', name='task_status'), nullable=True)
    created_at = Column(DateTime(
        timezone=False), server_default=func.now())
    updated_at = Column(DateTime(
        timezone=False), onupdate=func.now())
