PUB_COLOR_SCHEME = ["#6aa8ce", "#2e82b9", "#5ca3a3", "#aedc8b", "#6fbe58", "#44a035", "#b39c72", "#f57979", "#e31a1c"]
# next color: "#a6cee3"

SYN_TYPES_COLOR_SCHEME = ["#EF963B", "#C93277", "#EF533B", "#349600", "#57D4F1"]

BG_COLOR = "#d9d9d9"
BG_COLOR_PLOT = "#f2f2f2"

GRID_COLOR = "#b7b7b7"

FONT = {"plot_title": dict(size=16, color="black"),
        "axis_ticks": dict(size=12, color="black"),
        "axis_title": dict(size=14, color="black")}

PLOT_AXIS_STYLE = dict(xaxis=dict(title_font=FONT["axis_title"], title_standoff=10,
                                  linecolor="#000000", linewidth=2,
                                  tickfont=FONT["axis_ticks"],
                                  gridcolor=GRID_COLOR
                                  ),
                       yaxis=dict(title_font=FONT["axis_title"],
                                  linecolor="#000000", linewidth=2,
                                  tickfont=FONT["axis_ticks"],
                                  #gridcolor=GRID_COLOR,
                                  dtick=1))

PLOT_TITLE_STYLE = dict(title_font=FONT["plot_title"],
                        title_pad=dict(t=0, b=0, l=0, r=0))

TARGET_COLORS = {"bars_marker": "#da0909",
                 "bars_line": "#ad0707"}

PRECURSOR_COLORS = {"bars_marker": "#497608", #"rgba(219, 64, 82, 0.7)",
                    "bars_line": "#2f4d05"}#"rgba(219, 64, 82, 1.0)"}


VALENCE_COLORS = {"targets_bars_marker": "rgba(127, 198, 14, 0.7)",
                  "targets_bars_line": "rgba(127, 198, 14, 1.0)",
                  "precursors_bars_marker": "rgba(246, 162, 14, 0.7)",
                  "precursors_bars_line": "rgba(246, 162, 14, 1.0)"}


TEMPERATURE_COLORS = {"bars_marker": "rgba(55, 128, 191, 0.7)",
                      "bars_line": "rgba(55, 128, 191, 1.0)"}

TIME_COLORS = {"bars_marker": "rgba(50, 171, 96, 0.7)",
               "bars_line": "rgba(50, 171, 96, 1.0)"}

ENVIRONMENT_COLORS = {"bars_marker": "rgba(178, 77, 248, 0.7)",
                      "bars_line": "rgba(178, 77, 248, 1.0)"}

ENERGY_COLORS = {"pos": 'rgb(200, 7, 39)',
                 "neg": 'rgb(9, 127, 249)'}