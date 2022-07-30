function getImageLocation(img_path){
    var temp = img_path.split("/");
    return "/image/" + temp[temp.length - 1];
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
    results.style.display = 'block';

    $("#results-meta-text").html("");
    let innerHTML = "Relevant Results: " + data.results.length + " / " + data.total_images +" images<br>";
    if(data.row_id >= 0){
        innerHTML += "<div class='feedback row middle-xs center-xs'><div class='ui inverted button icon green feedback-btn' data-feedback='positive'><i class='green thumbs up icon' style='pointer-events: none'></i></div><div class='ui inverted button icon red feedback-btn' data-feedback='negative'><i class='red thumbs down icon' style='pointer-events: none'></i></div></div><p id='thanks' style='display:none'>Thanks for the feedback!</p>";
    }
    $("#results-meta-text").html(innerHTML);
    $(".feedback-btn").click((e)=>{
        const feedback = $(e.target).attr("data-feedback");
        const requestBody = {"row_id": data.row_id, "feedback": feedback};
        const url = "/feedback";
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        }).then(function(response) {
            return response.json();
        }).then(function(data) {
            $("#thanks").show();
            $(".feedback").remove();
        }).catch(function(e) {
            console.log(e);
        });
    })
    displayImages(data.results);
}

function getEmbedding(){
    const text = document.getElementById('search-bar').value.trim();
    console.log("Query: ", text);
    url = "/search?text="+text;
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

const indexerStatusLabel = document.getElementById("indexer-status-label")
function performUpdate(data) {
    let status_list = data.split('_')
    let percentage = String(Math.floor(Number(status_list[0])/Number(status_list[1])*100))
    $('#indexer-progress').progress({
        percent: percentage
    });
    indexerStatusLabel.innerHTML = String(status_list[0]) + "/" + String(status_list[1]) + " images indexed"
}

function updateIndexerProgress() {
    fetch("/indexer-progress").then(response => response.text()).then(text => performUpdate(text))
}
setInterval(updateIndexerProgress, 300)

window.onload = function initStuff(){
    displayPrompts();
    $('#indexer-progress').progress({
        percent: 0
    });
    $('.checkbox').checkbox('check');
    $('#ham').click(()=>{
        $('#sidebar').toggle();
    });
    getEmbedding();
} 
