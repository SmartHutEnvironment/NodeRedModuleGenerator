exports.pack = (data) =>
{
    if (data === null) return null;
    return { payload: data };
}

exports.updateState = (state, data) =>
{
    if (state && typeof(data) === "boolean")
    {
        state.update(data);
    }

    return data;
}

exports.extractBattery = (data) => {
    if (data.hasOwnProperty("battery")) return data["battery"];
    return null;
};

exports.extractLinkQuality = (data) => {
    if (data.hasOwnProperty("linkquality")) return data["linkquality"];
    return null;
};

exports.extractState = (data) => {
    if (data.hasOwnProperty("state")) return data["state"] === "ON";
    return null;
};

exports.extractLeftState = (data) => {
    if (data.hasOwnProperty("state_left")) return data["state_left"] === "ON";
    return null;
};

exports.extractRightState = (data) => {
    if (data.hasOwnProperty("state_right")) return data["state_right"] === "ON";
    return null;
};

exports.extractSingleClick = (data) => {
    if (data.hasOwnProperty("click") && data["click"] == "single") return true;
    return null;
};

exports.extractDoubleClick = (data) => {
    if (data.hasOwnProperty("click") && data["click"] == "double") return true;
    return null;
};

exports.extractLeftSingleClick = (data) => {
    if (data.hasOwnProperty("button_left")) return data["button_left"] == "single";
    return null;
};

exports.extractLeftDoubleClick = (data) => {
    if (data.hasOwnProperty("button_left")) return data["button_left"] != "single";
    return null;
};

exports.extractSingleRightClick = (data) => {
    if (data.hasOwnProperty("button_right")) return data["button_right"] == "single";
    return null;
};

exports.extractDoubleRightClick = (data) => {
    if (data.hasOwnProperty("button_right")) return data["button_right"] != "single";
    return null;
};

exports.extractLux = (data) => {
    if (data.hasOwnProperty("lux")) return data["lux"];
    return null;
};

exports.extractPower = (data) => {
    if (data.hasOwnProperty("power")) return data["power"];
    return null;
};

exports.extractConsumption = (data) => {
    if (data.hasOwnProperty("consumption")) return data["consumption"];
    return null;
};

exports.extractMotion = (data) => {
    if (data.hasOwnProperty("occupancy")) return data["occupancy"];
    return null;
};