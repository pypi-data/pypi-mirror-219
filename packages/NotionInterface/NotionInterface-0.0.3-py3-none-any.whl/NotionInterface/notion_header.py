def getHeader(api_key):
    return {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "Authorization": f"Bearer {api_key}",
        "content-type": "application/json"
    }