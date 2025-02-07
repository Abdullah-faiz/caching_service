from sqlmodel import Session, select

from .models import TransformedString, Payload

def get_transformed_string(session: Session, original: str):
    return session.exec(select(TransformedString).where(TransformedString.original == original)).first()

def create_transformed_string(session: Session, original: str, transformed: str):
    transformed_string = TransformedString(original=original, transformed=transformed)
    session.add(transformed_string)
    session.commit()
    return transformed_string

def get_payload(session: Session, output: str):
    return session.exec(select(Payload).where(Payload.output == output)).first()

def create_payload(session: Session, output: str):
    payload = Payload(output=output)
    session.add(payload)
    session.commit()
    return payload
