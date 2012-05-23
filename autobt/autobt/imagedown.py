from scrapy.contrib.pipeline.images import ImagesPipeline
from pymongo import Connection

class MyImagePipeline(ImagesPipeline):

	def item_completed(self, results, item, info):
		#conn = Connection()
		#db = conn.autobt
		#threads_db = db.threads
		#tt=threads_db.find_one({"url":item["name"]});
		images=[];
		for ok,x in results:
			if ok:
				images.append([x['url'],x['path']])
		'''	
		if images:
			tt["imgs"]=images;
			tt["completed"]=1;
			threads_db.save(tt);
		else:
			threads_db.remove({"url":item["name"]})
		'''
		item["images"]=images;
		return item
