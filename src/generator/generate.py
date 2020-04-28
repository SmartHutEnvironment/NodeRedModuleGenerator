import json, types;

class NodeConfig:
	def __init__(self, name, json):
		self.name = name;
		self.json = json;
		if "isConfig" in json and json["isConfig"]:
			self.isConfig = True;
		else:
			self.isConfig = False;
		self.GenerateFields();

	def GenerateFields(self):
		fieldsLayout = "";
		defaults = "{";
		for field in self.json['fields']:
			if field["type"] == "enum":
				fieldsLayout += f"""\t<div class="form-row"> <label for="node-{"config-" if self.isConfig else ""}input-{field['id']}"><i style="width:20px; text-align:left;" class="icon-tag"></i> {field['label']}</label><select id="node-{"config-" if self.isConfig else ""}input-{field['id']}">""";
				for option in field["values"]:
					fieldsLayout += f"""<option value="{option}">{option}</option>"""
				fieldsLayout += f"""</select></div>\n""";
			else:
				fieldsLayout += f"""\t<div class="form-row"> <label for="node-{"config-" if self.isConfig else ""}input-{field['id']}"><i style="width:20px; text-align:left;" class="icon-tag"></i> {field['label']}</label> <input type="{field['type']}" id="node-{"config-" if self.isConfig else ""}input-{field['id']}" placeholder="{field['label']}"> </div>\n""";

			defaults += f"""{field['id']}: {{ """;
			if 'default' in field:
				defaults += "value: \"" + field['default'] + "\", ";
			if 'dataType' in field:
				defaults += "type: \"" + field['dataType'] + "\", ";
			if 'required' in field:
				defaults += "required: " + ("true" if field['required'] else "false") + ", ";
			if 'validate' in field:
				defaults += "validate: " + field['validate'] + ", ";
			
			defaults += "}, ";
		defaults += "}";

		self.fieldsDefault = defaults;
		self.fieldsLayout = fieldsLayout;

	def GetSchema(self):
		if 'label' not in self.json:
			self.json['label'] = f"""function() {{ if(this.name) return this.name; else return "{self.name}";}}""";
		if 'paletteLabel' not in self.json:
			self.json['paletteLabel'] = f""" "{self.name}" """;

		result = f"""{{
			category: '{self.json['category']}',
			defaults: {self.fieldsDefault},
			label: {self.json['label']},
			{ "paletteLabel: " + self.json['paletteLabel'] + "," if "paletteLabel" in self.json else ""}
			{ "oneditsave: " + self.json['onSave'] + "," if "onSave" in self.json else ""}
			{ "oneditresize: " + self.json['onEdit'] + "," if "onEdit" in self.json else ""}

			{ "inputs: " + str(self.json['inputs']) + "," if "inputs" in self.json else ""}
			{ "outputs: " + str(self.json['outputs']) + "," if "outputs" in self.json else ""}
			{ "icon: '" + self.json['icon'] + "'," if "icon" in self.json else ""}
			{ "color: '" + self.json['color'] + "'," if "color" in self.json else ""}
			{ "align: '" + self.json['align'] + "'," if "align" in self.json else ""}
		}}""";
		return result;
	
	def GetLayout(self):
		return self.fieldsLayout

class NodeGenerator:

	def __init__(self, json, js):
		self.ParseJson(json);
		self.ParseJs(js);

	def ParseJson(self, file):
		with open(file) as f:
			data = json.load(f);
		self.ID = data['id'];
		self.ClassName = data['className'];
		self.Help = data['help'];
		self.Config = NodeConfig(data['name'], data['config']);

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