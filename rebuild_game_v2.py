import json

with open('vocab_game_clean.json', 'r') as f:
    categories = json.load(f)

game_data = []
for idx, cat in enumerate(categories):
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
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>🇫🇷 French Arcade</title>
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700;900&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
    
    <!-- Confetti -->
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>

    <style>
        :root {
            --bg: #121212;
            --surface: #1E1E1E;
            --primary: #FF00FF;
            --secondary: #00FFFF;
            --tertiary: #FFE600;
            --text: #FFFFFF;
            --dim: #888888;
            --success: #00FF99;
            --error: #FF3333;
            --radius: 16px;
        }

        /* RESET */
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        body {
            font-family: 'Outfit', sans-serif;
            background: var(--bg);
            color: var(--text);
            margin: 0; padding: 0;
            height: 100vh; overflow: hidden;
            display: flex; flex-direction: column;
            background-image: radial-gradient(#222 15%, transparent 16%);
            background-size: 20px 20px;
        }
        
        button { border: none; outline: none; font-family: inherit; }
        .hidden { display: none !important; }

        /* SCREENS */
        #screen-levels, #screen-game, #screen-result {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            display: flex; flex-direction: column;
            overflow-y: auto;
        }
        
        /* LEVEL SELECT */
        #screen-levels { padding: 20px; padding-bottom: 100px; }
        .header {
            font-size: 2.5rem; font-weight: 900; text-align: center;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin: 20px 0 5px;
        }
        .sub-header { text-align: center; color: var(--dim); margin-bottom: 20px; font-family: 'Space Mono', monospace; font-size: 0.9em; }

        .grid { display: grid; grid-template-columns: 1fr; gap: 15px; max-width: 600px; margin: 0 auto; width: 100%; }
        .level-card {
            background: var(--surface);
            border: 2px solid #333;
            border-radius: var(--radius);
            padding: 20px;
            display: flex; justify-content: space-between; align-items: center;
            cursor: pointer; transition: transform 0.1s;
        }
        .level-card:active { transform: scale(0.98); border-color: var(--secondary); }
        .level-info h3 { margin: 0; font-size: 1.1rem; }
        .level-info span { font-size: 0.8rem; color: var(--dim); font-family: 'Space Mono'; }
        .level-score { font-size: 1.2rem; opacity: 0.5; }

        /* SETTINGS TOGGLE */
        .mode-toggle {
            position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
            background: #222; padding: 10px 20px; border-radius: 50px;
            border: 1px solid #444; z-index: 999;
            display: flex; align-items: center; gap: 10px; cursor: pointer;
            box-shadow: 0 10px 20px rgba(0,0,0,0.5);
            transition: all 0.2s;
        }
        .mode-toggle:active { transform: translateX(-50%) scale(0.95); background: #333; }
        .flag { font-size: 1.2rem; }
        .arrow { color: var(--dim); font-weight: bold; }

        /* GAME SCREEN */
        #screen-game { background: rgba(18,18,18,0.98); }
        .top-bar {
            display: flex; justify-content: space-between; align-items: center;
            padding: 15px; max-width: 600px; margin: 0 auto; width: 100%;
        }
        .exit-btn { font-size: 1.5rem; color: var(--dim); background: none; padding: 5px; cursor: pointer; }
        .progress-track { flex: 1; height: 6px; background: #333; margin: 0 15px; border-radius: 3px; overflow: hidden; }
        .progress-fill { height: 100%; background: linear-gradient(90deg, var(--secondary), var(--primary)); width: 0%; transition: width 0.3s; }
        .hearts { font-size: 1.2rem; letter-spacing: 2px; }

        .game-content {
            flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center;
            padding: 20px; max-width: 600px; margin: 0 auto; width: 100%;
        }

        .card-box {
            position: relative;
            background: var(--surface);
            border: 3px solid var(--primary);
            border-radius: 20px;
            padding: 30px;
            width: 100%;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            margin-bottom: 30px;
            /* Float animation */
            animation: float 4s ease-in-out infinite;
        }
        @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-8px); } 100% { transform: translateY(0px); } }

        .label { display: block; color: var(--secondary); font-size: 0.8rem; letter-spacing: 1px; margin-bottom: 10px; text-transform: uppercase; font-weight: 700; }
        .word-text { font-size: 2.2rem; font-weight: 800; line-height: 1.1; margin-bottom: 10px; word-break: break-word;}
        
        .mic-btn {
            background: #333; color: white; border-radius: 50%; width: 50px; height: 50px;
            font-size: 1.5rem; display: flex; justify-content: center; align-items: center;
            margin: 0 auto; cursor: pointer; transition: background 0.2s;
            margin-top: 10px;
        }
        .mic-btn:active { background: var(--secondary); color: black; }

        /* INPUT */
        .input-group { width: 100%; position: relative; }
        input {
            width: 100%; background: transparent; border: none;
            border-bottom: 3px solid #444; color: white;
            font-size: 1.8rem; text-align: center; padding: 10px;
            font-family: 'Outfit'; font-weight: 500;
        }
        input:focus { border-color: var(--secondary); }
        input.correct { border-color: var(--success); color: var(--success); }
        input.wrong { border-color: var(--error); color: var(--error); }

        .accents {
            display: flex; justify-content: center; gap: 8px; margin-top: 15px; flex-wrap: wrap;
        }
        .key {
            background: #333; color: white; width: 36px; height: 36px; border-radius: 8px;
            font-size: 1.1rem; display: flex; justify-content: center; align-items: center;
            cursor: pointer; box-shadow: 0 3px 0 #111;
        }
        .key:active { transform: translateY(3px); box-shadow: none; }

        .action-btn {
            background: var(--secondary); color: black;
            font-family: 'Space Mono'; font-weight: 700; font-size: 1.2rem;
            width: 100%; padding: 18px; border-radius: 50px;
            margin-top: 30px; cursor: pointer;
            box-shadow: 0 5px 0 rgba(0,255,255,0.4);
            text-transform: uppercase;
        }
        .action-btn:active { transform: translateY(2px); box-shadow: 0 2px 0 rgba(0,255,255,0.4); }

        .feedback { text-align: center; min-height: 20px; margin-top: 10px; color: var(--tertiary); font-weight: bold; }

        /* RESULTS */
        #screen-result {
            background: rgba(0,0,0,0.95); justify-content: center; align-items: center; text-align: center; padding: 40px;
        }

    </style>
</head>
<body>

    <!-- LEVEL SELECT -->
    <div id="screen-levels">
        <div class="header">ARCADE 2.0</div>
        <div class="sub-header">SELECT MISSION</div>
        <div id="grid" class="grid"></div>

        <div class="mode-toggle" onclick="toggleMode()">
            <span class="flag" id="flag-src">🇺🇸</span>
            <span class="arrow">➔</span>
            <span class="flag" id="flag-dest">🇫🇷</span>
            <span style="font-size: 0.8rem; color: #aaa; margin-left: 5px;">TAP TO SWITCH</span>
        </div>
    </div>

    <!-- GAME -->
    <div id="screen-game" class="hidden">
        <div class="top-bar">
            <button class="exit-btn" onclick="exitGame()">✕</button>
            <div class="progress-track"><div class="progress-fill" id="bar"></div></div>
            <div class="hearts" id="hearts">❤️❤️❤️</div>
        </div>

        <div class="game-content">
            <div class="card-box">
                <span class="label" id="q-label">TRANSLATE</span>
                <div class="word-text" id="q-text">...</div>
                <div class="mic-btn" onclick="playAudio()" id="btn-audio">🔊</div>
            </div>

            <div class="input-group">
                <input type="text" id="inp" placeholder="..." autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
                <div class="accents" id="accent-bar">
                    <div class="key" onclick="typeKey('é')">é</div>
                    <div class="key" onclick="typeKey('è')">è</div>
                    <div class="key" onclick="typeKey('à')">à</div>
                    <div class="key" onclick="typeKey('ç')">ç</div>
                    <div class="key" onclick="typeKey('ê')">ê</div>
                    <div class="key" onclick="typeKey('ô')">ô</div>
                </div>
            </div>
            
            <div class="feedback" id="feedback"></div>
            <button class="action-btn" id="btn-action" onclick="check()">CHECK</button>
        </div>
    </div>

    <!-- RESULT -->
    <div id="screen-result" class="hidden">
        <h1 style="font-size: 3rem; margin:0;" id="res-title">CLEARED</h1>
        <div style="font-size: 6rem; font-weight: 900; color: var(--secondary); margin: 20px 0;" id="res-pct">100%</div>
        <button class="action-btn" onclick="exitGame()" style="max-width:300px;">MENU</button>
    </div>

<script>
    const DATA = ##JSON_DATA##;
    
    // STATE
    let mode = 'en_fr'; // or 'fr_en'
    let currentLevel = null;
    let queue = [];
    let currentIdx = 0;
    let score = 0;
    let lives = 3;
    let gameState = 'ready'; // ready, answered
    let audioText = ""; // Text to speak

    // ELEMENT REFS
    const elGrid = document.getElementById('grid');
    const elGame = document.getElementById('screen-game');
    const elLevels = document.getElementById('screen-levels');
    const elResult = document.getElementById('screen-result');
    const elInput = document.getElementById('inp');
    const elFeedback = document.getElementById('feedback');
    const elAction = document.getElementById('btn-action');
    const elAudioBtn = document.getElementById('btn-audio');
    
    // INIT
    window.onload = () => {
        renderLevels();
        initVoices();
    };

    function initVoices() {
        // Force load voices
        window.speechSynthesis.getVoices();
    }

    function toggleMode() {
        if (mode === 'en_fr') {
            mode = 'fr_en';
            document.getElementById('flag-src').innerText = '🇫🇷';
            document.getElementById('flag-dest').innerText = '🇺🇸';
        } else {
            mode = 'en_fr';
            document.getElementById('flag-src').innerText = '🇺🇸';
            document.getElementById('flag-dest').innerText = '🇫🇷';
        }
        // Save pref?
    }

    function renderLevels() {
        elGrid.innerHTML = '';
        DATA.forEach((L, i) => {
            const d = document.createElement('div');
            d.className = 'level-card';
            d.onclick = () => startGame(i);
            
            const saved = localStorage.getItem(`score_${i}_${mode}`);
            const badge = saved ? `<span>${saved}</span>` : '<span>PLAY</span>';
            
            d.innerHTML = `
                <div class="level-info"><h3>${L.name}</h3><span>${L.count} words</span></div>
                <div class="level-score">${badge}</div>
            `;
            elGrid.appendChild(d);
        });
    }

    function startGame(idx) {
        currentLevel = DATA[idx];
        // Shuffle & Slice
        let all = [...currentLevel.words].sort(() => Math.random() - .5);
        queue = all.slice(0, 15); // max 15 per round
        
        currentIdx = 0; lives = 3; gameState = 'ready';
        updateUI();
        
        elLevels.classList.add('hidden');
        elGame.classList.remove('hidden');
        elResult.classList.add('hidden');
        
        loadCard();
    }

    function loadCard() {
        gameState = 'ready';
        const item = queue[currentIdx];
        
        elInput.value = '';
        elInput.className = '';
        elInput.disabled = false;
        elInput.focus();
        elFeedback.innerText = '';
        elAction.innerText = 'CHECK';
        
        // Mode Logic
        if (mode === 'en_fr') {
            // ENGLISH -> FRENCH
            document.getElementById('q-label').innerText = "TRANSLATE TO FRENCH";
            document.getElementById('q-text').innerText = item.english;
            document.getElementById('accent-bar').style.display = 'flex';
            
            // Audio button hidden during guessing? 
            // Better: plays prompts? No prompt is English.
            // Target is French. Playing it reveals answer. Hide until answered.
            elAudioBtn.style.visibility = 'hidden';
            audioText = item.french; // store for later
            
        } else {
            // FRENCH -> ENGLISH
            document.getElementById('q-label').innerText = "TRANSLATE TO ENGLISH";
            document.getElementById('q-text').innerText = item.french;
            document.getElementById('accent-bar').style.display = 'none'; // No accents needed for English input
            
            // Audio visible immediately to help pronunciation
            elAudioBtn.style.visibility = 'visible';
            audioText = item.french;
        }

        updateProgress();
        updateLives();
    }

    function playAudio() {
        // Robust Player
        if(!audioText) return;
        
        // Clean text (remove parens)
        const clean = audioText.replace(/\(.*\)/, '').trim();
        
        // Cancel prev
        window.speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(clean);
        utterance.lang = 'fr-FR';
        utterance.rate = 0.9; // slightly slower for learning
        
        // Fallback voice selection
        const voices = window.speechSynthesis.getVoices();
        const frVoice = voices.find(v => v.lang.includes('fr'));
        if (frVoice) utterance.voice = frVoice;

        window.speechSynthesis.speak(utterance);
    }
    
    // Auto-typing listener
    elInput.addEventListener('keypress', (e) => {
        if(e.key === 'Enter') check();
    });

    function normalize(s) {
        return s.toLowerCase().replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").trim();
    }

    function check() {
        if (gameState === 'answered') {
            next();
            return;
        }

        const userVal = normalize(elInput.value);
        if (!userVal) return;
        
        const item = queue[currentIdx];
        let correct = false;
        let answerText = "";
        
        if (mode === 'en_fr') {
            // Checking French
            // Split options loop
            // Handle: "l'acteur/actrice" -> ["l'acteur", "actrice"]
            // Also raw: "l'acteur/actrice"
            let targets = item.french.split(/[,\/]/).map(normalize);
            targets.push(normalize(item.french.replace(/\(.*\)/,'')));
            
            if (targets.some(t => t === userVal)) correct = true;
            answerText = item.french;
            
        } else {
            // Checking English
            let targets = item.english.split(/[,\/]/).map(normalize);
            if (targets.some(t => t === userVal)) correct = true;
            answerText = item.english;
        }

        if (correct) {
            handleSuccess();
        } else {
            // Fuzzy logic for En->Fr Gender?
            if(mode === 'en_fr' && checkGenderError(userVal, item.french)) {
                elFeedback.innerText = "Check gender/article!";
                return; // Let them retry!
            }
            handleFail(answerText);
        }
        
        gameState = 'answered';
        elAction.innerText = 'CONTINUE';
    }

    function checkGenderError(user, target) {
        // Strip articles from both
        const clean = s => s.replace(/^(le |la |l'|un |une |des )/i, '').trim();
        const baseUser = clean(user);
        
        let targets = target.split(/[,\/]/).map(normalize).map(clean);
        return targets.includes(baseUser);
    }

    function handleSuccess() {
        playTone(600, 'sine');
        confetti({ origin: {y:0.6}, particleCount: 50 });
        elInput.classList.add('correct');
        score++;
        
        // Reveal audio button if hidden
        elAudioBtn.style.visibility = 'visible';
        // Auto play audio if French was the target
        if(mode === 'en_fr') setTimeout(playAudio, 200);
    }

    function handleFail(ans) {
        playTone(200, 'sawtooth');
        lives--;
        updateLives();
        elInput.classList.add('wrong');
        elFeedback.innerText = ans; // Show correct answer
        
        elAudioBtn.style.visibility = 'visible';
        if(mode === 'en_fr') setTimeout(playAudio, 200);
        
        if (lives <= 0) setTimeout(gameOver, 1000);
    }

    function next() {
        currentIdx++;
        if (currentIdx >= queue.length) {
            winLevel();
        } else {
            loadCard();
        }
    }

    function winLevel() {
        const pct = Math.round((score / queue.length) * 100) + '%';
        // Save header
        // use original unsliced length? Nah, just save result of this session
        localStorage.setItem(`score_${DATA.indexOf(currentLevel)}_${mode}`, pct);
        
        document.getElementById('res-title').innerText = "CLEARED!";
        document.getElementById('res-pct').innerText = pct;
        elGame.classList.add('hidden');
        elResult.classList.remove('hidden');
        confetti({ particleCount: 150, spread: 100 });
    }

    function gameOver() {
        document.getElementById('res-title').innerText = "GAME OVER";
        document.getElementById('res-pct').innerText = "💀";
        elGame.classList.add('hidden');
        elResult.classList.remove('hidden');
    }

    function exitGame() {
        elGame.classList.add('hidden');
        elResult.classList.add('hidden');
        elLevels.classList.remove('hidden');
        renderLevels();
    }

    function updateProgress() {
        document.getElementById('bar').style.width = ((currentIdx / queue.length) * 100) + '%';
    }
    
    function updateLives() {
        document.getElementById('hearts').innerText = "❤️".repeat(lives);
    }
    
    // Synth Sound
    const actx = new (window.AudioContext || window.webkitAudioContext)();
    function playTone(freq, type) {
        if(actx.state === 'suspended') actx.resume();
        const osc = actx.createOscillator();
        const g = actx.createGain();
        osc.connect(g); g.connect(actx.destination);
        osc.type = type;
        osc.frequency.value = freq;
        g.gain.value = 0.1;
        osc.start();
        g.gain.exponentialRampToValueAtTime(0.00001, actx.currentTime + 0.3);
        osc.stop(actx.currentTime + 0.3);
    }

    function typeKey(k) {
        elInput.value += k;
        elInput.focus();
    }
</script>
</body>
</html>
"""

html_content = html_template.replace('##JSON_DATA##', json.dumps(game_data))

with open('FrenchArcade.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Built FrenchArcade.html")
