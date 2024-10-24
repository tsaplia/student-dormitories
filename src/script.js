const layer = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
});

let map = new L.map('map' , {
    center: [52.517106, 13.407627],
    zoom: 13,
    layers: [layer]
});

setMarkers();

async function setMarkers(){
    let locations = await getData();

    locations.forEach(el => {
        let marker = new L.Marker([el.lat,el.lon]).addTo(map);
        marker.on("mouseover",event =>{
            event.target.bindPopup('<div class="card"><h3>'+el.title+'</h3></div>', {closeButton: false}).openPopup();
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