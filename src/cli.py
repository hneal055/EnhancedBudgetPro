import argparse
import os
import sys
from pathlib import Path
from datetime import datetime
from src.ScriptIngest import run_full_analysis, safe_run_full_analysis

try:
    from src.IntegrationEngine import IntegrationManager
    INTEGRATIONS_AVAILABLE = True
except ImportError:
    INTEGRATIONS_AVAILABLE = False


def cmd_analyze(args):
    script_path = args.input
    output_dir = args.out

    os.makedirs(output_dir, exist_ok=True)
    result = safe_run_full_analysis(script_path, output_dir)

    if isinstance(result, dict) and result.get("error"):
        print('ERROR:', result.get('error'))
        sys.exit(1)

    scenes = result["scenes"]
    characters = result["characters"]
    budget_summary = result["budget_summary"]
    risk_rows = result["risk_rows"]

    print("\n================ ANALYSIS =================")
    print(f"Script:        {script_path}")
    print(f"Scenes:        {len(scenes)}")
    print(f"Characters:    {len(set(characters))}")
    print("-------------------------------------------")
    print(f"Total Budget:  ${budget_summary['total_budget']:.2f}")
    print(f"Avg/Scene:     ${budget_summary['average_cost_per_scene']:.2f}")
    high = sum(1 for r in risk_rows if r["risk_level"] == "HIGH")
    med = sum(1 for r in risk_rows if r["risk_level"] == "MEDIUM")
    low = sum(1 for r in risk_rows if r["risk_level"] == "LOW")
    print(f"Risk Levels:   HIGH={high} MEDIUM={med} LOW={low}")
    print("-------------------------------------------")
    print(f"Output folder: {os.path.abspath(output_dir)}")
    print("===========================================\n")

    # Trigger integrations if available and configured
    if INTEGRATIONS_AVAILABLE:
        config_path = Path('integrations.json')
        if config_path.exists():
            try:
                print("Sending to integrations...")
                manager = IntegrationManager(str(config_path))
                enabled = manager.get_enabled_integrations()
                
                if enabled:
                    integration_data = {
                        'script_name': Path(script_path).name,
                        'format': Path(script_path).suffix,
                        'scene_count': len(scenes),
                        'character_count': len(set(characters)),
                        'budget': budget_summary['total_budget'],
                        'output_path': os.path.abspath(output_dir),
                        'timestamp': datetime.now().isoformat(),
                        'risk_summary': {'high': high, 'medium': med, 'low': low}
                    }
                    
                    results = manager.export_analysis(integration_data)
                    print(f"Integrations complete: {len([r for r in results.values() if r])}/{len(results)} succeeded\n")
            except Exception as e:
                print(f"Integration error: {e}")


def cmd_batch(args):
    input_dir = args.input_dir
    output_root = args.out

    os.makedirs(output_root, exist_ok=True)
    scripts = [
        f for f in os.listdir(input_dir)
        if not f.startswith(".")
    ]

    print(f"Found {len(scripts)} files in {input_dir}")

    for name in scripts:
        script_path = os.path.join(input_dir, name)
        base, _ = os.path.splitext(name)
        out_dir = os.path.join(output_root, base)

        print(f"\n=== Processing {name} to {out_dir} ===")
        try:
            run_full_analysis(script_path, out_dir)
            print("   OK")
        except Exception as exc:
            print(f"   Failed: {exc}")


def build_parser():
    parser = argparse.ArgumentParser(
        description="Enhanced Budget Pro CLI (Script to Budget and Risk)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # analyze
    p_analyze = sub.add_parser("analyze", help="Analyze a single script file")
    p_analyze.add_argument("--input", "-i", required=True,
                           help="Path to script (fdx, fountain, celtx/json, pdf, txt)")
    p_analyze.add_argument("--out", "-o", required=True,
                           help="Output directory")
    p_analyze.set_defaults(func=cmd_analyze)

    # batch
    p_batch = sub.add_parser("batch", help="Analyze all scripts in a folder")
    p_batch.add_argument("--input-dir", "-d", required=True,
                         help="Folder containing scripts")
    p_batch.add_argument("--out", "-o", required=True,
                         help="Root output folder")
    p_batch.set_defaults(func=cmd_batch)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
