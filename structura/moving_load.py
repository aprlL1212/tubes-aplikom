import numpy as np
import plotly.graph_objects as go


def reactions(L, P, x):
    return P * (L - x) / L, P * x / L


def moment_under_load(L, P, x):
    return P * x * (L - x) / L


def render_moving_load_html(L, P, initial_x):
    return f"""<div style='padding:2rem;text-align:center;border:1px solid #ccd6e0;border-radius:12px'>🚚 Beban {P:g} kN pada x = {initial_x:g} m dari bentang {L:g} m</div>"""


def _fig(L, P, x, moment=True):
    xs = np.linspace(0, L, 100)
    ys = np.where(xs <= x, reactions(L, P, x)[0] * xs, reactions(L, P, x)[1] * (L - xs)) if moment else np.where(xs < x, reactions(L, P, x)[0], reactions(L, P, x)[0] - P)
    return go.Figure(go.Scatter(x=xs, y=ys, mode="lines", name="BMD" if moment else "SFD")).update_layout(xaxis_title="x (m)", yaxis_title="M (kN·m)" if moment else "V (kN)")


def plotly_diagrams_figure(L, P, x): return _fig(L, P, x, True)
def plotly_sfd_figure(L, P, x): return _fig(L, P, x, False)


def influence_lines(L, c):
    xs = np.linspace(0, L, 101)
    r1 = (L - xs) / L
    r2 = xs / L
    v = np.where(xs < c, -xs / L, (L - xs) / L)
    m = np.where(xs <= c, xs * (L - c) / L, c * (L - xs) / L)
    return xs, r1, r2, v, m


def to_structura_model(L, P, x, num_elements):
    xs = np.linspace(0, L, num_elements + 1)
    nodes = [{"id": i + 1, "x": float(pos), "y": 0.0} for i, pos in enumerate(xs)]
    members = [{"id": i + 1, "ni": i + 1, "nj": i + 2, "E": 200000.0, "b": 300.0, "h": 500.0} for i in range(num_elements)]
    nearest = int(np.argmin(abs(xs - x))) + 1
    return {"nodes": nodes, "members": members, "supports": [{"node": 1, "ux": True, "uy": True, "rz": True}, {"node": num_elements + 1, "ux": False, "uy": True, "rz": False}], "nodal_loads": [{"node": nearest, "Fx": 0.0, "Fy": -P, "M": 0.0}], "member_loads": []}
