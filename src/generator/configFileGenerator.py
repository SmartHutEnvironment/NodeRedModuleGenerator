import yaml, json;

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        print("default is called");
        if isinstance(obj, str) and obj.startswith("function"):
        	print("----");
        	return obj;
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

class NodeConfig:
	def __init__(self, configFilePath):
		configFile = open(configFilePath);
		self.config = yaml.load(configFile.read())["node"];
		configFile.close();

	def GenerateSchema(self):
		result = {};
		result["label"] = self.config["name"];
		result["oneditsave"] = self.config["onEditSave"];
		return json.dumps(result, cls=ComplexEncoder);


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
	
	def GenerateConfig(self):
		print(self.GenerateSchema());
		#self.GenerateUI();
		return