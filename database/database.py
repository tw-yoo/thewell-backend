# 필요한 라이브러리 import하기
import subprocess

from sqlalchemy import create_engine, text, inspect, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# SQLAlchemy 사용할 DB URL 생성하기
# SQLALCHEMY_DATABASE_URL = "postgresql://localhost:5432/postgres"
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres@localhost:5432/postgres"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# SQLAlchemy engine 생성하기
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# Create a sessionmaker for database interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_db_and_tables():
    Base.metadata.create_all(engine)


def generate_revision():
    try:
        print("Generating Alembic revision...")
        subprocess.run(["alembic", "revision", "--autogenerate", "-m", "Auto revision"], check=True, capture_output=True, text=True)
        print("Alembic revision generated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error generating revision: {e}")
        raise e


def run_migrations():
    try:
        print("Running Alembic migrations...")
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("Alembic migrations applied successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running migrations: {e}")
        raise e




def is_latest_migration_applied():
    try:
        with engine.connect() as connection:
            # Query the alembic_version table to get the current version
            result = connection.execute(text("SELECT version_num FROM alembic_version"))
            version = result.scalar()  # Fetch the latest version number
            return version is not None  # If there's a version number, migrations have been applied
    except Exception as e:
        print(f"Error querying Alembic version: {e}")
        return False  # If the table doesn't exist, migrations haven't been run


def check_model_changes():
    """
    Checks for differences between the current models and the database schema.
    If differences are found, a migration will be triggered.
    """
    inspector = inspect(engine)
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Check if any of the tables or columns differ
    model_tables = Base.metadata.tables
    db_tables = inspector.get_table_names()

    for table_name in model_tables:
        if table_name not in db_tables:
            return True  # New table found, migration needed

        model_columns = model_tables[table_name].columns.keys()
        db_columns = [col['name'] for col in inspector.get_columns(table_name)]

        # Check if columns in model and database differ
        if set(model_columns) != set(db_columns):
            return True  # Columns differ, migration needed

    return False  # No differences found


def run_alembic_migration():
    """
    Runs alembic revision and upgrade if a schema change is detected.
    """
    if check_model_changes():
        try:
            print("Generating migration script...")
            # Generate alembic migration script
            result = subprocess.run(
                ["alembic", "revision", "--autogenerate", "-m", "Auto migration"],
                check=True,
                capture_output=True,  # Capture output
                text=True  # Output as text
            )
            print(result.stdout)  # Print stdout (success output)
            print(result.stderr)  # Print stderr (error output)

            print("Applying migration...")
            # Apply the migration
            result = subprocess.run(
                ["alembic", "upgrade", "head"],
                check=True,
                capture_output=True,  # Capture output
                text=True  # Output as text
            )
            print(result.stdout)  # Print stdout (success output)
            print(result.stderr)  # Print stderr (error output)

            print("Migration applied successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error during migration: {e}")
            print(e.stderr)  # Print the stderr from the command
    else:
        print("No model changes detected. Skipping migration.")
