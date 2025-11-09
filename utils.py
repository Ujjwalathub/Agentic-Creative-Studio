"""
Utility functions for the Creative Media Co-Pilot (Agentic AI)
Includes API validation, setup helpers, and output formatting
"""

import os
import dotenv

from dotenv import load_dotenv
from typing import Optional, Tuple


def validate_api_keys() -> Tuple[bool, list]:
    """
    Validate that all required API keys are present and properly formatted.
    
    Returns:
        Tuple of (is_valid: bool, missing_keys: list)
    """
    load_dotenv()
    
    required_keys = {
        "GROQ_API_KEY": "gsk_",
        "TOGETHER_API_KEY": ""  # Together AI keys don't have a standard prefix
    }
    
    missing_keys = []
    invalid_keys = []
    
    for key_name, prefix in required_keys.items():
        value = os.getenv(key_name)
        
        if not value:
            missing_keys.append(key_name)
        elif prefix and not value.startswith(prefix):
            invalid_keys.append(f"{key_name} (should start with '{prefix}')")
    
    all_issues = missing_keys + invalid_keys
    is_valid = len(all_issues) == 0
    
    return is_valid, all_issues


def setup_check():
    """
    Perform a comprehensive setup check before running the workflow.
    """
    print("🔍 Running Setup Validation...\n")
    
    # Check Python version
    import sys
    python_version = sys.version_info
    print(f"✅ Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("⚠️  Warning: Python 3.8+ is recommended")
    
    # Check .env file
    if os.path.exists(".env"):
        print("✅ .env file found")
    else:
        print("❌ .env file not found!")
        print("   → Copy .env.example to .env and add your API keys")
        return False
    
    # Validate API keys
    is_valid, issues = validate_api_keys()
    
    if is_valid:
        print("✅ All API keys are configured")
    else:
        print("❌ API Key Issues Found:")
        for issue in issues:
            print(f"   → {issue}")
        print("\n📖 Get your API keys:")
        print("   • Groq: https://console.groq.com/keys")
        print("   • Together AI: https://api.together.ai/settings/api-keys")
        return False
    
    # Check required packages
    required_packages = [
        "langgraph",
        "langchain",
        "langchain_huggingface",
        "replicate",
        "dotenv"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing Python packages:")
        for pkg in missing_packages:
            print(f"   → {pkg}")
        print("\n💡 Install with: pip install -r requirements.txt")
        return False
    else:
        print("✅ All required packages installed")
    
    print("\n✨ Setup validation complete! Ready to run.\n")
    return True


def format_campaign_output(result: dict, save_to_file: bool = False) -> str:
    """
    Format the campaign generation results into a nice output.
    
    Args:
        result: The final state from the workflow
        save_to_file: Whether to save the output to a file
    
    Returns:
        Formatted string output
    """
    output = []
    output.append("\n" + "="*80)
    output.append("📱 SOCIAL MEDIA CAMPAIGN - FINAL OUTPUT")
    output.append("="*80)
    
    # Ad Copy
    output.append("\n📝 AD COPY:")
    output.append("-" * 80)
    output.append(result.get('draft_text', 'N/A'))
    output.append("-" * 80)
    
    # Image
    output.append("\n🖼️  PROMOTIONAL IMAGE:")
    output.append(f"{result.get('image_url', 'N/A')}")
    
    # Metadata
    output.append("\n📊 GENERATION METADATA:")
    output.append(f"   • Total Iterations: {result.get('retries', 0)}")
    output.append(f"   • Review Cycles: {len(result.get('review_feedback', []))}")
    
    # Review History
    if result.get('review_feedback'):
        output.append("\n📋 REVIEW HISTORY:")
        for i, feedback in enumerate(result.get('review_feedback', []), 1):
            output.append(f"   {i}. {feedback}")
    
    output.append("\n" + "="*80 + "\n")
    
    formatted_output = "\n".join(output)
    
    # Save to file if requested
    if save_to_file:
        filename = f"campaign_output_{os.getpid()}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(formatted_output)
        print(f"💾 Output saved to: {filename}")
    
    return formatted_output


def print_architecture_diagram():
    """
    Print the system architecture diagram to console.
    """
    diagram = """
    ╔════════════════════════════════════════════════════════════════════╗
    ║         AGENTIC MEDIA CO-PILOT - SYSTEM ARCHITECTURE              ║
    ╚════════════════════════════════════════════════════════════════════╝
    
                         ┌─────────────────┐
                         │   USER INPUT    │
                         │ (Product Info)  │
                         └────────┬────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │   COPYWRITER AGENT      │
                    │   (Llama 3 8B - Groq)   │
                    │   "Generate Draft"      │
                    └──────────┬──────────────┘
                               │
                               ▼
                    ┌─────────────────────────┐
                    │   REVIEWER AGENT        │
                    │   (Llama 3 8B - Groq)   │
                    │   "Check Compliance"    │
                    └──────────┬──────────────┘
                               │
                               ▼
                    ┌─────────────────────────┐
                    │   ROUTER DECISION       │
                    │   (Conditional Logic)   │
                    └───┬─────────────────┬───┘
                        │                 │
                 [APPROVED?]         [REVISIONS?]
                        │                 │
                        ▼                 │
          ┌──────────────────────┐       │
          │  ART DIRECTOR AGENT  │       │
          │  (FLUX.1 - Together) │       │
          │  "Generate Image"    │       │
          └──────────┬───────────┘       │
                     │                   │
                     ▼                   │
              ┌────────────┐             │
              │    END     │             │
              └────────────┘             │
                                         │
                     ┌───────────────────┘
                     │ (Loop Back)
                     ▼
          ┌─────────────────────────┐
          │   COPYWRITER AGENT      │
          │   "Revise Based on      │
          │    Feedback"            │
          └─────────────────────────┘
    """
    print(diagram)


def create_env_file_interactive():
    """
    Interactive helper to create a .env file with user input.
    """
    print("\n🔧 .env File Creation Helper")
    print("="*50)
    
    if os.path.exists(".env"):
        response = input(".env file already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            return
    
    print("\n📖 You'll need API keys from:")
    print("   • Groq: https://console.groq.com/keys")
    print("   • Together AI: https://api.together.ai/settings/api-keys")
    print()
    
    groq_key = input("Enter your Groq API key (gsk_...): ").strip()
    together_key = input("Enter your Together AI API key: ").strip()
    
    env_content = f"""# API Keys for Creative Media Co-Pilot (Agentic AI)
# Generated automatically

GROQ_API_KEY={groq_key}
TOGETHER_API_KEY={together_key}
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("\n✅ .env file created successfully!")
    print("🔍 Validating API keys...")
    
    is_valid, issues = validate_api_keys()
    
    if is_valid:
        print("✅ All API keys are valid!")
    else:
        print("⚠️  Warning: Some API keys may be invalid:")
        for issue in issues:
            print(f"   → {issue}")


if __name__ == "__main__":
    """
    Run this script directly for setup assistance
    """
    print("🤖 Creative Media Co-Pilot (Agentic AI) - Setup Assistant\n")
    
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "check":
            setup_check()
        elif command == "create-env":
            create_env_file_interactive()
        elif command == "diagram":
            print_architecture_diagram()
        else:
            print(f"Unknown command: {command}")
            print("\nAvailable commands:")
            print("  python utils.py check       - Run setup validation")
            print("  python utils.py create-env  - Create .env file interactively")
            print("  python utils.py diagram     - Show architecture diagram")
    else:
        # Default: run setup check
        setup_check()
