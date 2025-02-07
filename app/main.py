from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session

from .database import init_db, get_session
from .models import Payload
from .schemas import PayloadRequest, PayloadResponse
from .views import get_transformed_string, create_transformed_string, get_payload, create_payload
from .utils import transform_string

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/payload", response_model=PayloadResponse)
def create_payload_api(payload_request: PayloadRequest, session: Session = Depends(get_session)):
   
    transformed_list_1 = []
    transformed_list_2 = []

    for text in payload_request.list_1:
        cached = get_transformed_string(session, text)
        transformed_list_1.append(cached.transformed if cached else create_transformed_string(
            session, text, transform_string(text)).transformed)

    for text in payload_request.list_2:
        cached = get_transformed_string(session, text)
        transformed_list_2.append(cached.transformed if cached else create_transformed_string(
            session, text, transform_string(text)).transformed)

    interleaved_output = \
    ", ".join([val for pair in zip(transformed_list_1, transformed_list_2) for val in pair])

    existing_payload = get_payload(session, interleaved_output)
    if existing_payload:
        return PayloadResponse(id=existing_payload.id, output=existing_payload.output)

    new_payload = create_payload(session, interleaved_output)
    return PayloadResponse(id=new_payload.id, output=new_payload.output)


@app.get("/payload/{payload_id}", response_model=PayloadResponse)
def get_payload_api(payload_id: str, session: Session = Depends(get_session)):
    payload = session.get(Payload, payload_id)
    if not payload:
        raise HTTPException(status_code=404, detail="Payload not found")
    return PayloadResponse(id=payload.id, output=payload.output)
