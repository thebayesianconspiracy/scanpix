function createCard(img, text){
    var cardDiv = document.createElement("div");
    var imageDiv = document.createElement("div");
    var image = document.createElement("img");
    var contentDiv = document.createElement("div");
    var content = document.createElement("span");
    
    cardDiv.className = 'card';
    imageDiv.className = 'image';
    image.setAttribute("data-src", img);
    image.setAttribute("height", 400);
    contentDiv.className = 'extra content';
    content.innerHTML = text;

    contentDiv.appendChild(content);
    imageDiv.appendChild(image);
    cardDiv.appendChild(imageDiv);
    cardDiv.appendChild(contentDiv);
    return cardDiv;
}

function displayImages(imageScores){
    const img_location = "file:///home/nuwandavek/Documents/rocketship/scanpix/data/images/";
    const imgList = document.getElementById("img-list");
    imgList.innerHTML = '';
    console.log(imageScores);
    imageScores = imageScores.sort((a, b) => { return b[1] - a[1] } )
    console.log(imageScores);
    
    imageScores.forEach(function (item, index) {
        const itemLoc = img_location + item[0];
        const itemText = item[0] + ": " + String(Math.round(item[1] * 100.0) / 100.0);
        imgList.appendChild(createCard(itemLoc, itemText))
    });

    $('.image img')
    .visibility({
        type       : 'image',
        transition : 'fade in',
        duration   : 1000
    })
;
}

function getEmbedding(){
    const text = document.getElementById('search-bar').value;
    url = "http://0.0.0.0:5001/search?text="+text;
    fetch(url).then(function(response) {
        return response.json();
    }).then(function(data) {
        // console.log(data);
        displayImages(data);
    }).catch(function(e) {
        console.log(e);
    });
}

const searchBtn = document.getElementById('search-button');
searchBtn.addEventListener('click', () => {
    getEmbedding();
})
const searchBar = document.getElementById('search-bar');
searchBar.addEventListener('keydown', (e) => {
    console.log(e.key);
    if(e.key === 'Enter'){
        getEmbedding();
    }
})
