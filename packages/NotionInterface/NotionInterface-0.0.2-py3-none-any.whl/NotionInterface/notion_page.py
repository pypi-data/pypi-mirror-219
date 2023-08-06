import requests
import notion_header as notion_header


class NotionPage:
	page_id:str
	key:str
	dbList = []
	def __init__(self, page_id:str, notion_key:str):
		self.page_id = page_id
		self.key = notion_key
	def getChildDataBase(self, page_id):
		url = f"https://api.notion.com/v1/blocks/{page_id}/children"
		print(f"Requesting: {url}")
		a = requests.get(url, headers=notion_header.getHeader(self.key)).json()
		for block in a['results']:
			if block['type'] == 'child_database':
				self.dbList.append((block["child_database"]['title'],block['id']))
			elif block['type'] == 'child_page':
				self.getChildDataBase(block['id'])
		return self.dbList
	
		