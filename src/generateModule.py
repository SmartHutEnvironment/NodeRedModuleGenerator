#!/usr/bin/python3
import yaml, json;
import sys;
import os.path;
from shutil import copy;
from generator import configFileGenerator, jsFileGenerator;

if len(sys.argv) != 3:
    print("Usage: ", sys.argv[0], " templateDirectory outputDirectory");
    exit(1);

def extractPaths(cfg, isFilePath=False):
    if not "to" in cfg:
        cfg["to"] = cfg["from"];
    src = sys.argv[1] + "/" + cfg["from"];
    dst = sys.argv[2] + "/" + cfg["to"];
    if not isFilePath:
        os.makedirs(dst, exist_ok=True);
    else:
        os.makedirs(os.path.dirname(dst), exist_ok=True);
    return (src, dst);

def moduleFiles(path):
    path = os.path.abspath(sys.argv[1] + "/" + path);
    basename = os.path.basename(path);
    return (basename + ".html", basename + ".js", basename + ".yml");




sourcePackageFile = open(sys.argv[1] + "/package.yml");
package = yaml.load(sourcePackageFile.read(), Loader=yaml.SafeLoader)["package"];
sourcePackageFile.close();

#print(package);

resources = {};

for resource in package["resources"]:
    (src, dst) = extractPaths(resource, isFilePath=True);
    copy(src, dst);
    resources[resource["id"]] = os.path.abspath(dst);

nodes = {};

for node in package["nodes"]:
    (src, dst) = extractPaths(node);
    (html, js, yml) = moduleFiles(src);

    config = configFileGenerator.NodeConfig(src + "/" + yml);
    script = jsFileGenerator.JsFileGenerator(src, js, config.config, resources);

    with open(dst + "/" + html, 'w') as f:
        f.write(config.GenerateConfig());
    with open(dst + "/" + js, 'w') as f:
        f.write(script.GetJsFile());
    nodes[config.config["id"]] = node["to"] + "/" + js;


npmPackage = {};

for key in ["name", "version", "description", "author"]:
    npmPackage[key] = package[key];

for key in ["homepage", "dependencies"]:
    if key in package:
        npmPackage[key] = package[key];

npmPackage["node-red"] = { "nodes": nodes };

with open(sys.argv[2] + "/package.json", 'w') as f:
        f.write(json.dumps(npmPackage, indent=4));
