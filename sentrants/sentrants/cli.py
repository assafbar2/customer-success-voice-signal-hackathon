from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from sentrants.census import DEFAULT_CENSUS, load_census
from sentrants.db import DEFAULT_DB, load_people, save_people
from sentrants.floor import write_floor
from sentrants.hatch import hatch
from sentrants.mix import mix_report
from sentrants.physics import pick_camp, score_seer_auto
from sentrants.slices import slices_report


def cmd_hatch(args: argparse.Namespace) -> None:
    census = load_census(Path(args.census) if args.census else None)
    people = hatch(census, seed=args.seed, n=args.n)
    db = save_people(people, seed=args.seed, path=Path(args.db) if args.db else None)
    html = write_floor(people)
    print(mix_report(people))
    print(f"sqlite: {db}")
    print(f"floor:  {html}")
    print("open the html file in a browser. color = geo. hover a dot.")


def cmd_mix(_: argparse.Namespace) -> None:
    print(mix_report(load_people()))


def cmd_floor(_: argparse.Namespace) -> None:
    path = write_floor(load_people())
    print(path)


def cmd_show(args: argparse.Namespace) -> None:
    people = load_people()
    if args.geo or args.shop:
        people = [
            p
            for p in people
            if (not args.geo or p["human"]["geo"] == args.geo)
            and (not args.shop or p["human"]["shop"] == args.shop)
        ]
    for p in people[: args.n]:
        h = p["human"]
        print(f"{p['display_name']:22} {h['age']} {h['seat']:8} {h['geo']:10} {h['shop']:10} {h['frameworks'][0]:8} {p['life']['stage']}")
        print(f"  {p['origin']}")
        print()


def cmd_slices(_: argparse.Namespace) -> None:
    print(slices_report(load_people()))


def cmd_walk(_: argparse.Namespace) -> None:
    people = load_people()
    camps = Counter(pick_camp(score_seer_auto(p)) for p in people)
    n = len(people)
    print("move: ship seer.auto  (Autofix opens PRs on its own)")
    for k, v in camps.most_common():
        print(f"  {k:18} {v:5}  {100.0 * v / n:5.1f}%")


def cmd_jump(args: argparse.Namespace) -> None:
    from sentrants.engine import run_jump

    out = run_jump(days=args.days)
    print(f"jumped {out['days']} days → day {out['day']}")
    print("transitions", out.get("transitions"))
    print("stages", out.get("stages"))


def cmd_serve(args: argparse.Namespace) -> None:
    import uvicorn

    print(f"floor → http://{args.host}:{args.port}/")
    uvicorn.run("sentrants.api:app", host=args.host, port=args.port, reload=False)


def main() -> None:
    p = argparse.ArgumentParser(prog="sentrants")
    sub = p.add_subparsers(dest="cmd", required=True)

    h = sub.add_parser("hatch", help="mint the swarm")
    h.add_argument("--seed", type=int, default=1)
    h.add_argument("--n", type=int, default=None)
    h.add_argument("--census", default=str(DEFAULT_CENSUS))
    h.add_argument("--db", default=str(DEFAULT_DB))
    h.set_defaults(func=cmd_hatch)

    sub.add_parser("mix", help="print the live mix").set_defaults(func=cmd_mix)
    sub.add_parser("slices", help="covering map + audience callouts").set_defaults(func=cmd_slices)
    sub.add_parser("floor", help="rewrite data/floor.html").set_defaults(func=cmd_floor)
    sub.add_parser("walk", help="score ship seer.auto").set_defaults(func=cmd_walk)

    j = sub.add_parser("jump", help="jump time (a month later)")
    j.add_argument("--days", type=int, default=30)
    j.set_defaults(func=cmd_jump)

    srv = sub.add_parser("serve", help="live floor + API")
    srv.add_argument("--host", default="127.0.0.1")
    srv.add_argument("--port", type=int, default=8765)
    srv.set_defaults(func=cmd_serve)

    s = sub.add_parser("show", help="print a few people")
    s.add_argument("-n", type=int, default=5)
    s.add_argument("--geo")
    s.add_argument("--shop")
    s.set_defaults(func=cmd_show)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
