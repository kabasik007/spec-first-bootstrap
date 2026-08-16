#!/usr/bin/env python3
"""Universal AI Development Bootstrap.

Local-first project discovery, autonomous architecture synthesis, capability packs,
dependency mapping, baseline intelligence, policy checks, knowledge, standards,
research agenda, and provenance-aware project memory.

No third-party Python packages are required.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from engine.harness import (
    VERSION,
    add_memory_target,
    build_context,
    check_policy_target,
    init_target,
    onboard_target,
    run_baseline,
    verify_target,
)


BOOTSTRAP_ROOT = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="bootstrap",
        description="Universal AI Development Bootstrap",
    )
    parser.add_argument("--version", action="version", version=VERSION)
    sub = parser.add_subparsers(dest="cmd", required=True)

    detect = sub.add_parser("detect", help="scan a target without modifying it")
    detect.add_argument("target", nargs="?", default=".")
    detect.add_argument("--intent", default="", help="optional one-line product/change intent for architecture synthesis")

    init = sub.add_parser("init", help="autonomously onboard the target and generate AI + human development context")
    init.add_argument("target", nargs="?", default=".")
    init.add_argument("--intent", default="", help="optional one-line product/change intent")
    init.add_argument("--force", action="store_true", help="replace generated .ai Markdown files")
    init.add_argument("--harness-only", action="store_true", help="skip human AGENTS/docs onboarding; preserve v1.1-style behavior")

    onboard = sub.add_parser("onboard", help="explicit alias for full autonomous onboarding")
    onboard.add_argument("target", nargs="?", default=".")
    onboard.add_argument("--intent", default="", help="optional one-line product/change intent")
    onboard.add_argument("--force", action="store_true", help="replace generated .ai Markdown files")

    verify = sub.add_parser("verify", help="validate the generated harness and human onboarding docs")
    verify.add_argument("target", nargs="?", default=".")

    baseline = sub.add_parser("baseline", help="inventory target or compare with a local reference")
    baseline.add_argument("target", nargs="?", default=".")
    baseline.add_argument("--reference", help="path to official/upstream/reference source tree")

    policy = sub.add_parser("policy-check", help="evaluate one path/command against .ai/policy.json")
    policy.add_argument("target")
    policy.add_argument("action", choices=["read", "write", "execute"])
    policy.add_argument("subject", help="path for read/write or full command for execute")

    memory = sub.add_parser("memory-add", help="store a verified project fact with provenance")
    memory.add_argument("target")
    memory.add_argument("key")
    memory.add_argument("value")
    memory.add_argument("--source", required=True, help="where this fact was verified")
    memory.add_argument("--confidence", type=float, default=1.0)

    args = parser.parse_args()
    target = Path(args.target).resolve()
    if not target.exists():
        parser.error("target does not exist: {}".format(target))

    if args.cmd == "detect":
        context = build_context(target, BOOTSTRAP_ROOT, args.intent)
        output = dict(context["facts"])
        output.update({
            "bootstrap_version": VERSION,
            "packs": context["packs"],
            "dependencies": context["dependencies"],
            "policy": context["policy"],
            "knowledge": context["knowledge"],
            "baseline": context["baseline"],
            "architecture": context["architecture"],
            "standards": context["standards"],
            "research": context["research"],
        })
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return 0

    if args.cmd == "init":
        result = init_target(
            target,
            BOOTSTRAP_ROOT,
            force=args.force,
            intent=args.intent,
            onboard=not args.harness_only,
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    if args.cmd == "onboard":
        print(json.dumps(onboard_target(target, BOOTSTRAP_ROOT, args.intent, args.force), indent=2, ensure_ascii=False))
        return 0

    if args.cmd == "verify":
        code, result = verify_target(target, BOOTSTRAP_ROOT)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return code

    if args.cmd == "baseline":
        reference = Path(args.reference).resolve() if args.reference else None
        if reference is not None and not reference.exists():
            parser.error("reference does not exist: {}".format(reference))
        report = run_baseline(target, BOOTSTRAP_ROOT, reference)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0

    if args.cmd == "policy-check":
        result = check_policy_target(target, args.action, args.subject)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 2 if result["decision"] == "deny" else (3 if result["decision"] == "confirm" else 0)

    item = add_memory_target(target, args.key, args.value, args.source, args.confidence)
    print(json.dumps({"status": "ok", "fact": item}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
