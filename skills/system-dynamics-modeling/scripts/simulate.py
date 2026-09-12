#!/usr/bin/env python3
"""Run a small deterministic stock-flow model with restricted expressions."""

from __future__ import annotations

import argparse
import ast
import csv
import json
import math
import sys
from pathlib import Path


FUNCTIONS = {"abs": abs, "min": min, "max": max, "exp": math.exp, "log": math.log, "sqrt": math.sqrt}
BINOPS = {ast.Add: lambda a, b: a + b, ast.Sub: lambda a, b: a - b, ast.Mult: lambda a, b: a * b,
          ast.Div: lambda a, b: a / b, ast.Pow: lambda a, b: a**b, ast.Mod: lambda a, b: a % b}
UNARYOPS = {ast.UAdd: lambda a: a, ast.USub: lambda a: -a}


def evaluate(expression: str, values: dict[str, float]) -> float:
    tree = ast.parse(expression, mode="eval")

    def visit(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.Name):
            if node.id not in values:
                raise ValueError(f"unknown name in expression: {node.id}")
            return float(values[node.id])
        if isinstance(node, ast.BinOp) and type(node.op) in BINOPS:
            return BINOPS[type(node.op)](visit(node.left), visit(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in UNARYOPS:
            return UNARYOPS[type(node.op)](visit(node.operand))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            function = FUNCTIONS.get(node.func.id)
            if function is None or node.keywords:
                raise ValueError(f"unsupported function: {node.func.id}")
            return float(function(*(visit(arg) for arg in node.args)))
        raise ValueError(f"unsupported expression syntax: {ast.dump(node, include_attributes=False)}")

    result = visit(tree)
    if not math.isfinite(result):
        raise ValueError(f"expression produced a non-finite result: {expression}")
    return result


def scenario_model(model: dict, name: str | None) -> dict:
    if not name:
        return model
    scenarios = model.get("scenarios", {})
    if name not in scenarios:
        raise ValueError(f"unknown scenario: {name}")
    selected = json.loads(json.dumps(model))
    override = scenarios[name]
    selected["parameters"].update(override.get("parameters", {}))
    for stock_name, initial in override.get("stocks", {}).items():
        if stock_name not in selected["stocks"]:
            raise ValueError(f"scenario references unknown stock: {stock_name}")
        selected["stocks"][stock_name]["initial"] = initial
    return selected


def run(model: dict) -> list[dict[str, float]]:
    config = model["simulation"]
    start, stop, dt = (float(config[key]) for key in ("start", "stop", "dt"))
    if dt <= 0 or stop < start:
        raise ValueError("require dt > 0 and stop >= start")
    raw_steps = (stop - start) / dt
    steps = round(raw_steps)
    if not math.isclose(raw_steps, steps, rel_tol=1e-9, abs_tol=1e-9):
        raise ValueError("dt must divide the simulation horizon")

    stock_defs = model["stocks"]
    stocks = {name: float(spec["initial"]) for name, spec in stock_defs.items()}
    parameters = {name: float(value) for name, value in model.get("parameters", {}).items()}
    auxiliaries = model.get("auxiliaries", {})
    flows = model.get("flows", {})
    rows: list[dict[str, float]] = []

    for step in range(steps + 1):
        time = start + step * dt
        environment = {**parameters, **stocks, "time": time}
        for name, expression in auxiliaries.items():
            environment[name] = evaluate(expression, environment)
        flow_values = {name: evaluate(spec["equation"], environment) for name, spec in flows.items()}
        rows.append({"time": time, **stocks, **{f"flow:{k}": v for k, v in flow_values.items()}})
        if step == steps:
            break

        derivatives = dict.fromkeys(stocks, 0.0)
        for flow_name, value in flow_values.items():
            for stock_name, direction in flows[flow_name].get("affects", {}).items():
                if stock_name not in derivatives:
                    raise ValueError(f"flow {flow_name} affects unknown stock: {stock_name}")
                derivatives[stock_name] += value * float(direction)
        for name in stocks:
            updated = stocks[name] + derivatives[name] * dt
            stocks[name] = max(0.0, updated) if stock_defs[name].get("nonnegative") else updated
    return rows


def self_test() -> None:
    model = {
        "simulation": {"start": 0, "stop": 2, "dt": 1},
        "stocks": {"customers": {"initial": 10, "nonnegative": True}},
        "parameters": {"gain": 2, "loss_fraction": 0.1},
        "auxiliaries": {"loss": "customers * loss_fraction"},
        "flows": {"gain": {"equation": "gain", "affects": {"customers": 1}},
                  "loss": {"equation": "loss", "affects": {"customers": -1}}},
    }
    rows = run(model)
    assert [row["customers"] for row in rows] == [10.0, 11.0, 11.9]
    try:
        evaluate("__import__('os')", {})
    except ValueError:
        pass
    else:
        raise AssertionError("unsafe expression was accepted")
    print("self-test passed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", nargs="?", type=Path)
    parser.add_argument("--scenario")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if args.model is None:
        parser.error("model is required unless --self-test is used")

    model = scenario_model(json.loads(args.model.read_text()), args.scenario)
    rows = run(model)
    target = args.output.open("w", newline="") if args.output else sys.stdout
    try:
        writer = csv.DictWriter(target, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    finally:
        if args.output:
            target.close()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2)
