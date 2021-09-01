var audio = document.querySelectorAll('audio');
var playButton = document.querySelectorAll('.play');
var forwardButton = document.querySelectorAll('.forward');
var backwardButton = document.querySelectorAll('.backward');
var seekBar = document.querySelectorAll('.seek');

var lengthTimer = document.querySelectorAll('.length-timer');
var durationTimer = document.querySelectorAll('.duration-timer');

var seeking = false;
var playing = undefined;

function updateProgress(i) {
	var duration = audio[i].duration;
	var multiplier = 100 / duration;
	var currentTime = audio[i].currentTime;
	seekBar[i].value = currentTime * multiplier;

	durationTimer[i].innerHTML = timeForSeconds(audio[i].currentTime);
}

function padTime(timer) {
	if (timer < 10) {
		return "0" + timer;
	}
	return timer;
}

function timeForSeconds(seconds) {
	var hours = padTime(Math.floor(((seconds/86500)%1)*24));
	var minutes = padTime(Math.floor(((seconds/3600)%1)*60));
	var seconds = padTime(Math.round(((seconds/60)%1)*60));
	return (
		hours + ":" + minutes + ":" + seconds
	);
}

function handleSeek(e, i) {
	seeking = true;
	var seekPosition = e.target.value / 100;
	var playFrom = audio[i].duration * seekPosition;
	handleAudioPlayback(i, playFrom);
	updateProgress(i);
}

function handleButtonClicked(i, time) {
	if (playing === undefined) {
		playing = i;
	}
	handleAudioPlayback(i, time);
}

function handleSkip(timestamp, i) {
	seeking = true;
	var playFrom = timestamp;
	handleAudioPlayback(i, playFrom);
	updateProgress(i);
}

function handleAudioPlayback(i, time) {
	var seekPosition = seekBar[i].value;
	if (playing !== i && !seeking) {
		audio[playing].pause();
		playing = i;
	}
	if (seeking) {
		audio[i].currentTime = time;
		seeking = false;
	} else if (audio[i].paused) {
		audio[i].play();
		playButton[i].innerHTML = "<svg width=\'30px\' height=\'30px\' viewBox=\'0 0 4267 4267\'><g id=\'Layer1\'><g transform=\'matrix(1.35841,0,0,1,127.132,-10.9882)\'><rect x=\'519.872\' y=\'192.448\' width=\'613.461\' height=\'3899.22\' /></g><g transform=\'matrix(1.35841,0,0,1,1793.8,-10.9882)\'><rect x=\'519.872\' y=\'192.448\' width=\'613.461\' height=\'3899.22\' /></g></g></svg>";
	} else {
		audio[i].pause();
		playButton[i].innerHTML = "<svg width=\'30px\' height=\'30px\' viewBox=\'0 0 4267 4267\'><g transform=\'matrix(-0.000548567,1.15446,-0.84241,-0.000400289,3881.96,-576.737)\'><path d=\'M2348.86,168.164L4039.58,3979.17L658.134,3979.17L2348.86,168.164Z\' /></g></svg>";
	}
}

audio.forEach((node, i) => {
	node.addEventListener('timeupdate', function(e) {
		updateProgress(i);
	});
	node.addEventListener('loadedmetadata', function() {
		lengthTimer[i].innerHTML = padTime(timeForSeconds(audio[i].duration));
	})
	seekBar[i].addEventListener('change', function(e) {
		handleSeek(e, i);
	});
	playButton[i].addEventListener('click', function(e) {
		handleButtonClicked(i, 0);
	});
	forwardButton[i].addEventListener('click', function(e) {
		var timestamp = Math.round(audio[i].currentTime)+30;
		handleSkip(timestamp, i);
	});
	backwardButton[i].addEventListener('click', function(e) {
		var timestamp = Math.round(audio[i].currentTime)-30;
		handleSkip(timestamp, i);
	});
})
