import pandas as pd


def _records(frame):
    return frame.fillna(0).to_dict("records") if isinstance(frame, pd.DataFrame) else list(frame or [])


def to_model(tables):
    model = {key: _records(tables.get(key, pd.DataFrame())) for key in ("nodes", "members", "supports", "nodal_loads", "member_loads")}
    errors = []
    for key in ("nodes", "members"):
        for row in model[key]:
            if key == "nodes" and not all(field in row for field in ("id", "x", "y")):
                errors.append("Kolom node belum lengkap.")
            if key == "members" and not all(field in row for field in ("id", "ni", "nj")):
                errors.append("Kolom elemen belum lengkap.")
    return model, errors


def validate(model):
    errors, warnings = [], []
    node_ids = {int(row["id"]) for row in model["nodes"] if row.get("id") not in (None, "")}
    if len(node_ids) != len(model["nodes"]):
        errors.append("ID node harus unik dan valid.")
    for member in model["members"]:
        if int(member.get("ni", 0)) not in node_ids or int(member.get("nj", 0)) not in node_ids:
            errors.append(f"Elemen {member.get('id')} merujuk node yang tidak ada.")
        if float(member.get("E", 1)) <= 0 or float(member.get("b", 1)) <= 0 or float(member.get("h", 1)) <= 0:
            errors.append(f"Properti elemen {member.get('id')} harus lebih besar dari nol.")
    if len(model["supports"]) == 0:
        warnings.append("Model belum memiliki tumpuan.")
    return errors, warnings
