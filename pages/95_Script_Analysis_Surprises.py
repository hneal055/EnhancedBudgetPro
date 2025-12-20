import os
import random
import re

import plotly.graph_objects as go
import streamlit as st

st.title("🎭 Script Analysis Surprises")

if "data" not in st.session_state or not st.session_state.data:
    st.warning("No script data loaded. Please analyze a script first.")
    st.stop()

scenes = st.session_state.data.get("scenes", [])
characters = st.session_state.data.get("characters", [])

# --- Genre Detector ---
genre_keywords = {
    "Action": ["fight", "explosion", "chase", "gun", "battle", "attack", "escape"],
    "Comedy": ["laugh", "funny", "joke", "giggle", "prank", "hilarious", "comedy"],
    "Drama": ["cry", "tears", "love", "betrayal", "family", "relationship", "drama"],
    "Horror": ["blood", "scream", "ghost", "monster", "dark", "kill", "fear"],
    "Sci-Fi": ["spaceship", "robot", "alien", "future", "technology", "laser", "space"],
    "Romance": ["kiss", "love", "date", "romantic", "heart", "relationship", "wedding"],
    "Thriller": ["mystery", "secret", "spy", "chase", "danger", "threat", "thriller"],
}


def detect_genre(scenes):
    keyword_counts = {genre: 0 for genre in genre_keywords}
    for scene in scenes:
        # Convert all items in lines to strings before joining
        text = " ".join(str(line) for line in scene.get("lines", [])).lower()
        for genre, keywords in genre_keywords.items():
            for kw in keywords:
                if kw in text:
                    keyword_counts[genre] += 1
    detected = max(keyword_counts, key=keyword_counts.get)
    return detected, keyword_counts


detected_genre, genre_scores = detect_genre(scenes)
st.subheader("🔎 Genre Detector")
st.info(f"**Likely Genre:** {detected_genre} (score: {genre_scores[detected_genre]})")

st.bar_chart(genre_scores, width="stretch")

# --- Character Relationship Network ---
st.subheader("👥 Character Relationship Network")


def build_relationship_edges(scenes, characters):
    # Simple co-occurrence: if two characters appear in the same scene, they are connected
    edges = {}
    for scene in scenes:
        chars = scene.get("characters", [])
        for i, c1 in enumerate(chars):
            for c2 in chars[i + 1 :]:
                pair = tuple(sorted([c1, c2]))
                edges[pair] = edges.get(pair, 0) + 1
    return edges


edges = build_relationship_edges(scenes, characters)
nodes = list({c for pair in edges for c in pair})

if nodes and edges:
    edge_x = []
    edge_y = []
    node_x = []
    node_y = []
    pos = {name: (random.uniform(0, 1), random.uniform(0, 1)) for name in nodes}
    for (c1, c2), weight in edges.items():
        x0, y0 = pos[c1]
        x1, y1 = pos[c2]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
    for name in nodes:
        x, y = pos[name]
        node_x.append(x)
        node_y.append(y)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=1, color="#888"),
            hoverinfo="none",
            mode="lines",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            marker=dict(size=20, color="skyblue"),
            text=nodes,
            textposition="bottom center",
        )
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "Nodes represent characters. Lines show how often characters appear together in scenes."
    )
else:
    st.info("Not enough character data to build a relationship network.")

# --- Random Script Surprise ---
st.subheader("🎲 Random Script Surprise")
surprises = [
    "Did you know? The character with the most scenes is: **{}**".format(
        max(
            [c for c in characters if isinstance(c, dict)],
            key=lambda c: len(c.get("scenes", [])),
            default={"name": "N/A"},
        ).get("name", "N/A")
    ),
    "Longest scene heading: **{}**".format(
        max(
            scenes, key=lambda s: len(s.get("heading", "")), default={"heading": "N/A"}
        ).get("heading", "N/A")
    ),
    "Total number of scenes: **{}**".format(len(scenes)),
    "Total number of unique characters: **{}**".format(len(characters)),
    "Shortest scene: **{}**".format(
        min(
            scenes, key=lambda s: len(s.get("lines", [])), default={"heading": "N/A"}
        ).get("heading", "N/A")
    ),
]
st.success(random.choice(surprises))


def needs_streamlit_import(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    # Check if 'st.' is used and 'import streamlit as st' is missing
    uses_st = re.search(r"\bst\.", content)
    has_import = re.search(r"^\s*import\s+streamlit\s+as\s+st", content, re.MULTILINE)
    return uses_st and not has_import


def add_streamlit_import(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # Insert after any shebang or encoding line, else at top
    insert_at = 0
    for i, line in enumerate(lines[:2]):
        if line.startswith("#!"):
            insert_at = i + 1
        elif "coding" in line:
            insert_at = i + 1
    lines.insert(insert_at, "import streamlit as st\n")
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"Added import to {filepath}")


def scan_and_fix(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".py"):
                filepath = os.path.join(dirpath, filename)
                if needs_streamlit_import(filepath):
                    add_streamlit_import(filepath)


if __name__ == "__main__":
    scan_and_fix(".")
