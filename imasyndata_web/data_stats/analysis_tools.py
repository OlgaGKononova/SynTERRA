import os
import requests
import regex as re
import pandas as pd

from imasyndata_web.utils import query_db, get_material_elements
from imasyndata_web.constants import METAL_TYPES, MAP_COLLECTIONS, ELEMENTS
from imasyndata_web.operations_utils import convert_temp, get_last_heating_step


def get_elements_freq(materials_data):

    me_elements = set(el for elements in METAL_TYPES.values() for el in elements)
    me_elements = sorted(list(me_elements))
    elements_freq = {el: [] for el in me_elements}
    for data in materials_data:
        elements = get_material_elements(data)
        for el in elements:
            if el in elements_freq:
                elements_freq[el].extend(t["syntype"] for t in data["alias_array"])

    return {el: {k: v for k, v in pd.Series(freq).value_counts().items()}
            for el, freq in elements_freq.items()}


def get_temperature_per_syntype(recipe_data):
    temperature = {t: [] for t in recipe_data.keys()}

    for s_type, dataset in recipe_data.items():
        for data in dataset:
            firing_step = get_last_heating_step(data["operations"])
            if firing_step:
                firing_operation = data["operations"][firing_step]
                temperature[s_type].extend(convert_temp(t) for t in firing_operation["attributes"]["temperature"]
                                           if convert_temp(t))

    return temperature


def get_precursor_anion(precursor):
    m_anions = ['H2PO4', 'HPO4', 'HCO3', 'HSO4', 'HSO3', 'C2O4']
    d_anions = ['CO3', 'PO4', 'PO3', 'NH4', 'NO3', 'NO2', 'SO4', 'SO3', 'OH', 'CN']
    s_anions = ['O', 'H', 'N', 'C', 'F', 'S', 'B', 'P']
    # ions = m_anions + d_anions + s_anions + ['Cl'] + ['Org'] + ['Ac'] + ['Elem']

    precursor_ions = set()

    num_elemts = len(set(e for c in precursor['composition'] for e in c['elements'].keys()))
    formula = precursor["material_formula"]
    if 'H2O' in formula[-3:]:
        formula = precursor["composition"][0]["formula"]

    prec = formula

    if formula in ELEMENTS and num_elemts == 1:
        precursor_ions.add("Elem")

    acetates = {'CH3COO', "CH3CO2"}
    if any(a in prec for a in acetates):
        precursor_ions.add("Ac")
        for a in acetates:
            prec = prec.replace(a, '')

    if len(re.findall('C[HO]{1}', prec)) > 1:
        precursor_ions.add("Org")
    else:
        for a in m_anions + d_anions:
            if a in prec:
                precursor_ions.add(a)
                prec = prec.replace(a, '')

        prec_ = prec.rstrip('0987654321⋅.*')
        if len(prec_) > 0:
            for a in s_anions:
                if a == prec_[-1] and num_elemts == 2 and len(prec_[:-1]) > 1:
                    precursor_ions.add(a)
            if prec_[-2:] == 'Cl':
                precursor_ions.add("Cl")

    return precursor_ions


def get_prec_ions_freq(materials_data):
    anions_freq = {}

    for data in materials_data:
        for a in data["alias_array"]:
            if a["role"] == "precursor":
                anions = get_precursor_anion(data)
                for ion in anions:
                    if ion not in anions_freq:
                        anions_freq[ion] = []
                    anions_freq[ion].append(a["syntype"])

    return {a: {k: v for k, v in pd.Series(freq).value_counts().items()}
            for a, freq in anions_freq.items()}
