#pylint:disable=W0105
'''
pysb - A Simple Python wrapper for StreamSB API.
    Copyright (C) 2021 Code-xed

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import requests

class StreamSBException(Exception):
	pass

class StreamSB:
	'''
	Base Class Which Extends All Available API Methods.
	'''
	def __init__(self, api_key):
		'''
		Initializes The API_KEY & The Base API_URL.
		
		Patameters:
			1. API_KEY
		'''
		self.base_api = "https://api.streamsb.com/api/"
		self.api_key = api_key
		self.file_name = None
	
	'''
	API Call Boilerplate To Reduce Code Repetation.
	'''
	def exe(self, param):
		if type(param) != type((1,2)):
			api = self.base_api + param
		r = requests.get(api)
		return r.json()
	
	'''
	Returns Account Details Of The  Given Account's API_KEY.
	
	Format:
		Parsed JSON / Python Dictionary
	'''
	def info(self):
		param = f"account/info?key={self.api_key}"
		return self.exe(param)
	
	'''
	Get DMCA Reported Files
	'''
	def dmca(self):
		api = f"dmca/list?key={self.api_key}"
		return self.exe(api)
		
	'''
	Returns Account Statistics
	
	Format:
		Parsed JSON / Python Dictionary
	Parameters:
		1. last - Number Of Days (+ve Integer)
		    Default: 7
	'''
	def stats(self, last=7):
		param = f"account/stats?key={self.api_key}&last={last}"
		return self.exe(param)	
		
	'''
	Uploads A Video Using URL.
	Supported URLs - Google Drive, Yandex Drive
	
	Parameters:
		Required:
			1. URL
		Optional:
			1. Video Title
	'''
	def upload_url(self, url, title = "", fetch_title = False):
		api = f"upload/url?key={self.api_key}&url={url}"
		response = self.exe(api)
		if title.isalnum():
			self.rename(response["result"]["filecode"], title)
		elif fetch_title:
			pass
		return response
		
	'''
	Upload From Local
	
	Parameters:
		1. File Path
		
	'''
	def upload(self, file, name):
		api = f"upload/server?key={self.api_key}"
		self.exe(api)
		
	'''
	Renames A Video On The Server.
	
	Parameters:
		1. FILECODE
		2. TITLE
	'''
	def rename(self, file_code, title):
		self.file_name = f"{title}.mp4"
		api = f"file/rename?key={self.api_key}&file_code={file_code}&title={title}&name={self.file_name}"
		return self.exe(api)
		
	'''
	Creates A Folder
	
	Parameters:
		1. parent_id - ID Of Parent Folder (Integer) -> Default: 0
		2. name - Name Of New Folder (String)
	'''
	def create_folder(self, name, parent_id=0):
		api = f"folder/create?key={self.api_key}&parent_id={parent_id}&name={name}"
		return self.exe(api)
	
	'''
	List Files
	
	Parameters:
		1. page - Page Number (Integer) -> Default: 0
		2. per_page - No Of Results Per Page (Integer) -> Default: 0
		3. fld_id - Folder ID (Integer) -> Default: 0
		Filters:
		4. public - Filter Results By Visibility (Integer):
			value: 0 -> Private
			value: 1 -> Public
			Default: 0
		5. created - Show Only Results Created After The Timestamp. Format (yyyy-mm-dd || hh:mm:ss) -> Default: ""
		6. title - Filter Video Titles (String) -> Default: ""
	'''
	def list_files(self, page=0, per_page=0, fld_id=0, created="", title="", public=0):
		api = f"file/list?key={self.api_key}&page={page}&per_page={per_page}&fld_id={fld_id}&public={public}&created={created}&title={title}"
		return self.exe(api)
		
	'''
	Clone StreamSB Video To Your Account
	
	Parameters:
		1. file_code - File Code Of The Video (String)
	'''
	def clone(self, file_code):
		api = f"file/clone?key={self.api_key}&file_code={file_code}"
		return self.exe(api)
	
	'''
	Show File Info
	
	Parameters:
		1. file_code - File Code Of The Video (String)
	'''
	def file_info(self, file_code):
		api = f"file/info?key={self.api_key}&file_code={file_code}"
		return self.exe(api)
	
	'''
	Show Deleted Files
	
	Parameters:
		1. last - No Of Files To Show (Integer) -> Default: 0
	'''
	def deleted(self, last=0):
		api = f"files/deleted?key={self.api_key}&last={last}"
		return self.exe(api)
	
	'''
	Get Direct Link Of File
	
	Parameters:
		Required:
			1. file_code - File Code Of The Video (String)
		Optional:
			2. q - Video Quality If Exists (String):
				value: "h" -> High (720p)
				value: "n" -> Normal (480p)
				value: "l" -> Low (360p)
				*Default Value: "l"
	'''
	def gld(self, file_code, q="l"):
		api = f"file/info?key={self.api_key}&file_code={file_code}&q={q}"
		return self.exe(api)
	
	#Player Customisation Methods
	'''
	Change / Set Thumbnail
	
	Parameters:
		1. file_code - File Code Of The Video (String)
		2. poster - Thumb URL (String)
	'''
	def thumb(self, file_code, poster):
		api = f"https://streamsb.net/embed-{file_code}.html?poster={poster}"
		return self.exe((api, True))
	
	'''
	Add Subtitles/CC [.srt only]
	
	Parameters:
		
	'''
	def subs(self, url_1, label_1, url_2, label_2):
		api = f"https://streamsb.net/embed-file_code.html?url_1={url_1}&sub_1={label_1}&caption_2={url_2}&sub_1={label_2}"
		return self.exe((api, True))
	
__copyright__ = "Copyright (c) 2021 Code-xed"
__license__ = "GNU Lesser General Public License v3 or later (LGPLv3+)"
