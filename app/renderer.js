let SIDEBAR_ON_TOGGLE = false;

function getImageLocation(img_name) {
    return "/image/" + img_name;
}

function getVideoLocation(video_name) {
    return "/video/" + video_name
}

function getThumbNailLocation(video_name) {
    return "/thumbnail/" + video_name
}


function displayMedia(imageScores, videoScores) {
    console.log(imageScores);
    console.log(videoScores);
    const imgList = document.getElementById("img-list");
    imgList.innerHTML = '';

    const imagesAndVideosToBeRendered = [];
    imageScores.forEach(function (imageScore) {
        const imageLoc = getImageLocation(imageScore[0]);
        const imageText = imageScore[0];
        console.log(imageLoc, imageText);
        // use same image as thumbnail
        imagesAndVideosToBeRendered.push({src: imageLoc, srct: imageLoc, title: imageText, description: "Image"})
    });

    //pushing videos
    videoScores.forEach(function (videoScore) {
        // videoScore is of the structure [video_src_path, [(score, frame_number, timestamp in s),....]]
        const videoLoc = getVideoLocation(videoScore[0]);
        const videoText = videoScore[0];
        const thumbNailName = "watermarked_" + videoScore[0] + "_frame_1.jpg";
        console.log(videoLoc, videoText, thumbNailName)

        imagesAndVideosToBeRendered.push({
            src: videoLoc,
            srct: getThumbNailLocation(thumbNailName),
            title: videoText,
            description: "Video"
        })
    });

    function getTimestamp(src, videoScores) {
        console.log(">>>>>>")
        console.log(src)
        var timestamp = 0
        videoScores.forEach(function(videoScore) {
            // videoScore is of the structure [video_src_path, [(score, frame_number, timestamp in s),....]]
            var videoSrc = ("http://0.0.0.0:5001/video/"+videoScore[0]).replaceAll(' ',"%20")
            console.log(videoSrc, videoSrc === src)
            if(videoSrc === src) {
                const score = videoScore[1][0][0]
                if(score !== -1) {
                    timestamp = videoScore[1][0][2]
                }
            }
        })
        return timestamp
    }

    imgList.addEventListener("click", function (){
            var videoElement = document.getElementsByTagName("video")
            console.log(`video Elements size ->${videoElement.length}`)
            var timeStamp = getTimestamp(videoElement[1].getElementsByTagName("source")[0].src, videoScores)
            console.log(`time -> ${timeStamp}`)
            videoElement[1].currentTime = timeStamp
    })

    if (imagesAndVideosToBeRendered.length == 0) {
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
        items: imagesAndVideosToBeRendered
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
    displayMedia(data.image_results, data.video_results);
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