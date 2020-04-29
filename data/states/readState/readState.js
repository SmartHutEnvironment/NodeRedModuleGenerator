/* onInit */
node.globalState = RED.nodes.getNode(node.config.state);
if (!node.globalState) {
    node.error('No shared state for: ' + node.name);
    return;
}

/* onEnter */
if (node.globalState.status.stateType == "List" && node.config.split_list) 
{
    node.globalState.readValue().value.forEach(function(data){
        node.send({
            topic: node.globalState.name,
            payload: data,
        });
    });
}
else{
    node.send({
        topic:node.globalState.name,
        payload:node.globalState.readValue().value,
    });
}
