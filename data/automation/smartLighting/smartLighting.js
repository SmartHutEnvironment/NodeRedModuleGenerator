class @env:className {

	constructor(config) {
		let node = this;
		RED.nodes.createNode(node, config);
		let globalContext = node.context().global;
		node.config = config;
				this.trigger = RED.nodes.getNode(node.config.trigger);
		this.light = RED.nodes.getNode(node.config.light);
		this.condition = RED.nodes.getNode(node.config.condition);
		this.forced = RED.nodes.getNode(node.config.forced);
		
		this._forcedState = false;
		this._conditionState = true;
		
		if (!this.trigger || !this.light) {
		    node.error("Not valid trigger or light state for automated light");
		    return;
		}
		
		this.trigger.on('changed', (value) => { this.triggerChanged(!!value); });
		this.light.on('changed', (value) => { this.lightChanged(!!value); });
		
		if (!!this.forced) this.forced.on('changed', (value) => { this.forcedChanged(!!value); });
		if (!!this.condition) this.condition.on('changed', (value) => { this.conditionChanged(!!value); });
		


		
	}

	triggerChanged(data) {
		// when it is in forced state...
		if (!!this.forced && !!this.forced.Get() ) return;
	
		// when the condition is given, but is says 'hey, dont do it, bro!'...
		if (data && !!this.condition && !this.condition.Get() ) return;
	
	    this.light.Set(data);
	}
	
	forcedChanged(data)
	{
		this._forcedState = data;
		this.triggerChanged(false);
	
		this.send([null, {payload: data}]);
	}
	
	conditionChanged(data)
	{
		this._conditionState = data;
	}
	
	lightChanged(data)
	{
		this.send([{payload: data}, null]);
	}

}