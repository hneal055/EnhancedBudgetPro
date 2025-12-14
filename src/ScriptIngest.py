# src/ScriptIngest.py

import os
import argparse

from src.IngestEngine.file_router import detect_format, route_file
from src.BudgetEngine import estimate_budget
from src.RiskModel import assess_risks
from src.ExportEngine import export_all
from src.errors import UnsupportedFormatError, ParseError
from src.validation import validate_parsed_script
from src.logging_cfg import get_logger

logger = get_logger()


def parse_script(path: str):
    fmt = detect_format(path)
    if fmt is None:
        raise UnsupportedFormatError(f"Unsupported format for file: {path}")
    data = route_file(path)
    try:
        validate_parsed_script(data)
    except Exception as e:
        raise ParseError(str(e))
    return data


def main():
    parser = argparse.ArgumentParser(
        description="Film & TV Script Intelligence Engine")
    parser.add_argument("--input", required=True, help="Path to script file")
    parser.add_argument("--out", required=True, help="Output directory")
    args = parser.parse_args()

    script_path = args.input
    output_dir = args.out

    print(f"🔍 Reading: {script_path}")
    data = parse_script(script_path)

    scenes = data.get("scenes", [])
    characters = data.get("characters", [])

    print("\n================ RESULTS ================")
    print(f"📄 Scenes parsed:      {len(scenes)}")
    print(f"🎭 Characters found:   {len(set(characters))}")
    print("=========================================\n")

    # ---- Phase 2: Budget & Risk Engines ----
    budget_summary, budget_rows = estimate_budget(scenes)
    risk_rows = assess_risks(scenes)

    print("💰 Budget Summary:")
    print(
        f"   Total Budget:       ${budget_summary['total_budget']:.2f} {budget_summary['currency']}")
    print(
        f"   Avg/Scene:          ${budget_summary['average_cost_per_scene']:.2f}")
    print()

    print("⚠ Risk Overview:")
    high = sum(1 for r in risk_rows if r["risk_level"] == "HIGH")
    med = sum(1 for r in risk_rows if r["risk_level"] == "MEDIUM")
    low = sum(1 for r in risk_rows if r["risk_level"] == "LOW")
    print(f"   HIGH:   {high}")
    print(f"   MEDIUM: {med}")
    print(f"   LOW:    {low}")
    print()

    # ---- Export packet ----
    summary = export_all(
        scenes=scenes,
        characters=characters,
        budget_rows=budget_rows,
        risk_rows=risk_rows,
        output_dir=output_dir,
        script_path=script_path,
    )

    print("📦 Export complete:")
    print(f"   Output folder: {os.path.abspath(output_dir)}")
    print(f"   Summary JSON:  {os.path.join(output_dir, 'summary.json')}")
    print(
        f"   Excel report:  {os.path.join(output_dir, 'production_report.xlsx')}")
    print("\n✅ Done.")


def run_full_analysis(script_path: str, output_dir: str):
    """
    Core pipeline used by CLI / Web / tools:
      - parse script
      - compute budget
      - compute risk
      - export CSV / Excel / JSON
      - return all key structures
    """
    data = parse_script(script_path)

    scenes = data.get("scenes", [])
    characters = data.get("characters", [])

    budget_summary, budget_rows = estimate_budget(scenes)
    risk_rows = assess_risks(scenes)

    export_summary = export_all(
        scenes=scenes,
        characters=characters,
        budget_rows=budget_rows,
        risk_rows=risk_rows,
        output_dir=output_dir,
        script_path=script_path,
    )

    return {
        "scenes": scenes,
        "characters": characters,
        "budget_summary": budget_summary,
        "budget_rows": budget_rows,
        "risk_rows": risk_rows,
        "export_summary": export_summary,
    }


if __name__ == "__main__":
    main()


def safe_run_full_analysis(script_path: str, output_dir: str):
    try:
        return run_full_analysis(script_path, output_dir)
    except Exception as e:
        logger.exception("run_full_analysis failed")
        return {"error": str(e)}

