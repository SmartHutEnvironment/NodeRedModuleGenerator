let base = require("@resource:baseClasses");

class @env:className {

	constructor(config) {
		let node = this;
		RED.nodes.createNode(node, config);
		let globalContext = node.context().global;
		node.config = config;
				switch(config.source)
		{
		    case "Memory": this._source = new base.MemorySource(config.name, globalContext); break;
		    case "Mqtt state": this._source = new base.MqttStateSource(RED.nodes.getNode(config.mqtt), config.mqtt_topic, config.mqtt_type); break;
		    case "Mqtt event": this._source = new base.MqttEventSource(RED.nodes.getNode(config.mqtt), config.mqtt_topic, config.mqtt_event_type); break;
		
		    break;
		}
		
		switch(config.mode)
		{
		    case "Boolean": this._globalState = new base.BooleanState(this._source, config.toggle); break;
		    case "Timer": this._globalState = new base.TimerState(this._source, config.toggle, config.timeout, config.allowResetTimer); break;
		}
		
		this._globalState.on("changed", (value) => { this.emit("changed", value); });
	}

	
	Set(data)
	{
	    this._source.Set(data);
	}
	
	Get()
	{
	    return this._source.Get();
	}
	


}