import plotly.express as px
import plotly.figure_factory as ff


def create_scene_gantt(scenes):
    """Create a Gantt chart visualization for scenes."""
    if not scenes:
        return None

    # Prepare data for Gantt chart
    gantt_data = []
    for scene in scenes:
        gantt_data.append(
            {
                "Task": f"Scene {scene.get('number', 'N/A')}",
                "Start": scene.get("start_date", "2024-01-01"),
                "Finish": scene.get("end_date", "2024-01-02"),
                "Resource": scene.get("location", "Unknown"),
            }
        )

    # Get unique resources for coloring
    resources = list(set([item["Resource"] for item in gantt_data]))

    # Create dynamic color list based on number of resources
    # Use Plotly's qualitative colors
    base_colors = px.colors.qualitative.Plotly

    # Extend if we need more colors
    colors = base_colors
    color_cycles = [
        px.colors.qualitative.Set1,
        px.colors.qualitative.Set2,
        px.colors.qualitative.Set3,
    ]

    color_idx = 0
    while len(colors) < len(resources):
        colors.extend(color_cycles[color_idx % len(color_cycles)])
        color_idx += 1

    # Take only needed colors
    colors = colors[: len(resources)]

    # Create the figure
    fig = ff.create_gantt(
        gantt_data,
        colors=colors,
        index_col="Resource",
        show_colorbar=True,
        group_tasks=True,
        showgrid_x=True,
        showgrid_y=True,
    )

    # Update layout
    fig.update_layout(
        title="Scene Schedule Gantt Chart",
        xaxis_title="Timeline",
        yaxis_title="Scenes",
        showlegend=True,
        height=400 + len(gantt_data) * 20,  # Dynamic height based on scenes
    )

    return fig


st.bar_chart(data, width="stretch")
