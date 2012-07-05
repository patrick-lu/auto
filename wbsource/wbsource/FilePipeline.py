from twisted.internet import defer, threads

from scrapy.selector import HtmlXPathSelector
from scrapy.shell import inspect_response

from scrapy.xlib.pydispatch import dispatcher
from scrapy import log
from scrapy.stats import stats
from scrapy.utils.misc import md5sum
from scrapy.http import Request
from scrapy import signals
from scrapy.exceptions import DropItem, NotConfigured, IgnoreRequest
from scrapy.contrib.pipeline.media import MediaPipeline
from scrapy.http import FormRequest

from collections import defaultdict
from cStringIO import StringIO
import re
import os
import hashlib

class FileException(Exception):
	"""General file error exception"""

class FilePipeline(MediaPipeline):
	MEDIA_NAME = 'file'
	fileTypes={
		'image/jpeg':'jpg',
		'image/gif':'gif',
		'image/png':'png',
		}
	def __init__(self, store_uri, download_func=None):
		self.created_directories = defaultdict(set)
		self.basedir = store_uri
		self._mkdir(self.basedir)
		
		super(FilePipeline, self).__init__(download_func=download_func)

	@classmethod
	def from_settings(cls, settings):
		store_uri = settings['FILES_STORE']
		return cls(store_uri)


	def media_downloaded(self, response, request, info):
		log.msg('+++++++++++++++++++++++')
		referer = request.headers.get('Referer')
		if response.status != 200:
			log.msg('File (code: %s): Error downloading file from %s referred in <%s>' \
                    % (response.status, request, referer), level=log.WARNING, spider=info.spider)
			raise FileException
		if not response.body:
			log.msg('File (empty-content): Empty file from %s referred in <%s>: no-content' \
                    % (request, referer), level=log.WARNING, spider=info.spider)
			raise FileException
	
		p=re.compile(r'filename=.+\.((\w|\d)+)')
		#inspect_response(response)
		suffix="unknown";
		
		if 'Content-Type' in response.headers :
			file_type = response.headers['Content-Type'];
			print ("+++++Content-Type")
			print file_type
			if file_type in self.fileTypes:
				suffix = self.fileTypes[file_type]
			else:
				print ("+++++++++unknown type")
			
		
		if 'Content-Disposition' in response.headers :
			header=  response.headers['Content-Disposition'];
			print ("+++++Content-Disposition")
			print header
			header = ''.join(header)
			match = p.search(header)
			if match:
				suffix=match.group(1)
		print suffix
		filename = self.gen_filename(request.url,suffix)

		absolute_path = self._get_filesystem_path(filename)
		self._mkdir(os.path.dirname(absolute_path))
		file = open(absolute_path,"wb")
		file.write(response.body)
		file.close
		#inspect_response(response)
		return {'url': request.url, 'path': filename}

	def gen_filename(self, url,suffix):
		file_guid = hashlib.sha1(url).hexdigest()
		return '%s.%s' % (file_guid,suffix);
		

	def _get_filesystem_path(self, key):
		path_comps = key.split('/')
		return os.path.join(self.basedir, *path_comps)

	def _mkdir(self, dirname, domain=None):
		seen = self.created_directories[domain] if domain else set()
		if dirname not in seen:
			if not os.path.exists(dirname):
				os.makedirs(dirname)
			seen.add(dirname)

	def get_media_requests(self, item, info):
		return [Request(x) for x in item.get('file_urls', [])]

	def item_completed(self, results, item, info):
		if 'files' in item.fields:
        	    item['files'] = [x for ok, x in results if ok]
        	return item

