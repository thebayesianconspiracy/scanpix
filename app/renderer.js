function isElectron(){
    if (typeof navigator === 'object' && typeof navigator.userAgent === 'string' && navigator.userAgent.indexOf('Electron') >= 0) {
        return true;
    }
    return false;
}

function getImageLocation(img_path){
    if (isElectron()){
        return "file://" + img_path;
    } 
    else {
        var temp = img_path.split("/");
        return "/image/" + temp[temp.length - 1];
    }
}

function getQueryURL(){
    if (isElectron()){
        return "http://0.0.0.0:5001";
    } 
    else {
        return "";
    }
}

function createCard(img, text){
    var cardDiv = document.createElement("div");
    var imageDiv = document.createElement("div");
    var image = document.createElement("img");
    var contentDiv = document.createElement("div");
    var content = document.createElement("span");
    
    cardDiv.className = 'card';
    imageDiv.className = 'image';
    imageDiv.style.height = "200px";
    image.setAttribute("data-src", img);
    image.style.objectFit = 'cover';
    contentDiv.className = 'extra content';
    content.innerHTML = text;

    contentDiv.appendChild(content);
    imageDiv.appendChild(image);
    cardDiv.appendChild(imageDiv);
    cardDiv.appendChild(contentDiv);
    return cardDiv;
}

function displayImages(imageScores){
    const imgList = document.getElementById("img-list");
    imgList.innerHTML = '';
    
    imageScores.forEach(function (item, index) {
        console.log(item);
        const itemLoc = getImageLocation(item[1]);
        console.log(itemLoc);
        const itemText = item[0] + ": " + String(Math.round(item[2] * 100.0) / 100.0);
        imgList.appendChild(createCard(itemLoc, itemText))
    });

    $('.image img')
    .visibility({
        type       : 'image',
        transition : 'fade in',
        duration   : 1000
    });
}


function displayResult(data){
    const results = document.getElementById("results-meta");
    const resultsText = document.getElementById("results-meta-text");
    results.style.display = 'block';
    resultsText.innerHTML = "Relevant Results: " + data.results.length + " / " + data.total_images +" images";
    displayImages(data.results);
}

function getEmbedding(){
    const text = document.getElementById('search-bar').value;
    console.log("Query: ", text)
    url = getQueryURL() + "/search?text="+text;
    fetch(url).then(function(response) {
        return response.json();
    }).then(function(data) {
        console.log("Number of relevant results: ", data.results.length);
        console.log("Total images: ", data.total_images);
        displayResult(data);
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
    if(e.key === 'Enter'){
        getEmbedding();
    }
})
