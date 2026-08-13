from __future__ import annotations

import json
from pathlib import Path

from sentrants.layout import LIFE

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "floor.html"

HTML = """<!doctype html>
<meta charset="utf-8" />
<title>Sentrants</title>
<style>
  html, body { margin: 0; background: #0b0d10; color: #d6d8db; font: 13px/1.4 ui-sans-serif, system-ui; }
  canvas { display: block; }
  #hud { position: absolute; left: 16px; top: 12px; pointer-events: none; }
  h1 { font-size: 14px; font-weight: 600; margin: 0 0 4px; letter-spacing: .04em; }
  .label { position: absolute; opacity: .45; font-size: 11px; letter-spacing: .16em; text-transform: uppercase; }
  #card {
    display: none; position: absolute; right: 16px; top: 16px; width: 320px;
    background: #161a20; border: 1px solid #2a313c; padding: 14px 16px; pointer-events: none;
  }
  #card b { color: #fff; }
  #card .muted { color: #8b919a; }
</style>
<div id="hud"><h1>Sentrants</h1><div id="count"></div></div>
<div id="card"></div>
<canvas id="c"></canvas>
<script>
const swarm = SWARM;
const camps = CAMPS;
const geoColor = {
  us: "#6ee7b7", europe: "#93c5fd", india: "#fbbf24",
  latam: "#f9a8d4", east_asia: "#c4b5fd",
};
const canvas = document.getElementById("c");
const ctx = canvas.getContext("2d");
const card = document.getElementById("card");
let W, H, hover = null;

function resize() {
  W = canvas.width = Math.max(1200, window.innerWidth);
  H = canvas.height = Math.max(720, window.innerHeight);
}
window.onresize = resize;
resize();

for (const p of swarm) {
  p.vx = (Math.random() - .5) * .25;
  p.vy = (Math.random() - .5) * .25;
}

function clamp(p) {
  const [x,y,w,h] = camps[p.stage];
  const pad = 10;
  if (p.x < x+pad) { p.x = x+pad; p.vx *= -1; }
  if (p.y < y+pad) { p.y = y+pad; p.vy *= -1; }
  if (p.x > x+w-pad) { p.x = x+w-pad; p.vx *= -1; }
  if (p.y > y+h-pad) { p.y = y+h-pad; p.vy *= -1; }
}

function tick() {
  ctx.clearRect(0,0,W,H);
  ctx.strokeStyle = "#1f2630";
  ctx.fillStyle = "#6b7280";
  ctx.font = "11px ui-sans-serif";
  for (const [x,y,w,h,name] of Object.values(camps)) {
    ctx.strokeRect(x, y, w, h);
    ctx.fillText(name, x + 10, y + 18);
  }
  for (const p of swarm) {
    p.vx += (Math.random() - .5) * .04;
    p.vy += (Math.random() - .5) * .04;
    p.vx *= 0.96; p.vy *= 0.96;
    p.x += p.vx; p.y += p.vy;
    clamp(p);
    ctx.beginPath();
    ctx.arc(p.x, p.y, hover === p ? 4.5 : 2.2, 0, Math.PI*2);
    ctx.fillStyle = geoColor[p.geo] || "#fff";
    ctx.globalAlpha = hover && hover !== p ? 0.25 : 0.9;
    ctx.fill();
  }
  ctx.globalAlpha = 1;
  requestAnimationFrame(tick);
}
tick();

document.getElementById("count").textContent = swarm.length + " · color = geo";

canvas.onmousemove = (e) => {
  const r = canvas.getBoundingClientRect();
  const x = e.clientX - r.left, y = e.clientY - r.top;
  hover = null;
  let best = 64;
  for (const p of swarm) {
    const d = (p.x-x)**2 + (p.y-y)**2;
    if (d < best) { best = d; hover = p; }
  }
  if (!hover) { card.style.display = "none"; return; }
  card.style.display = "block";
  card.innerHTML = `<b>${hover.name}</b><div class="muted">${hover.age} · ${hover.seat} · ${hover.shop} · ${hover.geo}</div>
    <div>${hover.framework} · ${hover.plan} · ${hover.stage}</div>
    <div class="muted" style="margin-top:8px">${hover.origin}</div>`;
};
</script>
"""


def write_floor(people: list[dict], path: Path | None = None) -> Path:
    path = path or OUT
    path.parent.mkdir(parents=True, exist_ok=True)
    swarm = [
        {
            "id": p["id"],
            "name": p["display_name"],
            "x": p["_x"],
            "y": p["_y"],
            "stage": p["life"]["stage"],
            "geo": p["human"]["geo"],
            "shop": p["human"]["shop"],
            "seat": p["human"]["seat"],
            "age": p["human"]["age"],
            "plan": p["sentry"]["plan"],
            "framework": p["human"]["frameworks"][0],
            "origin": p["origin"],
        }
        for p in people
    ]
    camps = {k: [*v, k] for k, v in LIFE.items()}
    html = HTML.replace("SWARM", json.dumps(swarm)).replace(
        "CAMPS", json.dumps(camps)
    )
    path.write_text(html)
    return path
