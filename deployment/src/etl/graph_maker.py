import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as pe

from deployment.src.analytics.risk_analytics import RiskAnalytics


class GraphMaker:
    def __init__(self):
        self.analytics = RiskAnalytics()
        self.colors = {
            "green": "#39FF14",
            "pink": "#FF10F0",
            "yellow": "#FFFF33",
            "blue": "#48CAE4",
        }
        plt.rcParams["font.family"] = "Consolas"

    def set_nebula_gradient(self, ax):
        # (im sure there is a better way to do this but i was having fun w this sue me)
        space_cmap = LinearSegmentedColormap.from_list(
            "space",
            [
                (0.00, "#0B1020"),
                (0.20, "#1F1535"),
                (0.35, "#4A0D67"),
                (0.45, "#8A1883"),
                (0.50, "#97188F"),
                (0.55, "#8A1883"),
                (0.65, "#4A0D67"),
                (0.80, "#1F1535"),
                (1.00, "#0B1020"),
            ],
        )

        gradient = np.tile(np.linspace(0, 1, 256), (500, 1))

        ax.imshow(
            gradient,
            aspect="auto",
            cmap=space_cmap,
            extent=[0, 1, 0, 1],
            transform=ax.transAxes,
            alpha=1.00,
            zorder=0,
        )

    def set_random_stars(self, ax):
        for _ in range(100):
            ax.scatter(
                np.random.rand(),
                np.random.rand(),
                s=np.random.randint(1, 4),
                color="#E9ECEF",
                alpha=np.random.uniform(0.1, 0.6),
                transform=ax.transAxes,
                zorder=0,
            )

    def risk_dist(self):
        results = self.analytics.get_risk_breakdown()

        """ category doesnt get queried at all if there are none,
        so if i still want the catagory to show even with 0,
        i need to store the value to use it """

        risk_counts = {"LOW": 0, "MODERATE": 0, "HIGH": 0, "EXTREMELY HIGH": 0}

        for row in results:
            risk_counts[row.risk_level.upper()] = row.asteroid_count

        risk_levels = np.array(list(risk_counts.keys()))
        counts = np.array(list(risk_counts.values()))
        colors = np.array(list(self.colors.values()))

        fig, ax = plt.subplots(figsize=(10, 6))

        bars = ax.barh(risk_levels, counts, color=colors)
        max_count = counts.max()
        label_offset = max_count * 0.02

        ax.set_xlim(0, max_count * 1.15)

        for bar in bars:
            width = bar.get_width()

            ax.text(
                width + label_offset,
                bar.get_y() + bar.get_height() / 2,
                str(int(width)),
                color=self.colors["blue"],
                fontsize=16,
                fontweight="bold",
                va="center",
                # helps num not blend in with stars
                path_effects=[pe.withStroke(linewidth=4, foreground="#0B1020")],
            )

        # sets bg color for entire image
        fig.patch.set_facecolor("#090D1A")

        # gradiant background
        self.set_nebula_gradient(ax)

        # for x-axis if you want that instead of #'s at end of bar
        """ for spine in ax.spines.values():
            spine.set_visible(False)

        ax.tick_params(colors="white") """

        ax.tick_params(axis="y", colors="white")

        # centers the title across the whole image not just plot area
        fig.suptitle(
            "TODAY'S ASTEROID RISK DISTRIBUTION",
            color="white",
            fontsize=20,
            fontweight="bold",
        )

        # ax.set_xlabel("Number of Asteroids", color="white")
        ax.set_xlabel("")
        ax.set_xticks([])
        ax.set_ylabel("Risk Level", color="white")

        self.set_random_stars(ax)

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.savefig(
            "deployment/src/notebooks/dashboard.png",
            facecolor=fig.get_facecolor(),
            bbox_inches="tight",
        )
        plt.close(fig)
