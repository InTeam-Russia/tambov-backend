import json
import time
import datetime
import urllib
from io import BytesIO
from typing import Annotated
from docxtpl import DocxTemplate

import requests

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, validator
from fastapi.responses import StreamingResponse

from auth.auth import get_current_user
from auth.db import db
from config import INN_TOKEN
from models.models import Date_model, User

task_routers = APIRouter()

#Response contains full information about company, needs to be formated on Frontend
@task_routers.post('/get_data_by_inn/{inn}')
async def select_by_inn(inn):
    headers = {
        'accept': 'application/json',
        'authorization': INN_TOKEN,
        'Content-Type': 'application/json',
    }

    json_data = {
        'query': inn,
        'count': 10,
        'restrict_value': False,
    }

    response = requests.post('https://api.gigdata.ru/api/v2/suggest/party', headers=headers, json=json_data)
    response_json = response.json()['suggestions']
    if len(response_json) == 0:
        raise HTTPException(status_code=404, detail='Companies with entered INN do not exist')
    data_lst = [el for el in response_json]
    return data_lst
#6318060980 (ИНН магнита)
#3009011845 (нн)

@task_routers.get('/download_RAMD/{inn}')
async def download_RAMD(inn, current_user: Annotated[User, Depends(get_current_user)]):
    with open('templates/OID_list.json') as j_file:
        OID_list = json.load(j_file)['records']

    for dct in OID_list:
        if dct['inn'] == str(inn) and ('deleteDate' not in dct):
            doc = DocxTemplate('templates/Template_RAMD.docx')
            context = {
                'date': datetime.datetime.now().strftime('%d.%m.%Y'),
                'full_name': dct['nameFull'],
                'oid': dct['oid'],
            }
            doc.render(context)
            file_stream = BytesIO()
            doc.save(file_stream)
            file_stream.seek(0)

            encoded_filename = urllib.parse.quote(f"{dct['nameShort']}_RAMD.docx")
            content_disposition = f"attachment; filename*=UTF-8''{encoded_filename}"

            return StreamingResponse(
                file_stream,
                media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                headers = {"Content-Disposition": content_disposition}
            )
    raise HTTPException(status_code=404, detail='Companies with entered INN do not exist')

@task_routers.get('/download_IAMK/{inn}')
async def download_IAMK(inn, current_user: Annotated[User, Depends(get_current_user)]):
    with open('templates/OID_list.json') as j_file:
        OID_list = json.load(j_file)['records']

    for dct in OID_list:
        if dct['inn'] == str(inn) and ('deleteDate' not in dct):
            doc = DocxTemplate('templates/Template_IAMK.docx')
            context = {
                'date': datetime.datetime.now().strftime('%d.%m.%Y'),
                'full_name': dct['nameFull'],
                'oid': dct['oid'],
            }
            doc.render(context)
            file_stream = BytesIO()
            doc.save(file_stream)
            file_stream.seek(0)

            encoded_filename = urllib.parse.quote(f"{dct['nameShort']}_IAMK.docx")
            content_disposition = f"attachment; filename*=UTF-8''{encoded_filename}"

            return StreamingResponse(
                file_stream,
                media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                headers = {"Content-Disposition": content_disposition}
            )

    raise HTTPException(status_code=404, detail='Companies with entered INN do not exist')