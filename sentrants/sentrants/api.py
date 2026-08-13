from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from sentrants import db as dbmod
from sentrants.engine import (
    current_day,
    person_card,
    run_jump,
    run_life,
    run_move,
    swarm_payload,
)
from sentrants.mix import mix_report
from sentrants.slices import slices_report

FLOOR = Path(__file__).with_name("static") / "index.html"

app = FastAPI(title="Sentrants")


class MoveIn(BaseModel):
    target: str = "seer.auto"
    remember: bool = False


class JumpIn(BaseModel):
    days: int = Field(default=30, ge=1, le=365)


def _need_swarm() -> None:
    if not dbmod.DEFAULT_DB.exists():
        raise HTTPException(404, "no swarm yet — run: python3 -m sentrants hatch")


@app.get("/", response_class=HTMLResponse)
def floor():
    if not FLOOR.exists():
        raise HTTPException(500, "floor missing")
    return FLOOR.read_text()


@app.get("/swarm")
def swarm():
    _need_swarm()
    return swarm_payload()


@app.get("/person/{person_id}")
def person(person_id: str):
    _need_swarm()
    card = person_card(person_id)
    if not card:
        raise HTTPException(404, "no such sentrant")
    return card


@app.post("/move")
def move(body: MoveIn):
    _need_swarm()
    try:
        return run_move(target=body.target, remember=body.remember)
    except KeyError:
        raise HTTPException(400, f"unknown move {body.target}") from None


@app.post("/jump")
def jump(body: JumpIn | None = None):
    _need_swarm()
    days = body.days if body else 30
    return run_jump(days=days)


@app.post("/life")
def life():
    _need_swarm()
    return run_life()


@app.get("/mix")
def mix():
    _need_swarm()
    return {"text": mix_report(dbmod.load_people()), "day": current_day()}


@app.get("/slices")
def slices():
    _need_swarm()
    return {"text": slices_report(dbmod.load_people())}
