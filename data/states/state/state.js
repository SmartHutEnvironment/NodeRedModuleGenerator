/* require */
let base = require("../../statePrimitives");

/* onInit */
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

/* functions */ class Tmp {

Set(data)
{
    this._source.Set(data);
}

Get()
{
    return this._source.Get();
}

/* functions */ }