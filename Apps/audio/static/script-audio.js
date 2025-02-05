document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("uploadFormBase").addEventListener("submit", uploadBase);
    document.getElementById("uploadFormOverlay").addEventListener("submit", uploadOverlay);
  });
  
  // Map button "effects" to the Flask endpoints
  function updateAudio(effect) {
    var overlaySection = document.getElementById("overlay-section");
    var audioSource = document.getElementById("audio-source");
    var audioPlayer = document.getElementById("audio-player");
  
    // Routes for each effect
    let effectsMap = {
      "play":    "/play-audio",
      "reverse": "/filter/reverse",
      "bass":    "/filter/bass",
      "treble":  "/filter/treble",
      "echo":    "/filter/echo",
      "overlay": "/filter/overlay"
    };
  
    // If we only want to show the overlay form
    if (effect === "showOverlay") {
      overlaySection.style.display = "block";
      return;
    } else {
      overlaySection.style.display = "none";
    }
  
    // If this is one of our known effects, fetch & play
    if (effectsMap[effect]) {
      audioSource.src = effectsMap[effect];
      audioPlayer.load();
      audioPlayer.play();
    }
  }
  
  // Called by "Apply Overlay" button to display the upload form
  function showOverlayUpload() {
    updateAudio("showOverlay");
  }
  
  // Upload Base Audio
  function uploadBase(event) {
    event.preventDefault();
    var formData = new FormData();
    var fileInput = document.getElementById("baseFile");
    formData.append("file", fileInput.files[0]);
  
    fetch("/upload", { method: "POST", body: formData })
      .then(response => response.json())
      .then(data => {
        if (data.status === "success") {
          // After uploading base, automatically play it
          updateAudio("play");
        } else {
          alert("Error: " + data.message);
        }
      })
      .catch(error => {
        console.error("Upload error:", error);
        alert("Upload failed.");
      });
  }
  
  // Upload Overlay Audio
  function uploadOverlay(event) {
    event.preventDefault();
    var formData = new FormData();
    var fileInput = document.getElementById("overlayFile");
    formData.append("overlay_file", fileInput.files[0]);
  
    fetch("/upload-overlay", { method: "POST", body: formData })
      .then(response => response.json())
      .then(data => {
        if (data.status === "success") {
          // Once overlay is uploaded, apply the overlay effect
          updateAudio("overlay");
        } else {
          alert("Error: " + data.message);
        }
      })
      .catch(error => {
        console.error("Upload error:", error);
        alert("Upload failed.");
      });
  }
  