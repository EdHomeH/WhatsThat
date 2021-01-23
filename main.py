from fastapi import FastAPI, File, UploadFile
from google.cloud import vision

app = FastAPI()


@app.post("/detect_image/")
async def detect_image(image: bytes = File(...)):
    return {"image_size": len(image), \
            "result": localize_objects(image)}


def localize_objects(image_file):
    
    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=image_file)

    objects = client.object_localization( # pylint: disable=no-member
        image=image).localized_object_annotations

    result = {'Number of objects found': f'{len(objects)}'}

    for object_ in objects:
        result[f'{object_.name}'] = {'confidence':f'{object_.score}'}
        result[f'{object_.name}']['vertices']=list()
        for vertex in object_.bounding_poly.normalized_vertices:
            result[f'{object_.name}']['vertices'].append((vertex.x, vertex.y))

    return result