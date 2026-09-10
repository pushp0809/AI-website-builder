#!/usr/bin/env python3
"""CLI for AgentSite multi-agent website building framework."""

import argparse
import sys
from pathlib import Path


def cmd_init(args):
    """Initialize the project structure."""
    print("AgentSite initialized!")
    print(f"Working directory: {Path.cwd()}")
    print("\nAvailable commands:")
    print("  python cli.py run \"<requirement>\"  - Run the full pipeline")
    print("  python cli.py validate               - Validate generated artifacts")
    print("  python cli.py security               - Run security audit")
    print("  python cli.py docs                   - Show documentation")
    print("  python cli.py report                 - Generate execution report")
    return 0


def cmd_run(args):
    """Run the full pipeline."""
    requirement = args.requirement
    
    if not requirement:
        print("Error: Please provide a requirement string")
        print("Usage: python cli.py run \"Build an employee benefits portal\"")
        return 1
    
    print(f"Running AgentSite with requirement: {requirement}")
    print("=" * 60)
    
    try:
        from agentsite.orchestrator import Orchestrator
        
        orchestrator = Orchestrator()
        result = orchestrator.run(requirement)
        
        if result.get("success"):
            print("\n" + "=" * 60)
            print("✓ Pipeline completed successfully!")
            print("=" * 60)
            
            # Show summary
            state = result.get("state", {})
            print(f"\nPipeline ID: {state.get('pipeline_id', 'N/A')}")
            print(f"Status: {state.get('final_status', 'N/A')}")
            
            # List generated artifacts
            artifacts_dir = Path("artifacts")
            if artifacts_dir.exists():
                print(f"\nGenerated artifacts in /artifacts:")
                for f in sorted(artifacts_dir.iterdir()):
                    print(f"  - {f.name}")
            
            # Show generated app location
            generated_app = Path("generated_app")
            if generated_app.exists():
                print(f"\nGenerated application in /generated_app:")
                for f in sorted(generated_app.iterdir()):
                    if f.is_file():
                        print(f"  - {f.name}")
            
            print("\nTo run the generated application:")
            print("  python -m uvicorn generated_app.main:app --host 0.0.0.0 --port 8000")
            print("\nThen open http://localhost:8000 in your browser.")
            
            return 0
        else:
            print("\n" + "=" * 60)
            print("✗ Pipeline failed")
            print("=" * 60)
            print(f"Error: {result.get('message', 'Unknown error')}")
            return 1
            
    except Exception as e:
        print(f"\nError running pipeline: {e}")
        import traceback
        traceback.print_exc()
        return 1


def cmd_validate(args):
    """Validate generated artifacts."""
    print("Validating artifacts...")
    
    try:
        from agentsite.artifact_store import ArtifactStore
        from agentsite.validation_gates import ValidationGates
        from agentsite.state_manager import StateManager
        
        artifact_store = ArtifactStore()
        state_manager = StateManager()
        gates = ValidationGates(artifact_store, state_manager)
        
        results = gates.check_all_gates()
        
        all_passed = True
        for gate_name, passed in results.items():
            status = "✓" if passed else "✗"
            print(f"  {status} {gate_name}")
            if not passed:
                all_passed = False
        
        if all_passed:
            print("\n✓ All validation gates passed!")
            return 0
        else:
            print("\n✗ Some validation gates failed")
            return 1
            
    except Exception as e:
        print(f"Error during validation: {e}")
        return 1


def cmd_security(args):
    """Run security audit."""
    print("Running security audit...")
    
    try:
        from agentsite.agents.registry import initialize_registry, AgentRegistry
        from agentsite.artifact_store import ArtifactStore
        
        initialize_registry()
        artifact_store = ArtifactStore()
        
        agent = AgentRegistry.create_agent("SecurityAuditorAgent", artifact_store=artifact_store)
        result = agent.execute({})
        
        if result.get("passed"):
            print("\n✓ Security audit PASSED")
            print(f"Findings: {len(result.get('findings', []))}")
        else:
            print("\n✗ Security audit FAILED")
            print(f"Critical/High findings: {len([f for f in result.get('findings', []) if f.get('severity') in ['CRITICAL', 'HIGH']])}")
        
        # Show report location
        if artifact_store.exists("08_security_report.md"):
            print(f"\nFull report: artifacts/08_security_report.md")
        
        return 0 if result.get("passed") else 1
        
    except Exception as e:
        print(f"Error during security audit: {e}")
        return 1


def cmd_docs(args):
    """Show documentation."""
    print("Documentation files:")
    
    docs = [
        ("README.md", "Main project README"),
        ("ARCHITECTURE.md", "Architecture overview"),
        ("SECURITY.md", "Security documentation"),
        ("DEMO_SCRIPT.md", "Demo presentation script"),
        ("IMPLEMENTATION_PLAN.md", "Implementation plan"),
    ]
    
    for doc, description in docs:
        path = Path(doc)
        exists = "✓" if path.exists() else " "
        print(f"  [{exists}] {doc}: {description}")
    
    # Also check generated app docs
    app_docs = Path("artifacts/README_APP.md")
    if app_docs.exists():
        print(f"\nGenerated application documentation:")
        print(f"  ✓ artifacts/README_APP.md")
    
    return 0


def cmd_report(args):
    """Generate execution report."""
    print("Generating execution report...")
    
    try:
        from agentsite.state_manager import StateManager
        from pathlib import Path
        
        state_manager = StateManager()
        state = state_manager.get_state()
        
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        
        # Generate comprehensive report
        report = state_manager.get_summary()
        
        report_path = reports_dir / "latest_report.md"
        with open(report_path, "w") as f:
            f.write("# Latest Execution Report\n\n")
            f.write(report)
        
        print(f"\nReport saved to: {report_path}")
        print("\n" + report)
        
        return 0
        
    except Exception as e:
        print(f"Error generating report: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="AgentSite - Multi-agent website building framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py init
  python cli.py run "Build an employee benefits portal"
  python cli.py validate
  python cli.py security
  python cli.py docs
  python cli.py report
        """,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # init command
    init_parser = subparsers.add_parser("init", help="Initialize project")
    init_parser.set_defaults(func=cmd_init)
    
    # run command
    run_parser = subparsers.add_parser("run", help="Run the pipeline")
    run_parser.add_argument("requirement", nargs="?", help="Natural language requirement")
    run_parser.set_defaults(func=cmd_run)
    
    # validate command
    validate_parser = subparsers.add_parser("validate", help="Validate artifacts")
    validate_parser.set_defaults(func=cmd_validate)
    
    # security command
    security_parser = subparsers.add_parser("security", help="Run security audit")
    security_parser.set_defaults(func=cmd_security)
    
    # docs command
    docs_parser = subparsers.add_parser("docs", help="Show documentation")
    docs_parser.set_defaults(func=cmd_docs)
    
    # report command
    report_parser = subparsers.add_parser("report", help="Generate report")
    report_parser.set_defaults(func=cmd_report)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
