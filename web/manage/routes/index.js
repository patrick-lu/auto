var zeromq = require("zmq");

/*
 * GET home page.
 */

exports.index = function(req, res){
  console.log('request is coming')
  res.render('index', { title: 'Express' })
};
exports.grab = function(req, res){
  console.log('request grab')

  var start=parseInt(req.body.start)
  limit =2
  var mongo = require('mongodb'),
  Server = mongo.Server,
  Db = mongo.Db;

  var server = new Server('localhost', 27017, {auto_reconnect: true});
  var db = new Db('autobt', server);

  db.open(function(err, db) {
	con={'publish':{$exists:false}}
    if(!err) {
	db.collection('threads', function(err, collection) {
		collection.find(con).skip(start).sort( { grab_time : -1 } ).limit(limit).toArray(function(err,items){
		if(items){
			var len = items.length;
			var is_end = 0;
			if(len<limit) is_end=1
			//console.log(items)
			var out={
          		  result:1,
			  end: start+len,
			  is_end:is_end,
			  data:items
			}
			console.log("iii")
			console.log(out)
			res.end(JSON.stringify(out));
		}else{
			var out={result:0,error:'empty'}
			res.end(JSON.stringify(out));

		}
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
exports.do_pub = function(req, res){
  console.log('request to publish')
  var socket = zeromq.socket('req');
  socket.connect("tcp://127.0.0.1:6400")

    socket.on('message', function(data) {
      console.log("Answer data: "+data);
	var out={
          result:1,
	  data:""+data
	}
	res.end(JSON.stringify(out));
    });
    msg={cmd:'publish',url:req.body.url}
    socket.send(JSON.stringify(msg));

 
}


exports.pub = function(req, res){
  console.log('request pub')

  var start=parseInt(req.params.id)
  limit =2
  var mongo = require('mongodb'),
  Server = mongo.Server,
  Db = mongo.Db;

  var server = new Server('localhost', 27017, {auto_reconnect: true});
  var db = new Db('autobt', server);

  db.open(function(err, db) {
        con={'publish':{$exists:true}}
    if(!err) {
        db.collection('threads', function(err, collection) {
                collection.find(con).skip(start).sort({pub_time:-1}).limit(limit).toArray(function(err,items){
                if(items){
                        var len = items.length;
                        var is_end = 0;
                        if(len<limit) is_end=1
                        //console.log(items)
                        var out={
                          result:1,
                          end: start+len,
                          is_end:is_end,
                          data:items
                        }
			console.log(len)
			console.log(start)
			console.log("ooo")
			console.log(out)
                        res.end(JSON.stringify(out));
                }else{
                        var out={result:0,error:'empty'}
                        res.end(JSON.stringify(out));

                }
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


