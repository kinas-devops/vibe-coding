const colors = ["red", "blue", "green", "yellow", "purple", "orange"];
let secretCode = [];
let currentGuess = [];
let board = document.getElementById("board");
let preview = document.getElementById("preview");
let maxGuesses = 10;
let guessCount = 0;
let gameOver = false;
let timeLimit = 60;
let timeLeft = 60;
let timerStarted = false;
let timerInterval;

function updatePreview() {
  preview.innerHTML = "";
  currentGuess.forEach(color => {
    const slot = document.createElement("div");
    slot.className = "slot selected";
    slot.style.background = color;
    preview.appendChild(slot);
  });
}


function generateCode() {
  secretCode = [];
  while (secretCode.length < 4) {
    const color = colors[Math.floor(Math.random() * colors.length)];
    secretCode.push(color);
  }
  console.log("Secret Code:", secretCode); // For debugging
}

function createRow(guess, feedback) {
  const row = document.createElement("div");
  row.className = "row";

  const guessSection = document.createElement("div");
  guessSection.className = "guess-section";

  guess.forEach(color => {
    const slot = document.createElement("div");
    slot.className = "slot";
    slot.style.background = color;
    guessSection.appendChild(slot);
  });

  const feedbackSection = document.createElement("div");
  feedbackSection.className = "feedback-section";

  feedback.forEach(type => {
    const peg = document.createElement("div");
    peg.className = "feedback";
    peg.style.background = type === "black" ? "black" : "white";
    feedbackSection.appendChild(peg);
  });

  row.appendChild(guessSection);
  row.appendChild(feedbackSection);
  board.appendChild(row);
}

function getFeedback(guess, code) {
  let black = 0;
  let white = 0;
  let codeCopy = [...code];
  let guessCopy = [...guess];

  // First pass: check for correct color and position
  for (let i = 0; i < 4; i++) {
    if (guessCopy[i] === codeCopy[i]) {
      black++;
      codeCopy[i] = guessCopy[i] = null;
    }
  }

  // Second pass: check for correct color in wrong position
  for (let i = 0; i < 4; i++) {
    if (guessCopy[i]) {
      const index = codeCopy.indexOf(guessCopy[i]);
      if (index !== -1) {
        white++;
        codeCopy[index] = null;
      }
    }
  }

  return Array(black).fill("black").concat(Array(white).fill("white"));
}

function startTimer() {
  timerInterval = setInterval(() => {
    timeLeft--;
    document.getElementById("timerDisplay").textContent = `Time left: ${timeLeft}s`;

    if (timeLeft <= 0) {
      clearInterval(timerInterval);
      endGame(false, "⏰ Time's up!");
    }
  }, 1000);
}

function endGame(won, message = "") {
  gameOver = true;
  clearInterval(timerInterval);

  if (won) {
    alert("🎉 You cracked the code!");
  } else {
    alert(message + "\nThe code was: " + secretCode.join(", "));
  }

  // Disable controls
  document.getElementById("submit").disabled = true;
  document.getElementById("clear").disabled = true;
  document.querySelectorAll(".color").forEach(btn => btn.disabled = true);
}

document.querySelectorAll(".color").forEach(btn => {
  btn.addEventListener("click", () => {
    if (currentGuess.length < 4) {
      currentGuess.push(btn.dataset.color);
      updatePreview();
    }
  });
});

document.getElementById("submit").addEventListener("click", () => {
  if (gameOver) return;

  if (!timerStarted) {
    timeLimit = parseInt(document.getElementById("timeLimit").value);
    timeLeft = timeLimit;
    document.getElementById("timeLimit").disabled = true;
    startTimer();
    timerStarted = true;
  }

  if (currentGuess.length !== 4) {
    alert("Pick 4 colors!");
    return;
  }

  const feedback = getFeedback(currentGuess, secretCode);
  createRow(currentGuess, feedback);
  guessCount++;

  if (feedback.filter(f => f === "black").length === 4) {
    endGame(true);
  } else if (guessCount >= maxGuesses) {
    endGame(false, "💥 Out of guesses!");
  }

  currentGuess = [];
  updatePreview();
});

document.getElementById("restart").addEventListener("click", () => {
  // Reset game state
  guessCount = 0;
  gameOver = false;
  timerStarted = false;
  clearInterval(timerInterval);

  // Reset timer
  timeLeft = parseInt(document.getElementById("timeLimit").value);
  document.getElementById("timeLimit").disabled = false;
  document.getElementById("timerDisplay").textContent = `Time left: ${timeLeft}s`;

  // ✅ Re-enable controls FIRST
  document.getElementById("submit").disabled = false;
  document.getElementById("clear").disabled = false;
  document.querySelectorAll(".color").forEach(btn => btn.disabled = false);

  // 🎬 Animate board fade-out
  const board = document.getElementById("board");
  board.classList.add("board-hidden");

  // Wait for animation to finish before resetting
  setTimeout(() => {
    board.innerHTML = "";
    board.classList.remove("board-hidden");

    // Reset preview and generate new code
    currentGuess = [];
    updatePreview();
    secretCode = generateSecretCode();
  }, 500); // Match the CSS transition duration
});

document.getElementById("clear").addEventListener("click", () => {
  currentGuess = [];
  updatePreview();
});


generateCode();