"""
Scene Gantt Chart Engine
Creates timeline visualizations of scenes with character tracking
"""

import plotly.figure_factory as ff
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class GanttChartEngine:
    """Creates Gantt chart visualizations of script timeline."""
    
    def __init__(self):
        logger.info("GanttChartEngine initialized")
    
    def estimate_scene_duration(self, scene: Dict) -> int:
        """
        Estimate scene duration in minutes based on content.
        
        Rule of thumb: 1 page ≈ 1 minute
        Average: dialogue_lines * 0.5 + action_lines * 0.3
        """
        dialogue_lines = scene.get("dialogue_lines", 0)
        action_lines = scene.get("action_lines", 0)
        
        # Estimate duration (minutes)
        duration = max(1, int(dialogue_lines * 0.5 + action_lines * 0.3))
        return duration
    
    def create_scene_gantt(self, scenes: List[Dict]) -> go.Figure:
        """
        Create Gantt chart for scenes with character tracking.
        
        Args:
            scenes: List of scene dictionaries
            
        Returns:
            Plotly Figure with Gantt chart
        """
        if not scenes:
            return go.Figure()
        
        # Build task list
        tasks = []
        start_time = datetime(2024, 1, 1, 9, 0)  # Arbitrary start
        current_time = start_time
        
        for idx, scene in enumerate(scenes):
            heading = scene.get("heading", f"Scene {idx+1}")
            duration_min = self.estimate_scene_duration(scene)
            characters = scene.get("characters", [])
            
            # Truncate long headings
            if len(heading) > 40:
                heading = heading[:37] + "..."
            
            task = dict(
                Task=heading,
                Start=current_time,
                Finish=current_time + timedelta(minutes=duration_min),
                Resource=", ".join(characters[:3])  # First 3 characters
            )
            tasks.append(task)
            
            current_time += timedelta(minutes=duration_min)
        
        # Create Gantt chart
        colors = {
            'INT': 'rgb(46, 137, 205)',
            'EXT': 'rgb(114, 183, 74)',
            'INT/EXT': 'rgb(255, 158, 74)',
        }
        
        df = pd.DataFrame(tasks)
        
        fig = ff.create_gantt(
            df,
            index_col='Resource',
            show_colorbar=True,
            group_tasks=True,
            showgrid_x=True,
            showgrid_y=True,
            title='Scene Timeline (Estimated Duration)'
        )
        
        fig.update_layout(
            xaxis_title="Timeline",
            yaxis_title="Scene",
            height=max(400, len(scenes) * 30),
            hovermode='closest'
        )
        
        return fig
    
    def create_character_timeline(self, scenes: List[Dict], character: str) -> go.Figure:
        """
        Create timeline showing when character appears.
        
        Args:
            scenes: List of scene dictionaries
            character: Character name to track
            
        Returns:
            Plotly Figure with character timeline
        """
        appearances = []
        start_time = datetime(2024, 1, 1, 9, 0)
        current_time = start_time
        
        for idx, scene in enumerate(scenes):
            duration_min = self.estimate_scene_duration(scene)
            
            if character in scene.get("characters", []):
                heading = scene.get("heading", f"Scene {idx+1}")
                if len(heading) > 40:
                    heading = heading[:37] + "..."
                
                appearances.append(dict(
                    Task=heading,
                    Start=current_time,
                    Finish=current_time + timedelta(minutes=duration_min),
                    Resource=character
                ))
            
            current_time += timedelta(minutes=duration_min)
        
        if not appearances:
            # No appearances
            fig = go.Figure()
            fig.add_annotation(
                text=f"'{character}' does not appear in any scenes",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        df = pd.DataFrame(appearances)
        
        fig = ff.create_gantt(
            df,
            index_col='Resource',
            show_colorbar=False,
            group_tasks=False,
            showgrid_x=True,
            showgrid_y=True,
            title=f"'{character}' Scene Timeline"
        )
        
        fig.update_layout(
            xaxis_title="Timeline",
            yaxis_title="Scene",
            height=max(300, len(appearances) * 40)
        )
        
        return fig
    
    def get_production_schedule(self, scenes: List[Dict]) -> Dict:
        """
        Generate production schedule with shoot days estimate.
        
        Args:
            scenes: List of scene dictionaries
            
        Returns:
            Dict with schedule information
        """
        total_duration = sum(self.estimate_scene_duration(s) for s in scenes)
        
        # Assume 12-hour shoot days, 5 pages/day typical
        estimated_shoot_days = max(1, len(scenes) // 5)
        
        # Group by location type
        int_scenes = sum(1 for s in scenes if s.get("heading", "").startswith("INT"))
        ext_scenes = sum(1 for s in scenes if s.get("heading", "").startswith("EXT"))
        
        return {
            "total_scenes": len(scenes),
            "estimated_duration_minutes": total_duration,
            "estimated_shoot_days": estimated_shoot_days,
            "interior_scenes": int_scenes,
            "exterior_scenes": ext_scenes,
            "avg_scene_duration_minutes": total_duration / len(scenes) if scenes else 0
        }
