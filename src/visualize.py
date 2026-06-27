import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Rectangle

from config import settings


def _draw_court(ax, color="black", lw=2):
    """Draw a half court on the given axes. Units are feet, hoop at (0, 0)."""
    hoop = Circle((0, 0), radius=0.75, linewidth=lw, color=color, fill=False)
    backboard = Rectangle((-3, -0.75), 6, -0.1, linewidth=lw, color=color)

    # the paint
    outer_box = Rectangle((-8, -4.75), 16, 19, linewidth=lw, color=color, fill=False)
    inner_box = Rectangle((-6, -4.75), 12, 19, linewidth=lw, color=color, fill=False)

    # free throw arcs
    top_ft = Arc((0, 14.25), 12, 12, theta1=0, theta2=180, linewidth=lw, color=color)
    bottom_ft = Arc((0, 14.25), 12, 12, theta1=180, theta2=360,
                    linewidth=lw, color=color, linestyle="dashed")

    # restricted area
    restricted = Arc((0, 0), 8, 8, theta1=0, theta2=180, linewidth=lw, color=color)

    # three point line
    corner_left = Rectangle((-22, -4.75), 0, 14, linewidth=lw, color=color)
    corner_right = Rectangle((22, -4.75), 0, 14, linewidth=lw, color=color)
    arc_three = Arc((0, 0), 47.5, 47.5, theta1=22, theta2=158, linewidth=lw, color=color)

    for element in [hoop, backboard, outer_box, inner_box, top_ft,
                    bottom_ft, restricted, corner_left, corner_right, arc_three]:
        ax.add_patch(element)

    return ax


def plot_shot_chart(shots, title=None, save=True):
    """Render a hexbin shot chart for the cleaned shot DataFrame."""
    fig, ax = plt.subplots(figsize=(9, 8.5))

    hb = ax.hexbin(
        shots["LOC_X"], shots["LOC_Y"],
        gridsize=30, cmap="inferno", mincnt=1, extent=(-25, 25, -5, 30),
    )
    _draw_court(ax, color="white")

    ax.set_xlim(-25, 25)
    ax.set_ylim(-5, 30)
    ax.set_facecolor("#1a1a1a")
    ax.set_xticks([])
    ax.set_yticks([])

    chart_title = title or f"{settings.PLAYER_NAME} Shot Density ({settings.SEASON})"
    ax.set_title(chart_title, color="white", fontsize=14, pad=12)
    fig.colorbar(hb, ax=ax, label="Shot frequency")
    fig.patch.set_facecolor("#1a1a1a")

    if save:
        settings.CHARTS_DIR.mkdir(parents=True, exist_ok=True)
        name = settings.PLAYER_NAME.replace(" ", "_")
        out = settings.CHARTS_DIR / f"shotchart_{name}_{settings.SEASON.replace('-', '')}.png"
        fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
        print(f"[visualize] saved chart to {out.name}")

    return fig, ax