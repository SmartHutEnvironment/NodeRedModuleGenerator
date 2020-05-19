import yaml;
import json;
import os.path;
import re;

class NodeConfig:
	def __init__(self, configFilePath):
		self.path = os.path.dirname(configFilePath);
		configFile = open(configFilePath);
		self.config = yaml.load(configFile.read(), Loader=yaml.SafeLoader)["node"];
		configFile.close();

		self.htmlScript = None;
		htmlPath = os.path.dirname(configFilePath) + "/html.js";
		print(htmlPath);
		if os.path.exists(htmlPath):
			script = open(htmlPath);
			self.htmlScript = script.read();
			script.close();

	def GenerateSchema(self):
		result = {};

		appendConfig(self.config, result, "name", dstName="label", required=True);
		appendConfig(self.config, result, "category", required=True);
		appendConfig(self.config, result, "onEditSave", dstName="oneditsave");
		appendConfig(self.config, result, "onEditPrepare", dstName="oneditprepare");
		appendConfig(self.config, result, "onEditResize", dstName="oneditresize");

		for key in ["align", "color", "icon", "inputs", "outputs"]:
			appendConfig(self.config, result, key);

		result["defaults"] = self.GetSchemaDefaults();

		data = json.dumps(result, indent=4);
		data = data.replace("\">>>", "");
		data = data.replace("<<<\"", "");
		return data;

	def GetSchemaDefaults(self):
		result = {};

		for p in self.config["properties"]:
			cfg = self.config["properties"][p];
			data = {};

			appendConfig(cfg, data, "default", dstName="value");
			appendConfig(cfg, data, "required");
			appendConfig(cfg, data, "type");
			appendConfig(cfg, data, "validate");

			result[p] = data;

		return result;

	def GenerateHTML(self):
		ui = self.ProcessFields(self.config["ui"]);
		html = f"""<script type="text/x-red" data-template-name="{self.config["id"]}">
{ui}
</script>
""";
		return html;

	def ProcessFields(self, src):
		prefix = "node-config-input" if self.config["category"] == "config" else "node-input";
		result = "";
		for field in src:
			if not "field" in field:
				continue;
			name = field["field"];
			data = self.config["properties"][name];
			if data["input"] == "text":
				result += textInput(prefix, name, data["label"]);
			if data["input"] == "enum":
				result += selectOption(prefix, name, data["label"], data["options"], default=(data["default"] if "default" in data else None))

		return result;
	
	def GenerateConfig(self):
		schema = self.GenerateSchema();

		script = "";

		if self.htmlScript != None:
			match = re.search("\@include\(\"(.*?)\"\)", self.htmlScript);
			while match:
				target = self.path + "/" + match.group(1);
				if os.path.exists(target):
					f = open(target);
					text = f.read();
					f.close();
					self.htmlScript = self.htmlScript.replace(match.group(0), text);
				else:
					print("File not found: ", target);
				match = re.search("\@include\(\"(.*?)\"\)", self.htmlScript);

			script += f"""
<script type="text/javascript">
{self.htmlScript}
</script>""";

		script += f"""
<script type="text/javascript">
RED.nodes.registerType('{self.config["id"]}', {schema});
</script>
"""

		return script + self.GenerateHTML();

def appendConfig(src, dst, srcName, dstName=None, required=False, default=None):
		if dstName == None:
			dstName = srcName;

		if not srcName in src:
			if required:
				raise Exception("missing key");
			else:
				return;

		value = src[srcName];
		if isinstance(value, str) and value.startswith("function"):
			value = ">>>" + value + "<<<";
		dst[dstName] = value;

def textInput(prefix, name, label, placeholder=""):
	name = prefix + "-" + name;
	return f"""<div class="form-row">
	<label for="{name}">
		<i style="width:20px; text-align:left;" class="icon-tag"></i> 
		{label}
	</label>
	<input type="text" id="{name}" placeholder="{placeholder}"> 
</div>
""";

def selectOption(prefix, name, label, options, default=None):
	name = prefix + "-" + name;
	optionsHTML = "";
	for option in options:
		optionsHTML += f"""		<option value="{option}" {"selected" if option == default else ""}>{option}</option>""" + "\r\n";

	return f"""<div class="form-row">
	<label for="{name}">
		<i style="width:20px; text-align:left;" class="icon-tag"></i> 
		{label}
	</label>
	<select id="{name}">
{optionsHTML}
	</select>
</div>
""";
