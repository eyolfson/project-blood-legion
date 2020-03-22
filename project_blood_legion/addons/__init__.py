import project_blood_legion

import html.parser
import json
import os
import requests
import shutil
import tempfile
import zipfile

class ElvUIHTMLParser(html.parser.HTMLParser):

	def __init__(self):
		super().__init__()
		self._depth = 0
		self._is_version_next = False

	def handle_starttag(self, tag, attrs):
		is_extras_tag = tag == 'div' and ('id', 'extras') in attrs
		if self._depth > 0 or is_extras_tag:
			self._depth += 1

	def handle_endtag(self, tag):
		if self._depth > 0:
			self._depth -= 1

	def handle_data(self, data):
		if self._depth > 0:
			if data == 'The latest version of this addon is ':
				self._is_version_next = True
			elif self._is_version_next:
				self.version = data
				self._is_version_next = False

def elvui_update(entry, addons_dir):
	url = 'https://www.tukui.org/classic-addons.php?id=2#extras'
	response = requests.get(url)
	parser = ElvUIHTMLParser()
	parser.feed(response.text)
	version = parser.version
	if entry['version'] == version:
		return
	print('Updating', entry['version'], 'to', version)
	with tempfile.TemporaryDirectory() as tmp_dir, \
	     tempfile.TemporaryFile() as tmp_file:
		url = 'https://www.tukui.org/classic-addons.php?download=2'
		response = requests.get(url)
		tmp_file.write(response.content)
		with zipfile.ZipFile(tmp_file) as f:
			f.extractall(tmp_dir)
		for d in entry['dirs']:
			shutil.rmtree(os.path.join(addons_dir, d),
			              ignore_errors=True)
		dirs = os.listdir(tmp_dir)
		for d in dirs:
			shutil.move(os.path.join(tmp_dir, d),
			            os.path.join(addons_dir, d))
		entry['version'] = version
		entry['dirs'] = dirs

def update(path):
	addons_dir = os.path.join(path, 'Interface', 'AddOns')
	database_path = os.path.join(addons_dir, 'database.json')

	with open(database_path, 'r') as f:
		database = json.load(f)

	if 'elvui' in database:
		elvui_update(database['elvui'], addons_dir)

	with open(database_path, 'w') as f:
		json.dump(database, f, indent=2)
		f.write('\n')
