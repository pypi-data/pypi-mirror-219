import requests
import json
from . import constants
from .notion_header import getHeader
from .notion_database_types import getValue, generateNotionProperty
import pandas as pd

class NotionDatabase:
    db_id:str
    key:str
    columns=None

    def __init__(self, database_id:str, notion_key:str):
        self.db_id = database_id
        self.key = notion_key
        self.columns = self.getColumns()
    
    def getColumns(self):
        if self.columns != None:
            return self.columns
        
        url = f"https://api.notion.com/v1/databases/{self.db_id}"

        res_dict = requests.get(url, headers=getHeader(self.key)).json()

        if (res_dict['object'] != 'database'):
            raise Exception(constants.ERROR_NOT_DATABASE)

        result = {}
        properties = {}
        result['database_id'] = self.db_id
        result['database_title'] = res_dict["title"][0]['text']['content']
        for key in res_dict['properties'].keys():
            properties[key] = res_dict['properties'][key]['type']
        result['properties'] = properties
        
        return result
    
    def getAllRecords(self, next_cursor=None):
        url = f"https://api.notion.com/v1/databases/{self.db_id}/query"

        if (next_cursor==None):
            payload = {"page_size": 100}
        else:
            payload = {"start_cursor": next_cursor}
        
        res_dict = requests.post(url, json=payload, headers=getHeader(self.key)).json()

        if (res_dict['object'] != 'list'):
            raise Exception(constants.ERROR_NOT_LIST)

        result = []
        for res in res_dict['results']:
            linha = {}
            properties = {}
            linha['id'] = res['id']
            linha['created_time'] = res['created_time']
            linha['last_edited_time'] = res['last_edited_time']

            for key in res['properties'].keys():
                properties[key] = getValue(res['properties'][key])
            linha['properties'] = properties

            result.append(linha)

        # RECURSÃO PARA PRÓXIMO CURSOR
        if res_dict['next_cursor'] != None:
            result_rec = self.getAllRecords(next_cursor=res_dict['next_cursor'])
            result.extend(result_rec)

        return result


    def getRecord(self, pageId:str):
        pageId = self.formatURLString(pageId)
        url = f"https://api.notion.com/v1/pages/{pageId}"

        res_dict = requests.get(url, headers=getHeader(self.key)).json()
        if (res_dict['object'] != 'page'):
            raise Exception(constants.ERROR_NOT_PAGE)

        record = {}
        properties = {}
        record['id'] = res_dict['id']
        record['created_time'] = res_dict['created_time']
        record['last_edited_time'] = res_dict['last_edited_time']

        for key in res_dict['properties'].keys():
            properties[key] = getValue(res_dict['properties'][key])

        record['properties'] = properties

        return record

    def putRecord(self, record):
        record_insert = {}
        record_insert['parent'] = { "database_id": self.db_id }
        properties = {}
        for prop in record['properties']:
            generatedProp = generateNotionProperty(key=prop, value=record['properties'][prop], columns=self.columns)
            properties[prop] = generatedProp
        record_insert['properties'] = properties

        record = json.dumps(record_insert)
        url = f"https://api.notion.com/v1/pages/"

        res_dict = requests.post(url, headers=getHeader(self.key), data=record)

        if (res_dict.status_code!=200):
            raise Exception(constants.ERROR_POST_API + ": " + res_dict.text)
        
        return res_dict.json()['id'] 
    
    def editRecord(self, pageId:str, record):
        pageId = self.formatURLString(pageId)
        record_insert = {}
        record_insert['parent'] = { "database_id": self.db_id }
        properties = {}
        for prop in record['properties']:
            generatedProp = generateNotionProperty(key=prop, value=record['properties'][prop], columns=self.columns)
            properties[prop] = generatedProp
        record_insert['properties'] = properties

        record = json.dumps(record_insert)
        url = f"https://api.notion.com/v1/pages/{pageId}"

        res_dict = requests.patch(url, headers=getHeader(self.key), data=record)

        if (res_dict.status_code!=200):
            raise Exception(constants.ERROR_POST_API + ": " + res_dict.text)
        
        return res_dict.json()['id']
     
    def ConvertToExcel(self, path:str = "output.xlsx"):
        records = self.getAllRecords()
        aux = []
        for record in records:
            id = record['id']
            record['properties']['id'] = id
            aux.append(record['properties'])
        df = pd.DataFrame(aux)
        
        df.to_excel(path, index=False)

    @staticmethod
    def formatURLString(url:str):
        if len(url) == 36:
            return url
        if len(url) != 32:
            raise ValueError("Invalid input string length. The input string must have a length of 32 characters.")

        parts = [
            url[:8],
            url[8:12],
            url[12:16],
            url[16:20],
            url[20:]
        ]

        return "-".join(parts)
