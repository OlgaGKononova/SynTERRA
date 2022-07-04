from imasyndata_web.utils import get_material_elements
from imasyndata_web.data_handler.targets.components import targets_stats_plot

def __get_targets_table(data):
    all_targets = {}
    per_element = {}
    if all("_target" in row for row in data):
        for row in data:
            t_elements = get_material_elements(row["_target"])
            t_formula = row["_target"]["material_formula"]
            if t_formula not in all_targets:
                all_targets[t_formula] = 0
            all_targets[t_formula] += 1

            for el in t_elements:
                if el not in per_element:
                    per_element[el] = set()
                per_element[el].add(t_formula)

    return all_targets, per_element


def build_targets_content(data):

    all_targets, per_element = __get_targets_table(data)
    if not all_targets:
        return [], [], ""

    checkbox_options = [{"label": el, "value": el} for el in sorted(per_element.keys())]
    checkbox_label = "Show targets containing element(s):\n"

    all_targets = [(k, v) for k, v in sorted(all_targets.items(), key=lambda x: x[1])]

    targets_plot = targets_stats_plot(all_targets,
                                      "targets-counts",
                                      "{:,} unique targets".format(len(all_targets)))

    return targets_plot, checkbox_options, checkbox_label


def build_targets_elem_stats(data, chosen_elements):
    if not chosen_elements:
        return ""

    all_targets, per_element = __get_targets_table(data)
    if not all_targets:
        return ""

    element_targets = {}
    if chosen_elements:
        element_targets = {t: all_targets[t] for el in chosen_elements for t in per_element.get(el, {})}

    element_targets = [(k, v) for k, v in sorted(element_targets.items(), key=lambda x: x[1])]

    plot_title = "{:,} unique targets for {}".format(len(element_targets), ", ".join(chosen_elements))
    element_targets_plot = targets_stats_plot(element_targets, "targets-elem-counts", plot_title)

    return element_targets_plot
