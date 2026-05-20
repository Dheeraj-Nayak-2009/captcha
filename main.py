from flask import Flask, Response, render_template_string
import time
import random
import string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Totally Human Verification</title>

<style>

*{
    box-sizing:border-box;
}

body{
    margin:0;
    background:#f1f3f4;
    font-family:Arial,sans-serif;

    height:100vh;

    display:flex;
    justify-content:center;
    align-items:center;

    overflow:hidden;
}

.box{
    width:440px;

    background:white;

    border-radius:14px;

    padding:30px;

    box-shadow:
        0 20px 50px rgba(0,0,0,0.1);
}

h2{
    margin-top:0;
}

.verify{
    border:2px solid #ddd;

    padding:22px;

    border-radius:10px;

    display:flex;
    align-items:center;

    gap:15px;

    position:relative;
}

.checkbox{
    width:30px;
    height:30px;

    border:2px solid #777;

    border-radius:4px;

    cursor:pointer;

    display:flex;
    justify-content:center;
    align-items:center;

    font-size:20px;

    user-select:none;

    transition:0.2s;
}

.checkbox:hover{
    transform:scale(1.05);
}

.loader{
    width:24px;
    height:24px;

    border:3px solid #ddd;
    border-top:3px solid #4285f4;

    border-radius:50%;

    animation:spin 1s linear infinite;

    display:none;
}

@keyframes spin{
    to{
        transform:rotate(360deg);
    }
}

.status{
    margin-top:20px;

    min-height:30px;

    color:#666;

    line-height:1.5;
}

.big-warning{
    margin-top:16px;

    color:#d93025;

    font-weight:bold;

    font-size:14px;
}

.popup{
    position:fixed;

    inset:0;

    background:rgba(0,0,0,0.6);

    display:none;

    justify-content:center;
    align-items:center;

    z-index:999;
}

.popup-content{
    width:440px;

    background:white;

    border-radius:14px;

    padding:25px;
}

button{
    padding:12px 18px;

    border:none;

    background:#4285f4;

    color:white;

    border-radius:8px;

    cursor:pointer;

    font-size:15px;

    margin-top:10px;
}

button:hover{
    opacity:0.9;
}

input{
    width:100%;

    padding:14px;

    margin-top:15px;

    border-radius:8px;

    border:1px solid #ccc;

    font-size:16px;
}

.taskBox{
    margin-top:15px;

    padding:14px;

    background:#f8f9fa;

    border-radius:8px;

    font-size:14px;

    color:#444;
}

.redPulse{
    animation:redPulse 0.6s infinite;
}

@keyframes redPulse{
    0%{color:#d93025;}
    50%{color:#ff0000;}
    100%{color:#d93025;}
}

.fakeMetrics{
    margin-top:20px;

    font-size:13px;

    color:#888;

    line-height:1.8;
}

.glitch{
    animation:glitch 0.08s infinite;
}

@keyframes glitch{
    0%{transform:translate(1px,0);}
    25%{transform:translate(-1px,1px);}
    50%{transform:translate(1px,-1px);}
    75%{transform:translate(-1px,0);}
    100%{transform:translate(1px,1px);}
}

</style>
</head>
<body>

<div class="box" id="mainBox">

    <h2>Human Verification</h2>

    <div class="verify">

        <div class="checkbox" id="checkbox"></div>

        <div class="loader" id="loader"></div>

        <div>
            <strong>I am probably human</strong>
        </div>

    </div>

    <div class="status" id="status"></div>

    <div
        class="big-warning"
        id="warningText">

        Verification required for the sake of humanity.

    </div>

    <div class="fakeMetrics">

        Humanity Score:
        <span id="humanityScore">2%</span>
        <br>

        Cursor Stability:
        unstable
        <br>

        Emotional Ping:
        482ms
        <br>

        Organic Confidence:
        questionable

    </div>

</div>

<div class="popup" id="popup">

    <div class="popup-content">

        <h3>
            Advanced Human Verification
        </h3>

        <div class="taskBox" id="taskText">

        </div>

        <button
            id="downloadBtn"
            onclick="downloadFile()">

            Download Verification Image

        </button>

        <input
            id="answer"
            placeholder="Enter text from image..."
        >

        <button onclick="submitAnswer()">

            Verify Humanity

        </button>

    </div>

</div>

<script>

const checkbox =
    document.getElementById("checkbox");

const loader =
    document.getElementById("loader");

const popup =
    document.getElementById("popup");

const status =
    document.getElementById("status");

const warningText =
    document.getElementById("warningText");

const taskText =
    document.getElementById("taskText");

const humanityScore =
    document.getElementById("humanityScore");

let rotations = 0;

let lastAngle = null;

let accumulatedRotation = 0;

let rotationTaskActive = false;

let touchTaskActive = false;

let downloading = false;

const isTouch =
    "ontouchstart" in window ||
    navigator.maxTouchPoints > 0;

const weirdMessages = [

    "Human hesitation detected.",

    "Your vibes are statistically unusual.",

    "Calibrating soul resonance...",

    "Organic movement confidence low.",

    "The server hamster is exhausted.",

    "Please cooperate emotionally.",

    "Behavior resembles a microwave.",

    "Authenticating carbon-based lifeform..."

];

function randomMessage(){

    return weirdMessages[
        Math.floor(
            Math.random() * weirdMessages.length
        )
    ];
}

checkbox.addEventListener("click", () => {

    if(rotationTaskActive ||
       touchTaskActive ||
       downloading) return;

    warningText.classList.add("redPulse");

    if(isTouch){

        touchTaskActive = true;

        let taps = 0;

        status.innerText =
            "Suspicious touchscreen detected.";

        warningText.innerText =
            "Tap all four corners of the screen.";

        const touched = {};

        function handleTouch(e){

            const x = e.touches[0].clientX;
            const y = e.touches[0].clientY;

            const w = window.innerWidth;
            const h = window.innerHeight;

            if(x < 100 && y < 100)
                touched.tl = true;

            if(x > w-100 && y < 100)
                touched.tr = true;

            if(x < 100 && y > h-100)
                touched.bl = true;

            if(x > w-100 && y > h-100)
                touched.br = true;

            taps =
                Object.keys(touched).length;

            status.innerText =
                "Corner verification: " +
                taps + "/4";

            if(taps >= 4){

                document.removeEventListener(
                    "touchstart",
                    handleTouch
                );

                touchTaskActive = false;

                startVerification();
            }
        }

        document.addEventListener(
            "touchstart",
            handleTouch
        );

    }else{

        rotationTaskActive = true;

        status.innerText =
            "Suspiciously efficient click.";

        warningText.innerText =
            "Mandatory wrist exercises required.";

        status.innerText =
            "Rotate your cursor around the checkbox 10 times.";
    }
});

document.addEventListener("mousemove", e => {

    if(!rotationTaskActive) return;

    const rect =
        checkbox.getBoundingClientRect();

    const cx =
        rect.left + rect.width / 2;

    const cy =
        rect.top + rect.height / 2;

    const dx = e.clientX - cx;
    const dy = e.clientY - cy;

    const angle =
        Math.atan2(dy, dx);

    if(lastAngle !== null){

        let delta =
            angle - lastAngle;

        if(delta > Math.PI)
            delta -= Math.PI * 2;

        if(delta < -Math.PI)
            delta += Math.PI * 2;

        accumulatedRotation += delta;

        if(Math.abs(accumulatedRotation)
            > Math.PI * 2){

            rotations++;

            accumulatedRotation = 0;

            humanityScore.innerText =
                (rotations * 7) + "%";

            status.innerText =
                "Athletic verification: " +
                rotations + "/10 rotations";

            if(Math.random() < 0.3){

                status.innerText +=
                    " • " + randomMessage();
            }

            if(rotations >= 10){

                rotationTaskActive = false;

                startVerification();
            }
        }
    }

    lastAngle = angle;
});

function startVerification(){

    checkbox.style.display = "none";

    loader.style.display = "block";

    status.innerText =
        "Analyzing behavioral integrity...";

    let metrics = 0;

    const fakeScan = setInterval(() => {

        metrics++;

        humanityScore.innerText =
            (metrics * 9) + "%";

        status.innerText =
            randomMessage();

        if(Math.random() < 0.25){

            document.body.classList.add(
                "glitch"
            );

            setTimeout(() => {

                document.body.classList.remove(
                    "glitch"
                );

            }, 120);
        }

        if(metrics >= 11){

            clearInterval(fakeScan);

            loader.style.display = "none";

            popup.style.display = "flex";

            taskText.innerHTML = `

                Humanity confidence:
                <strong>4%</strong>

                <br><br>

                Download the encrypted image.

                <br><br>

                The image contains a hidden
                verification phrase.

                <br><br>

                Failure may disappoint the server.

            `;
        }

    }, 800);
}

function downloadFile(){

    downloading = true;

    status.innerText =
        "Starting encrypted download...";

    document.getElementById(
        "downloadBtn"
    ).innerText =
        "Downloading...";

    setInterval(() => {

        status.innerText =
            randomMessage();

    }, 1500);

    window.location.href = "/download";
}

function submitAnswer(){

    const value =
        document.getElementById("answer").value;

    if(value.trim().length !== 6){

        alert(
            "Verification failed. Humanity unclear."
        );

        return;
    }

    popup.style.display = "none";

    checkbox.style.display = "flex";

    checkbox.innerHTML = "✓";

    warningText.innerText =
        "Human verified successfully.";

    warningText.classList.remove(
        "redPulse"
    );

    humanityScore.innerText = "100%";

    status.innerText =
        "Congratulations. You are slightly organic.";
}

</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/download")
def download():

    def generate():

        total_size = 1024 * 1024 * 8

        sent = 0

        while sent < total_size:

            chunk = ''.join(
                random.choices(
                    string.ascii_letters +
                    string.digits,
                    k=1
                )
            ).encode()

            yield chunk

            sent += len(chunk)

            # THROTTLE
            time.sleep(0.01)

    return Response(
        generate(),
        headers={
            "Content-Disposition":
                "attachment; filename=verification_image.jpg",

            "Content-Type":
                "image/jpeg"
        }
    )

if __name__ == "__main__":
    app.run(debug=True)
