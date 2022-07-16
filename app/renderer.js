function getImageLocation(img_path){
    var temp = img_path.split("/");
    return "/image/" + temp[temp.length - 1];
}

function getQueryURL(){ 
    if (window.location.href.includes('localhost')) {
        console.log("isDev");
        return "http://0.0.0.0:8000";
    }
    else {
        return "http://0.0.0.0:5001" ;
    }
}

function displayImages(imageScores){
    console.log(imageScores);
    const imgList = document.getElementById("img-list");
    imgList.innerHTML = '';
    
    const items = [];
    imageScores.forEach(function (item, index) {
        const itemLoc = getImageLocation(item[1]);
        var itemText = item[0];
        // itemText = itemText + ": " + String(Math.round(item[2] * 100.0) / 100.0);
        console.log(itemLoc, itemText);
        items.push({src: itemLoc, srct: itemLoc, title: itemText})
    });

    $("#img-list").nanogallery2('destroy');
    $("#img-list").nanogallery2({
        thumbnailHeight:  300,
        thumbnailWidth:  'auto',
        itemsBaseURL:     '',
        thumbnailBorderVertical: 0,
        thumbnailBorderHorizontal: 0,
        thumbnailLabel: { valign: "bottom", position: 'overImage', align: 'left' },
        viewerGalleryTWidth: 100,
        viewerGalleryTHeight: 100,
      
        items: items
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
    const text = document.getElementById('search-bar').value.trim();
    if (text === ""){
        return '';
    }
    console.log("Query: ", text);
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

function displayPrompts() {
    const promptDiv = document.getElementById('prompts');
    const prompts = [
        "pug",
        "pug eating dinner",
        "pug with a cone",
        "waterfall",
        "outdoors"
    ]
    prompts.forEach(function (item, index) {
        var promptEle = document.createElement("a");
        promptEle.className = "ui label white prompts";
        promptEle.innerHTML = item;
        promptEle.addEventListener("click", function(){
            console.log(this.innerHTML);
            document.getElementById('search-bar').value = this.innerHTML;
            document.getElementById('search-button').click();
        })
        promptDiv.appendChild(promptEle)
    });
}

const indexerWebSocket = new WebSocket("ws://0.0.0.0:7070");
indexerWebSocket.onmessage = function (event) {
    $('#indexer-progress').progress({
        percent: event.data
    });
}

window.onload = function initStuff(){
    displayPrompts();
    $('#indexer-progress').progress({
        percent: 0
    });
    $('.checkbox')
        .checkbox('check')
}
