import json
import re

# Read grouped data
with open('vocab_game.json', 'r') as f:
    categories = json.load(f)

# Structure for JS:
# const LEVELS = [
#   { id: 'level_0', name: 'Intro', words: [...] }
# ]

game_data = []
for idx, cat in enumerate(categories):
    # Only keep empty categories out? Or maybe some are empty?
    if not cat['words']:
        continue
        
    game_data.append({
        "id": f"level_{idx}",
        "name": cat['name'],
        "words": cat['words'],
        "count": len(cat['words'])
    })


html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>🇫🇷 French Arcade</title>
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700;900&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
    
    <!-- Confetti -->
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>

    <style>
        :root {
            /* Palette: Vibrant Pop */
            --bg: #121212;
            --surface: #1E1E1E;
            --primary: #FF00FF; /* Magenta */
            --secondary: #00FFFF; /* Cyan */
            --tertiary: #FFE600; /* Yellow */
            --text-main: #FFFFFF;
            --text-dim: #AAAAAA;
            --success: #00FF99;
            --error: #FF3333;
            
            --border-radius: 16px;
            --border-width: 3px;
        }

        * {
            box-sizing: border-box;
            user-select: none; /* App-like feel */
            -webkit-tap-highlight-color: transparent;
        }

        body {
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            /* Cool subtle grid pattern */
            background-image: radial-gradient(var(--surface) 15%, transparent 16%);
            background-size: 20px 20px;
        }

        /* --- UTILS --- */
        .hidden { display: none !important; }
        .flex-center { display: flex; justify-content: center; align-items: center; }
        .full-screen { width: 100%; height: 100%; position: absolute; top:0; left:0; overflow-y: auto; }
        .btn-push { transition: transform 0.1s; }
        .btn-push:active { transform: scale(0.95); }

        /* --- SCREENS --- */
        /* Level Select */
        #screen-levels {
            padding: 20px;
            padding-bottom: 80px; /* scroll space */
        }
        
        .header-big {
            font-size: 2.5em;
            font-weight: 900;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 20px 0 10px 0;
            text-align: center;
            letter-spacing: -2px;
        }
        
        .sub-header {
            text-align: center;
            color: var(--text-dim);
            margin-bottom: 30px;
            font-family: 'Space Mono', monospace;
            font-size: 0.9em;
        }

        .level-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 15px;
            max-width: 600px;
            margin: 0 auto;
        }

        .level-card {
            background: var(--surface);
            border: 2px solid #333;
            border-radius: var(--border-radius);
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            transition: all 0.2s;
            position: relative;
            overflow: hidden;
        }
        
        .level-card:hover {
            border-color: var(--secondary);
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0, 255, 255, 0.2);
        }

        .level-info h3 { margin: 0; font-size: 1.2em; font-weight: 700; }
        .level-info span { font-size: 0.8em; color: var(--text-dim); font-family: 'Space Mono', monospace; }
        
        .level-score {
            font-size: 1.5em;
            opacity: 0.5; /* dim until played */
        }
        .level-score.done { opacity: 1; text-shadow: 0 0 10px var(--tertiary); }


        /* Game UI */
        #screen-game {
            display: flex;
            flex-direction: column;
            max-width: 600px;
            margin: 0 auto;
            position: relative;
            background: rgba(18, 18, 18, 0.9);
        }

        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 20px;
            border-bottom: 2px solid #333;
        }

        .btn-icon {
            background: none;
            border: 2px solid #555;
            color: white;
            width: 40px; height: 40px;
            border-radius: 50%;
            font-size: 1.2em;
            cursor: pointer;
        }

        .progress-container {
            flex-grow: 1;
            margin: 0 15px;
            height: 10px;
            background: #333;
            border-radius: 5px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--secondary), var(--primary));
            width: 0%;
            transition: width 0.3s;
        }

        .lives {
            font-size: 1.5em;
            letter-spacing: 2px;
        }

        /* Question Card */
        .game-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
            position: relative;
        }

        .card-stack {
            position: relative;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .flash-card {
            background: var(--surface);
            border: var(--border-width) solid var(--primary);
            border-radius: 24px;
            padding: 40px 20px;
            width: 100%;
            text-align: center;
            box-shadow: 10px 10px 0px rgba(255, 0, 255, 0.2);
            margin-bottom: 40px;
            animation: float 6s ease-in-out infinite;
        }
        
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }

        .q-label {
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--secondary);
            font-size: 0.8em;
            margin-bottom: 10px;
            display: block;
            font-weight: 700;
        }

        .q-text {
            font-size: 2.2em;
            font-weight: 900;
            line-height: 1.1;
            color: white;
        }

        /* Input Zone */
        .input-zone {
            width: 100%;
            max-width: 400px;
            position: relative;
        }

        input {
            width: 100%;
            background: transparent;
            border: none;
            border-bottom: 3px solid #555;
            color: white;
            font-size: 2em;
            text-align: center;
            font-family: 'Outfit', sans-serif;
            padding: 10px;
            outline: none;
            transition: border-color 0.3s;
        }
        
        input:focus { border-color: var(--tertiary); }
        input.correct { border-color: var(--success); color: var(--success); }
        input.wrong { border-color: var(--error); color: var(--error); }

        /* Keyboard Helper (Accents) */
        .keyboard-row {
            display: flex;
            gap: 8px;
            justify-content: center;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        
        .key-btn {
            background: #333;
            color: white;
            border: none;
            border-radius: 8px;
            width: 40px; height: 40px;
            font-size: 1.1em;
            font-family: 'Outfit', sans-serif;
            cursor: pointer;
            box-shadow: 0 4px 0 #111;
        }
        .key-btn:active {
            transform: translateY(4px);
            box-shadow: none;
        }

        .main-btn {
            background: var(--secondary);
            color: var(--bg);
            border: none;
            padding: 15px 0;
            width: 100%;
            max-width: 400px; /* match input */
            margin-top: 30px;
            border-radius: 50px;
            font-size: 1.2em;
            font-weight: 900;
            text-transform: uppercase;
            cursor: pointer;
            box-shadow: 0 4px 0 rgba(0,255,255,0.5);
            font-family: 'Space Mono', monospace;
        }
        .main-btn:active { transform: translateY(2px); box-shadow: 0 2px 0 rgba(0,255,255,0.5); }
        
        /* Modals / Overlays */
        .overlay {
            background: rgba(0,0,0,0.95);
            z-index: 100;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 40px;
            opacity: 0; pointer-events: none; transition: opacity 0.3s;
        }
        .overlay.active { opacity: 1; pointer-events: auto; }
        
        .result-title { font-size: 3em; margin: 0; }
        .result-score { font-size: 5em; font-weight: 900; color: var(--tertiary); margin: 20px 0; }
        
        .toggle-switch {
           position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
           background: #333; padding: 10px 20px; border-radius: 30px;
           display: flex; gap: 10px; align-items: center;
           z-index: 50;
           font-size: 0.8em;
           border: 1px solid #555;
        }
        
        .mic-btn {
            position: absolute;
            right: 0; top: 10px;
            background: transparent; border: none; font-size: 1.5em; opacity: 0.5;
            cursor: pointer;
        }

    </style>
</head>
<body>

    <!-- LEVEL SELECT SCREEN -->
    <div id="screen-levels" class="full-screen">
        <div class="header-big">FRENCH<br>ARCADE</div>
        <div class="sub-header">CHOOSE YOUR MISSION</div>
        
        <div id="level-container" class="level-grid">
            <!-- Injected by JS -->
        </div>
        
        <div class="toggle-switch">
             <span>��🇸 ➔ 🇫🇷</span>
        </div>
    </div>

    <!-- GAME SCREEN -->
    <div id="screen-game" class="full-screen hidden">
        <div class="top-bar">
            <button class="btn-icon btn-push" onclick="exitGame()">✕</button>
            <div class="progress-container">
                <div class="progress-fill" id="progress-bar"></div>
            </div>
            <div class="lives" id="lives-display">❤️❤️❤️</div>
        </div>

        <div class="game-area">
            <div class="flash-card">
                <span class="q-label" id="q-label">Translate</span>
                <div class="q-text" id="q-text">...</div>
                <button class="mic-btn" onclick="speakCurrent()" id="mic-btn">🔈</button>
            </div>

            <div class="input-zone">
                <input type="text" id="g-input" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" placeholder="...">
            </div>

            <div class="keyboard-row">
                <button class="key-btn" onclick="typeKey('é')">é</button>
                <button class="key-btn" onclick="typeKey('è')">è</button>
                <button class="key-btn" onclick="typeKey('à')">à</button>
                <button class="key-btn" onclick="typeKey('ç')">ç</button>
                <button class="key-btn" onclick="typeKey('ê')">ê</button>
                <button class="key-btn" onclick="typeKey('ô')">ô</button>
            </div>

            <button class="main-btn btn-push" id="action-btn" onclick="checkAnswer()">CHECK IT</button>
             <div id="feedback-msg" style="height: 20px; margin-top: 10px; color: var(--tertiary); font-weight: bold;"></div>
        </div>
    </div>

    <!-- RESULTS OVERLAY -->
    <div id="screen-result" class="full-screen overlay">
        <h1 class="result-title" id="res-title">LEVEL COMPLETE</h1>
        <div class="result-score" id="res-score">100%</div>
        <div style="margin-bottom: 40px; color: #aaa;" id="res-sub">Perfect run!</div>
        <button class="main-btn btn-push" onclick="exitGame()">BACK TO MENU</button>
    </div>

<script>
    // DATA
    const DATA = ##JSON_DATA##;

    // STATE
    let currentLevel = null;
    let queue = [];
    let currentIndex = 0;
    let lives = 3;
    let score = 0;
    let correctCount = 0;
    
    // DOM
    const elLevels = document.getElementById('level-container');
    const elScreenLevels = document.getElementById('screen-levels');
    const elScreenGame = document.getElementById('screen-game');
    const elScreenResult = document.getElementById('screen-result');
    const elInput = document.getElementById('g-input');
    const elActionBtn = document.getElementById('action-btn');
    const elFeedback = document.getElementById('feedback-msg');
    
    // SOUNDS (Simple Synth)
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    let audioCtx = new AudioCtx();
    
    function playTone(type) {
        if(audioCtx.state === 'suspended') audioCtx.resume();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        
        if (type === 'success') {
            osc.type = 'sine';
            osc.frequency.setValueAtTime(500, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(1000, audioCtx.currentTime + 0.1);
            gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
            osc.start(); osc.stop(audioCtx.currentTime + 0.3);
        } else if (type === 'error') {
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(200, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(100, audioCtx.currentTime + 0.2);
            gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
            osc.start(); osc.stop(audioCtx.currentTime + 0.3);
        }
    }

    // INIT
    function init() {
        renderLevels();
        
        elInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') handleAction();
        });
    }

    function renderLevels() {
        elLevels.innerHTML = '';
        DATA.forEach((cat, idx) => {
            const div = document.createElement('div');
            div.className = 'level-card btn-push';
            div.onclick = () => startLevel(idx);
            
            // Check if saved score exists (mock)
            const saved = localStorage.getItem('cassia_score_' + idx);
            const status = saved ? '🔥' : '🔒'; // Just a visual, all unlocked for now
            const opacity = saved ? 'done' : '';
            
            div.innerHTML = `
                <div class="level-info">
                    <h3>${cat.name}</h3>
                    <span>${cat.count} WORDS</span>
                </div>
                <div class="level-score ${opacity}">${saved || ''} ${status}</div>
            `;
            elLevels.appendChild(div);
        });
    }

    // GAME LOGIC
    function startLevel(idx) {
        currentLevel = DATA[idx];
        // Shuffle words
        queue = [...currentLevel.words].sort(() => Math.random() - 0.5);
        // Take max 10 for a "round" to keep it snappy? Or all?
        // Let's do batches of 10 if list > 15
        if (queue.length > 15) queue = queue.slice(0, 15);
        
        currentIndex = 0;
        lives = 3;
        correctCount = 0;
        
        updateLives();
        elScreenLevels.classList.add('hidden');
        elScreenGame.classList.remove('hidden');
        elScreenResult.classList.remove('active');
        elScreenResult.classList.add('hidden'); // ensure hidden
        
        loadCard();
    }

    function exitGame() {
        elScreenGame.classList.add('hidden');
        elScreenResult.classList.remove('active');
        elScreenLevels.classList.remove('hidden');
        renderLevels(); // update scores
    }

    function updateLives() {
        let hearts = "";
        for(let i=0; i<lives; i++) hearts += "❤️";
        document.getElementById('lives-display').innerText = hearts;
    }

    function loadCard() {
        const item = queue[currentIndex];
        document.getElementById('q-text').innerText = item.english;
        document.getElementById('q-label').innerText = "TRANSLATE TO FRENCH";
        
        // Reset input
        elInput.value = '';
        elInput.className = '';
        elInput.disabled = false;
        elInput.focus();
        
        elFeedback.innerText = '';
        elActionBtn.innerText = "CHECK IT";
        elActionBtn.onclick = checkAnswer;
        
        // Update bar
        const pct = (currentIndex / queue.length) * 100;
        document.getElementById('progress-bar').style.width = pct + '%';
        
        // Hide mic until answered? Or show? Show but play french?
        // Right now prompt is English. Mic checks textContent of q-text... 
        // We want mic to play FRENCH.
        // So we store the french text
        elInput.dataset.target = item.french;
        elInput.dataset.clean = item.french.replace(/\(.*\)/, '').trim();
    }

    function normalize(str) {
        return str.toLowerCase().replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").trim().replace(/\s{2,}/g," ");
    }

    function handleAction() {
        if (elActionBtn.innerText === "NEXT") {
            nextCard();
        } else {
            checkAnswer();
        }
    }

    function checkAnswer() {
        const userRaw = elInput.value.trim();
        const userNorm = normalize(userRaw);
        if (!userNorm) return;

        const item = queue[currentIndex];
        const targets = item.french.split(/[,\/]/).map(normalize);
        // Also add clean version without parens
        targets.push(normalize(item.french.replace(/\(.*\)/, '').trim()));

        // Validate
        // Check fuzzy match for gender?
        const articleRegex = /^(le |la |l'|un |une |des |les )/i;
        const strip = s => s.replace(articleRegex, '').trim();
        
        let correct = targets.some(t => t === userNorm);
        let almost = false;
        
        if (!correct) {
            // Check without article
            const baseUser = normalize(strip(userRaw));
            const baseTargets = targets.map(t => normalize(strip(t)));
            if (baseTargets.includes(baseUser)) {
                almost = true;
            }
        }

        if (correct) {
            success();
        } else if (almost) {
            elInput.classList.add('wrong');
            elFeedback.innerText = "Check the gender (le/la/un/une)!";
            playTone('error');
            // Don't reduce lives for gender mistake? Or yes? 
            // Let's be nice. No heart loss, but must fix.
        } else {
            fail(item.french);
        }
    }

    function success() {
        playTone('success');
        elInput.classList.add('correct');
        elActionBtn.innerText = "NEXT";
        elActionBtn.onclick = nextCard;
        confetti({
            particleCount: 50,
            spread: 60,
            origin: { y: 0.7 },
            colors: ['#00FFFF', '#FF00FF']
        });
        correctCount++;
        speakRaw(elInput.dataset.clean);
    }

    function fail(correctText) {
        playTone('error');
        lives--;
        updateLives();
        elInput.classList.add('wrong');
        elFeedback.innerText = correctText;
        elActionBtn.innerText = "NEXT";
        elActionBtn.onclick = nextCard;
        
        speakRaw(elInput.dataset.clean); // Let them hear it

        if (lives <= 0) {
            setTimeout(gameOver, 1000);
        }
    }

    function nextCard() {
        currentIndex++;
        if (currentIndex >= queue.length) {
            levelComplete();
        } else {
            loadCard();
        }
    }

    function levelComplete() {
        const pct = Math.round((correctCount / queue.length) * 100);
        document.getElementById('res-title').innerText = "MISSION CLEAR";
        document.getElementById('res-score').innerText = pct + "%";
        document.getElementById('res-sub').innerText = lives === 3 ? "FLAWLESS VICTORY" : "Good job!";
        
        elScreenResult.classList.remove('hidden');
        setTimeout(() => elScreenResult.classList.add('active'), 10);
        
        // Save score
        localStorage.setItem('cassia_score_' + DATA.indexOf(currentLevel), pct + '%');
        
        confetti({
            particleCount: 200,
            spread: 100,
            origin: { y: 0.6 }
        });
    }

    function gameOver() {
        document.getElementById('res-title').innerText = "GAME OVER";
        document.getElementById('res-score').innerText = "💀";
        document.getElementById('res-sub').innerText = "Don't give up! Try again.";
        elScreenResult.classList.remove('hidden');
        setTimeout(() => elScreenResult.classList.add('active'), 10);
    }

    // UTILS
    function typeKey(char) {
        elInput.value += char;
        elInput.focus();
    }
    
    function speakRaw(text) {
        const u = new SpeechSynthesisUtterance(text);
        u.lang = 'fr-FR';
        window.speechSynthesis.speak(u);
    }
    
    function speakCurrent() {
        speakRaw(elInput.dataset.clean);
    }

    // Boot
    window.onload = init;

</script>
</body>
</html>
"""

html_content = html_template.replace('##JSON_DATA##', json.dumps(game_data))

with open('CassiaFrenchGame.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Created CassiaFrenchGame.html")
