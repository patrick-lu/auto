
/*
 * GET home page.
 */

exports.index = function(req, res){
  console.log('request is coming')
  res.render('index', { title: 'Express' })
};
exports.grab = function(req, res){
  console.log('request grab')

  start=req.body.start
  limit =2
  var mongo = require('mongodb'),
  Server = mongo.Server,
  Db = mongo.Db;

  var server = new Server('localhost', 27017, {auto_reconnect: true});
  var db = new Db('autobt', server);

  db.open(function(err, db) {
    if(!err) {
	db.collection('threads', function(err, collection) {
		collection.find().skip(start).limit(limit).toArray(function(err,items){
			var len = items.length;
			var is_end = 0;
			if(len<limit) is_end=1
			console.log(items)
			var out={
          		  result:1,
			  end: start+len,
			  is_end:is_end,
			  data:items
			}
			res.end(JSON.stringify(out));
		})
	});
	
    }else{
	var out={
          result:0,
	  error:"database error"
	}
	res.end(JSON.stringify(out));
    }
  });
}
