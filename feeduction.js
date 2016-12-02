//how to use zerorpc with node as client and python as server
/*var zerorpc = require("zerorpc");

var client = new zerorpc.Client();
client.connect("tcp://127.0.0.1:4242");
//calls the method on the python object
client.invoke("hello", "World", function(error, reply, streaming) {
    if(error){
        console.log("ERROR: ", error);
    }
    console.log(reply);
});
*/

var express = require('express');
//var bodyParser = require('body-parser'); FOR POST METHOD
var app     = express();


//NPM Module to integrate Handlerbars UI template engine with Express
var server = require('http').Server(app);
var exphbs  = require('express-handlebars');
//to connect to mongodb server
var mongo = require('mongodb');
var MongoClient = require('mongodb').MongoClient
  , assert = require('assert');
//to encrypt password
var bcrypt = require('bcrypt');
const saltRounds = 10;
//to parse reuests
var bodyParser  = require('body-parser')
app.use(bodyParser.urlencoded({
  extended: true
}));

app.engine('handlebars', exphbs({defaultLayout: 'main'}));
app.set('view engine', 'handlebars');

// Connection URL 
var url = 'mongodb://localhost:27017/feeduction';



app.get('/',function(req,res){
	res.sendFile( __dirname + '/views/login.html')
});

app.post('/login',function(req,res){
	// Use connect method to connect to the Server 
	MongoClient.connect(url, function(err, db) {
  	assert.equal(null, err);
  	console.log("Connected correctly to server");
 	
 	login(db,req,res);
	});

});

//will give the register page
app.get('/register',function (req,res){
	res.render('register');
});


app.post('/adduser',function (req,res){

	// Use connect method to connect to the Server 
	MongoClient.connect(url, function(err, db) {
  	assert.equal(null, err);
  	console.log("Connected correctly to server");
 	
 	addUser(db,req,res);
	});
 });


app.get('/addFeedLinks',function(req,res){
	res.render('addFeedLinks');
})

app.get('/addLinks',function(req,res){
	var link = req.query.link;

	MongoClient.connect(url, function(err, db){
		var addFeedLinks = db.collection('feedLinks');
		var packet = {"link" : link}
		addFeedLinks.insert(packet,function(err, result){
			 if(err)
		    {
		    	console.log("Error not able to add link")
		    	console.log(err);
		    	res.render('option',{message : "please try again some time later"});
		    	db.close();
		    }
		    
		    
		    if(!err)
		    {
		    	console.log("link inserted");

		    	//TOADD what will display after registration
		    	res.render('options');
		    	db.close();
		    }
		});
	});
})

app.get('/feeds',function(req,res){
	var feeds=[];
	var i=0;
	MongoClient.connect(url, function(err, db) {
	  	assert.equal(null, err);
	  	console.log("Connected correctly to server");
	 	var collection = db.collection('feedsUnread');
	 	collection.find({}).toArray(function(err,docs){
	 		clust = [];
	 		for(cluster in docs)
	 		{
	 			//console.log("here");
	 			var clus = docs[cluster];
	 			feed = [];
	 			count = 0;
	 			box = {};
	 			//console.log(clus);
	 			//console.log("             "+i)
	 					
				//console.log("i am hre"+cl);
				cl = clus['feeds'];
				for(feeds in cl)
				{
					//console.log(feeds);
					fd = cl[feeds];
					
					count++;
					//console.log("am i printing ");
					//console.log(clus['_id']);
					temp = {};
					temp['id'] = clus['_id'];
					temp['title'] = fd['feed']['title'];
					temp['summary'] = fd['feed']['summary'];
					feed.push(temp);
				}

	 			box['feed'] = feed;
	 			box['count'] = count;
	 			clust.push(box);
	 			i++;
	 		}
	 		res.render('feeds',{feeds:clust});
 		});
	});
	
})


app.get('/feedRead',function(req,res){
	var id = req.query.id;
	console.log(id);
	MongoClient.connect(url, function(err, db){
		var feedUnRead = db.collection('feedsUnread');
		var o_id = new mongo.ObjectID(id);
		var feed = feedUnRead.find({"_id" : o_id}).toArray(function(err,docs){
			if(err)
				console.log(err);
			else
			{
				var feedRead = db.collection('feedsRead');
				console.log(docs[0]);
				feedRead.insert(docs[0], function(err, result) {
					if(err)
					{
						console.log(err);
					}
					else
					{
						feedUnRead.remove({"_id" : o_id});
					}
				});
			}
		});
		
		//console.log(feed);
	})
})


server.listen(3000, function () {
     console.log("Express server listening on port " + 3000);
});

var login = function(db,req,res){
	var username = req.body.username;
	var pass = req.body.pass;

	var collection = db.collection('users');

	collection.findOne({"username":username},function(err,docs){
		if(err)
		{
			res.render('login',{message : "try again later"});
			db.close();
		}
		else if(!err)
		{
			if(docs && bcrypt.compareSync(pass, docs.password)){
				console.log("login succesful");
				res.render('options');
				//TOADD where to go after login
			}
			else if(docs){
				console.log("incorrect password");
				res.render('login',{message:"password is incorrect"});
				db.close();
			}
			else{
				console.log("incorrect username");
				res.render('login',{message: "username does not exist"});
				db.close();
			}
		}
	});

}


var addUser = function(db,req,res) {
	const username = req.body.username;
	var pass = req.body.pass;
	var name = req.body.name;
	var email = req.body.email;
	var no = req.body.no;

	var salt = bcrypt.genSaltSync(saltRounds);
	pass = bcrypt.hashSync(pass, salt);
	var user = {
		"username":username,
		"password":pass,
		"name":name,
		"email":email,
		"phone":no
	}

  // Get the documents collection 
  var collection = db.collection('users');

  collection.findOne({"username":username},function(err, docs) {
  	if(err)
  	{
  		console.log(" Error adduser matching username")
    	res.render('login',{message : "please try to register some time later"});
    	db.close();
  	}

    if(docs){
	    console.log("Username already exists");
	    res.render('register',{message : "username already exist"});
	    db.close();
    }
    else if(!err)
    {

	  	// Insert some documents 
	  	collection.insert(user, function(err, result) {
		    if(err)
		    {
		    	console.log("Error adduser not able to add user")
		    	console.log(err);
		    	res.render('login',{message : "please try to register some time later"});
		    	db.close();
		    }
		    
		    
		    if(!err)
		    {
		    	console.log("Inserted 1 user into the users collection");

		    	//TOADD what will display after registration
		    	res.render('options');
		    	db.close();
		    }
	  	});
    }
  });

}


