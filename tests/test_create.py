from sqlmodel import Session, create_engine
from app.models import SQLModel, String, Payload
from app.views import create_transformed_string, get_transformed_string, create_payload, get_payload
from app.utils import transform_string


DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)

def test_transformed_string():
    with Session(engine) as session:
        original_text = "test"
        transformed_text = transform_string(original_text)

        create_transformed_string(session, original_text, transformed_text)
        fetched = get_transformed_string(session, original_text)

        assert fetched is not None
        assert fetched.transformed == "TEST"

def test_payload():
    with Session(engine) as session:
        output_text = "TEST STRING, ANOTHER STRING"

        created_payload = create_payload(session, output_text)
        fetched_payload = get_payload(session, output_text)

        assert fetched_payload is not None
        assert created_payload.id == fetched_payload.id
