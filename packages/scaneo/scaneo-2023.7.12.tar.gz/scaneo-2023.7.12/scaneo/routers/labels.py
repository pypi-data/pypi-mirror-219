from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from src.storage import Storage

router = APIRouter(prefix="/labels", tags=["labels"])


class Body(BaseModel):
    labels: list


@router.post("")
def save_labels(body: Body):
    try:
        storage = Storage()
        storage.save("labels.json", body.json())
        return {"status": "201 Created", "labels": body.labels}
    except Exception as e:
        print("error labels:save_labels", e)
        return HTTPException(status_code=500, detail="Could not save new label")


@router.get("")
def get_labels():
    try:
        storage = Storage()
        labels_file = "labels.json"
        if storage.exists(labels_file):
            return storage.read(labels_file)
        return HTTPException(status_code=404, detail="Labels file not found")
    except Exception as e:
        print("error labels:get_labels", e)
        return HTTPException(status_code=500, detail="Could not get labels")
