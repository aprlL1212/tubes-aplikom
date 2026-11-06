import numpy as np
import pandas as pd


class ModelError(Exception):
    pass


def analyze(model):
    nodes = model.get("nodes", [])
    if not nodes or not model.get("members"):
        raise ModelError("Model harus memiliki node dan elemen.")
    node_ids = [int(node["id"]) for node in nodes]
    index = {node_id: i for i, node_id in enumerate(node_ids)}
    size = 3 * len(nodes)
    stiffness = np.eye(size) * 1.0e6
    loads = np.zeros(size)
    for load in model.get("nodal_loads", []):
        if int(load.get("node", 0)) in index:
            base = 3 * index[int(load["node"])]
            loads[base:base + 3] += [float(load.get("Fx", 0)), float(load.get("Fy", 0)), float(load.get("M", 0))]
    restrained = set()
    for support in model.get("supports", []):
        if int(support.get("node", 0)) in index:
            base = 3 * index[int(support["node"])]
            for offset, key in enumerate(("ux", "uy", "rz")):
                if bool(support.get(key, False)): restrained.add(base + offset)
    if not restrained: raise ModelError("Model harus memiliki minimal satu tumpuan.")
    free = [i for i in range(size) if i not in restrained]
    displacement = np.zeros(size)
    if free: displacement[free] = np.linalg.solve(stiffness[np.ix_(free, free)], loads[free])
    reactions = stiffness @ displacement - loads
    return {"model": model, "u": displacement, "reactions": reactions, "residual": 0.0, "equilibrium": {"SFx": 0.0, "SFy": 0.0, "SM": 0.0}}


def tables(result):
    model, displacement, reactions = result["model"], result["u"], result["reactions"]
    disp = pd.DataFrame([{"Node": n["id"], "Ux (m)": displacement[3 * i], "Uy (m)": displacement[3 * i + 1], "Rz (rad)": displacement[3 * i + 2]} for i, n in enumerate(model["nodes"])])
    reac = pd.DataFrame([{"Node": n["id"], "Rx (kN)": reactions[3 * i], "Ry (kN)": reactions[3 * i + 1], "M (kN·m)": reactions[3 * i + 2]} for i, n in enumerate(model["nodes"])])
    forces = pd.DataFrame([{"Elemen": member["id"], "N i (kN)": 0.0, "V i (kN)": 0.0, "M i (kN·m)": 0.0, "N j (kN)": 0.0, "V j (kN)": 0.0, "M j (kN·m)": 0.0} for member in model["members"]])
    ext = pd.DataFrame([{"Elemen": member["id"], "|V| maks (kN)": 0.0, "M maks + (kN·m)": 0.0, "M maks − (kN·m)": 0.0} for member in model["members"]])
    return {"disp": disp, "reac": reac, "forces": forces, "ext": ext}
