# Copilot Instructions for Enhanced Budget Pro

## Project Overview

**EnhancedBudgetPro** is a comprehensive film & TV production budget intelligence system. It ingests scripts in multiple formats (FDX, Fountain, Celtx, PDF, plain text), analyzes story structure and character intelligence, calculates production budgets, and performs risk analysis—all exportable as CSV, Excel, and PDF reports.

**Core Architecture**: Modular Python pipeline with three UI entry points (CLI, Flask web app, Streamlit dashboard).

## Key Architectural Components

### 1. IngestEngine (src/IngestEngine/)
- file_router.py: Detects format by extension and routes to correct loader
- Loaders: fdx_loader, fountain_loader, celtx_loader, plaintext_loader, pdf_loader
- Output Contract: All loaders return {scenes[], characters[], scene_count}
- Scene Structure: {heading, lines[], characters[], dialogue_lines, action_lines}

### 2. AnalysisEngine (src/AnalysisEngine/)
- character_intelligence.py: Scene frequency, dialogue density, screen time estimation
- scene_density_engine.py: Dialogue/action ratio, scene classification (ACTION/DIALOGUE/BALANCED)
- cost_impact_engine.py: Character-to-budget mapping (lead roles cost more)
- burn_rate_engine.py: Daily cost projections
- monte_carlo_engine.py: Budget risk simulations
- risk_analysis_engine.py: Risk level assignment (HIGH/MEDIUM/LOW)

### 3. ProductionBudgetEngine (src/ProductionBudgetEngine/)
- crew_budget_engine.py: Crew daily rates
- equipment_budget_engine.py: Camera, lighting, grip packages
- location_budget_engine.py: Scout costs, permits, fees
- post_budget_engine.py: Editing, VFX, sound design
- insurance_contingency_engine.py: 12% contingency + insurance
- master_production_budget_engine.py: Aggregates all engines
CRITICAL: Returns totals independent of scene count. Scale by shoot_days.

### 4. ExportEngine (src/ExportEngine/)
- csv_exporter.py, excel_exporter.py, pdf_reporter.py
- production_budget_pdf_exporter.py, stripboard_pdf_exporter.py

## Entry Points & Workflows

### CLI (src/cli.py)
python -m src.cli analyze --input script.fdx --out ./output
python -m src.cli batch --input_dir ./scripts --out ./batch_results
Uses run_full_analysis() from src/ScriptIngest.py

### Web App (web_app.py)
- /: Upload form
- /analyze: Triggers run_full_analysis(), saves to web_output/{job_id}/
- /download/{job_id}/{filename}: File serving
- Each upload creates new job_id with timestamp

### Streamlit UI (ui_app.py + pages/)
- Session State: st.session_state caches parsed data, intelligence, budget across reloads
- Pages: Story_Intelligence, Financial_Intelligence, Production_Budget, Risk_Monte_Carlo, Export_Center
- Pattern: if st.session_state.data: guards against re-computing

## Project-Specific Conventions

### Data Contracts
- Loaders: {scenes[], characters[], scene_count}
- Scene: {heading, lines[], characters[], dialogue_lines, action_lines}
- Character stats: {scenes, dialogue_lines, estimated_screen_time_min}
- Budget rows: {category, item, rate, quantity, total}
- Risk rows: {scene, risk_type, risk_level, mitigation}

### Naming Patterns
- Loaders: {format}_loader.py with load_{format}(path) function
- Engines: {domain}_{component}_engine.py with {Component}Engine class
- Exporters: {format}_exporter.py with {Format}Exporter class

### Testing
- Samples: samples/test_script.fdx, test_script.fountain, test_script.celtx.json
- Output fixtures: output/, batch_output/, web_output/

## Critical Developer Tasks

Adding a Script Format:
1. Create src/IngestEngine/{format}_loader.py with load_{format}(path)
2. Add extension detection to file_router.detect_format()
3. Add router case to route_file()
4. Return {scenes[], characters[], scene_count}

Adding a Budget Category:
1. Create src/ProductionBudgetEngine/{category}_budget_engine.py
2. Implement .calculate(shoot_days) method
3. Import and aggregate in master_production_budget_engine.py

Adding a Streamlit Page:
1. Create pages/{number}_{title}.py
2. Access st.session_state.data, st.session_state.intel, etc.
3. Use st.stop() if prerequisite data missing

## Environment & Dependencies

- Python: 3.12+ (.venv available)
- Key Dependencies: pandas, streamlit, openpyxl, reportlab, pdfplumber, plotly
- Virtual Environment: .venv\Scripts\activate (Windows)
- Install: pip install -r requirements.txt

## Common Workflows

.\.venv\Scriptsctivate
python -m src.cli analyze --input samples/test_script.fdx --out ./output
streamlit run ui_app.py
python web_app.py

## Gotchas & Design Decisions

1. ProductionBudgetEngine has NO script dependency - calculates fixed costs scaled by shoot_days
2. Scene Risk != Budget Risk - independent contingency layers
3. Session State: Always check if st.session_state.key exists before using
4. File Router: detect_format() returns None for unsupported types, not exception
5. Export Timestamp: web_app.py uses {slug}_{YYYYMMDD_HHMMSS} format for output folders to avoid collisions
