import numpy as np
from imasyndata_web.constants import IMAGES_LOCATION
from imasyndata_web.data_handler.operations.components import \
    serve_layout, plot_operation_attributes, plot_operation_precursors
from imasyndata_web.data_handler.operations.attributes import get_operation_attributes, get_operation_precursors
import imasyndata_web.data_handler.operations.constants as consts
from imasyndata_web.data_handler.operations.cytoscape_stylesheet import SYN_GRAPH_STYLESHEET


def __generate_graph_elements(graph, threshold):

    location = IMAGES_LOCATION

    edges, width = np.transpose(np.where(graph > threshold)), graph[np.where(graph > threshold)]
    max_width, min_width = np.max(width), np.min(width)
    
    elements = [{'data': {'id': op.lower(),
                          'label': op,
                          'url': location + op.lower() + '_100px.png'},
                 'position': consts.LABELS_POSITION[op]} for op in consts.ID2STEP]
    
    elements.extend({'data': {'id': consts.ID2STEP[ids[0]].lower() + consts.ID2STEP[ids[1]].lower(),
                              'source': consts.ID2STEP[ids[0]].lower(),
                              'target': consts.ID2STEP[ids[1]].lower(),
                              'amount': w}} for ids, w in zip(edges, width))

    stylesheet = [{'selector': 'node', 'style': SYN_GRAPH_STYLESHEET["nodes"]},
                  {'selector': 'edge', 'style': SYN_GRAPH_STYLESHEET["edges"]}]
    scale = SYN_GRAPH_STYLESHEET["edge_width_scale"] / (max_width - min_width)
    stylesheet.extend({'selector': '#' + consts.ID2STEP[ids[0]].lower() + consts.ID2STEP[ids[1]].lower(),
                       'style': {'width': scale * (w - min_width + 1)}} for ids, w in zip(edges, width))

    return elements, stylesheet


def __convert_into_graph(operations):
    matrix_size = len(consts.ID2STEP)
    syn_graph = np.zeros((matrix_size, matrix_size), dtype=int)
    operations_sequence = ['Start']
    operations_sequence.extend(consts.OPERATIONS_STEP_MAP.get(op['type'], "") for op in operations)
    operations_sequence.append("End")

    previous_operation = 0
    for step in operations_sequence[1:]:
        if step:
            next_operation = consts.STEP2ID[step]
            syn_graph[previous_operation, next_operation] = syn_graph[previous_operation, next_operation] + 1
            previous_operation = next_operation

    return syn_graph


def draw_operations_graph(data, threshold=""):

    if not data:
        return [], [], 0, {}

    threshold = 0 if not threshold else int(threshold)

    if all('_operations' in row for row in data):
        synthesis_graphs = [__convert_into_graph(row['_operations']) for row in data]
        sum_edges = np.sum(np.array(synthesis_graphs), 0)
    else:
        return [], [], 0, {}

    graph_elements = []
    graph_style = []
    max_value = np.max(sum_edges)
    marks = {}
    if max_value:
        graph_elements, graph_style = __generate_graph_elements(sum_edges, threshold)
        step = int(max_value / 10) if max_value > 40 else 2
        marks = {i * step: '{}'.format(i * step) for i in range(int(max_value / step))}

    return graph_elements, graph_style, max_value, marks


def build_operations_content(data):
    graph_elements, graph_style, max_value, marks = draw_operations_graph(data)
    return serve_layout(graph_elements, graph_style, max_value, marks)


def draw_operation_attributes(data, operation):
    graph = "Click a graph node to display attributes..."
    label_text = consts.DEFAULT_ATTRIBUTES_LBL
    attributes = get_operation_attributes(data, operation)
    if any(a for a in attributes.values()):
        graph = plot_operation_attributes(attributes, "operation-attributes_graph")
        label_text = "Operation attributes for "+ operation["label"].upper()
    return graph, label_text


def draw_operation_precursors(data, edge):
    graph = "Click a graph edge to display attributes..."
    label_text = consts.DEFAULT_PRECURSORS_LBL
    if all('_operations' in row for row in data) and edge:
        operation_precursors = [{"graph": __convert_into_graph(row['_operations']),
                                 "precursors": [p['material_formula'] for p in row["_precursors"]]} for row in data]
        all_precursors = get_operation_precursors(operation_precursors, edge)
        graph = plot_operation_precursors(all_precursors, "operation-precursors_graph")
        label_text = "Common precursors used with the step " + edge['source'].upper() + '->' + edge['target'].upper()
    return graph, label_text
