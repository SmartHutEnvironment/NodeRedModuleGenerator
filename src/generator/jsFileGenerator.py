import os.path;

class JsFileGenerator:
	def __init__(self, path, name, config, resources):
		self.path = path;
		self.name = name;
		self.config = config;
		self.resources = resources;
		self.className = config["id"].replace("-", "");

	def GenerateFromComplexFile(self):
		f = open(self.path + "/" + self.name + ".js");
		data = f.read();

		schema = f"""let RED;
const state = module.exports = function(red) {{
	red.nodes.registerType("{self.config["id"]}", {self.className});
}}

{data}
""";
		return self.Replace(schema);

	def Replace(self, data):
		data = data.replace("@env:className", self.className);

		for name in self.resources:
			data = data.replace("@resource:" + name, self.resources[name]);

		return data;

	def GetJsFile(self):
		if os.path.exists(self.path + "/" + self.name + ".js"):
			return self.GenerateFromComplexFile();
		else:
			return "";