"""
Character Arc PDF Exporter
Creates individual PDF reports for character emotional arcs
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from typing import Dict, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class CharacterArcPDFExporter:
    """Exports individual character arc analysis to PDF."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        logger.info("CharacterArcPDFExporter initialized")
    
    def _setup_custom_styles(self):
        """Create custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='MetricLabel',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#7f8c8d')
        ))
    
    def export_character_arc(
        self, 
        character_name: str,
        arc_data: Dict,
        scenes: List[Dict],
        output_path: str
    ) -> str:
        """
        Export character arc to PDF.
        
        Args:
            character_name: Character name
            arc_data: Character arc analysis data
            scenes: List of all scenes
            output_path: Output PDF path
            
        Returns:
            Path to created PDF file
        """
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []
        
        # Title
        title = Paragraph(f"Character Arc Analysis<br/><b>{character_name}</b>", 
                         self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        # Metadata
        metadata = Paragraph(
            f"<i>Generated: {datetime.now().strftime('%B %d, %Y')}</i>",
            self.styles['MetricLabel']
        )
        story.append(metadata)
        story.append(Spacer(1, 0.5*inch))
        
        # Overview section
        story.append(Paragraph("Overview", self.styles['SectionHeader']))
        
        overview_data = [
            ["Metric", "Value"],
            ["Scenes Appeared", str(arc_data.get("scenes", 0))],
            ["Dialogue Lines", str(arc_data.get("dialogue_lines", 0))],
            ["Estimated Screen Time", f"{arc_data.get('estimated_screen_time_min', 0):.1f} minutes"],
            ["Dominant Emotion", arc_data.get("dominant_emotion", "N/A").capitalize()],
        ]
        
        overview_table = Table(overview_data, colWidths=[3*inch, 2*inch])
        overview_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(overview_table)
        story.append(Spacer(1, 0.4*inch))
        
        # Emotional profile
        story.append(Paragraph("Emotional Profile", self.styles['SectionHeader']))
        
        emotions = arc_data.get("emotions", {})
        if emotions:
            emotion_data = [["Emotion", "Score"]]
            for emotion, score in sorted(emotions.items(), key=lambda x: x[1], reverse=True):
                emotion_data.append([emotion.capitalize(), f"{score:.2f}"])
            
            emotion_table = Table(emotion_data, colWidths=[3*inch, 2*inch])
            emotion_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ecc71')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            story.append(emotion_table)
        else:
            story.append(Paragraph("<i>No emotional data available</i>", self.styles['Normal']))
        
        story.append(Spacer(1, 0.4*inch))
        
        # Scene appearances
        story.append(Paragraph("Scene Appearances", self.styles['SectionHeader']))
        
        char_scenes = [s for s in scenes if character_name in s.get("characters", [])]
        
        if char_scenes:
            scene_data = [["Scene #", "Heading", "Dialogue Lines"]]
            for idx, scene in enumerate(char_scenes[:15]):  # First 15 scenes
                scene_num = scenes.index(scene) + 1
                heading = scene.get("heading", "Unknown")
                if len(heading) > 40:
                    heading = heading[:37] + "..."
                
                # Count dialogue for this character
                char_dialogue = sum(1 for line in scene.get("lines", []) 
                                  if isinstance(line, dict) 
                                  and line.get("type") == "dialogue"
                                  and line.get("character") == character_name)
                
                scene_data.append([str(scene_num), heading, str(char_dialogue)])
            
            scene_table = Table(scene_data, colWidths=[0.8*inch, 3.2*inch, 1*inch])
            scene_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('ALIGN', (2, 0), (2, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('FONTSIZE', (0, 1), (-1, -1), 9)
            ]))
            story.append(scene_table)
            
            if len(char_scenes) > 15:
                story.append(Spacer(1, 0.2*inch))
                story.append(Paragraph(
                    f"<i>Showing 15 of {len(char_scenes)} total appearances</i>",
                    self.styles['MetricLabel']
                ))
        else:
            story.append(Paragraph("<i>No scene appearances found</i>", self.styles['Normal']))
        
        # Build PDF
        doc.build(story)
        logger.info(f"Created character arc PDF: {output_path}")
        return output_path
    
    def export_all_character_arcs(
        self,
        character_arcs: Dict[str, Dict],
        scenes: List[Dict],
        output_dir: str
    ) -> List[str]:
        """
        Export PDFs for all characters.
        
        Args:
            character_arcs: Dict of character name -> arc data
            scenes: List of all scenes
            output_dir: Output directory for PDFs
            
        Returns:
            List of created PDF file paths
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        pdf_files = []
        for char_name, arc_data in character_arcs.items():
            # Sanitize filename
            safe_name = "".join(c if c.isalnum() else "_" for c in char_name)
            output_path = os.path.join(output_dir, f"character_arc_{safe_name}.pdf")
            
            self.export_character_arc(char_name, arc_data, scenes, output_path)
            pdf_files.append(output_path)
        
        logger.info(f"Created {len(pdf_files)} character arc PDFs in {output_dir}")
        return pdf_files
