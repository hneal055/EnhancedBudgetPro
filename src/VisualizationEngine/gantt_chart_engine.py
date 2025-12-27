import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from datetime import datetime, timedelta
from collections import defaultdict


class GanttChartEngine:
    """Engine for creating Gantt chart visualizations."""
    
    def __init__(self):
        """Initialize the Gantt Chart Engine."""
        self.minutes_per_day = 480  # 8-hour shooting day
    
    def estimate_scene_duration(self, scene):
        """Estimate the duration of a scene in minutes.
        
        Args:
            scene: Dictionary with 'dialogue_lines' and 'action_lines'
            
        Returns:
            int: Estimated duration in minutes (minimum 1)
        """
        if not scene:
            return 1
        
        dialogue_lines = scene.get('dialogue_lines', 0)
        action_lines = scene.get('action_lines', 0)
        
        # Calculate: dialogue = 0.5 min/line, action = 0.3 min/line
        duration = int(dialogue_lines * 0.5 + action_lines * 0.3)
        
        # Minimum 1 minute
        return max(duration, 1)
    
    def get_production_schedule(self, scenes):
        """Generate a production schedule for scenes.
        
        Args:
            scenes: List of scene dictionaries
            
        Returns:
            dict: Schedule information with counts and estimates
        """
        if not scenes:
            return {
                'total_scenes': 0,
                'estimated_duration_minutes': 0,
                'estimated_shoot_days': 0,
                'interior_scenes': 0,
                'exterior_scenes': 0
            }
        
        total_duration = 0
        interior_count = 0
        exterior_count = 0
        
        for scene in scenes:
            duration = self.estimate_scene_duration(scene)
            total_duration += duration
            
            heading = scene.get('heading', '')
            if 'INT.' in heading.upper():
                interior_count += 1
            elif 'EXT.' in heading.upper():
                exterior_count += 1
        
        # Estimate shoot days
        shoot_days = max(1, int(total_duration / self.minutes_per_day))
        if total_duration % self.minutes_per_day > 0:
            shoot_days += 1
        
        return {
            'total_scenes': len(scenes),
            'estimated_duration_minutes': total_duration,
            'estimated_shoot_days': shoot_days,
            'interior_scenes': interior_count,
            'exterior_scenes': exterior_count
        }
    
    def create_scene_gantt(self, scenes):
        """Create a Gantt chart visualization for scenes.
        
        Args:
            scenes: List of scene dictionaries
            
        Returns:
            plotly figure or empty figure if no scenes
        """
        if not scenes:
            # Return empty figure with annotation
            fig = go.Figure()
            fig.add_annotation(
                text="No scenes to display",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        # Prepare data for Gantt chart
        gantt_data = []
        current_date = datetime(2024, 1, 1)
        
        for i, scene in enumerate(scenes):
            duration = self.estimate_scene_duration(scene)
            days_needed = max(1, duration / self.minutes_per_day)
            
            end_date = current_date + timedelta(days=days_needed)
            
            gantt_data.append({
                "Task": f"Scene {i+1}",
                "Start": current_date.strftime("%Y-%m-%d"),
                "Finish": end_date.strftime("%Y-%m-%d"),
                "Resource": scene.get('heading', 'Unknown')[:20]
            })
            
            current_date = end_date
        
        # Get unique resources for coloring
        resources = list(set([item["Resource"] for item in gantt_data]))
        
        # Create dynamic color list
        base_colors = px.colors.qualitative.Plotly
        colors = base_colors[:len(resources)]
        
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
            height=400 + len(gantt_data) * 20,
        )
        
        return fig
    
    def create_character_timeline(self, scenes, character_name):
        """Create a timeline showing when a character appears.
        
        Args:
            scenes: List of scene dictionaries with 'characters' field
            character_name: Name of the character to track
            
        Returns:
            plotly figure showing character timeline
        """
        if not scenes:
            fig = go.Figure()
            fig.add_annotation(
                text="No scenes to display",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        # Find scenes with this character
        character_scenes = []
        current_date = datetime(2024, 1, 1)
        
        for i, scene in enumerate(scenes):
            characters = scene.get('characters', [])
            duration = self.estimate_scene_duration(scene)
            days_needed = max(1, duration / self.minutes_per_day)
            
            if character_name in characters:
                end_date = current_date + timedelta(days=days_needed)
                character_scenes.append({
                    "Task": f"Scene {i+1}",
                    "Start": current_date.strftime("%Y-%m-%d"),
                    "Finish": end_date.strftime("%Y-%m-%d"),
                    "Resource": character_name
                })
            
            current_date += timedelta(days=days_needed)
        
        if not character_scenes:
            # Character not found - create figure with annotation
            fig = go.Figure()
            fig.add_annotation(
                text=f"{character_name} does not appear in any scenes",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        # Create Gantt chart for character
        fig = ff.create_gantt(
            character_scenes,
            colors=["#FF6B6B"],
            index_col="Resource",
            show_colorbar=False,
            group_tasks=True,
            showgrid_x=True,
            showgrid_y=True,
        )
        
        fig.update_layout(
            title=f"Timeline for {character_name}",
            xaxis_title="Timeline",
            yaxis_title="Scenes",
            height=300,
        )
        
        return fig
    
    def create_daily_schedule(self, scenes, start_date=None):
        """Create daily shooting schedule breakdown.
        
        Args:
            scenes: List of scene dictionaries
            start_date: Starting date (default: today)
            
        Returns:
            dict: Daily schedule with scenes grouped by day
        """
        if not scenes:
            return {'days': [], 'total_days': 0}
        
        if start_date is None:
            start_date = datetime.now()
        elif isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
        
        daily_schedule = []
        current_day = {'date': start_date, 'scenes': [], 'total_minutes': 0}
        
        for i, scene in enumerate(scenes):
            duration = self.estimate_scene_duration(scene)
            
            # Check if scene fits in current day
            if current_day['total_minutes'] + duration > self.minutes_per_day:
                # Save current day and start new one
                if current_day['scenes']:
                    daily_schedule.append(current_day)
                current_day = {
                    'date': start_date + timedelta(days=len(daily_schedule)),
                    'scenes': [],
                    'total_minutes': 0
                }
            
            # Add scene to current day
            current_day['scenes'].append({
                'scene_number': i + 1,
                'heading': scene.get('heading', 'Unknown'),
                'duration_minutes': duration,
                'characters': scene.get('characters', [])
            })
            current_day['total_minutes'] += duration
        
        # Add final day
        if current_day['scenes']:
            daily_schedule.append(current_day)
        
        return {
            'days': daily_schedule,
            'total_days': len(daily_schedule)
        }
    
    def calculate_resource_needs(self, scenes):
        """Estimate crew, equipment, and budget needs.
        
        Args:
            scenes: List of scene dictionaries
            
        Returns:
            dict: Resource requirements and estimates
        """
        if not scenes:
            return {
                'crew_size': 0,
                'equipment_packages': [],
                'estimated_budget': 0,
                'location_count': 0,
                'character_count': 0
            }
        
        # Analyze scenes
        locations = set()
        all_characters = set()
        interior_count = 0
        exterior_count = 0
        night_count = 0
        
        for scene in scenes:
            heading = scene.get('heading', '')
            locations.add(heading)
            
            if 'INT.' in heading.upper():
                interior_count += 1
            if 'EXT.' in heading.upper():
                exterior_count += 1
            if 'NIGHT' in heading.upper():
                night_count += 1
            
            characters = scene.get('characters', [])
            all_characters.update(characters)
        
        # Estimate crew size based on production scale
        total_scenes = len(scenes)
        base_crew = 10  # Minimum skeleton crew
        
        if total_scenes > 50:
            crew_size = 30  # Large production
        elif total_scenes > 20:
            crew_size = 20  # Medium production
        else:
            crew_size = base_crew  # Small production
        
        # Equipment packages needed
        equipment = ['Camera Package']
        if interior_count > 0:
            equipment.append('Lighting Package (Interior)')
        if exterior_count > 0:
            equipment.append('Lighting Package (Exterior)')
        if night_count > 0:
            equipment.append('Night Lighting Package')
        equipment.append('Sound Package')
        equipment.append('Grip & Electric')
        
        # Budget estimation (rough)
        schedule = self.get_production_schedule(scenes)
        shoot_days = schedule['estimated_shoot_days']
        
        # Basic daily rates
        crew_day_rate = crew_size * 500  # $500/person/day average
        equipment_day_rate = len(equipment) * 1000  # $1000/package/day
        location_day_rate = len(locations) * 2000  # $2000/location/day
        
        estimated_budget = shoot_days * (crew_day_rate + equipment_day_rate + location_day_rate)
        
        return {
            'crew_size': crew_size,
            'equipment_packages': equipment,
            'estimated_budget': estimated_budget,
            'location_count': len(locations),
            'character_count': len(all_characters),
            'shoot_days': shoot_days,
            'interior_scenes': interior_count,
            'exterior_scenes': exterior_count,
            'night_scenes': night_count
        }
    
    def export_to_pdf(self, fig, filename="gantt_chart.pdf"):
        """Export Gantt chart to PDF.
        
        Args:
            fig: Plotly figure object
            filename: Output PDF filename
            
        Returns:
            str: Path to saved PDF file
        """
        if fig is None:
            raise ValueError("Cannot export None figure to PDF")
        
        try:
            # Use plotly's built-in PDF export
            fig.write_image(filename, format="pdf")
            return filename
        except Exception as e:
            # Fallback: save as HTML if PDF export fails
            html_filename = filename.replace('.pdf', '.html')
            fig.write_html(html_filename)
            return html_filename
    
    def export_schedule_to_csv(self, scenes, filename="production_schedule.csv"):
        """Export production schedule to CSV.
        
        Args:
            scenes: List of scene dictionaries
            filename: Output CSV filename
            
        Returns:
            str: Path to saved CSV file
        """
        import csv
        
        daily_schedule = self.create_daily_schedule(scenes)
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Day', 'Date', 'Scene', 'Heading', 'Duration (min)', 'Characters'])
            
            for day_num, day in enumerate(daily_schedule['days'], 1):
                date_str = day['date'].strftime('%Y-%m-%d')
                for scene in day['scenes']:
                    writer.writerow([
                        day_num,
                        date_str,
                        scene['scene_number'],
                        scene['heading'],
                        scene['duration_minutes'],
                        ', '.join(scene['characters'])
                    ])
        
        return filename
