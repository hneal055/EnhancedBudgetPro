"""
Character Relationship Graph Engine
Analyzes and visualizes character interactions using NetworkX
"""

import networkx as nx
import plotly.graph_objects as go
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class RelationshipGraphEngine:
    """Builds and analyzes character relationship networks."""
    
    def __init__(self):
        self.graph = None
        logger.info("RelationshipGraphEngine initialized")
    
    def build_graph(self, scenes: List[Dict], characters: List[str]) -> nx.Graph:
        """Build character relationship graph from scenes."""
        G = nx.Graph()
        
        # Add all characters as nodes
        for char in characters:
            G.add_node(char, scenes=0, dialogue_lines=0)
        
        # Build edges from co-occurrences
        for scene in scenes:
            scene_chars = scene.get("characters", [])
            
            # Update node attributes
            for char in scene_chars:
                if char in G.nodes:
                    G.nodes[char]["scenes"] += 1
            
            # Count dialogue lines
            for line in scene.get("lines", []):
                if isinstance(line, dict) and line.get("type") == "dialogue":
                    char = line.get("character", "")
                    if char in G.nodes:
                        G.nodes[char]["dialogue_lines"] += 1
            
            # Create edges for all pairs in same scene
            for i, char1 in enumerate(scene_chars):
                for char2 in scene_chars[i+1:]:
                    if char1 in G.nodes and char2 in G.nodes:
                        if G.has_edge(char1, char2):
                            G[char1][char2]["weight"] += 1
                        else:
                            G.add_edge(char1, char2, weight=1)
        
        self.graph = G
        logger.info(f"Built graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        return G
    
    def get_network_metrics(self) -> Dict:
        """Calculate network analysis metrics."""
        if self.graph is None:
            return {}
        
        G = self.graph
        
        degree_centrality = nx.degree_centrality(G)
        betweenness_centrality = nx.betweenness_centrality(G, weight='weight')
        
        top_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        top_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        
        metrics = {
            "nodes": G.number_of_nodes(),
            "edges": G.number_of_edges(),
            "density": nx.density(G),
            "top_degree_centrality": top_degree,
            "top_betweenness_centrality": top_betweenness,
            "degree_centrality": degree_centrality,
            "betweenness_centrality": betweenness_centrality
        }
        
        if G.number_of_edges() > 0:
            metrics["average_clustering"] = nx.average_clustering(G, weight='weight')
        
        return metrics
    
    def create_plotly_visualization(self, title: str = "Character Relationship Network") -> go.Figure:
        """Create interactive Plotly visualization."""
        if self.graph is None:
            return go.Figure()
        
        G = self.graph
        pos = nx.spring_layout(G, k=1, iterations=50, seed=42)
        
        # Create edge traces
        edge_traces = []
        for edge in G.edges(data=True):
            char1, char2, data = edge
            weight = data.get('weight', 1)
            x0, y0 = pos[char1]
            x1, y1 = pos[char2]
            
            edge_trace = go.Scatter(
                x=[x0, x1, None], y=[y0, y1, None],
                mode='lines',
                line=dict(width=weight*0.5, color='#888'),
                hovertext=f"{char1} ↔ {char2}<br>Scenes: {weight}",
                hoverinfo='text',
                showlegend=False
            )
            edge_traces.append(edge_trace)
        
        # Create node trace
        node_x, node_y, node_text, node_size = [], [], [], []
        for node in G.nodes(data=True):
            char, data = node
            x, y = pos[char]
            node_x.append(x)
            node_y.append(y)
            scenes = data.get('scenes', 0)
            dialogue = data.get('dialogue_lines', 0)
            node_text.append(f"<b>{char}</b><br>Scenes: {scenes}<br>Dialogue: {dialogue}")
            node_size.append(10 + scenes * 2)
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=[t.split('<br>')[0].replace('<b>', '').replace('</b>', '') for t in node_text],
            textposition='top center',
            hovertext=node_text,
            hoverinfo='text',
            marker=dict(size=node_size, color='lightblue', line=dict(width=2, color='darkblue')),
            showlegend=False
        )
        
        fig = go.Figure(data=edge_traces + [node_trace])
        fig.update_layout(
            title=title, title_font={'size': 16}, showlegend=False,
            hovermode='closest', margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='white', height=600
        )
        return fig
    
    def get_character_relationships(self, character: str, top_n: int = 5) -> List[Tuple[str, int]]:
        """Get strongest relationships for a character."""
        if self.graph is None or character not in self.graph.nodes:
            return []
        
        relationships = [(neighbor, self.graph[character][neighbor]['weight']) 
                        for neighbor in self.graph.neighbors(character)]
        relationships.sort(key=lambda x: x[1], reverse=True)
        return relationships[:top_n]
