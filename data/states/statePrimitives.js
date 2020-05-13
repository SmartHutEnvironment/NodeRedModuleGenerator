let fk = require("./extractStates");
let events = require('events');

class DataSource extends events.EventEmitter
{
	constructor(name) 
	{ 
		super();
		this._value = false;
	}

	Set(data) 
	{
		console.log("call Set on DataSource", data);
		if (data == this._value)
		{
			this.emit("updated", data);
			console.log("DataSource updated");
		}

		console.log("DataSource changed");
		this._value = data;
		this.emit("changed", data);
	}

	Get() 
	{ 
		return this._value; 
	}
}

class MemorySource extends DataSource
{
	constructor(name, globalContext)
	{
		super(name);

		if (globalContext.keys().indexOf('state') < 0) {
		    globalContext.set('state', {});
		}

		this.globalState = globalContext.get('state');
		this._name = name;

		let storedState = this.globalState[name];
		if (storedState) 
		{
		    this._value = storedState.value;
		    this.emit('init', node.exposedState());
		}
	}

	Set(data)
	{
		if (data == this._value) return;

		this._value = data;
		this.globalState[this._name] = { value: data };
	    this.emit('changed', data);
	}
}

class MqttSource extends DataSource
{
	constructor(connection, topic)
	{
		super("");
		this._connection = connection;
		this._topic = topic;

		connection.subscribe(topic, this.onMsg.bind(this));
	}

	onMsg(data)
	{
		console.log("Warning: onMsg method must be overridden");
	}
}

class MqttStateSource extends MqttSource
{
	constructor(connection, topic, side)
	{
		super(connection, topic);
		this._side = side;
	}

	onMsg(data)
	{
		let value = null;

		switch (this._side)
		{
			case "Single": value = fk.extractState(data); break;
			case "Double - left": value = fk.extractLeftState(data); break;
			case "Double - right": value = fk.extractRightState(data); break;
		}

		if (value !== null)
		{
			// Parents set maintaines the _value member and emitting changed event
			super.Set(value);
		}
	}

	Set(data)
	{
		console.log("Set mqtt state", data, this._topic);
		let pkg = {};
		if (data === true) data = "ON"; else data = "OFF";

		switch (this._side)
		{
			case "Single": pkg["state"] = data; break;
			case "Double - left": pkg["state_left"] = data; break;
			case "Double - right": pkg["state_right"] = data; break;
		}

		this._connection.publish(this._topic + "/set", pkg);
	}
}

class MqttEventSource extends MqttSource
{
	constructor(connection, topic, eventType)
	{
		super(connection, topic);
		this._event = eventType;
		this._value = false;
	}

	onMsg(data)
	{
		let value = null;

		switch (this._event)
		{
			case "Motion": value = fk.extractMotion(data); break;
			case "Single click": value = fk.extractSingleClick(data); break;
			case "Double click": value = fk.extractDoubleClick(data); break;
		}

		if (value !== null)
		{
			super.Set(value);
		}
	}

	Set(data)
	{
	}
}

class GlobalState extends events.EventEmitter
{
	constructor(source, toggleMode)
	{
		super();
		this._source = source;
		this._value = false;
		this._toggleMode = false;
		source.on("changed", (value) => {this.onChanged(value);});
		source.on("updated", (value) => {this.onUpdated(value);});
	}

	Get()
	{
		return this._value;
	}

	Set(data)
	{
		this._source.Set(data);
	}

	onChanged(data)
	{
		console.log("GlobalState source changed");
		if (this._toggleMode && data === true)
		{
			data = !this._value;
		}

		this._value = data;
		this.emit("changed", data);
	}

	onUpdated(data)
	{
		this.emit("updated", data);
	}
}


class BooleanState extends GlobalState
{
	constructor(source, toggleMode)
	{
		super(source, toggleMode);
	}
}

class TimerState extends GlobalState
{
	constructor(source, toggleMode, timeout, allowResetTimer)
	{
		super(source, toggleMode);
		this._value = false;
		this._timer = null;
		this._timeout = timeout;
		this._allowResetTimer = allowResetTimer;
	}

	onChanged(data)
	{
		console.log("TimerState source has changed", data);
		if (this._toggleMode && data === true)
		{
			data = !this._value;
		}

		if (!data && this._allowResetTimer)
		{
			console.log("stop timer");
			this.stopTimer();
			this.emit("changed", false);
		}

		let prevState = this._value;
		if (data) {
			console.log("(re)start timer");
			this.stopTimer();
			this.startTimer();

			if (!prevState) 
			{
				console.log("emit changed - true");
				this.emit("changed", true);
			}
		}
	}

	onUpdated(data)
	{
		if (false && this._timer !== null)
		{
			this.stopTimer();
			this.startTimer();
		}

		super.onUpdated(data);
	}


	stopTimer()
	{
		if (this._timer !== null) clearTimeout(this._timer);
		this._value = false;
	}

	startTimer()
	{
		this._value = true;
		this._timer = setTimeout(() => {
	    		this._value = false;
	    		this._timer = null;
	    		this.emit("changed", false);
	    	}, this._timeout * 1000);
	}
}

module.exports = { MemorySource, MqttStateSource, MqttEventSource, BooleanState, TimerState };