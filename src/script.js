const layer = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
});

let map = new L.map('map' , {
    center: [52.517106, 13.407627],
    zoom: 12,
    layers: [layer]
});

setMarkers();

async function setMarkers(){
    let locations = await getData();

    locations.forEach(el => {
        let marker = new L.Marker([el.lat,el.lon]).addTo(map);
        marker.on("mouseover",event =>{
            event.target.bindPopup(createPopupContent(el), {closeButton: false}).openPopup();
        });
        marker.on("mouseout", event => {
            event.target.closePopup();
        });
        marker.on("click" , () => {
            window.open(el.url);
        });
    });
}

function getData(){
    return fetch('data/full_data.json')
        .then(response => response.json())
        .catch(err => {
            console.error('Error loading the JSON:', err);
            return []
        });
}

function createPopupContent(el) {
    let content = `<div class="card"><h3>${el.title}</h3><ul>`
    el["apartments"].forEach(a=>{
        content +=  "<li>"+
                    `<span class="info">${a.people} Personen (${a.price})</span><br>`+
                    `<span class="waiting">${a.waiting}</span>`+
                    "</li>"
    });
    content += "</ul></div>";
    return content;
}