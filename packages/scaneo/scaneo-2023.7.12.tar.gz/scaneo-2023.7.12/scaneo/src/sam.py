import rasterio as rio
import json
import os
from samgeo import SamGeo
import shutil

from .image.image_utils import to_uint8

sam = None


def generate_mask(storage, image_name, bands, points, pointsLabel, label):
    image_url = storage.get_url(image_name)
    # sam temporary files
    sam_tmp_folder = "/tmp/sam/"
    os.makedirs(sam_tmp_folder, exist_ok=True)
    image_name = os.path.splitext(image_name)[0]
    rgb_file = sam_tmp_folder + "rgb" + "_" + image_name + ".tif"
    mask_tif_file = sam_tmp_folder + "mask" + "_" + image_name + ".tif"
    mask_geojson_file = sam_tmp_folder + "mask" + "_" + image_name + ".geojson"
    # generate RGB image
    red = int(bands["bands"]["red"])
    green = int(bands["bands"]["green"])
    blue = int(bands["bands"]["blue"])
    stretch_maximum = int(bands["stretch"]["maximum"])
    stretch_minimum = int(bands["stretch"]["minimum"])
    ds = rio.open(image_url)
    bands = ds.read((red, green, blue))
    rgb = to_uint8(bands, stretch_minimum, stretch_maximum)
    # save RGB as local tif
    profile = ds.profile
    profile.update(count=3, dtype="uint8")
    if not os.path.exists(rgb_file):
        with rio.open(rgb_file, "w", **profile) as dst:
            dst.write(rgb)
    # generate mask
    global sam
    if sam is None:
        sam = SamGeo(
            checkpoint="sam_vit_h_4b8939.pth",
            model_type="vit_h",
            automatic=False,
            sam_kwargs=None,
        )
    sam.set_image(rgb_file)
    sam.predict(
        points,
        point_labels=pointsLabel,
        point_crs="EPSG:4326",  # validar ???
        output=mask_tif_file,
    )
    sam.raster_to_vector(
        mask_tif_file,
        mask_geojson_file,
    )
    # adapt reponse to the format expected by the front-end
    with open(mask_geojson_file, "r") as f:
        geojson_data = json.load(f)
    geometries = []
    for feature in geojson_data["features"]:
        geometries.append(feature["geometry"]["coordinates"])
    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "MultiPolygon", "coordinates": geometries},
                "properties": {"label": label},
            }
        ],
    }
    prompt_object = {"type": "FeatureCollection", "features": []}
    for i, point in enumerate(points):
        prompt_object["features"].append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [point[0], point[1]]},
                "properties": {
                    "label": label,
                    "background": pointsLabel[i],
                },
            }
        )
    shutil.rmtree(sam_tmp_folder)
    # save prompts
    storage.save(image_name + "_prompts.geojson", json.dumps(prompt_object))
    return geojson_data
