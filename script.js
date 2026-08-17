const canvas = document.querySelector("#creature");
const ctx = canvas.getContext("2d");

const count = 31;
const spacing = 13;
const body = [];

let pointer = {
  x: innerWidth / 2,
  y: innerHeight / 2
};

let lastPointer = {
  ...pointer
};

let motion = 0;
let time = 0;

function resize() {
  const dpr = Math.min(devicePixelRatio || 1, 2);

  canvas.width = innerWidth * dpr;
  canvas.height = innerHeight * dpr;

  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}

function reset() {
  body.length = 0;

  for (let i = 0; i < count; i++) {
    body.push({
      x: pointer.x - i * spacing,
      y: pointer.y,
      angle: 0
    });
  }
}

addEventListener("resize", () => {
  resize();
  reset();
});

addEventListener("pointermove", (event) => {
  pointer.x = event.clientX;
  pointer.y = event.clientY;
});

resize();
reset();

function line(x1, y1, x2, y2, width = 1) {
  ctx.lineWidth = width;
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();
}

function update() {
  body[0].x += (pointer.x - body[0].x) * 0.19;
  body[0].y += (pointer.y - body[0].y) * 0.19;

  motion = Math.min(
    1,
    Math.hypot(
      pointer.x - lastPointer.x,
      pointer.y - lastPointer.y
    ) / 16
  );

  lastPointer = { ...pointer };

  for (let i = 1; i < count; i++) {
    const lead = body[i - 1];
    const part = body[i];

    const dx = lead.x - part.x;
    const dy = lead.y - part.y;

    const angle = Math.atan2(dy, dx);

    const sway =
      Math.sin(time * 0.14 - i * 0.72) * motion * 0.28;

    part.x = lead.x - Math.cos(angle + sway) * spacing;
    part.y = lead.y - Math.sin(angle + sway) * spacing;
    part.angle = angle;
  }

  body[0].angle = Math.atan2(
    body[0].y - body[1].y,
    body[0].x - body[1].x
  );
}

function drawLeg(x, y, angle, side, length, index) {
  const bend =
    angle +
    side * (
      1.04 +
      Math.sin(time * 0.18 - index * 0.8) * 0.1
    );

  const elbowX = x + Math.cos(bend) * length * 0.57;
  const elbowY = y + Math.sin(bend) * length * 0.57;

  const claw = bend + side * 0.72;

  line(x, y, elbowX, elbowY, 1.05);

  line(
    elbowX,
    elbowY,
    elbowX + Math.cos(claw) * length * 0.56,
    elbowY + Math.sin(claw) * length * 0.56,
    0.8
  );

  line(
    elbowX + Math.cos(claw) * length * 0.42,
    elbowY + Math.sin(claw) * length * 0.42,
    elbowX + Math.cos(claw + side * 0.48) * length * 0.59,
    elbowY + Math.sin(claw + side * 0.48) * length * 0.59,
    0.55
  );
}

function draw() {
  ctx.clearRect(0, 0, innerWidth, innerHeight);

  ctx.save();

  ctx.lineCap = "round";
  ctx.lineJoin = "round";
  ctx.strokeStyle = "rgba(246, 244, 255, 0.92)";
  ctx.shadowColor = "#bdafff";
  ctx.shadowBlur = 7;

  for (let i = 3; i < count - 2; i += 2) {
    const p = body[i];
    const taper = 1 - i / count;

    drawLeg(p.x, p.y, p.angle, -1, 19 + taper * 16, i);
    drawLeg(p.x, p.y, p.angle, 1, 19 + taper * 16, i);
  }

  ctx.strokeStyle = "rgba(122, 110, 157, 0.65)";
  ctx.lineWidth = 3;

  ctx.beginPath();
  ctx.moveTo(body[0].x, body[0].y);

  body.slice(1).forEach((p) => {
    ctx.lineTo(p.x, p.y);
  });

  ctx.stroke();

  ctx.strokeStyle = "#fff";
  ctx.fillStyle = "rgba(225, 219, 255, 0.14)";

  for (let i = 1; i < count - 1; i++) {
    const p = body[i];
    const taper = 1 - i / (count + 4);
    const rib = 5.5 + taper * 7;

    ctx.save();

    ctx.translate(p.x, p.y);
    ctx.rotate(p.angle);

    ctx.beginPath();
    ctx.ellipse(
      0,
      0,
      4.8 + taper * 2.2,
      rib,
      0,
      0,
      Math.PI * 2
    );

    ctx.fill();
    ctx.lineWidth = 1.05;
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(0, 0, 1.45, 0, Math.PI * 2);
    ctx.fillStyle = "#fff";
    ctx.fill();

    ctx.restore();
  }

  const h = body[0];
  const a = h.angle;

  ctx.fillStyle = "#fbfaff";

  ctx.beginPath();
  ctx.moveTo(
    h.x + Math.cos(a) * 13,
    h.y + Math.sin(a) * 13
  );

  ctx.lineTo(
    h.x + Math.cos(a + 2.15) * 10,
    h.y + Math.sin(a + 2.15) * 10
  );

  ctx.lineTo(
    h.x + Math.cos(a - 2.15) * 10,
    h.y + Math.sin(a - 2.15) * 10
  );

  ctx.closePath();
  ctx.fill();

  ctx.strokeStyle = "#fff";

  [-1, 1].forEach((side) => {
    const baseX = h.x + Math.cos(a + side * 0.7) * 6;
    const baseY = h.y + Math.sin(a + side * 0.7) * 6;

    line(
      baseX,
      baseY,
      baseX + Math.cos(a + side * 0.58) * 26,
      baseY + Math.sin(a + side * 0.58) * 26,
      0.75
    );
  });

  ctx.restore();
}

function frame() {
  time++;
  update();
  draw();
  requestAnimationFrame(frame);
}

frame();