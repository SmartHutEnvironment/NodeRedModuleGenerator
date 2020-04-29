import yaml, types;
from partGenerator import configFileGenerator;

class NodeGenerator:

	def __init__(self, json, js):
		self.Config = configFileGenerator.NodeConfig(data['name'], data['config']);
		#self.ParseJson(json);
		#self.ParseJs(js);

	def ParseJson(self, file):
		with open(file) as f:
			data = json.load(f);
		self.ID = data['id'];
		self.ClassName = data['className'];
		self.Help = data['help'];
		self.Config = configFileGenerator.NodeConfig(data['name'], data['config']);

	def GenerateHtml(self):
		result = f"""<script type="text/javascript">
RED.nodes.registerType('{self.ID}',{self.Config.GetSchema()});
</script>

<script type="text/x-red" data-template-name="{self.ID}">
{self.Config.GetLayout()}
</script>

<!-- Help Text -->
<script type="text/x-red" data-help-name="{self.ID}">
{self.Help}
</script>
""";
		return result;


	def ParseJs(self, file):	
		with open(file) as f:
			lines = f.readlines();
		self.JsSections = {
			"onInit": "",
			"onEnter": "",
			"functions": "",
			"require": "",
		};

		section = "";
		indent = 0;
		for line in lines:
			if line.startswith("/*") and "onInit" in line:
				section = "onInit";
				indent = 2;
				continue;
			if line.startswith("/*") and "onEnter" in line:
				section = "onEnter";
				indent = 2;
				continue;
			if line.startswith("/*") and "require" in line:
				section = "require";
				indent = 0;
				continue;
			if line.startswith("/*") and "functions" in line:
				section = "functions";
				indent = 1;
				continue;
			
			if section in self.JsSections:
				self.JsSections[section] += ("\t" * indent) + line;
	
	def GenerateJs(self):
		jsFunctions = "";
		if self.JsSections['onEnter'] != "":
			jsFunctions += "\tonInput(msg) {\n\t\tlet node = this;\n" + self.JsSections['onEnter'] + "\n\t}\n\n";
			jsFunctions += "\tonInputInternal(msg) {\n\t\tlet node = this; \n\t\tlet result = this.onInput(msg); \n\t\tif(result) node.send(result);\n\t}\n\n";
		jsFunctions += self.JsSections['functions'];

		content = f"""
{self.JsSections['require']}
let RED;
const state = module.exports = function(red) {{
	RED = red;
	RED.nodes.registerType("{self.ID}", {self.ClassName});
}}

class {self.ClassName} {{

	constructor(config) {{
		let node = this;
		RED.nodes.createNode(node, config);
		let globalContext = node.context().global;
		node.config = config;
		{self.JsSections['onInit']}

		{ "node.on('input', node.onInputInternal.bind(this));" if self.JsSections['onEnter'] != "" else ""}
	}}

{jsFunctions}

}}""";
		return content;