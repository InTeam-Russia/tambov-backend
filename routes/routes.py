import json
import time
import datetime
from typing import Annotated
from docxtpl import DocxTemplate

import requests

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, validator

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
        raise HTTPException(status_code=404, detail='No suggestions')
    data_lst = [el for el in response_json]
    return data_lst
#6318060980 (ИНН магнита)

@task_routers.get('/download_RAMD/{inn}')
async def download_RAMD(inn):
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
            doc.save(f'ready_documents/{dct['nameShort']}_RAMD.docx')
            return {'message': 'File generated successfully and ready for download'}
    raise HTTPException(status_code=404, detail='OID not found')

@task_routers.get('/download_IAMK/{inn}')
async def download_IAMK(inn):
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
            doc.save(f'ready_documents/{dct['nameShort']}_IAMK.docx')
            return {'message': 'File generated successfully and ready for download'}
    raise HTTPException(status_code=404, detail='OID not found')