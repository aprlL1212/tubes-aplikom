import pandas as pd

COLS = ("nodes", "members", "supports", "nodal_loads", "member_loads")
MODELS = ["🏢 Portal sederhana", "🌉 Balok sederhana", "📐 Kantilever"]


def from_model(model):
    model = model or {}
    return {
        "nodes": pd.DataFrame(model.get("nodes", []), columns=["id", "x", "y"]),
        "members": pd.DataFrame(model.get("members", []), columns=["id", "ni", "nj", "E", "b", "h"]),
        "supports": pd.DataFrame(model.get("supports", []), columns=["node", "ux", "uy", "rz"]),
        "nodal_loads": pd.DataFrame(model.get("nodal_loads", []), columns=["node", "Fx", "Fy", "M"]),
        "member_loads": pd.DataFrame(model.get("member_loads", []), columns=["member", "type", "dir", "value", "a"]),
    }


def _base(kind):
    nodes = [{"id": 1, "x": 0.0, "y": 0.0}, {"id": 2, "x": 6.0, "y": 0.0}]
    members = [{"id": 1, "ni": 1, "nj": 2, "E": 200000.0, "b": 300.0, "h": 500.0}]
    supports = [{"node": 1, "ux": True, "uy": True, "rz": kind == "📐 Kantilever"}, {"node": 2, "ux": False, "uy": True, "rz": False}]
    if kind == "📐 Kantilever":
        nodes = [{"id": 1, "x": 0.0, "y": 0.0}, {"id": 2, "x": 6.0, "y": 0.0}]
        supports = [{"node": 1, "ux": True, "uy": True, "rz": True}]
    return {"nodes": nodes, "members": members, "supports": supports,
            "nodal_loads": [{"node": 2, "Fx": 0.0, "Fy": -20.0, "M": 0.0}],
            "member_loads": []}


def load(name):
    return from_model(_base(name))
