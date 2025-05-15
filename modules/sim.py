import ltspice
import numpy as np
import pandas as pd
import re

def get_sim_data(file_path: str):
    lts = ltspice.Ltspice(file_path)
    lts.parse()
    return lts

def get_separate_signals(expr: str):
    # Match differential voltage: V(node1, node2)
    match_diff = re.match(r'V\(\s*([\w\d]+)\s*,\s*([\w\d]+)\s*\)', expr)
    if match_diff:
        pos_node, neg_node = match_diff.groups()
        return f"V({pos_node})", f"V({neg_node})"
    
    # Match single-ended voltage: V(node)
    match_single = re.match(r'V\(\s*([\w\d]+)\s*\)', expr)
    if match_single:
        pos_node = match_single.group(1)
        return f"V({pos_node})", None

    # If neither matches, it's an invalid format
    raise ValueError(f"Invalid voltage expression: {expr}")



def get_rms_reading(sim_data, net_name):
    try:
        waveform = sim_data.get_data(net_name)
        return np.sqrt(np.mean(waveform ** 2))
    except Exception as e:
        print(f"[ERROR] RMS for '{net_name}' failed: {e}")
        return None

def get_rms_diff(sim_data, pos_net, neg_net):
    try:
        v_pos = sim_data.get_data(pos_net)
        v_neg = sim_data.get_data(neg_net)
        diff = v_pos - v_neg
        return np.sqrt(np.mean(diff ** 2))
    except Exception as e:
        print(f"[ERROR] Diff RMS between '{pos_net}' and '{neg_net}' failed: {e}")
        return None

def get_peak_reading(sim_data, net_name):
    try:
        waveform = sim_data.get_data(net_name)
        return np.max(np.abs(waveform))
    except Exception as e:
        print(f"[ERROR] Peak for '{net_name}' failed: {e}")
        return None

def get_peak_to_peak_reading(sim_data, net_name):
    try:
        waveform = sim_data.get_data(net_name)
        return np.max(waveform) - np.min(waveform)
    except Exception as e:
        print(f"[ERROR] Peak-to-peak for '{net_name}' failed: {e}")
        return None

def get_peak_diff(sim_data, pos_net, neg_net):
    try:
        v_pos = sim_data.get_data(pos_net)
        v_neg = sim_data.get_data(neg_net)
        diff = v_pos - v_neg
        return np.max(np.abs(diff))
    except Exception as e:
        print(f"[ERROR] Peak diff between '{pos_net}' and '{neg_net}' failed: {e}")
        return None

def get_peak_to_peak_diff(sim_data, pos_net, neg_net):
    try:
        v_pos = sim_data.get_data(pos_net)
        v_neg = sim_data.get_data(neg_net)
        diff = v_pos - v_neg
        return np.max(diff) - np.min(diff)
    except Exception as e:
        print(f"[ERROR] Peak-to-peak diff between '{pos_net}' and '{neg_net}' failed: {e}")
        return None

def get_signal_dataframe(sim_data, pos_net, neg_net=None, label=None):
    try:
        time = sim_data.get_time_vector()
        v_pos = sim_data.get_data(pos_net)
        
        if neg_net:
            v_neg = sim_data.get_data(neg_net)
            y = v_pos - v_neg
            name = label if label else f"{pos_net}-{neg_net}"
        else:
            y = v_pos
            name = label if label else pos_net

        return pd.DataFrame({'time': time, name: y})
    
    except Exception as e:
        print(f"[ERROR] Failed to create DataFrame for '{pos_net}'{' and ' + neg_net if neg_net else ''}: {e}")
        return None
