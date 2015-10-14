// This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = $('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;                             // iframe player object

// Interactive page content
var playpauseButton = $("#play-pause"); // play/pause button
var button_icon = playpauseButton.find('span');
var prevButton = $("#prev");            // previous video button
var nextButton = $("#next");            // next video button
var img_link = $("#img-link");          // link to current video
var img = $("#sidebar-img");            // video thumbnail image
var time_display = $("#timeholder");    // text display of current time
var dur_display = $("#duration");       // text display of song duration
var play_slider = $("#player-slider");  // slider for player scrubbing
var vol_slider = $("#volume-slider");   // slider for volume control

var shuffle_button = $("#shuffle");     // button for shuffling playlist order
var shuffle_icon = shuffle_button.find('span');

var loop_button = $("#loop");           // button for loop on playlist and song
var loop_icon = loop_button.find('span');

var song_name_artist = $("#song-name-artist");

// Player flags
var loop = 0
var shuffle = false;

// Resize the table whenever the window is resized
$(window).resize(function() {
    $('.header-fixed > tbody').css('height', ($(window).height() - 200) + 'px');
    $('.playlist-table').css('width', (0.8 * $(window).width()) + 'px');
    $('.sidebar').css('width', (0.2 * $(window).width()) + 'px');
});
$(window).resize();

// This function creates an <iframe> (and YouTube player)
// after the API code downloads.
function onYouTubeIframeAPIReady() {
    player = new YT.Player('player', {
        playerVars: {'controls': 0},
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange,
            'onError': onPlayerError
        }
    });
}

// The API will call this function when the video player is ready.
function onPlayerReady(event) {
    // video_ids is a list of video ids that is filled out by django templating
    player.cuePlaylist(video_ids)

    // Event listeners for playlist control buttons
    playpauseButton.click(function() {
        state = player.getPlayerState();
        if (state === 1) {
            player.pauseVideo();
        } else {
            player.playVideo();
        }
    });
    
    nextButton.click(function() {
        player.nextVideo();
    });

    
    // If the current time is below three seconds, move to the previous video
    // otherwise, play the current video from the beginning
    prevButton.click(function() {
        if (player.getCurrentTime() <= 3) {
            player.previousVideo();
        } else {
            player.seekTo(0, true);
            player.playVideo();
        }
    });

    // var shuffle = false;
    // shuffle_button.click(function() {
    //     shuffle = !shuffle;

    // });

    loop_button.click(function() {
        loop = (loop + 1) % 3;
        switch (loop) {
            case 0:
                loop_button.removeClass('active');
                loop_icon.attr('class', 'icon icon-loop2');
                player.setLoop(false);
                break;
            // The playlist will restart on completion
            case 1:
                loop_button.addClass('active');
                loop_icon.attr('class', 'icon icon-loop2 active');
                player.setLoop(true);
                break;
            // A single video will play continuously
            case 2:
                loop_icon.attr('class', 'icon icon-infinite active');
        }
    });

    // Create a JQuery-UI slider for volume control
    $(function() {
        vol_slider.slider({
            value: 100,
            min: 0,
            max: 100,
            range: "min",
            change: function(event, ui) { player.setVolume(ui.value); },
            slide: function(event, ui) { player.setVolume(ui.value); }
        });
    });

    // Create a JQuery-UI slider for scrubbing through the video
    $(function() {
        play_slider.slider({
            value: 0,
            min: 0,
            max: 100,
            range: "min",
            change: function(event, ui) {
                if (event.originalEvent) {
                    player.seekTo(ui.value, true);
                    player.playVideo();
                }
            },
            slide: function(event, ui) {
                player.pauseVideo();
            }
        });
    });

    // Go through the table and add click events to each row
    var rows = $("#song-table").find("tr");

    if (rows != null) {
        rows.each(function(index, row) {
            $(row).dblclick(function(event) {
                button_icon.attr('class', 'glyphicon glyphicon-pause');
                loadImage(index);
                songID(index);
                $(row).addClass('highlight').siblings().removeClass('highlight'); 
            })
        });
    }

    loadImage(0);  // Load the image for the first song in the playlist
}

// The API will call this function whenever the state of the player changes
var secondTimer;
function onPlayerStateChange(event) {

    // This event is thrown as soon as the video begins to load
    if (event.data === -1) {
        var index = player.getPlaylistIndex();
        loadImage(index);
        var time = Math.floor(player.getDuration());
        var clockTime = getClockTime(time);
        dur_display.text(clockTime);
        time_display.text('0:00');
        play_slider.slider('option', 'value', 0);
        play_slider.slider('option', 'max', time);

        var row = $("#song-table").find("tr")[index]
        var data = $(row).find("td");
        var name = $(data[0]).text();
        var artist = $(data[1]).text();

        song_name_artist.text(name + ' - ' + artist);
    }

    if (event.data === 0) {
        if (loop == 2) {
            player.playVideo();
        }
    }

    // While the video is playing, update the timer
    if (event.data === YT.PlayerState.PLAYING) {
        setButtonPause();
        secondTimer = setInterval(function() {
            var time = Math.floor(player.getCurrentTime());
            var clockTime = getClockTime(time);
            time_display.text(clockTime);
            play_slider.slider('option', 'value', time);
        }, 100);
    } else {
        setButtonPlay();
        clearInterval(secondTimer)
    }
}

function onPlayerError(event) {
    switch (event.data) {
        case 2:
            console.log("Invalid video id.");
            break;
        case 5:
            console.log("Problem with the html5 player.");
            break;
        case 100:
            console.log("Video requested was not found.");
            break;
        case 101:
            console.log("The owner of this video does not allow embedded playback.");
            break;
        case 150:
            console.log("The owner of this video does not allow embedded playback.");
            break;
        default:
            console.log("There has been an unexpected error in playing this video.");
            break;
    }
}

// Play a video from the playlist at a given index
function songID(index) {
    player.playVideoAt(index);
}

// Load the thumbnail image and link for a given video index
function loadImage(index) {
    var video_id = video_ids[index];
    img.attr('src', 'https://i3.ytimg.com/vi/' + video_id + '/default.jpg');
    img_link.attr('href', 'https://youtube.com/watch?v=' + video_id);
}

// Take in the player time in seconds and return a string presenting the time
function getClockTime(time) {
    var minutes = Math.floor(time / 60);  // integer division
    var seconds = time % 60;
    if (seconds < 10)
        seconds = '0' + seconds;
    var clockTime = minutes + ":" + seconds;
    return clockTime;
}

function setButtonPlay() {
    button_icon.attr('class', 'glyphicon glyphicon-play');
}

function setButtonPause() {
    button_icon.attr('class', 'glyphicon glyphicon-pause');
}
