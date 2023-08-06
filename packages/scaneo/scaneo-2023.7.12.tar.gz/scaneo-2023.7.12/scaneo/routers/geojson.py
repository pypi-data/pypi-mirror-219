from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import os

from src.storage import Storage

router = APIRouter(prefix="/geojson", tags=["geojson"])


class GeoJSONFeature(BaseModel):
    type: str
    geometry: dict
    properties: dict


class GeoJSON(BaseModel):
    type: str
    features: List[GeoJSONFeature]


class Body(BaseModel):
    name: str
    geojson: GeoJSON


@router.post("")
def save_geojson(
    body: Body,
):
    try:
        storage = Storage()
        # sam_path = data + "/sam/"
        # prompts_geojson_file = sam_path + "prompts" + "_" + file_name + ".geojson"
        storage.save(
            os.path.splitext(body.name)[0] + ".geojson",
            body.geojson.json(),
        )
        # if os.path.isfile(prompts_geojson_file):
        #     shutil.copy(prompts_geojson_file, data)
        return {
            "status": "201 Created",
            "geojson": body.geojson,
            "imageName": body.name,
        }

    except Exception as e:
        print("error geojson:save_geojson", e)
        return HTTPException(status_code=500, detail="Could not save geojson")


@router.get("/{name}")
def get_geojson(name: str):
    try:
        storage = Storage()
        file_name = os.path.splitext(name)[0] + ".geojson"
        return storage.read(file_name)
    except Exception as e:
        print("error geojson:get_geojson", e)
        return HTTPException(status_code=500, detail="Could not get geojson")
