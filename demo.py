"""
🎬 DEMO SCRIPT - Creative Media Co-Pilot
Interactive demonstration of multi-agent creative workflow with multiple campaigns
"""

import time
from main import run_campaign_generator

def demo_header():
    """Display beautiful demo header"""
    print("\n" + "="*80)
    print("🎬 CREATIVE MEDIA CO-PILOT - LIVE DEMONSTRATION")
    print("="*80)
    print("\n📋 This demo showcases a multi-agent AI system that:")
    print("   ✓ Generates creative marketing copy")
    print("   ✓ Validates compliance automatically")
    print("   ✓ Refines content through validation loops")
    print("   ✓ Generates promotional images")
    print("\n🔧 Technology: LangGraph + Llama 3.1 8B + FLUX.1-schnell")
    print("="*80 + "\n")


def demo_single_campaign(product_name, product_description):
    """Run a single campaign with descriptions"""
    print("\n" + "█"*80)
    print(f"CAMPAIGN: {product_name}")
    print("█"*80 + "\n")
    
    print(f"📦 Product: {product_description}\n")
    print("⏱️  Executing workflow...\n")
    
    start_time = time.time()
    result = run_campaign_generator(product_description)
    duration = time.time() - start_time
    
    if result:
        print(f"\n✅ Campaign completed in {duration:.1f} seconds!")
        print(f"\n📊 Metrics:")
        print(f"   • Iterations: {result['retries']}")
        print(f"   • Review cycles: {len(result['review_feedback'])}")
        print(f"   • Approved: {'Yes ✅' if result['is_approved'] else 'No ❌'}")
        
        return result
    else:
        print("\n❌ Campaign failed")
        return None


def demo_multi_campaign():
    """Run multiple campaigns demonstrating various product categories"""
    
    demo_header()
    
    campaigns = [
        {
            "name": "CAMPAIGN 1: Eco-Friendly Product",
            "description": "Eco-friendly water bottle made with sustainable bamboo, keeps drinks cold for 24 hours"
        },
        {
            "name": "CAMPAIGN 2: Tech Product",
            "description": "AI-powered smartwatch with health monitoring, sleep tracking, and 7-day battery life"
        },
        {
            "name": "CAMPAIGN 3: Beauty & Skincare",
            "description": "Natural skincare serum with vitamin C and hyaluronic acid, cruelty-free and vegan"
        }
    ]
    
    results = []
    
    for i, campaign in enumerate(campaigns, 1):
        print(f"\n{'─'*80}")
        print(f"🔄 Campaign {i}/{len(campaigns)}")
        print(f"{'─'*80}\n")
        
        result = demo_single_campaign(campaign['name'], campaign['description'])
        
        if result:
            results.append({
                "campaign": campaign['name'],
                "result": result
            })
        
        if i < len(campaigns):
            print("\n⏳ Waiting before next campaign...\n")
            time.sleep(2)
    
    # Summary
    print("\n" + "="*80)
    print("📊 DEMO SUMMARY")
    print("="*80)
    print(f"\nSuccessfully completed {len(results)}/{len(campaigns)} campaigns\n")
    
    for item in results:
        approval_status = "✅ APPROVED" if item['result']['is_approved'] else "⏳ PENDING"
        print(f"• {item['campaign']}: {approval_status} ({item['result']['retries']} iterations)")
    
    print("\n" + "="*80 + "\n")
    
    return results


def demo_specific_campaign(product_description):
    """Run a specific campaign from user input"""
    demo_header()
    
    print(f"🎯 Running custom campaign...\n")
    result = run_campaign_generator(product_description)
    
    return result


def demo_architecture_overview():
    """Display system architecture"""
    print("\n" + "="*80)
    print("🏗️ SYSTEM ARCHITECTURE")
    print("="*80 + "\n")
    
    architecture = """
    ┌─────────────────────────────────────────────────────────────┐
    │                   USER INPUT / BRIEF                        │
    │        (Product description, campaign goals, etc.)          │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
    ╔═════════════════════════════════════════════════════════════╗
    ║              MULTI-AGENT ORCHESTRATION LAYER                ║
    ║                                                             ║
    ║  ┌──────────────────────────────────────────────────────┐  ║
    ║  │ 🖊️  WRITER AGENT                                     │  ║
    ║  │ Model: Llama 3.1 8B (Groq)                           │  ║
    ║  │ Task: Generate creative social media copy            │  ║
    ║  │ Output: draft_text                                   │  ║
    ║  └──────────────────────────────────────────────────────┘  ║
    ║                      │                                      ║
    ║                      ▼                                      ║
    ║  ┌──────────────────────────────────────────────────────┐  ║
    ║  │ ⚖️  REVIEWER AGENT                                    │  ║
    ║  │ Model: Llama 3.1 8B (Groq)                           │  ║
    ║  │ Task: Validate compliance & brand voice              │  ║
    ║  │ Output: APPROVED or [FEEDBACK]                       │  ║
    ║  └──────────────────────────────────────────────────────┘  ║
    ║                      │                                      ║
    ║                      ▼                                      ║
    ║  ┌──────────────────────────────────────────────────────┐  ║
    ║  │ 🔀 ROUTER (Conditional Decision Engine)              │  ║
    ║  │                                                       │  ║
    ║  │ if approved → proceed to Art Director                │  ║
    ║  │ if not approved → loop back to Writer                │  ║
    ║  │ if max retries → force to Art Director (safety)      │  ║
    ║  └──────────────────────────────────────────────────────┘  ║
    ║                 │                    │                      ║
    ║        ✅ APPROVED          ❌ REVISION NEEDED             ║
    ║                 │                    │                      ║
    ║                 ▼                    ▼                      ║
    ║  ┌──────────────────────┐  ┌────────────────────┐          ║
    ║  │ 🎨 ART DIRECTOR      │  │  Loop back to     │          ║
    ║  │ Model: FLUX.1        │  │  Writer with      │          ║
    ║  │ Task: Image gen      │  │  feedback         │          ║
    ║  └──────────────────────┘  └────────────────────┘          ║
    ║           │                          │                      ║
    ║           └──────────┬───────────────┘                      ║
    ║                      │                                      ║
    ╚═════════════════════════════════════════════════════════════╝
                           │
                           ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                    FINAL ASSETS                             │
    │                                                             │
    │  📝 Approved Copy: "Discover our eco-friendly water..."    │
    │  🖼️  Generated Image: promotional_image_12345.png          │
    │  📋 Review History: [Iteration 1, Iteration 2, ...]        │
    │  ⏱️  Execution Time: ~25 seconds                            │
    └─────────────────────────────────────────────────────────────┘
    """
    
    print(architecture)
    print("="*80 + "\n")


def demo_state_evolution():
    """Show how state evolves through workflow"""
    print("\n" + "="*80)
    print("📊 STATE EVOLUTION EXAMPLE")
    print("="*80 + "\n")
    
    state_evolution = """
    INITIAL STATE:
    {
      user_prompt: "Eco-friendly water bottle made with bamboo",
      draft_text: "",
      review_feedback: [],
      retries: 0,
      is_approved: false
    }

    ⬇️  [WRITER AGENT] ⬇️

    AFTER WRITER (Iteration 1):
    {
      user_prompt: "Eco-friendly water bottle made with bamboo",
      draft_text: "🌿 100% bamboo bottle! GUARANTEED to change 
                    your life! BEST DEAL EVER! 🌍",
      review_feedback: [],
      retries: 1,
      is_approved: false
    }

    ⬇️  [REVIEWER AGENT] ⬇️

    AFTER REVIEWER (Iteration 1):
    {
      ...,
      review_feedback: ["[CLAIM] Remove '100%' and 'GUARANTEED'"],
      is_approved: false
    }

    ⬇️  [ROUTER] - NOT APPROVED, LOOP BACK ⬇️

    AFTER WRITER (Iteration 2):
    {
      draft_text: "Discover our bamboo water bottle. Eco-friendly 
                   design, keeps drinks cold for 24 hours. 💚",
      review_feedback: ["[CLAIM] Remove '100%' and 'GUARANTEED'"],
      retries: 2,
      is_approved: false
    }

    ⬇️  [REVIEWER AGENT] ⬇️

    AFTER REVIEWER (Iteration 2):
    {
      review_feedback: [
        "[CLAIM] Remove '100%' and 'GUARANTEED'",
        "APPROVED"
      ],
      final_approved_text: "Discover our bamboo water bottle...",
      is_approved: true
    }

    ⬇️  [ROUTER] - APPROVED, PROCEED ⬇️

    FINAL STATE (After Art Director):
    {
      final_approved_text: "Discover our bamboo water bottle...",
      image_url: "generated_image_12345.png",
      review_feedback: [...],
      retries: 2,
      is_approved: true,
      execution_time: 25.3
    }
    """
    
    print(state_evolution)
    print("="*80 + "\n")


def demo_agent_specialization():
    """Show how each agent specializes"""
    print("\n" + "="*80)
    print("🧠 AGENT SPECIALIZATION")
    print("="*80 + "\n")
    
    specialization = """
    1️⃣  WRITER AGENT (Copywriter)
    ┌─────────────────────────────────────────────────────────┐
    │ Model: Llama 3.1 8B (Temperature: 0.75)                 │
    │ Personality: Creative, energetic, persuasive             │
    │ Goal: Capture attention and drive action                │
    │                                                         │
    │ Input:  "Eco-friendly water bottle"                     │
    │ Output: "🌿 Discover our sustainable bottle!            │
    │         Keep your drinks cold, planet cooler. 💚"       │
    │                                                         │
    │ Specialization:                                         │
    │   ✓ Generates engaging copy                             │
    │   ✓ Incorporates feedback from reviewer                 │
    │   ✓ Adapts tone based on product type                   │
    │   ✓ Uses emojis and platform-appropriate length         │
    └─────────────────────────────────────────────────────────┘

    2️⃣  REVIEWER AGENT (Compliance Officer)
    ┌─────────────────────────────────────────────────────────┐
    │ Model: Llama 3.1 8B (Temperature: 0.30)                 │
    │ Personality: Strict, analytical, thorough               │
    │ Goal: Ensure compliance and brand standards             │
    │                                                         │
    │ Input:  "🌿 Our bottle is 100% guaranteed best!"        │
    │ Output: "[CLAIM] Remove unverified claims"              │
    │                                                         │
    │ Checks:                                                 │
    │   ✓ Unverified claims (100%, miracle, guaranteed)       │
    │   ✓ Brand voice alignment (energetic, positive)         │
    │   ✓ Clarity and factuality                              │
    │   ✓ Platform constraints (280 chars)                    │
    │   ✓ Potentially harmful language                        │
    └─────────────────────────────────────────────────────────┘

    3️⃣  ART DIRECTOR AGENT (Visual Creator)
    ┌─────────────────────────────────────────────────────────┐
    │ Model: FLUX.1-schnell (via Hugging Face)                │
    │ Personality: Visually meticulous, modern                │
    │ Goal: Create high-quality promotional imagery           │
    │                                                         │
    │ Input:  Approved copy + product description             │
    │ Output: Professional 4K product photography             │
    │                                                         │
    │ Specialization:                                         │
    │   ✓ Generates high-quality imagery (4K)                 │
    │   ✓ Maintains professional aesthetic                    │
    │   ✓ Aligns visuals with copy                            │
    │   ✓ Optimized for social media platforms                │
    └─────────────────────────────────────────────────────────┘
    """
    
    print(specialization)
    print("="*80 + "\n")


def demo_validation_loop():
    """Show the validation loop in action"""
    print("\n" + "="*80)
    print("🔄 VALIDATION & REFINEMENT LOOP")
    print("="*80 + "\n")
    
    loop_demo = """
    The key innovation: AUTONOMOUS VALIDATION LOOP
    
    Traditional Workflow:           Agentic AI Workflow:
    ┌──────────────┐               ┌──────────────┐
    │ User writes  │               │   User       │
    │ ad copy      │               │   provides   │
    └──────┬───────┘               │   product    │
           │                       └──────┬───────┘
           ▼                              │
    ┌──────────────┐                      ▼
    │ Marketer     │              ┌──────────────┐
    │ reviews      │              │ Writer Agent │
    │ manually     │              │ generates    │
    └──────┬───────┘              └──────┬───────┘
           │                             │
           ▼                             ▼
    ┌──────────────┐              ┌──────────────┐
    │ Compliance   │              │ Reviewer     │
    │ check        │              │ Agent        │
    └──────┬───────┘              └──────┬───────┘
           │                             │
           ▼                             ▼
    ┌──────────────┐         ┌──────────────────┐
    │ Approved?    │         │ Router Decision  │
    │ NO ❌        │         │ Approved?        │
    │ → Revise     │         └──────┬───────────┘
    │ again        │                │
    │ (Manual!)    │      ┌─────────┴─────────┐
    │              │      │                   │
    └──────┬───────┘      ▼                   ▼
           │        ┌─────────┐    ┌──────────────┐
           │        │Proceed  │    │  Loop back   │
           │        │to design│    │  to Writer   │
           │        └────┬────┘    │ (Automatic!) │
           │             │         └──────┬───────┘
           ▼             │                │
    ┌──────────────┐     │     ┌──────────┘
    │ Designer     │     │     │
    │ creates      │     │     ▼
    │ visual       │     │   (Repeat until
    └──────┬───────┘     │    APPROVED)
           │             │
           ▼             ▼
    ┌──────────────────────────┐
    │   Final Assets           │
    │ (Maybe needs revisions?) │
    └──────────────────────────┘
    
    TIME TO DELIVERY:
    Traditional: ~4-8 hours (manual coordination)
    Agentic:     ~25-45 seconds (autonomous)
    
    SPEED IMPROVEMENT: ~300-1000x faster ⚡
    """
    
    print(loop_demo)
    print("="*80 + "\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "architecture":
            demo_architecture_overview()
        elif command == "specialization":
            demo_agent_specialization()
        elif command == "state":
            demo_state_evolution()
        elif command == "loop":
            demo_validation_loop()
        elif command == "custom":
            if len(sys.argv) > 2:
                product = " ".join(sys.argv[2:])
                demo_specific_campaign(product)
            else:
                print("Usage: python demo.py custom 'product description'")
        else:
            print(f"Unknown command: {command}")
            print("\nAvailable demos:")
            print("  python demo.py architecture   - Show system architecture")
            print("  python demo.py specialization - Show agent specialization")
            print("  python demo.py state          - Show state evolution")
            print("  python demo.py loop           - Show validation loop")
            print("  python demo.py custom 'prod'  - Run custom campaign")
            print("  python demo.py                - Run full multi-campaign demo")
    else:
        # Default: run multi-campaign demo
        demo_multi_campaign()
