
var mqtt = require('mqtt');
var stringify = function(obj, prop) {
    var placeholder = '____PLACEHOLDER____';
    var fns = [];
    var json = JSON.stringify(obj, function(key, value) {
      if (typeof value === 'function') {
        fns.push(value);
        return placeholder;
      }
      return value;
    }, 2);
    json = json.replace(new RegExp('"' + placeholder + '"', 'g'), function(_) {
      return fns.shift();
    });
    return 'this["' + prop + '"] = ' + json + ';';
  };

class @env:className {

	constructor(config) {
		let node = this;
		RED.nodes.createNode(node, config);
		let globalContext = node.context().global;
		node.config = config;
				node.connection = mqtt.connect(config.host);
		node.callbacks = {};
		node.connection.on('message', function(topic, data){
		    console.log("new mqtt msg", topic);
		    if (node.callbacks.hasOwnProperty(topic)){
		        node.callbacks[topic].forEach(function(item){
		            if (item === null) return;
		
		            item(JSON.parse(data));
		        });
		    }
		});


		
	}

	
	publish(topic, data)
	{
	    let node = this;
	    node.connection.publish(topic, JSON.stringify(data));
	}
	
	subscribe(topic, callback)
	{
	    console.log("Subscribe to", topic);
	    let node = this;
	
	    if (!node.callbacks.hasOwnProperty(topic))
	    {
	        node.callbacks[topic] = [];
	    }
	    node.callbacks[topic][node.callbacks[topic].length] = callback;
	    node.connection.subscribe(topic);
	}
	


}