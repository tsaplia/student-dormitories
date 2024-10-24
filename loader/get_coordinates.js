const fs = require("fs");
const { exit } = require("process");

const URL = "https://nominatim.openstreetmap.org/search"

fs.readFile("../data/data.json", "utf8", async (err, text) => {
    if (err) {
        console.log("Error reading file from disk:", err);
        exit();
    }
    
    data = JSON.parse(text);
    await addCordsData(data);
    writeFullData(data);
});

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// nominatim request
function getCords(adress){
    let query = adress.replace(" ", "+");
    return fetch(`${URL}?q=${query}&format=jsonv2`)
    .then(response => {
        if(!response.ok) throw new Error("Bad response status: "+response.status);
        return response.json();
    }).then(json=>{
        if(json.length === 0) throw new Error("No resuls found");
        box = json[0]["boundingbox"];
        return [box[0], box[2]];
    });
}

async function addCordsData(json){
    for(let i=0; i<json.length; i++){
        let [lat, lon] = await getCords(json[i]["adress"]);
        json[i]["lat"] = lat;
        json[i]["lon"] = lon;
        await sleep(1000)
    }
}

function writeFullData(json){
    text = JSON.stringify(json, null, 2);
    fs.writeFile('../data/full_data.json', text, err => {
        if (err) {
            console.log('Error writing file', err);
        } else {
            console.log('Successfully wrote file');
        }
    });
}
