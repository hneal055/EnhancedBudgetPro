# src/ExportEngine/__init__.py
from .csv_exporter import CSVExporter
from .excel_exporter import ExcelExporter
from .pdf_reporter import PDFBudgetReport

__all__ = ['CSVExporter', 'ExcelExporter', 'PDFBudgetReport', 'export_all']



def export_all(scenes, characters, budget_rows, risk_rows, output_dir, script_path):
    """Export all analysis results to CSV and JSON."""
    import json
    from pathlib import Path
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Export scene data as CSV
    csv_exp = CSVExporter()
    scene_data = {'scenes': scenes}
    csv_exp.export(scene_data, str(output_path / 'scenes.csv'))
    
    # Export summary JSON
    summary = {
        'script': str(script_path),
        'scene_count': len(scenes),
        'character_count': len(characters),
        'total_budget': sum(row.get('total_cost', 0) for row in budget_rows),
        'risk_count': len(risk_rows)
    }
    with open(output_path / 'summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    return {
        'output_dir': str(output_path),
        'files_created': ['scenes.csv', 'summary.json']
    }
