from sentrants.census import load_census
from sentrants.hatch import hatch
from sentrants.physics import apply_move
from sentrants.room import room_talk


def test_room_talk_is_stratified_and_capped():
    people = hatch(load_census(), seed=1, n=200)
    apply_move(people, target="seer.auto")
    quotes = room_talk(people, per_camp=10, max_n=60)
    assert 1 <= len(quotes) <= 60
    camps = {q["camp"] for q in quotes}
    geos = {q["geo"] for q in quotes}
    assert len(camps) >= 2
    assert len(geos) >= 2
    spoken = [p for p in people if p.get("_quote")]
    assert len(spoken) == len(quotes)
