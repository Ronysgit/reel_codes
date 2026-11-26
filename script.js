const cube = document.querySelector("#cube");
const cubeLayer = document.querySelector("#cube-layer");
const timerDisplay = document.querySelector("#timer");
const moveDisplay = document.querySelector("#move-count");
const bestDisplay = document.querySelector("#best-time");
const undoButton = document.querySelector("#undo-button");
const resetButton = document.querySelector("#reset-button");
const shuffleButton = document.querySelector("#shuffle-button");
const liveRegion = document.querySelector("#live-region");
const installButton = document.querySelector("#install-button");
const installDialog = document.querySelector("#install-dialog");
const installSummary = document.querySelector("#install-summary");
const installSteps = document.querySelector("#install-steps");
const installNote = document.querySelector("#install-note");

const faceNames = {
  U: "Up",
  D: "Down",
  L: "Left",
  R: "Right",
  F: "Front",
  B: "Back"
};
const colors = {
  U: "#f4f0e5",
  D: "#f4d447",
  L: "#f18a48",
  R: "#e65348",
  F: "#72bd65",
  B: "#5b91d2"
};
const faces = {
  U: { axis: "y", layer: -1, direction: -1 },
  D: { axis: "y", layer: 1, direction: 1 },
  L: { axis: "x", layer: -1, direction: 1 },
  R: { axis: "x", layer: 1, direction: -1 },
  F: { axis: "z", layer: 1, direction: 1 },
  B: { axis: "z", layer: -1, direction: -1 }
};
const sideVectors = {
  U: [0, -1, 0],
  D: [0, 1, 0],
  L: [-1, 0, 0],
  R: [1, 0, 0],
  F: [0, 0, 1],
  B: [0, 0, -1]
};
const vectorSides = Object.fromEntries(
  Object.entries(sideVectors).map(([side, vector]) => [vector.join(","), side])
);
const sideClasses = {
  U: "up",
  D: "down",
  L: "left",
  R: "right",
  F: "front",
  B: "back"
};
const faceSides = ["U", "D", "L", "R", "F", "B"];
const pieces = [];
const history = [];
const moveQueue = [];
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const turnDuration = reducedMotion ? 1 : 235;

let isProcessing = false;
let moveCount = 0;
let timerStartedAt = null;
let timerFrame = 0;
let bestTime = readBestTime();
let viewX = -24;
let viewY = -34;
let dragPointer = null;
let deferredInstallPrompt = null;

function isInstalled() {
  return navigator.standalone === true || window.matchMedia("(display-mode: standalone)").matches;
}

function getInstallGuide() {
  const isAppleMobile =
    /iPhone|iPad|iPod/i.test(navigator.userAgent) ||
    (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  const isMac = /Mac/i.test(navigator.platform) && !isAppleMobile;
  const isAndroid = /Android/i.test(navigator.userAgent);

  if (isAppleMobile) {
    return {
      summary: "iPhone par Share menu se Cube Lab ko Home Screen par add karein:",
      steps: [
        "Safari mein Cube Lab ka HTTPS link kholen.",
        "Share button (square aur upar arrow) tap karein.",
        "Add to Home Screen chunein, phir Add tap karein."
      ],
      note: "Agar “Open as Web App” option dikhe, use on rehne dein. Icon aapki Home Screen par aa jayega."
    };
  }

  if (isMac) {
    return {
      summary: "Laptop par app jaisa shortcut banane ke liye:",
      steps: [
        "Chrome ya Edge mein address bar ke Install icon par click karein; ya browser menu kholen.",
        "Chrome: Save and share → Install page as app. Edge: Apps → Install this site as an app.",
        "Safari (macOS Sonoma ya newer): File → Add to Dock."
      ],
      note: "Install option browser aur version ke hisaab se alag jagah ho sakta hai."
    };
  }

  if (isAndroid) {
    return {
      summary: "Android par browser menu se app install karein:",
      steps: [
        "Chrome mein Cube Lab ka HTTPS link kholen.",
        "Install app ya Add to Home screen chunein.",
        "Install confirm karein; app icon Home Screen par aa jayega."
      ],
      note: "Menu ka label Chrome version ke hisaab se badal sakta hai."
    };
  }

  return {
    summary: "Is website ko app window mein kholne ke liye browser ka install option use karein:",
    steps: [
      "Chrome ya Edge mein Cube Lab ka HTTPS link kholen.",
      "Address bar ke Install icon par click karein, ya browser menu se Install page as app chunein.",
      "Install confirm karein."
    ],
    note: "Firefox mein app normal tab mein chalegi; PWA install ke liye Chrome, Edge, ya supported Safari use karein."
  };
}

function openInstallGuide() {
  const guide = getInstallGuide();
  installSummary.textContent = guide.summary;
  installSteps.replaceChildren(
    ...guide.steps.map((step) => {
      const item = document.createElement("li");
      item.textContent = step;
      return item;
    })
  );
  installNote.textContent = `${guide.note} App install ke liye site ka HTTPS link live hona zaroori hai.`;
  installDialog.showModal();
}

installButton.hidden = isInstalled();

window.addEventListener("beforeinstallprompt", (event) => {
  event.preventDefault();
  deferredInstallPrompt = event;
  installButton.hidden = isInstalled();
});

window.addEventListener("appinstalled", () => {
  deferredInstallPrompt = null;
  installButton.hidden = true;
  liveRegion.textContent = "Cube Lab was installed.";
});

installButton.addEventListener("click", async () => {
  if (!deferredInstallPrompt) {
    openInstallGuide();
    return;
  }

  const prompt = deferredInstallPrompt;
  deferredInstallPrompt = null;
  await prompt.prompt();
  const result = await prompt.userChoice;
  if (result.outcome === "dismissed") openInstallGuide();
});

document.querySelector("#install-close").addEventListener("click", () => installDialog.close());
document.querySelector("#install-done").addEventListener("click", () => installDialog.close());

if ("serviceWorker" in navigator && location.protocol !== "file:" && navigator.onLine) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("./sw.js").catch((error) => {
      console.error("Cube Lab offline support could not be registered.", error);
    });
  });
}

function readBestTime() {
  try {
    const saved = Number(window.localStorage.getItem("cubelab-best-time"));
    return Number.isFinite(saved) && saved > 0 ? saved : null;
  } catch {
    return null;
  }
}

function saveBestTime(time) {
  try {
    window.localStorage.setItem("cubelab-best-time", String(time));
  } catch {
    liveRegion.textContent = "Best time could not be saved in this browser.";
  }
}

function makePiece(x, y, z) {
  const stickers = {};
  if (x === -1) stickers.L = "L";
  if (x === 1) stickers.R = "R";
  if (y === -1) stickers.U = "U";
  if (y === 1) stickers.D = "D";
  if (z === 1) stickers.F = "F";
  if (z === -1) stickers.B = "B";

  const element = document.createElement("div");
  element.className = "cubie";
  const faceElements = {};

  faceSides.forEach((side) => {
    const face = document.createElement("div");
    face.className = `cubie-face face-${sideClasses[side]}`;
    face.setAttribute("aria-hidden", "true");
    element.append(face);
    faceElements[side] = face;
  });

  const piece = {
    x,
    y,
    z,
    homeX: x,
    homeY: y,
    homeZ: z,
    stickers: { ...stickers },
    homeStickers: { ...stickers },
    element,
    faceElements
  };
  pieces.push(piece);
  renderPiece(piece);
}

function renderPiece(piece) {
  const offset = (coordinate) => {
    if (coordinate === 0) return "0px";
    return coordinate > 0 ? "var(--unit)" : "calc(0px - var(--unit))";
  };
  piece.element.style.setProperty("--x", offset(piece.x));
  piece.element.style.setProperty("--y", offset(piece.y));
  piece.element.style.setProperty("--z", offset(piece.z));

  faceSides.forEach((side) => {
    const sticker = piece.stickers[side];
    piece.faceElements[side].style.setProperty(
      "--sticker",
      sticker ? colors[sticker] : "transparent"
    );
  });
}

function buildCube() {
  for (let x = -1; x <= 1; x++) {
    for (let y = -1; y <= 1; y++) {
      for (let z = -1; z <= 1; z++) {
        if (x || y || z) makePiece(x, y, z);
      }
    }
  }
  cubeLayer.append(...pieces.map((piece) => piece.element));
  updateCubeDescription();
}

function rotateVector(vector, axis, direction) {
  let [x, y, z] = vector;
  const turns = direction > 0 ? 1 : 3;

  for (let turn = 0; turn < turns; turn++) {
    if (axis === "x") [x, y, z] = [x, -z, y];
    if (axis === "y") [x, y, z] = [z, y, -x];
    if (axis === "z") [x, y, z] = [-y, x, z];
  }

  return [x, y, z];
}

function inverseMove(move) {
  return move.endsWith("'") ? move[0] : `${move}'`;
}

function isSolved() {
  return pieces.every((piece) => {
    if (piece.x !== piece.homeX || piece.y !== piece.homeY || piece.z !== piece.homeZ) {
      return false;
    }
    return faceSides.every((side) => piece.stickers[side] === piece.homeStickers[side]);
  });
}

function formatTime(milliseconds, includeHundredths = true) {
  const totalHundredths = Math.floor(milliseconds / 10);
  const minutes = Math.floor(totalHundredths / 6000);
  const seconds = Math.floor(totalHundredths / 100) % 60;
  const hundredths = totalHundredths % 100;
  const base = `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
  return includeHundredths ? `${base}.${String(hundredths).padStart(2, "0")}` : base;
}

function elapsedTime() {
  return timerStartedAt === null ? 0 : performance.now() - timerStartedAt;
}

function renderStats() {
  timerDisplay.textContent = formatTime(elapsedTime());
  moveDisplay.textContent = String(moveCount);
  bestDisplay.textContent = bestTime === null ? "—" : formatTime(bestTime, false);
  undoButton.disabled = isProcessing || history.length === 0;
}

function tickTimer() {
  renderStats();
  if (timerStartedAt !== null) timerFrame = requestAnimationFrame(tickTimer);
}

function startTimer() {
  if (timerStartedAt !== null) return;
  timerStartedAt = performance.now();
  timerFrame = requestAnimationFrame(tickTimer);
}

function stopTimer() {
  if (timerStartedAt === null) return;
  const finalTime = elapsedTime();
  timerStartedAt = null;
  cancelAnimationFrame(timerFrame);
  renderStats();

  if (moveCount > 0 && (bestTime === null || finalTime < bestTime)) {
    bestTime = finalTime;
    saveBestTime(finalTime);
    renderStats();
    liveRegion.textContent = `Solved in ${formatTime(finalTime)}. New personal best!`;
  } else {
    liveRegion.textContent = `Cube solved in ${formatTime(finalTime)}.`;
  }
}

function updateCubeDescription() {
  cube.setAttribute(
    "aria-label",
    `${isSolved() ? "Solved" : "Mixed"} 3 by 3 Rubik's Cube. Drag to rotate the view.`
  );
}

function updateControls() {
  document.querySelectorAll(".move-button").forEach((button) => {
    button.disabled = isProcessing;
  });
  shuffleButton.disabled = isProcessing;
  resetButton.disabled = isProcessing;
  undoButton.disabled = isProcessing || history.length === 0;
}

function animateTurn(move) {
  const face = faces[move[0]];
  const direction = face.direction * (move.endsWith("'") ? -1 : 1);
  const angle = direction * 90;
  const layer = document.createElement("div");
  layer.className = "turn-layer";
  layer.style.transitionDuration = `${turnDuration}ms`;
  cubeLayer.append(layer);

  const turningPieces = pieces.filter((piece) => piece[face.axis] === face.layer);
  turningPieces.forEach((piece) => layer.append(piece.element));
  void layer.offsetWidth;

  return new Promise((resolve) => {
    let finished = false;
    const finish = () => {
      if (finished) return;
      finished = true;
      window.clearTimeout(fallback);

      turningPieces.forEach((piece) => {
        const position = rotateVector([piece.x, piece.y, piece.z], face.axis, direction);
        [piece.x, piece.y, piece.z] = position;

        const rotatedStickers = {};
        Object.entries(piece.stickers).forEach(([side, color]) => {
          const nextVector = rotateVector(sideVectors[side], face.axis, direction);
          rotatedStickers[vectorSides[nextVector.join(",")]] = color;
        });
        piece.stickers = rotatedStickers;
        renderPiece(piece);
        cubeLayer.append(piece.element);
      });

      layer.remove();
      updateCubeDescription();
      resolve();
    };

    layer.addEventListener("transitionend", (event) => {
      if (event.target === layer && event.propertyName === "transform") finish();
    });

    const fallback = window.setTimeout(finish, turnDuration + 100);
    requestAnimationFrame(() => {
      layer.style.transform = `rotate${face.axis.toUpperCase()}(${angle}deg)`;
    });
  });
}

async function processQueue() {
  if (isProcessing || moveQueue.length === 0) return;
  isProcessing = true;
  updateControls();

  try {
    while (moveQueue.length > 0) {
      const item = moveQueue.shift();
      await animateTurn(item.move);
      if (item.record) history.push(item.move);
      if (item.countMove) moveCount++;
      if (item.startTimer) startTimer();
      renderStats();

      if (timerStartedAt !== null && isSolved()) stopTimer();
    }
  } finally {
    isProcessing = false;
    updateControls();
    renderStats();
  }
}

function enqueueMoves(moves, options = {}) {
  const { countMove = true, record = true, startTimerOnTurn = true } = options;
  moves.forEach((move) => {
    moveQueue.push({
      move,
      countMove,
      record,
      startTimer: startTimerOnTurn
    });
  });
  updateControls();
  void processQueue();
}

function resetStats() {
  cancelAnimationFrame(timerFrame);
  timerStartedAt = null;
  moveCount = 0;
  history.length = 0;
  timerDisplay.textContent = "00:00.00";
  renderStats();
}

function resetCube() {
  resetStats();
  pieces.forEach((piece) => {
    piece.x = piece.homeX;
    piece.y = piece.homeY;
    piece.z = piece.homeZ;
    piece.stickers = { ...piece.homeStickers };
    renderPiece(piece);
    cubeLayer.append(piece.element);
  });
  updateCubeDescription();
  liveRegion.textContent = "Cube reset to its solved state.";
}

function scramble() {
  const facesList = Object.keys(faces);
  const moves = [];
  let previousFace = "";
  for (let index = 0; index < 20; index++) {
    let nextFace = facesList[Math.floor(Math.random() * facesList.length)];
    while (nextFace === previousFace) {
      nextFace = facesList[Math.floor(Math.random() * facesList.length)];
    }
    moves.push(Math.random() < 0.5 ? nextFace : `${nextFace}'`);
    previousFace = nextFace;
  }

  resetStats();
  liveRegion.textContent = "Shuffling the cube.";
  enqueueMoves(moves, { countMove: false, record: false, startTimerOnTurn: false });
}

document.querySelectorAll(".move-button").forEach((button) => {
  button.addEventListener("click", () => {
    enqueueMoves([button.dataset.move]);
  });
});

shuffleButton.addEventListener("click", scramble);
resetButton.addEventListener("click", resetCube);
undoButton.addEventListener("click", () => {
  const previousMove = history.pop();
  if (previousMove) enqueueMoves([inverseMove(previousMove)], { record: false });
  renderStats();
});

document.addEventListener("keydown", (event) => {
  if (event.altKey || event.ctrlKey || event.metaKey) return;
  if (event.target instanceof HTMLElement && event.target.closest("button, a, input, textarea, select")) return;
  const face = event.key.toUpperCase();
  if (!faces[face]) return;
  event.preventDefault();
  enqueueMoves([event.shiftKey ? `${face}'` : face]);
});

cube.addEventListener("pointerdown", (event) => {
  if (event.button !== undefined && event.button !== 0) return;
  dragPointer = { id: event.pointerId, x: event.clientX, y: event.clientY };
  cube.classList.add("is-dragging");
  cube.setPointerCapture(event.pointerId);
});

cube.addEventListener("pointermove", (event) => {
  if (!dragPointer || event.pointerId !== dragPointer.id) return;
  const deltaX = event.clientX - dragPointer.x;
  const deltaY = event.clientY - dragPointer.y;
  viewY += deltaX * 0.65;
  viewX = Math.max(-82, Math.min(82, viewX - deltaY * 0.65));
  cube.style.transform = `rotateX(${viewX}deg) rotateY(${viewY}deg)`;
  dragPointer.x = event.clientX;
  dragPointer.y = event.clientY;
});

function endDrag(event) {
  if (!dragPointer || event.pointerId !== dragPointer.id) return;
  dragPointer = null;
  cube.classList.remove("is-dragging");
  if (cube.hasPointerCapture(event.pointerId)) cube.releasePointerCapture(event.pointerId);
}

cube.addEventListener("pointerup", endDrag);
cube.addEventListener("pointercancel", endDrag);

buildCube();
renderStats();
