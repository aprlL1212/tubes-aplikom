import plotly.graph_objects as go


def model_fig(model, title="Model"):
    by_id = {int(n["id"]): n for n in model.get("nodes", [])}
    fig = go.Figure()
    for member in model.get("members", []):
        a, b = by_id.get(int(member["ni"])), by_id.get(int(member["nj"]))
        if a and b: fig.add_trace(go.Scatter(x=[a["x"], b["x"]], y=[a["y"], b["y"]], mode="lines+markers", name=f"E{member['id']}"))
    return fig.update_layout(title=title, xaxis_title="x (m)", yaxis_title="y (m)", height=420)


def deformed_fig(result, scale=1.0): return model_fig(result["model"], f"Deformasi x{scale:g}")
def diagram_fig(result, kind): return go.Figure().update_layout(title=f"Diagram {kind}", height=420)
