from copy import deepcopy
import pandas as pd
import networkx as nx
from itertools import chain
from hashlib import sha1


def conditional_add_edge(u, v, graph: nx.Graph, attributes: dict):
    if graph.has_edge(u, v):
        # update edge
        cur_edge_data = graph.get_edge_data(u, v)
        for key, value in attributes.items():
            if key in ['time']:
                pass
            else:
                cur_edge_data[key] += value
    else:
        graph.add_edge(u, v, **attributes)


def update_edge_details(final_edge_data: dict, prev_edge_data: dict) -> dict:
    for k, v in prev_edge_data.items():
        if k in ['pos', 'time', 'data']:
            continue
        if k not in final_edge_data:
            final_edge_data[k] = v
        else:
            final_edge_data[k] += v
    return final_edge_data


def update_node_details(final_node_data: dict, prev_node_data: dict) -> dict:
    for k, v in prev_node_data.items():
        if k in ['pos', 'time', 'data']:
            continue
        if k not in final_node_data:
            final_node_data[k] = v
        else:
            final_node_data[k] += v

    return final_node_data


class Prediction(dict):
    """Data Structure to wrap a Prediction dictionary with additional functionality

    Provides interfaces for generating NetworkX graphs from prediction information

    """

    def __init__(self, prediction: dict = None, metadata: list = None, **kwargs):
        """Constuct Prediction class object. Optionally provide
        metadata information for sequence

        Args:
            prediction (dict, optional): Prediction dictionary. Defaults to None.
            metadata (list, optional): Optional sequence of metadata
                pertaining to prediction object (from model). Defaults to None.
        """
        if prediction is None:
            prediction = kwargs
        self.confidence: float = prediction["confidence"]
        self.confluence: float = prediction["confluence"]
        self.emotives: dict = prediction["emotives"]
        self.entropy: float = prediction["entropy"]
        self.evidence: float = prediction["evidence"]
        self.extras: list = prediction["extras"]
        self.fragmentation: float = prediction["fragmentation"]
        self.frequency: int = prediction["frequency"]
        self.future: list = prediction["future"]
        self.grand_hamiltonian: float = prediction["grand_hamiltonian"]
        self.hamiltonian: float = prediction["hamiltonian"]
        self.itfdf_similarity: float = prediction["itfdf_similarity"]
        self.matches: list = prediction["matches"]
        self.missing: list = prediction["missing"]
        self.name: str = prediction["name"]
        self.past: list = prediction["past"]
        self.potential: float = prediction["potential"]
        self.present: list = prediction["present"]
        self.similarity: float = prediction["similarity"]
        self.snr: float = prediction["snr"]
        self.type: str = prediction["type"]

        self.events = chain(self.past, self.present, self.future)
        
        if metadata is None:
            metadata = [[None for _ in self.events]]
        self.metadata = metadata
        pass

    def __repr__(self) -> str:
        return f"Prediction(MODEL|{self.name}, potential={self.potential})"

    def toJSON(self) -> dict:
        """Convert Prediction Object back into dictionary format

        Returns:
            dict: prediction in dict format
        """
        return {
            "confidence": self.confidence,
            "confluence": self.confluence,
            "emotives": self.emotives,
            "entropy": self.entropy,
            "evidence": self.evidence,
            "extras": self.extras,
            "fragmentation": self.fragmentation,
            "frequency": self.frequency,
            "future": self.future,
            "grand_hamiltonian": self.grand_hamiltonian,
            "hamiltonian": self.hamiltonian,
            "itfdf_similarity": self.itfdf_similarity,
            "matches": self.matches,
            "missing": self.missing,
            "name": self.name,
            "past": self.past,
            "potential": self.potential,
            "present": self.present,
            "similarity": self.similarity,
            "snr": self.snr,
            "type": self.type,
        }

    def toPastStateGraph(self, starting_idx=0) -> nx.Graph:
        G = nx.Graph()

        idx = starting_idx
        event: list
        event_indexes = []
        for event in self.past:
            symbol: str
            for symbol in event:
                # node metadata for graph (might not mean much for past state)
                symbol_attributes = {'symbol_type': None}
                if symbol in self.missing:
                    symbol_attributes['symbol_type'] = 'missing'
                elif symbol in self.matches:
                    symbol_attributes['symbol_type'] = 'matches'
                elif symbol in self.extras:
                    symbol_attributes['symbol_type'] = 'extras'
                G.add_node(idx, **symbol_attributes)
                event_indexes.append(idx)
                if idx != 0:
                    G.add_edge(idx - 1, idx)
                idx += 1

        return G

    def toPresentStateGraph(self, starting_idx=0) -> nx.Graph:
        G = nx.Graph()

        idx = starting_idx
        event: list
        event_indexes = []
        for event in self.present:
            symbol: str
            for symbol in event:
                # node metadata for graph
                symbol_attributes = {'symbol_type': None}
                if symbol in self.missing:
                    symbol_attributes['symbol_type'] = 'missing'
                elif symbol in self.matches:
                    symbol_attributes['symbol_type'] = 'matches'
                elif symbol in self.extras:
                    symbol_attributes['symbol_type'] = 'extras'
                G.add_node(idx, **symbol_attributes)
                event_indexes.append(idx)
                if idx != 0:
                    G.add_edge(idx - 1, idx)
                idx += 1

            event_indexes = []
        return G

    def toEventGraph(self) -> nx.Graph:
        G = nx.Graph()

        idx = 0
        past_idxs = []
        present_idxs = []
        future_idxs = []
        for e in self.past:
            past_idxs.append(idx)
            idx += 1
        for e in self.present:
            present_idxs.append(idx)
            idx += 1
        for e in self.future:
            future_idxs.append(idx)
            idx += 1
        print(f'{past_idxs=}, {present_idxs=}, {future_idxs=}')

        G.add_nodes_from(
            zip(past_idxs, [{'data': e, 'time': 'past'} for e in self.past]))
        G.add_nodes_from(
            zip(present_idxs, [{'data': e, 'time': 'present'} for e in self.present]))
        G.add_nodes_from(
            zip(future_idxs, [{'data': e, 'time': 'future'} for e in self.future]))

        for i, idx in enumerate(past_idxs):
            if i >= len(past_idxs) - 1:
                break
            u, v = past_idxs[i], past_idxs[i+1]
            attributes = {'time': 'past',
                          'weight': 1,
                          'frequency': self.frequency}
            conditional_add_edge(u=u, v=v, graph=G, attributes=attributes)
        for i, event in enumerate(present_idxs):
            if i == 0 and self.past:
                u, v = past_idxs[-1], present_idxs[i]
                attributes = {'time': 'past_to_present',
                              'weight': 1,
                              'frequency': self.frequency}
                conditional_add_edge(u=u, v=v, graph=G, attributes=attributes)
            if i >= len(present_idxs) - 1:
                break
            else:
                u, v = present_idxs[i], present_idxs[i+1]
                attributes = {'time': 'present',
                              'weight': 1,
                              'frequency': self.frequency}
                conditional_add_edge(u=u, v=v, graph=G, attributes=attributes)

        for i, event in enumerate(future_idxs):
            if i == 0 and self.present:

                u, v = present_idxs[-1], future_idxs[i]
                attributes = {'time': 'present_to_future',
                              'weight': 1,
                              'frequency': self.frequency}
                conditional_add_edge(u=u, v=v, graph=G, attributes=attributes)
            if i == len(self.future) - 1:
                break
            else:
                u, v = future_idxs[i], future_idxs[i+1]
                attributes = {'time': 'future',
                              'weight': 1,
                              'frequency': self.frequency}
                conditional_add_edge(u=u, v=v, graph=G, attributes=attributes)

        return G

    def toLoopingEventGraph(self) -> nx.DiGraph:

        G = nx.DiGraph()
        past_event_hashes = []
        present_event_hashes = []
        future_event_hashes = []

        # hash each event in prediction, use as node "id" in graph
        for e in self.past:
            past_event_hashes.append(sha1(str(e).encode()).hexdigest()[:8])
        for e in self.present:
            present_event_hashes.append(sha1(str(e).encode()).hexdigest()[:8])
        for e in self.future:
            future_event_hashes.append(sha1(str(e).encode()).hexdigest()[:8])

        # add a node for each event, including symbol list, time information in node_data
        G.add_nodes_from(
            zip(past_event_hashes, [{'data': e} for e in self.past]))
        G.add_nodes_from(
            zip(present_event_hashes, [{'data': e} for e in self.present]))
        G.add_nodes_from(
            zip(future_event_hashes, [{'data': e} for e in self.future]))

        for i, _ in enumerate(past_event_hashes):
            if i >= len(past_event_hashes) - 1:
                break
            u, v = past_event_hashes[i], past_event_hashes[i+1]
            attributes = {'time': 'past',
                          'weight': 1,
                          'frequency': self.frequency}
            conditional_add_edge(u=u, v=v, graph=G, attributes=attributes)

        for i, _ in enumerate(present_event_hashes):
            if i == 0 and self.past:
                u, v = past_event_hashes[-1], present_event_hashes[i]
                attributes = {'time': 'past_to_present',
                              'weight': 1,
                              'frequency': self.frequency}
                conditional_add_edge(u=u, v=v, graph=G, attributes=attributes)
            if i >= len(present_event_hashes) - 1:
                break

            u, v = present_event_hashes[i], present_event_hashes[i+1]
            attributes = {'time': 'present',
                          'weight': 1,
                          'frequency': self.frequency}
            conditional_add_edge(u=u, v=v, graph=G, attributes=attributes)

        for i, _ in enumerate(future_event_hashes):
            if i == 0 and self.present:

                u, v = present_event_hashes[-1], future_event_hashes[i]
                attributes = {'time': 'present_to_future',
                              'weight': 1,
                              'frequency': self.frequency}
                conditional_add_edge(u=u, v=v, graph=G, attributes=attributes)

            if i == len(self.future) - 1:
                break

            u, v = future_event_hashes[i], future_event_hashes[i+1]
            attributes = {'time': 'future',
                          'weight': 1,
                          'frequency': self.frequency}
            conditional_add_edge(u=u, v=v, graph=G, attributes=attributes)
        return G


class PredictionEnsemble:
    def __init__(self, ensemble, metadata_dict: dict = None, node_name: str = None) -> None:
        """Convert Prediction ensemble into class object

        Args:
            ensemble (_type_): the ensemble in list or dict form
            metadata_dict (dict, optional): dict of {model_name: metadata}. Defaults to None.
            node_name (str, optional): Node name for ensemble if provided as list. Defaults to None.
        """
        if node_name is None:
            node_name = "NODE"

        if isinstance(ensemble, list):
            ensemble = {node_name: ensemble}

        self._ensemble = deepcopy(ensemble)
        self.ensemble = {}

        for k, preds in self._ensemble.items():
            if metadata_dict:
                self.ensemble[k] = [Prediction(
                    prediction=p, metadata=metadata_dict[p['name']]) for p in preds]
            else:
                self.ensemble[k] = [Prediction(prediction=p) for p in preds]

    def __repr__(self) -> str:
        return f"PredictionEnsemble(nodes={list(self.ensemble.keys())})"

    def toDataFrame(self) -> pd.DataFrame:
        """Construct pandas DataFrame using prediction as a row

        Returns:
            pd.DataFrame: _description_
        """
        predictions = []
        for k, preds in self.ensemble.items():
            pred: Prediction
            for pred in preds:
                predictions.append({**pred.toJSON(), **{'node': k}})

        return pd.DataFrame(predictions)

    def toEventGraph(self) -> nx.DiGraph:
        pred_graphs = []
        for preds in self.ensemble.values():
            pred: Prediction
            for pred in preds:
                pred_graphs.append(pred.toLoopingEventGraph())

        graph: nx.DiGraph
        for i, graph in enumerate(pred_graphs):
            for j, (node, node_data) in enumerate(graph.nodes(data=True)):
                node_data['pos'] = (10*j, i)

        final_graph = nx.DiGraph()
        graph: nx.DiGraph
        for graph in pred_graphs:
            for node, prev_node_data in graph.nodes(data=True):
                # prev_node_data['time'] = None
                if not final_graph.has_node(node):
                    final_graph.add_node(node, **prev_node_data)
                else:
                    # need to merge node data
                    nx.set_node_attributes(final_graph, {node: update_node_details(
                        final_graph.nodes[node], prev_node_data)})

            for u, v, prev_edge_data in graph.edges(data=True):
                prev_edge_data['time'] = None
                if not final_graph.has_edge(u, v):
                    final_graph.add_edge(u, v, **prev_edge_data)
                else:
                    # need to merge node data
                    nx.set_edge_attributes(final_graph, {(u, v): update_edge_details(
                        final_graph.edges[u, v], prev_edge_data)})

        return final_graph
