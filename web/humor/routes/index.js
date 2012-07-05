var zeromq = require("zmq");

/*
 * GET home page.
 */

exports.index = function(req, res){
  console.log('request is coming')
  res.render('index', { title: 'Express' })
};
exports.last = function(req, res){
  console.log('request last')

  var start=parseInt(req.body.start)
  limit =10
  var mongo = require('mongodb'),
  Server = mongo.Server,
  Db = mongo.Db;

  var server = new Server('localhost', 27017, {auto_reconnect: true});
  var db = new Db('weibo', server);

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
exports.pub = function(req, res){
  console.log('request to publish')
/*
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
*/
  if( !req.body.id || !req.body.hasOwnProperty("comm") ){
	var out={
          result:0,
          error:"Error 500!"
        }
        res.end(JSON.stringify(out));
        return
  }

  var id=req.body.id;
  var comm=req.body.comm;


  var mongo = require('mongodb'),
  Server = mongo.Server,
  Db = mongo.Db;
  var server = new Server('localhost', 27017, {auto_reconnect: true});
  var db = new Db('weibo', server);

  db.open(function(err, db) { 
	if(!err) {

	  db.collection('threads', function(err, collection) {
		var BSON = require('mongodb').BSONPure;
		var obj_id = BSON.ObjectID.createFromHexString(id);
		collection.findOne({_id:obj_id},function(err,result){
			if(result){
			    var out={ result:1,data:null}
			    res.end(JSON.stringify(out));
			    result.publish={
					pub_time:new Date(),
					progress:"0",
					comment:comm
				}
			    collection.save(result);
			}else{
			    var out={
			          result:0,
			          error:"database error"
       				 }
		            res.end(JSON.stringify(out));

			}
		});
	  })

	};
	
  })
}




