// Object containing key codes and corresponding audio files
const sound = {
    65: new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav"),
    87: new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav"),
    83: new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav"),
    69: new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav"),
    68: new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav"),
    70: new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav"),
    84: new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav"),
    71: new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav"),
    89: new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav"),
    72: new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav"),
    85: new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav"),
    74: new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav"),
    75: new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav"),
    79: new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav"),
    76: new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav"),
    80: new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav"),
    186: new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav")
};
console.log("loaded sounds-----------------")

// Audio file for creepy sound effect
const creepySound = new Audio("https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3?_=1")

// Object to identify top row keys
const toprow = {
    "87": 1, "69": 1, "84": 1, "89": 1, "85": 1, "79": 1, "80": 1
};

// Object to identify all letter keys
const letters = {
    "W": 1, "E": 1, "T": 1, "Y": 1, "U": 1, "O": 1, "P": 1, "A": 1, "S": 1, "D": 1, "F": 1, "G": 1, "H": 1, "J": 1, "K": 1, "L": 1, ";": 1
};

// Variable to control if sound can be played
var canPlaySound = true;

// Index for rainbow colors
var i = 0;

// Variables to store recent key presses
var recentKey1 = 0;
var recentKey2 = 0;
var recentKey3 = 0;
var recentKey4 = 0;
var recentKey5 = 0;
var recentKey6 = 0;
var recentKey7 = 0;
var recentKey8 = 0;

// Function to return the next color in the rainbow sequence
function rainbowColor() {
    const colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"];
    if (i >= colors.length) {
        i = 0;
    }
    return colors[i++];
}

// Event listener for keydown events
document.addEventListener('keydown', function(event) {
    if (sound[event.keyCode] && canPlaySound) {
        console.log(`'${String.fromCharCode(event.keyCode)}' key was pressed`);
        const audio = sound[event.keyCode].cloneNode();
        try {
            document.getElementById("key" + event.keyCode).style.backgroundColor = rainbowColor();
            // Update recent key presses
            recentKey8 = recentKey7;
            recentKey7 = recentKey6;
            recentKey6 = recentKey5;
            recentKey5 = recentKey4;
            recentKey4 = recentKey3;
            recentKey3 = recentKey2;
            recentKey2 = recentKey1;
            recentKey1 = event.keyCode;
            console.log(recentKey1, recentKey2, recentKey3, recentKey4, recentKey5, recentKey6, recentKey7, recentKey8);
            // Check for Great Old One
            if (recentKey1 == 85 && recentKey2 == 79 && recentKey3 == 89 && recentKey4 == 69 && recentKey5 == 69 && recentKey6 == 83 && recentKey7 == 69 && recentKey8 == 87) {
                canPlaySound = false;
                document.getElementById("OldOne").style.zIndex = 5;
                document.getElementById("OldOne").style.opacity = 1;
                creepySound.play();
            }
        } catch (e) {}
        audio.play();
    }
});

// Event listener for keyup events
document.addEventListener('keyup', function(event) {
    if (sound[event.keyCode]) {
        try {
            if (toprow[event.keyCode]) {
                document.getElementById("key" + event.keyCode).style.backgroundColor = "black";
            } else {
                document.getElementById("key" + event.keyCode).style.backgroundColor = "white";
            }
        } catch (e) {}
    }
});

// Event listener for mouseover events on main elements
document.querySelectorAll('main').forEach(key => {
    key.addEventListener('mouseover', function(event) {
        const keyCode = event.target.id.substring(3);
        if ((sound[keyCode] || event.target.id == "overlay") && canPlaySound) {
            console.log(`Mouse is hovering over '${String.fromCharCode(keyCode)}' key`);
            document.getElementById("overlay").style.opacity = 1;
        } else {
            document.getElementById("overlay").style.opacity = 0;
        }
    });
});
