""" Script para obtener el conjunto de imágenes que forman
el dataset para aplicar transfer-learning a los modelos predefinidos
en keras.


- selección de características por capa en un servicio propio de WMS

"""
import csv
import json
import os
import requests
import sys

sys.path.append(str(os.path.basename('../../')))
from src.settings import models_settings

# Globals
URL_MAIN_SENTINEL = "https://services.sentinel-hub.com"
URL_UWEST_SENTINEL = "https://services-uswest2.sentinel-hub.com"
WMS_SERVICE = "/ogc/wms"
FIS_SERVICE = "/ogc/fis"
DATES = ["2019-05-12","2019-06-01","2019-06-26","2019-07-06","2019-07-11","2019-07-16","2019-07-21","2019-08-05","2019-08-10","2019-08-15","2019-08-25","2019-08-30","2019-09-04","2019-09-19","2019-09-29","2019-10-04","2019-10-09","2019-10-14","2019-10-19"]
WMS_MAIN_SERVICE = f"{URL_MAIN_SENTINEL}{WMS_SERVICE}"
WMS_UWEST_SERVICE = f"{URL_UWEST_SENTINEL}{WMS_SERVICE}"
WMS_BASIC_ID = "241431ed-6892-4075-ba38-8eaec8369cc2" # necesario crear una cuenta en Sentinel
WMS_RADIATION_ID = "6a48e3ac-d650-45b7-ab45-8f4e15779dc6" # necesario crear una cuenta en Sentinel
GEOMETRY = "0103000000010000000c0000001c739bf9e023454001b196af89e40ec07018d4d0e923454080f800a5ede40ec054bc1807ef2345400100000d1ae70ec0844c28131a24454001000038a2e80ec0d89357b42c24454000000004c6e90ec03cf7337b5a244540ffffffabf4e50ec0b4aafced55244540fdffff0b68e50ec08c188cd34c244540feffff5301e60ec00c9690862c244540fffffff1ebe40ec0803644a52924454080249e004be50ec0142b1f59eb2345400054c0dd5ce30ec01c739bf9e023454001b196af89e40ec0"
BBOX = "42.28030319299998%2C-3.8641472160816193%2C42.28401126897231%2C-3.861016972000016"
WIDTH = 50
HEIGHT = 80
IMAGE_FORMAT = ["image/png"]

QUERY = f"?geometry={GEOMETRY}&bbox={BBOX}&width={WIDTH}&height={HEIGHT}&request=GetMap&crs=EPSG:4326"
QUERY_WMS = QUERY + "&time={date}&layers={layers}&format={format}"
QUERY_FIS = QUERY + "&time={date}/{date}&layer={layer}"


DATA = [
    # NDVI
    {
        "url_wms": f"{URL_MAIN_SENTINEL}{WMS_SERVICE}/{WMS_BASIC_ID}",
        "url_fis": f"{URL_MAIN_SENTINEL}{FIS_SERVICE}/{WMS_BASIC_ID}",
        "layers_wms": "NDVI_COLOR",
        "layers_fis": "NDVI",
        "name": models_settings.FILES_FOLDER + "ndvi/{date}_NDVI.{format}",
        "dates": DATES,
    },
    # Radiation
    # {
    #     "url_wms": f"{URL_UWEST_SENTINEL}{WMS_SERVICE}/{WMS_RADIATION_ID}",
    #     "url_fis": f"{URL_UWEST_SENTINEL}{FIS_SERVICE}/{WMS_RADIATION_ID}",
    #     "layers_wms": "THERMAL",
    #     "layers_fis": "THERMAL",
    #     "name": models_settings.FILES_FOLDER + "thermal/{date}_THERMAL.{format}",
    #     "dates": DATES,
    # },
]

if __name__ == "__main__":
    for data in DATA:
        if data.get('layers_fis') == "NDVI":
            f = open(models_settings.FILES_FOLDER + "ndvi/data.csv", 'w')
            writer = csv.writer(f)
            writer.writerow(['date', 'ndvi'])

        for date in data['dates']:
            for format in IMAGE_FORMAT:
                # descargar imágenes
                r = requests.get(data.get('url_wms') + QUERY_WMS.format(date=date, layers=data.get('layers_wms'), format=format), allow_redirects=True)
                open(data.get('name').format(date=date, format=format.split("/")[1]), 'wb').write(r.content)

                # obtener los valores de ndvi
                if data.get('layers_fis') == "NDVI":
                    r = requests.get(data.get('url_fis') + QUERY_FIS.format(date=date, layer=data.get('layers_fis')), allow_redirects=True)
                    json_data = json.loads(r.content)
                    try:
                        value = [d for d in json_data.get('C0') if d.get('date') == date][0].get('basicStats').get('mean')
                        print(f"LAYER {data.get('layers_fis')} => {value}")
                        writer.writerow([date, value])
                    except Exception as e:
                        print(f"Fallo en {date}: {data.get('layers_fis')}")

        if data.get('layers_fis') == "NDVI":
            f.close()