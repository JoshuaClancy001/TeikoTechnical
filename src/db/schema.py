import argparse
import os

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.environ.get("DB_PATH", os.path.join(_ROOT, "data", "clinical_trial.db"))
DB_URL = f"sqlite:///{DB_PATH}"


class Base(DeclarativeBase):
    pass


class Subject(Base):
    """One row per patient."""

    __tablename__ = "subjects"

    subject_id = Column(String(50), primary_key=True)
    project = Column(String(100))
    condition = Column(String(100))
    age = Column(Integer)
    sex = Column(String(10))       # "M" | "F"
    treatment = Column(String(100))
    response = Column(String(50))  # e.g. "yes" | "no" | ""(empty)

class Sample(Base):
    """One row per biological sample / timepoint."""

    __tablename__ = "samples"

    sample_id = Column(String(50), primary_key=True)
    subject_id = Column(String(50), ForeignKey("subjects.subject_id"), nullable=False)
    sample_type = Column(String(100))
    time_from_treatment_start = Column(Integer)  # days


class CellCount(Base):
    """One row per immune population measurement."""

    __tablename__ = "cell_counts"

    id = Column(Integer, primary_key=True)
    sample_id = Column(String(50), ForeignKey("samples.sample_id"), nullable=False)
    population = Column(String(100), nullable=False)
    count = Column(Integer, nullable=False)


def create_schema(db_url: str = DB_URL, *, drop_existing: bool = False) -> None:
    db_file = db_url.replace("sqlite:///", "")
    if db_file:
        os.makedirs(os.path.dirname(db_file) or ".", exist_ok=True)
    engine = create_engine(db_url, echo=False)
    if drop_existing:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print(f"Schema created: {db_url}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialise the clinical trial database.")
    parser.add_argument("--reset", action="store_true", help="Drop and recreate all tables.")
    parser.add_argument("--db-url", default=DB_URL, help="SQLAlchemy database URL.")
    args = parser.parse_args()
    create_schema(args.db_url, drop_existing=args.reset)
