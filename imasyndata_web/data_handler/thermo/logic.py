from imasyndata_web.utils import get_material_elements


def __get_energies_table(data, temp_value):
    all_targets = {}

    if all('_target' in row for row in data):
        data = [row for row in data if row['_target']['thermo']]
        for idx, row in enumerate(data):
            material = {}
            material["composition"] = [c for c in row['_target']['composition'] if c['formula'] != 'H2O']
            elements = get_material_elements(material)
            formula_id = '-'.join(sorted(elements))
            if formula_id not in all_targets:
                all_targets[formula_id] = []

            thermo =  row['_target']['thermo']
            hf = thermo['Hf'] if temp_value < 300 else thermo['T'][str(temp_value)]['dGf']
            hd = thermo['Hd'] if temp_value < 300 else thermo['T'][str(temp_value)]['dGd']
            all_targets[formula_id].append({'Hf': hf, 'Hd': hd})

    return all_targets


def build_materials_thermo_content(data, temp_value, sorting_flag):
    temp_value = int(temp_value)
    all_targets = __get_energies_table(data, temp_value)

    if not all_targets:
        return ""

    all_targets = [(k, v)
                   for k, v in sorted(all_targets.items(), key=lambda x: np.mean([d[sorting_flag] for d in x[1]]))]

    energy_graph = plot_material_energies(all_targets, "energy-data")

    return [html.Div(energy_graph, id="target-energy_plot"),
            html.Div("", id="expand-material", className="row")]