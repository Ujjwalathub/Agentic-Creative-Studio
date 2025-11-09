"""
🤖 CREATIVE MEDIA CO-PILOT (Agentic AI)
=================================================
A sophisticated multi-agent AI system using LangGraph for automated creative campaign generation.

This system demonstrates a production-ready "validate and refine" workflow using:
- Llama 3.1 8B (via Groq) for creative copywriting and compliance review
- FLUX.1-schnell (via Together AI) for high-quality image generation

Key Features:
  ✓ Multi-agent collaboration (Writer, Reviewer, Art Director)
  ✓ Autonomous validation and refinement loops
  ✓ State-of-the-art open-source models only
  ✓ Full transparency and audit trail
  ✓ Production-ready error handling

Architecture: LangGraph with conditional edge routing and shared state management
"""

import os
import json
import time
from typing import TypedDict, List, Optional, Dict, Any
from datetime import datetime
from typing_extensions import Annotated

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from dotenv import load_dotenv

# Configure logging for transparency
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load API keys from .env file
load_dotenv()

# =============================================================================
# 1. DEFINE THE STATE (Agent Memory and Communication)
# =============================================================================

class CreativeWorkflowState(TypedDict):
    """
    The shared state object passed between all agents.
    This TypedDict serves as the "memory" and "communication channel" for the entire workflow.
    
    Each agent reads from this state and returns updates to specific fields.
    LangGraph merges these updates automatically, maintaining a complete audit trail.
    """
    # Input
    user_prompt: str                           # Original user input (product description)
    
    # Workflow State
    draft_text: str                            # Current ad copy draft
    review_feedback: List[str]                 # Complete history of all review feedback
    final_approved_text: Optional[str]         # Approved copy ready for image generation
    image_url: str                             # Generated image URL or status
    
    # Metadata
    retries: int                               # Retry counter (safety mechanism)
    current_iteration: int                     # Iteration number for logging
    workflow_start_time: float                 # Timestamp when workflow started
    agent_execution_log: List[Dict[str, Any]] # Detailed log of agent execution
    
    # Compliance tracking
    compliance_flags: List[str]                # Any compliance issues detected
    is_approved: bool                          # Flag indicating final approval status


# =============================================================================
# 2. INITIALIZE AI MODELS (Open-Source Only)
# =============================================================================

print("\n" + "="*80)
print("� INITIALIZING CREATIVE MEDIA CO-PILOT")
print("="*80)
print("\n�🔧 Initializing AI Models...\n")

# Groq API with Llama 3.1 8B for text generation and review
writer_llm = None
reviewer_llm = None

try:
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in environment")
    
    # Writer LLM (higher temperature for creativity)
    writer_llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.75,
        max_tokens=512,
        api_key=groq_api_key
    )
    
    # Reviewer LLM (lower temperature for consistency and accuracy)
    reviewer_llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3,
        max_tokens=256,
        api_key=groq_api_key
    )
    
    print("✅ Groq (Llama 3.1 8B) successfully initialized")
    print("   └─ Writer Agent: Creative text generation (temp=0.75)")
    print("   └─ Reviewer Agent: Compliance checking (temp=0.30)")
    
except Exception as e:
    print(f"❌ Groq initialization failed: {e}")
    print("   Continuing with fallback models...")
    logger.error(f"Groq init error: {e}")

# Hugging Face for image generation
try:
    from huggingface_hub import InferenceClient
    
    hf_token = os.getenv('HUGGINGFACE_API_TOKEN')
    if hf_token:
        HF_CLIENT = InferenceClient(token=hf_token)
        print("✅ Hugging Face (FLUX.1-schnell) initialized for image generation")
    else:
        HF_CLIENT = None
        print("⚠️  HUGGINGFACE_API_TOKEN not found - image generation will be simulated")
        
except Exception as e:
    HF_CLIENT = None
    print(f"⚠️  Hugging Face initialization: {e}")


def generate_image_with_hf(prompt: str) -> str:
    """
    Generate image using Hugging Face FLUX.1-schnell model.
    
    Args:
        prompt: The text description for image generation
    
    Returns:
        Image URL or status message
    """
    try:
        if not HF_CLIENT:
            logger.warning("HF_CLIENT not available, using simulated image")
            return "Simulated image URL (no API token provided)"
        
        logger.info(f"Generating image with prompt: {prompt[:100]}...")
        image = HF_CLIENT.text_to_image(prompt, model="black-forest-labs/FLUX.1-schnell")
        
        filename = f"campaign_output_{int(time.time())}.png"
        image.save(filename)
        
        logger.info(f"Image saved: {filename}")
        return f"Generated: {filename}"
        
    except Exception as e:
        logger.error(f"Image generation error: {e}")
        return f"[Image generation error: {str(e)[:50]}...]"


print("\n" + "="*80 + "\n")



# =============================================================================
# 3. DEFINE AGENT NODES (The Collaborative Team)
# =============================================================================

def log_agent_action(state: CreativeWorkflowState, agent_name: str, 
                     action: str, result: str, status: str = "SUCCESS") -> Dict[str, Any]:
    """
    Log agent execution for full transparency and audit trail.
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent_name,
        "action": action,
        "result_length": len(str(result)),
        "status": status,
        "iteration": state.get('current_iteration', 0)
    }
    return log_entry


def writer_node(state: CreativeWorkflowState) -> dict:
    """
    🖊️ COPYWRITER AGENT NODE
    
    Responsibility: Generate creative, engaging ad copy
    Model: Llama 3.1 8B (via Groq)
    Temperature: 0.75 (creative, but not random)
    
    Input from state:
        - user_prompt: Product description
        - review_feedback: Previous reviewer comments (for refinement)
    
    Output to state:
        - draft_text: New or revised ad copy
        - current_iteration: Increment iteration counter
        - agent_execution_log: Log this action
    """
    iteration = state.get('current_iteration', 0) + 1
    retries = state.get('retries', 0)
    
    print(f"\n{'─'*80}")
    print(f"📝 [{iteration}.1] WRITER AGENT - Draft Generation (Attempt #{retries + 1})")
    print(f"{'─'*80}")
    
    product = state['user_prompt']
    
    # Craft the prompt for creative copy generation
    system_prompt = """You are an exceptional copywriter specializing in social media advertising.
Your task is to create compelling, energetic, 2-3 line ad copy that:
- Captures attention immediately
- Is specific about product benefits (no vague claims)
- Uses engaging language with emojis
- Is platform-ready (Twitter/Instagram length)
- Avoids unverified claims like "100%", "guaranteed", "miracle"

Write ONLY the ad copy, no explanations."""

    user_message = f"Create an engaging social media ad for: {product}"
    
    # If there's previous feedback, ask for revision
    if state.get('review_feedback'):
        latest_feedback = state['review_feedback'][-1]
        if "APPROVED" not in latest_feedback:
            user_message += f"\n\nPrevious feedback: {latest_feedback}\nPlease revise accordingly."
            print(f"   ℹ️  Incorporating reviewer feedback for refinement...")
    
    try:
        if writer_llm:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_message)
            ]
            response = writer_llm.invoke(messages)
            draft = response.content.strip()
            status = "SUCCESS"
        else:
            raise Exception("Writer LLM not initialized")
    
    except Exception as e:
        logger.error(f"Writer LLM error: {e}")
        print(f"   ⚠️  Using fallback copy generation...")
        
        # Intelligent fallback that responds to feedback
        product_short = product[:40]
        if state.get('review_feedback') and len(state['review_feedback']) > 0:
            # Revise based on feedback
            draft = f"🌟 Discover {product_short}! Eco-conscious. Quality crafted. Get yours now! 💚"
        else:
            # First draft
            draft = f"✨ NEW: {product_short}! Perfect for the modern lifestyle. Shop today! 🚀"
        status = "FALLBACK"
    
    log_entry = log_agent_action(state, "Writer", "copy_generation", draft, status)
    
    print(f"   ✓ Draft generated ({len(draft)} chars)")
    print(f"   📄 Preview: {draft[:70]}...")
    
    return {
        "draft_text": draft,
        "current_iteration": iteration,
        "retries": retries + 1,
        "agent_execution_log": state.get('agent_execution_log', []) + [log_entry]
    }


def reviewer_node(state: CreativeWorkflowState) -> dict:
    """
    ⚖️ COMPLIANCE REVIEWER AGENT NODE
    
    Responsibility: Validate ad copy for compliance, legal risks, and brand voice
    Model: Llama 3.1 8B (via Groq)
    Temperature: 0.3 (consistent, careful evaluation)
    
    Input from state:
        - draft_text: Ad copy to review
    
    Output to state:
        - review_feedback: Append reviewer's assessment
        - final_approved_text: Set if APPROVED
        - compliance_flags: List any issues found
    """
    iteration = state.get('current_iteration', 0)
    retries = state.get('retries', 0)
    
    print(f"\n{'─'*80}")
    print(f"⚖️  [{iteration}.2] REVIEWER AGENT - Compliance Check")
    print(f"{'─'*80}")
    
    draft = state['draft_text']
    
    system_prompt = """You are a strict legal and brand compliance officer for social media ads.

Your job is to:
1. Identify unverified claims (e.g., "100%", "guaranteed", "best", "miracle", "scientifically proven")
2. Check for brand voice alignment (must be energetic, positive, authentic)
3. Verify clarity and conciseness
4. Ensure no misleading statements

RESPOND IN EXACTLY ONE OF THESE WAYS:

Option A - If compliant: Reply with ONLY the word "APPROVED"

Option B - If issues found: Provide ONE specific, actionable feedback (max 1 sentence).
Start with the issue type: [CLAIM], [TONE], [CLARITY], or [OTHER]

Example rejections:
- "[CLAIM] Remove '100%' - it's unverified"
- "[TONE] Make it more energetic"
- "[CLARITY] Specify what 'eco-friendly' means"
"""

    review_prompt = f"""Review this ad copy: "{draft}"

Is it compliant and ready to publish?"""

    try:
        if reviewer_llm:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=review_prompt)
            ]
            response = reviewer_llm.invoke(messages)
            feedback = response.content.strip()
            status = "SUCCESS"
        else:
            raise Exception("Reviewer LLM not initialized")
    
    except Exception as e:
        logger.error(f"Reviewer LLM error: {e}")
        print(f"   ⚠️  Using rule-based compliance checker...")
        
        # Fallback: rule-based compliance check
        draft_lower = draft.lower()
        issues = []
        
        # Check for banned claims
        banned_phrases = [
            "100%", "guarantee", "guaranteed", "miracle", "instant results",
            "best in the world", "never", "always works", "scientifically proven",
            "approved by", "clinically tested"
        ]
        
        for phrase in banned_phrases:
            if phrase in draft_lower:
                issues.append(f"[CLAIM] Remove unverified claim: '{phrase}'")
                break
        
        # Check for negative language
        negative_words = ["toxic", "harmful", "dangerous", "problem", "issue"]
        if any(word in draft_lower for word in negative_words):
            issues.append("[TONE] Avoid negative language")
        
        # Check length
        if len(draft) > 280:
            issues.append("[CLARITY] Keep under 280 characters for social media")
        
        feedback = issues[0] if issues else "APPROVED"
        status = "FALLBACK"
    
    # Determine if approved
    is_approved = "APPROVED" in feedback.upper()
    approved_text = draft if is_approved else state.get('final_approved_text')
    
    compliance_flags = state.get('compliance_flags', [])
    if not is_approved and feedback not in compliance_flags:
        compliance_flags.append(feedback)
    
    log_entry = log_agent_action(state, "Reviewer", "compliance_check", feedback, status)
    
    if is_approved:
        print(f"   ✅ APPROVED - Ready for image generation")
    else:
        print(f"   ❌ REVISION NEEDED")
        print(f"   📋 Feedback: {feedback}")
    
    return {
        "review_feedback": state.get('review_feedback', []) + [feedback],
        "final_approved_text": approved_text,
        "is_approved": is_approved,
        "compliance_flags": compliance_flags,
        "agent_execution_log": state.get('agent_execution_log', []) + [log_entry]
    }


def art_director_node(state: CreativeWorkflowState) -> dict:
    """
    🎨 ART DIRECTOR AGENT NODE
    
    Responsibility: Generate promotional image based on approved copy
    Model: FLUX.1-schnell (via Together AI / Hugging Face)
    
    Input from state:
        - final_approved_text: Approved ad copy
        - user_prompt: Product description
    
    Output to state:
        - image_url: Generated image location/URL
    """
    iteration = state.get('current_iteration', 0) + 1
    
    print(f"\n{'─'*80}")
    print(f"🎨 [{iteration}.3] ART DIRECTOR AGENT - Visual Generation")
    print(f"{'─'*80}")
    
    product = state['user_prompt']
    approved_text = state.get('final_approved_text', state['draft_text'])
    
    # Craft a detailed image generation prompt
    image_prompt = (
        f"Professional product photography and marketing design. "
        f"Product: {product}. "
        f"Style: High-quality, clean background, vibrant colors, modern marketing aesthetic. "
        f"Resolution: 4K, studio lighting, professional product shot."
    )
    
    print(f"   🖼️  Generating promotional image...")
    print(f"   📝 Description: {product[:60]}...")
    
    try:
        image_url = generate_image_with_hf(image_prompt)
        status = "SUCCESS"
    except Exception as e:
        logger.error(f"Art director error: {e}")
        image_url = f"[Image generation unavailable: {str(e)[:40]}...]"
        status = "ERROR"
    
    log_entry = log_agent_action(state, "Art Director", "image_generation", image_url, status)
    
    print(f"   ✓ Image generation complete")
    print(f"   📍 Result: {image_url[:70]}...")
    
    return {
        "image_url": image_url,
        "current_iteration": iteration,
        "agent_execution_log": state.get('agent_execution_log', []) + [log_entry]
    }


# =============================================================================
# 4. CONDITIONAL ROUTING (The Decision Engine)
# =============================================================================

def router_function(state: CreativeWorkflowState) -> str:
    """
    🔀 ROUTING DECISION ENGINE
    
    This is the key to the autonomous "validate and refine" loop.
    It makes intelligent decisions about whether to:
    1. Loop back to Writer for revisions (if feedback indicates issues)
    2. Proceed to Art Director (if content is approved)
    3. Force exit (if max retries reached - safety mechanism)
    
    Decision Logic:
        if retries > MAX_RETRIES → Exit for safety
        elif latest_feedback contains "APPROVED" → Generate image
        else → Send back for revision
    """
    max_retries = 3
    latest_feedback = state.get('review_feedback', [''])[-1] if state.get('review_feedback') else ''
    current_retries = state.get('retries', 0)
    iteration = state.get('current_iteration', 0)
    
    print(f"\n{'─'*80}")
    print(f"🔀 [{iteration}.4] ROUTER - Decision Engine")
    print(f"{'─'*80}")
    print(f"   📊 Current state:")
    print(f"      • Iteration: {current_retries}")
    print(f"      • Latest feedback: {latest_feedback[:60]}...")
    print(f"      • Max retries: {max_retries}")
    
    # Safety check: prevent infinite loops
    if current_retries > max_retries:
        print(f"\n   ⚠️  MAX RETRIES REACHED ({max_retries})")
        print(f"   └─ Force proceeding to image generation for safety")
        return "generate_image"
    
    # Check if the latest feedback indicates approval
    if "APPROVED" in latest_feedback.upper():
        print(f"\n   ✅ CONTENT APPROVED")
        print(f"   └─ Routing to: Art Director Agent")
        return "generate_image"
    
    # Otherwise, send back for revisions
    else:
        print(f"\n   🔄 REVISIONS NEEDED")
        print(f"   └─ Looping back to: Writer Agent")
        return "revise_draft"


# =============================================================================
# 5. BUILD THE LANGGRAPH WORKFLOW
# =============================================================================

print("🏗️  Building LangGraph Workflow...\n")

# Create the state graph
workflow = StateGraph(CreativeWorkflowState)

# Add agent nodes
workflow.add_node("writer", writer_node)
workflow.add_node("reviewer", reviewer_node)
workflow.add_node("art_director", art_director_node)

# Set entry point
workflow.set_entry_point("writer")

# Add deterministic edges
workflow.add_edge("writer", "reviewer")        # Writer → Reviewer (always)
workflow.add_edge("art_director", END)         # Art Director → End (completes workflow)

# Add conditional edge (THE KEY TO THE VALIDATION LOOP)
workflow.add_conditional_edges(
    source="reviewer",
    path=router_function,
    path_map={
        "generate_image": "art_director",
        "revise_draft": "writer",
        "end": END
    }
)

# Compile the graph
app = workflow.compile()

print("✅ LangGraph workflow compiled successfully!")
print("   Nodes: [Writer] → [Reviewer] → [Router] → {[Art Director] OR loop}")
print("   Safety: Max 3 revision cycles with intelligent routing\n")
print("="*80 + "\n")


# =============================================================================
# 6. RUN THE WORKFLOW (Main Execution Function)
# =============================================================================

def run_campaign_generator(product_description: str) -> Optional[Dict[str, Any]]:
    """
    Execute the complete multi-agent creative campaign workflow.
    
    This function:
    1. Initializes the workflow state with the product description
    2. Streams execution through the agent graph
    3. Tracks all decisions and outputs
    4. Returns the final assets (copy + image)
    
    Args:
        product_description: Description of the product to create campaign for
    
    Returns:
        Dictionary containing final_approved_text, image_url, and metadata
    """
    
    print("\n" + "="*80)
    print("🚀 STARTING CREATIVE CAMPAIGN GENERATION")
    print("="*80)
    print(f"\n📦 INPUT PRODUCT: {product_description}\n")
    
    # Initialize the workflow state
    workflow_start = time.time()
    inputs = {
        "user_prompt": product_description,
        "draft_text": "",
        "review_feedback": [],
        "final_approved_text": None,
        "image_url": "",
        "retries": 0,
        "current_iteration": 0,
        "workflow_start_time": workflow_start,
        "agent_execution_log": [],
        "compliance_flags": [],
        "is_approved": False
    }
    
    # Execute the workflow
    final_state = None
    try:
        for event in app.stream(inputs, {"recursion_limit": 10}):
            final_state = event
    except Exception as e:
        print(f"\n❌ Workflow execution error: {e}")
        logger.error(f"Workflow error: {e}")
        return None
    
    # Extract results from final state
    if not final_state:
        print("\n❌ Workflow produced no output")
        return None
    
    # Get the output from the last node
    last_node_key = list(final_state.keys())[-1]
    result_state = final_state[last_node_key]
    
    workflow_duration = time.time() - workflow_start
    
    # =========================================================================
    # DISPLAY FINAL RESULTS
    # =========================================================================
    
    print("\n" + "="*80)
    print("✅ WORKFLOW COMPLETE")
    print("="*80)
    
    print(f"\n⏱️  Total execution time: {workflow_duration:.2f}s")
    print(f"🔄 Total iterations: {result_state.get('retries', 0)}")
    print(f"📋 Review cycles: {len(result_state.get('review_feedback', []))}")
    
    if result_state.get('compliance_flags'):
        print(f"⚠️  Compliance flags encountered:")
        for flag in result_state['compliance_flags']:
            print(f"   • {flag}")
    
    # Display the final approved copy
    approved_copy = result_state.get('final_approved_text') or result_state.get('draft_text', 'N/A')
    
    print("\n" + "="*80)
    print("📝 FINAL APPROVED COPY:")
    print("="*80)
    print(f"\n{approved_copy}\n")
    
    # Display the image URL
    image_url = result_state.get('image_url', 'N/A')
    print("="*80)
    print("🖼️  GENERATED IMAGE:")
    print("="*80)
    print(f"\n{image_url}\n")
    
    # Display review history
    if result_state.get('review_feedback'):
        print("="*80)
        print("📋 REVIEW HISTORY (Transparency & Audit Trail):")
        print("="*80)
        for i, feedback in enumerate(result_state.get('review_feedback', []), 1):
            status_icon = "✅" if "APPROVED" in feedback.upper() else "🔄"
            print(f"{i}. {status_icon} {feedback}")
        print()
    
    # Display execution log
    if result_state.get('agent_execution_log'):
        print("="*80)
        print("📊 AGENT EXECUTION LOG (Complete Transparency):")
        print("="*80)
        for log_entry in result_state['agent_execution_log']:
            status_icon = "✓" if log_entry['status'] == "SUCCESS" else "⚠"
            print(f"{status_icon} [{log_entry['timestamp']}] "
                  f"{log_entry['agent']}: {log_entry['action']} "
                  f"({log_entry['status']})")
        print()
    
    print("="*80 + "\n")
    
    return {
        "final_approved_text": approved_copy,
        "image_url": image_url,
        "retries": result_state.get('retries', 0),
        "review_feedback": result_state.get('review_feedback', []),
        "compliance_flags": result_state.get('compliance_flags', []),
        "execution_time": workflow_duration,
        "agent_log": result_state.get('agent_execution_log', []),
        "is_approved": result_state.get('is_approved', False)
    }


# =============================================================================
# 7. ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    import sys
    
    # Get product description from CLI args or interactive input
    if len(sys.argv) > 1:
        product = " ".join(sys.argv[1:])
    else:
        try:
            product = input("📦 Enter your product idea or creative prompt: ").strip()
        except EOFError:
            product = None
    
    # Use default if no input provided
    if not product:
        product = "Eco-friendly water bottle made with sustainable bamboo, keeps drinks cold for 24 hours"
        print(f"ℹ️  Using example product: {product}\n")
    
    # Run the campaign generator
    result = run_campaign_generator(product)
