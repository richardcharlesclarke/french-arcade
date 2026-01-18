import json
import re

# Read data
with open('vocab.json', 'r') as f:
    vocab_list = json.load(f)

# HTML Template
html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cassia's French Fun</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        :root {
            --primary: #FF6B6B;
            --secondary: #4ECDC4;
            --dark: #2C3E50;
            --light: #F7FFF7;
            --accent: #FFE66D;
            --error: #FF4757;
            --success: #2ED573;
            --warning: #FFA502;
        }
        
        * { box-sizing: border-box; }
        
        body {
            font-family: 'Nunito', sans-serif;
            margin: 0;
            padding: 0;
            min-height: 100vh;
            background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            color: var(--dark);
            overflow-x: hidden;
        }

        .container {
            width: 100%;
            max-width: 600px;
            padding: 20px;
        }

        .card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            padding: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
            position: relative;
        }

        .stats-bar {
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
            font-weight: 700;
            color: #888;
            font-size: 0.9em;
        }
        
        .question-box { margin: 30px 0; }
        
        .question-label {
            display: block;
            text-transform: uppercase;
            font-size: 0.8em;
            letter-spacing: 2px;
            color: #aaa;
            margin-bottom: 10px;
        }
        
        .question-text {
            font-size: 2.5em;
            font-weight: 900;
            color: var(--dark);
            line-height: 1.2;
            margin-bottom: 10px;
        }

        .audio-btn {
            background: none;
            border: 2px solid var(--secondary);
            color: var(--secondary);
            width: 40px;
            height: 40px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 1.2em;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-top: 10px;
        }

        .audio-btn:hover {
            background: var(--secondary);
            color: white;
            transform: scale(1.1);
        }

        .input-group { margin-bottom: 20px; }
        
        input[type="text"] {
            width: 100%;
            padding: 20px;
            border: 3px solid #eee;
            border-radius: 16px;
            font-size: 1.5em;
            text-align: center;
            font-family: 'Nunito', sans-serif;
            transition: border-color 0.3s;
            outline: none;
        }
        
        input[type="text"]:focus { border-color: var(--secondary); }
        
        input[type="text"].correct { border-color: var(--success); background-color: #eafff2; }
        input[type="text"].wrong { border-color: var(--error); background-color: #fff0f0; }
        input[type="text"].warning { border-color: var(--warning); background-color: #fffaf0; }

        .accents-bar {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        
        .accent-btn {
            background: #eee;
            border: none;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 1.1em;
            cursor: pointer;
            transition: background 0.2s;
            font-family: inherit;
        }
        
        .accent-btn:hover { background: #ddd; }

        .primary-btn {
            background: var(--primary);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 1.2em;
            border-radius: 50px;
            cursor: pointer;
            font-weight: 700;
            box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
            transition: transform 0.2s, box-shadow 0.2s;
            width: 100%;
        }
        
        .primary-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(255, 107, 107, 0.5);
        }

        .feedback {
            margin-top: 20px;
            min-height: 24px;
            font-weight: 700;
            font-size: 1.1em;
        }
        
        .feedback.success { color: var(--success); }
        .feedback.error { color: var(--error); }
        .feedback.warning { color: var(--warning); }

        .settings {
            position: absolute;
            top: 20px;
            right: 20px;
            cursor: pointer;
            opacity: 0.3;
        }
        .settings:hover { opacity: 1; }
        
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 100;
            justify-content: center;
            align-items: center;
        }
        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 20px;
            width: 90%;
            max-width: 400px;
        }

        .hidden { display: none !important; }
        
        @media (max-width: 400px) {
            .question-text { font-size: 1.8em; }
            .card { padding: 20px; }
        }
    </style>
</head>
<body>

<div class="container" id="app">
    
    <div id="settingsModal" class="modal">
        <div class="modal-content">
            <h3>Settings</h3>
            <label><input type="checkbox" id="examFilter" checked> Needed for Exam only</label>
            <br><br>
            <div style="margin-bottom: 10px;">Direction:</div>
            <label><input type="radio" name="mode" value="en_fr" checked> English -> French</label><br>
            <label><input type="radio" name="mode" value="fr_en"> French -> English</label>
            <br><br>
            <button class="primary-btn" onclick="closeSettings()" style="padding: 10px;">Save & Restart</button>
        </div>
    </div>

    <!-- Start Screen -->
    <div id="start-screen" class="card">
        <h1>Bonjour Cassia!</h1>
        <h2>Ready to practice?</h2>
        <div class="stats-bar" style="justify-content: center; gap: 20px;">
             <span><span id="total-count">0</span> words loaded</span>
        </div>
        <button class="primary-btn" onclick="startSession()">Start Quiz</button>
        <div style="margin-top: 20px; color: #888; cursor: pointer; text-decoration: underline;" onclick="openSettings()">Options</div>
    </div>

    <!-- Quiz Screen -->
    <div id="quiz-screen" class="card hidden">
        <div class="settings" onclick="openSettings()">⚙️</div>
        
        <div class="stats-bar">
            <span>Score: <span id="score">0</span></span>
            <span>Streak: <span id="streak">0</span></span>
        </div>

        <div class="question-box">
            <span class="question-label" id="q-label">Translate</span>
            <div class="question-text" id="q-text">Loading...</div>
            <button class="audio-btn" id="audio-btn" onclick="playAudioFromCard()" title="Listen">🔊</button>
        </div>

        <div class="input-group">
            <input type="text" id="answer-input" placeholder="Type here..." autocomplete="off">
        </div>

        <div class="accents-bar">
            <button class="accent-btn" onclick="typeChar('é')">é</button>
            <button class="accent-btn" onclick="typeChar('è')">è</button>
            <button class="accent-btn" onclick="typeChar('à')">à</button>
            <button class="accent-btn" onclick="typeChar('ç')">ç</button>
            <button class="accent-btn" onclick="typeChar('ê')">ê</button>
            <button class="accent-btn" onclick="typeChar('î')">î</button>
            <button class="accent-btn" onclick="typeChar('ô')">ô</button>
            <button class="accent-btn" onclick="typeChar('û')">û</button>
             <button class="accent-btn" onclick="typeChar('ë')">ë</button>
        </div>

        <button class="primary-btn" id="action-btn" onclick="handleAction()">Check</button>
        <div class="feedback" id="feedback"></div>
    </div>
</div>

<script>
    const VOCAB_DATA = ##JSON_DATA##;

    let sessionVocab = [];
    let currentItem = null;
    let score = 0;
    let streak = 0;
    let mode = 'en_fr';
    let textToSpeak = "";
    let questionState = 'input'; // 'input' or 'result'
    
    const startScreen = document.getElementById('start-screen');
    const quizScreen = document.getElementById('quiz-screen');
    const input = document.getElementById('answer-input');
    const feedback = document.getElementById('feedback');
    const actionBtn = document.getElementById('action-btn');
    
    window.onload = function() {
        updateCount();
        input.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') handleAction();
        });
    };

    function updateCount() {
        const examOnly = document.getElementById('examFilter').checked;
        const count = VOCAB_DATA.filter(i => !examOnly || i.needed === 'Yes').length;
        document.getElementById('total-count').innerText = count;
    }

    function openSettings() { document.getElementById('settingsModal').style.display = 'flex'; }
    function closeSettings() {
        document.getElementById('settingsModal').style.display = 'none';
        updateCount();
        if(!startScreen.classList.contains('hidden')) return; // no restart if on start screen
        startSession();
    }

    function startSession() {
        const examOnly = document.getElementById('examFilter').checked;
        const modeRadios = document.getElementsByName('mode');
        for(let r of modeRadios) if(r.checked) mode = r.value;

        sessionVocab = VOCAB_DATA.filter(i => !examOnly || i.needed === 'Yes');
        if (sessionVocab.length === 0) { alert("No words found!"); return; }

        sessionVocab.sort(() => Math.random() - 0.5);
        score = 0; streak = 0; updateStats();
        startScreen.classList.add('hidden');
        quizScreen.classList.remove('hidden');
        nextQuestion();
    }

    function updateStats() {
        document.getElementById('score').innerText = score;
        document.getElementById('streak').innerText = streak;
    }

    function nextQuestion() {
        if (sessionVocab.length === 0) {
            sessionVocab = VOCAB_DATA.filter(i => (!document.getElementById('examFilter').checked) || i.needed === 'Yes');
            sessionVocab.sort(() => Math.random() - 0.5); // Reshuffle infinite loop or end?
            // Infinite loop preferred for practice
        }
        
        currentItem = sessionVocab[Math.floor(Math.random() * sessionVocab.length)];
        // Ensure strictly new word? Random is fine.
        
        const isEnFr = (mode === 'en_fr');
        document.getElementById('q-label').innerText = isEnFr ? "Translate to French" : "Translate to English";
        document.getElementById('q-text').innerText = isEnFr ? currentItem.english : currentItem.french;
        
        // Setup Audio Clean
        // Remove (m) etc for speech
        let cleanFrench = currentItem.french.replace(/\(.*\)/, '').trim();
        textToSpeak = cleanFrench;

        const audioBtn = document.getElementById('audio-btn');
        if (isEnFr) {
            audioBtn.style.visibility = 'hidden'; 
        } else {
            audioBtn.style.visibility = 'visible';
        }

        input.value = "";
        input.className = "";
        input.disabled = false;
        input.focus();
        feedback.innerText = "";
        feedback.className = "feedback";
        actionBtn.innerText = "Check";
        questionState = 'input';
    }

    function handleAction() {
        if (questionState === 'input') {
            checkAnswer();
        } else {
            nextQuestion();
        }
    }

    function playAudio(text) {
        if (!text) return;
        const u = new SpeechSynthesisUtterance(text);
        u.lang = 'fr-FR';
        window.speechSynthesis.speak(u);
    }
    
    function playAudioFromCard() { playAudio(textToSpeak); }
    function typeChar(c) { input.value += c; input.focus(); }
    
    function normalize(str) {
        return str.toLowerCase().replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").trim().replace(/\s{2,}/g," ");
    }

    function checkAnswer() {
        const userRaw = input.value.trim();
        const userNorm = normalize(userRaw);
        if (!userNorm) return;

        const isEnFr = (mode === 'en_fr');
        // Get target text
        let targetText = isEnFr ? currentItem.french : currentItem.english;
        // Clean metadata for matching "l'acteur/actrice (m./f.)" -> "l'acteur/actrice"
        let cleanTarget = targetText.replace(/\(.*\)/, '').trim();

        // Split options
        const rawTargets = cleanTarget.split(/[,\/]/).map(s => s.trim());
        const normTargets = rawTargets.map(s => normalize(s));
        
        // 1. Strict Check
        let correct = normTargets.some(t => t === userNorm);
        let genderWarning = false;

        if (isEnFr) {
             // 2. Gender/Article Hints
            // If they are wrong strictly, check if they matched the 'bare' word
            if (!correct) {
                const articleRegex = /^(le |la |l'|un |une |des |les )/i;
                const strip = s => s.replace(articleRegex, '').trim();
                
                const bareUser = normalize(strip(userRaw));
                const bareTargets = rawTargets.map(t => normalize(strip(t)));
                
                if (bareTargets.includes(bareUser)) {
                    // It IS the right word, just wrong gender/article
                    genderWarning = true;
                }
            }
        }
        
        if (correct) {
            handleCorrect();
        } else if (genderWarning) {
            input.classList.add('warning');
            feedback.innerText = "Almost! Check the article/gender (le/la/l').";
            feedback.className = "feedback warning";
            // Do not advance streak or score yet? Or give them a chance?
            // "Interactive" -> let them fix it?
            // Let's keep input active!
            // Don't change 'questionState' to 'result'.
            return;
        } else {
            handleWrong(cleanTarget);
        }
        
        questionState = 'result';
        actionBtn.innerText = "Next Word";
    }

    function handleCorrect() {
        input.classList.add('correct');
        feedback.innerText = "Correct! Bien joué!";
        feedback.className = "feedback success";
        confetti({particleCount: 100, spread: 70, origin: { y: 0.6 }});
        
        if (mode === 'en_fr') {
             playAudio(textToSpeak);
             document.getElementById('audio-btn').style.visibility = 'visible';
        }
        score++; streak++; updateStats();
    }

    function handleWrong(answer) {
        input.classList.add('wrong');
        feedback.innerText = "The answer was: " + answer;
        feedback.className = "feedback error";
        streak = 0; updateStats();
        
        if (mode === 'en_fr') {
             playAudio(textToSpeak);
             document.getElementById('audio-btn').style.visibility = 'visible';
        }
    }
</script>
</body>
</html>
"""

# Enrich vocab list with cleaner fields if needed, but JS does regex now.
# Just dump raw
html_content = html_template.replace('##JSON_DATA##', json.dumps(vocab_list))

with open('CassiaFrenchApp.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Created CassiaFrenchApp.html")
