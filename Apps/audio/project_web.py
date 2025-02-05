from flask import Flask, Response, request, render_template, jsonify
from pydub import AudioSegment
from pydub.effects import low_pass_filter, high_pass_filter
import io

app = Flask(__name__, template_folder="templates", static_folder="static")

# Store references to the uploaded audio segments
base_audio = None
overlay_audio = None

@app.route("/")
def home():
    return render_template("index-audio.html")

# --------------------------------------------------
#                  Upload Endpoints
# --------------------------------------------------
@app.route("/upload", methods=["POST"])
def upload_file():
    """Upload the base audio."""
    global base_audio
    file = request.files.get("file")

    if not file:
        return jsonify({"status": "error", "message": "No file uploaded"})

    try:
        # Load into a Pydub AudioSegment
        base_audio = AudioSegment.from_file(file, format=file.filename.split(".")[-1])
        return jsonify({"status": "success", "message": "Base audio uploaded"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/upload-overlay", methods=["POST"])
def upload_overlay():
    """Upload the overlay audio."""
    global overlay_audio
    file = request.files.get("overlay_file")

    if not file:
        return jsonify({"status": "error", "message": "No overlay file uploaded"})

    try:
        # Load into a Pydub AudioSegment
        overlay_audio = AudioSegment.from_file(file, format=file.filename.split(".")[-1])
        return jsonify({"status": "success", "message": "Overlay audio uploaded"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# --------------------------------------------------
#                  Basic Playback
# --------------------------------------------------
@app.route("/play-audio")
def play_audio():
    """Return the base audio as MP3."""
    global base_audio
    if base_audio is None:
        return jsonify({"status": "error", "message": "No base audio uploaded"})

    buffer = io.BytesIO()
    base_audio.export(buffer, format="mp3")
    buffer.seek(0)
    return Response(buffer, mimetype="audio/mpeg")

# --------------------------------------------------
#                  Filters
# --------------------------------------------------
@app.route("/filter/reverse")
def filter_reverse():
    """Reverse the base audio."""
    global base_audio
    if base_audio is None:
        return jsonify({"status": "error", "message": "No base audio uploaded"})

    try:
        reversed_audio = base_audio.reverse()

        buffer = io.BytesIO()
        reversed_audio.export(buffer, format="mp3")
        buffer.seek(0)
        return Response(buffer, mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/filter/bass")
def filter_bass():
    """Apply a simple bass boost: 
       1) Low-pass filter to isolate low frequencies
       2) Boost them by a few dB
       3) Overlay back onto the original
    """
    global base_audio
    if base_audio is None:
        return jsonify({"status": "error", "message": "No base audio uploaded"})

    try:
        # Low-pass filter around ~200 Hz (adjust as needed)
        lows = low_pass_filter(base_audio, cutoff=200)
        # Boost the low-freq portion by +6 dB (adjust as desired)
        lows = lows + 6
        # Overlay boosted lows onto the original
        bass_boosted = base_audio.overlay(lows)

        buffer = io.BytesIO()
        bass_boosted.export(buffer, format="mp3")
        buffer.seek(0)
        return Response(buffer, mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/filter/treble")
def filter_treble():
    """Apply a simple treble boost:
       1) High-pass filter to isolate high frequencies
       2) Boost them
       3) Overlay back onto the original
    """
    global base_audio
    if base_audio is None:
        return jsonify({"status": "error", "message": "No base audio uploaded"})

    try:
        # High-pass filter around ~3000 Hz (adjust as needed)
        highs = high_pass_filter(base_audio, cutoff=3000)
        # Boost high freq portion by +6 dB (adjust as desired)
        highs = highs + 6
        # Overlay boosted highs onto the original
        treble_boosted = base_audio.overlay(highs)

        buffer = io.BytesIO()
        treble_boosted.export(buffer, format="mp3")
        buffer.seek(0)
        return Response(buffer, mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/filter/echo")
def filter_echo():
    """Apply a simple echo effect:
       - We'll overlay repeated, attenuated copies of the track with some delay.
    """
    global base_audio
    if base_audio is None:
        return jsonify({"status": "error", "message": "No base audio uploaded"})

    try:
        # Quick "echo" hack: overlay repeated, quieter versions offset in time
        output = base_audio
        attenuated = base_audio - 9  # reduce volume ~9 dB for each repeat
        delay_ms = 500  # half-second delay
        repeats = 2

        for i in range(1, repeats + 1):
            output = output.overlay(attenuated, position=delay_ms * i)

        buffer = io.BytesIO()
        output.export(buffer, format="mp3")
        buffer.seek(0)
        return Response(buffer, mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/filter/overlay")
def apply_overlay():
    """Overlay the second audio (overlay_audio) on top of base_audio."""
    global base_audio, overlay_audio
    if base_audio is None or overlay_audio is None:
        return jsonify({"status": "error", "message": "Base or overlay audio missing"})

    try:
        mixed_audio = base_audio.overlay(overlay_audio, position=0)
        buffer = io.BytesIO()
        mixed_audio.export(buffer, format="mp3")
        buffer.seek(0)
        return Response(buffer, mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# --------------------------------------------------
#                Run the Flask App
# --------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
