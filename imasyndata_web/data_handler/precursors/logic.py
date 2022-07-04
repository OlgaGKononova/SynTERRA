from imasyndata_web.utils import get_material_elements
from imasyndata_web.data_handler.precursors.components import precursors_stats_plot


def __get_precursors_table(data):
    all_precursors = {}
    per_element = {}
    if all("_precursors" in row for row in data):
        for row in data:
            for p in row["_precursors"]:
                p_elements = get_material_elements(p)
                p_formula = p["material_formula"]
                if p_formula not in all_precursors:
                    all_precursors[p_formula] = 0
                all_precursors[p_formula] += 1

                for el in p_elements:
                    if el not in per_element:
                        per_element[el] = set()
                    per_element[el].add(p_formula)

    return all_precursors, per_element


def build_precursors_content(data):

    all_precursors, per_element = __get_precursors_table(data)
    if not all_precursors:
        return [], [], ""

    checkbox_options = [{"label": el, "value": el} for el in sorted(per_element.keys())]
    checkbox_label = "Show precursors containint element(s):\n"

    all_precursors = [(k, v) for k, v in sorted(all_precursors.items(), key=lambda x: x[1])]

    precursors_plot = precursors_stats_plot(all_precursors,
                                            "precursors-counts",
                                            "{:,} unique precursors".format(len(all_precursors)))

    return precursors_plot, checkbox_options, checkbox_label


def build_precursors_elem_stats(data, chosen_elements):
    if not chosen_elements:
        return ""

    all_precursors, per_element = __get_precursors_table(data)
    if not all_precursors:
        return ""

    element_precursors = {}
    if chosen_elements:
        element_precursors = {t: all_precursors[t] for el in chosen_elements for t in per_element.get(el, {})}

    element_precursors = [(k, v) for k, v in sorted(element_precursors.items(), key=lambda x: x[1])]

    plot_title = "{:,} unique precursors for {}".format(len(element_precursors), ", ".join(chosen_elements))
    element_precursors_plot = precursors_stats_plot(element_precursors, "precursors-elem-counts", plot_title)

    return element_precursors_plot
