from . import constants

def getValue(item):
    result=""

    try:
        if (item["type"]=='title'):
            for string in item['title']:
                result += string['text']['content']
        elif (item["type"])=='rich_text':
            for string in item['rich_text']:
                result += string['text']['content']
        elif (item["type"])=='multi_select':
            vet_aux = []
            for aux in item['multi_select']:
                vet_aux.append(aux['name'])
            result = vet_aux
        elif (item["type"])=='number':
            result = item['number']
        elif (item["type"])=='select':
            result = item['select']['name']
        elif (item["type"])=='status':
            result = item['status']['name']
        elif (item["type"])=='date':
            result = {
                'start' : item['date']['start'],
                'end' : item['date']['end'],
                'time_zone' :item['date']['time_zone']
            }
        elif (item["type"])=='people':
            vet_aux = []
            for aux in item['people']:
                vet_aux.append(aux['id'])
            result = vet_aux
        elif (item["type"])=='checkbox':
            result = item['checkbox']
        elif (item["type"])=='phone_number':
            result = item['phone_number']
        elif (item["type"])=='url':
            result = item['url']
        elif (item["type"])=='email':
            result = item['email']
        elif (item["type"])=='relation':
            return item['relation']
        elif (item["type"])=='files':
            vet_aux = []
            for aux in item['files']:
                aux_item = {
                    'name' : aux['name'],
                    'file' : aux['file']['url']
                }
                vet_aux.append(aux_item)
            result = vet_aux
        else:
            print(str(item))
    except:
        result = None
    return result

def generateNotionProperty(key, value, columns):
    if not (key in columns['properties']):
        raise Exception(constants.ERROR_PROPERTY_NOT_EXISTS + key) 
    elif columns['properties'][key]=='title':
        return { "title": [ { "text": { "content": value } } ] }
    elif columns['properties'][key] == 'checkbox':
        return {"checkbox": value} 
    elif columns['properties'][key] == 'date':
        if (len(value) == 2):
            return {"date": {"start": value[0],
                             "end": value[1]}}
        return {"date": {"start": value[0]}} #TODO tá certo assim?
    elif columns['properties'][key] == 'email':
        return {"email": value}
    elif columns['properties'][key] == 'files':
        #The Notion API does not yet support uploading files to Notion.
        #This could change in the future, but for now, you can only add an url to a file
        organized_data = []
        for file in value:
            organized_data.append({
                "name": file['name'],
                "external": {
                    "url": file['file']
                }
            })
        return {"files": organized_data}
    elif columns['properties'][key] == 'multi_select':
        organized_data = []
        for name in value:
            organized_data.append({"name": name})
        return {"multi_select": organized_data}
    elif columns['properties'][key] == 'number':
        return {"number": value}
    elif columns['properties'][key] == 'people':
        organized_data = []
        for code in value:
            organized_data.append({
                "object": "user",
                "id": code
            })
        return {"people": organized_data}
    elif columns['properties'][key] == 'phone_number':
        return {"phone_number": value}
    elif columns['properties'][key]=='rich_text':
        return { "rich_text": [ { "text": { "content": value } } ] }
    elif columns['properties'][key] == 'select':
        return {"select": {"name": value}}
    elif columns['properties'][key] == 'status':
        return {
            "status": {
                "name": value
            }
        }
    elif columns['properties'][key] == 'url':
        return {"url": value}
    
    
    elif columns['properties'][key] == 'relation':
        organized_data = []
        for code in value:
            organized_data.append({
                "id":  formatURLString(code)
            })
        return {"relation": organized_data}
    elif columns['properties'][key] == 'url':
        return {"url": value}
    
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

