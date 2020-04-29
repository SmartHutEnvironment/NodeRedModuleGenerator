#!/usr/bin/python3
import yaml;
import sys;
import os.path;
from generator import configFileGenerator;

if len(sys.argv) != 3:
    print("Usage: ", sys.argv[0], " templateDirectory outputDirectory");
    exit(1);

sourcePackageFile = open(sys.argv[1] + "/package.yml");
package = yaml.load(sourcePackageFile.read())["package"];
sourcePackageFile.close();

print(package);

for nodePath in package["nodes"]:
    path = os.path.abspath(sys.argv[1] + "/" + nodePath);
    basename = os.path.basename(path);

    print(nodePath);

    config = configFileGenerator.NodeConfig(path + "/" + basename + ".yml");
    config.GenerateConfig();

for resource in package["resources"]:
    print(resource);








exit(0);
import os;
import os.path;
from generator import generate;

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