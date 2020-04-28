import json;
import os;
import os.path;
from generator import generate;

f = open("gen.json");
data = json.load(f);
f.close();

print("Start processing of", len(data['nodes']), "nodes");

nodeList = {"a":"b"};

for entry in data['nodes']:
    jsonFile = entry['source'];
    jsFile = jsonFile[:-2];
    print("Process", jsonFile, "with", jsFile);
    node = generate.NodeGenerator(jsonFile, jsFile);

    fileName = os.path.basename(jsonFile)[:-5];
    os.makedirs(entry['target'], exist_ok=True);

    with open(entry['target'] + "/" + fileName + ".html", 'w') as f:
        f.write(node.GenerateHtml());
    with open(entry['target'] + "/" + fileName + ".js", 'w') as f:
        f.write(node.GenerateJs());
    
    nodeList[node.ID] = entry['target'] + "/" + fileName + ".js";

print("package:", json.dumps(nodeList, indent=4));