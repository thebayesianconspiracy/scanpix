let SIDEBAR_ON_TOGGLE = false;

function getImageLocation(img_name) {
    return "/image/" + img_name;
}

function getVideoLocation(video_name) {
    return "/video/" + video_name
}


function displayMedia(imageScores) {
    console.log(imageScores);
    const imgList = document.getElementById("img-list");
    imgList.innerHTML = '';

    const items = [];
    imageScores.forEach(function (item, index) {
        const itemLoc = getImageLocation(item[0]);
        var itemText = item[0];
        // itemText = itemText + ": " + String(Math.round(item[2] * 100.0) / 100.0);
        console.log(itemLoc, itemText);
        items.push({src: itemLoc, srct: itemLoc, title: itemText})
    });

    //pushing videos
    items.push({src: "/video/sample_1.mp4", srct: "/video/sample_1.mp4", title: "og_bunny_vid"})

    if (items.length == 0) {
        $("#no-result").show();
    } else {
        $("#no-result").hide();
    }

    $("#img-list").nanogallery2('destroy');
    $("#img-list").nanogallery2({
        thumbnailHeight: 300,
        thumbnailWidth: 'auto',
        itemsBaseURL: '',
        thumbnailBorderVertical: 0,
        thumbnailBorderHorizontal: 0,
        thumbnailLabel: {valign: "bottom", position: 'overImage', align: 'left'},
        viewerGalleryTWidth: 100,
        viewerGalleryTHeight: 100,
        items: items
    });

    $('.image img')
        .visibility({
            type: 'image',
            transition: 'fade in',
            duration: 1000
        });
}


function displayResult(data) {
    const results = document.getElementById("results-meta");
    results.style.display = 'block';

    $("#results-meta-text").html("");
    let innerHTML = "Relevant Results: " + data.result_count + " / " + data.total_images + " images<br>";
    if (data.row_id >= 0) {
        innerHTML += "<div class='feedback row middle-xs center-xs'><div class='ui button icon green feedback-btn' data-feedback='positive'><i class='thumbs up icon' style='pointer-events: none'></i></div><div class='ui button icon red feedback-btn' data-feedback='negative'><i class='thumbs down icon' style='pointer-events: none'></i></div></div><p id='thanks' style='display:none'>Thanks for the feedback!</p>";
    }
    $("#results-meta-text").html(innerHTML);
    $(".feedback-btn").click((e) => {
        const feedback = $(e.target).attr("data-feedback");
        const requestBody = {"row_id": data.row_id, "feedback": feedback};
        const url = "/feedback";
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        }).then(function (response) {
            return response.json();
        }).then(function (data) {
            $("#thanks").show();
            $(".feedback").remove();
        }).catch(function (e) {
            console.log(e);
        });
    })
    displayMedia(data.results);
}

function getEmbedding() {
    $("#spinny").show();
    const text = document.getElementById('search-bar').value.trim();
    console.log("Query: ", text);
    url = "/search?text=" + text;
    fetch(url).then(function (response) {
        return response.json();
    }).then(function (data) {
        console.log("Number of relevant results: ", data.result_count);
        console.log("Total images: ", data.total_images);
        displayResult(data);
        $("#spinny").hide();

    }).catch(function (e) {
        console.log(e);
    });
}

const searchBtn = document.getElementById('search-button');
searchBtn.addEventListener('click', () => {
    getEmbedding();
})
const searchBar = document.getElementById('search-bar');
searchBar.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        getEmbedding();
    }
})

function displayPrompts() {
    const promptDiv = document.getElementById('prompts');
    $.getScript("./constants.js").done(function () {
        console.log("prompts: ", prompts);
        prompts.forEach(function (item, index) {
            var promptEle = document.createElement("a");
            promptEle.className = "ui label white prompts";
            promptEle.innerHTML = item;
            promptEle.addEventListener("click", function () {
                console.log(this.innerHTML);
                document.getElementById('search-bar').value = this.innerHTML;
                document.getElementById('search-button').click();
                if (SIDEBAR_ON_TOGGLE) {
                    toggleit();
                }
            })
            promptDiv.appendChild(promptEle)
        });
    })

}

function toggleit() {
    SIDEBAR_ON_TOGGLE = !SIDEBAR_ON_TOGGLE;
    $("#img-list").toggle();
    $("#search-button").click();
    $('#sidebar').toggle();
    $("#ham-on").toggle();
    $("#ham-off").toggle();

}


window.onload = function initStuff() {
    displayPrompts();
    $('#indexer-progress').progress({
        percent: 100
    });
    $('.checkbox').checkbox('check');
    $('#ham').click(() => {
        toggleit();
    });
    getEmbedding();
}

/* IndexerUI Update */
const indexerStatusLabel = document.getElementById("indexer-status-label")

function performUpdate(data) {
    let status_list = data.split('_')
    let percentage = String(Math.floor(Number(status_list[0]) / Number(status_list[1]) * 100))
    $('#indexer-progress').progress({
        percent: percentage
    });
    indexerStatusLabel.innerHTML = String(status_list[0]) + "/" + String(status_list[1]) + " images indexed"
}

/* origin = http(s)://(hostname):(port)
The Socket.io client needs an origin with any http(s) protocol for the initial handshake. Web sockets don't run over the http(s) protocol, so you don't need to provide URL pathnames. */
let origin = window.location.origin;
let socket = io.connect(origin)
socket.on("connect", (event) => {
    console.log("javascript socketio client connected successfully")
})
socket.on("send_progress_to_frontend", (data) => {
    console.log(`data received for indexer progress -> ${data}`)
    performUpdate(data)
})