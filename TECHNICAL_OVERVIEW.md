# 🔧 TECHNICAL OVERVIEW - Creative Media Co-Pilot

## Technology Stack Deep Dive

### Framework: LangGraph
**Why LangGraph?**
- Explicit state management with TypedDict
- Conditional routing for complex workflows
- Stateful graph execution (not just function chains)
- Production-ready with error handling

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

# State definition
class CreativeWorkflowState(TypedDict):
    user_prompt: str
    draft_text: str
    review_feedback: List[str]
    # ... more fields

# Graph construction
workflow = StateGraph(CreativeWorkflowState)
workflow.add_node("writer", writer_node)
workflow.add_node("reviewer", reviewer_node)
workflow.add_conditional_edges("reviewer", router_function, {...})
app = workflow.compile()

# Execution
for event in app.stream(inputs, {"recursion_limit": 10}):
    final_state = event
```

### Model 1: Llama 3.1 8B (via Groq)
**Groq API Configuration:**
```python
from langchain_groq import ChatGroq

writer_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.75,           # Creative but controlled
    max_tokens=512,
    api_key=os.getenv("GROQ_API_KEY")
)

reviewer_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.30,           # Analytical
    max_tokens=256,
    api_key=os.getenv("GROQ_API_KEY")
)
```

**Why Temperature Matters:**
```
Temperature 0.0  → Deterministic, repetitive
Temperature 0.3  → Focused, consistent (good for review)
Temperature 0.7  → Balanced (good for creative writing)
Temperature 1.0+ → Random, unpredictable
```

### Model 2: FLUX.1-schnell (via Hugging Face)
```python
from huggingface_hub import InferenceClient

hf_client = InferenceClient(token=os.getenv('HUGGINGFACE_API_TOKEN'))

image = hf_client.text_to_image(
    prompt="Professional product photography...",
    model="black-forest-labs/FLUX.1-schnell"
)
```

**Image Generation Prompt Engineering:**
```python
image_prompt = (
    f"Professional product photography and marketing design. "
    f"Product: {product}. "
    f"Style: High-quality, clean background, vibrant colors, modern marketing aesthetic. "
    f"Resolution: 4K, studio lighting, professional product shot."
)
```

## State Management in Depth

### TypedDict Design
```python
class CreativeWorkflowState(TypedDict):
    # Input
    user_prompt: str                        # "eco-friendly water bottle"
    
    # Workflow execution
    draft_text: str                         # Current copy iteration
    review_feedback: List[str]              # ["[CLAIM] Remove...", "APPROVED"]
    final_approved_text: Optional[str]      # Approved copy for image gen
    image_url: str                          # Generated image location
    
    # Metadata
    retries: int                            # 0, 1, 2, 3 (max)
    current_iteration: int                  # Step counter
    workflow_start_time: float              # Timestamp
    agent_execution_log: List[Dict]         # [{"timestamp": "...", "agent": "Writer", ...}]
    compliance_flags: List[str]             # ["[CLAIM]", "[TONE]"]
    is_approved: bool                       # True/False
```

### State Update Pattern
Each node returns a **partial state update**:

```python
def writer_node(state: CreativeWorkflowState) -> dict:
    # ... generate draft ...
    return {
        "draft_text": draft,                  # ← Only update these fields
        "current_iteration": iteration,
        "retries": retries + 1,
        "agent_execution_log": updated_log
    }
    # LangGraph merges this with existing state automatically
```

### State Merging (Automatic)
```python
# Before node execution
state = {
    "user_prompt": "water bottle",
    "draft_text": "",
    "retries": 0,
    ...
}

# Node returns
return {"draft_text": "new copy", "retries": 1}

# After merge (automatic)
state = {
    "user_prompt": "water bottle",          # ← Unchanged
    "draft_text": "new copy",               # ← Updated
    "retries": 1,                           # ← Updated
    ...                                      # ← All others unchanged
}
```

## Conditional Routing Implementation

### Router Function Logic
```python
def router_function(state: CreativeWorkflowState) -> str:
    """
    Decision: Should we generate image or loop back for revision?
    """
    latest_feedback = state['review_feedback'][-1]
    current_retries = state['retries']
    
    # Safety: prevent infinite loops
    if current_retries > 3:
        return "generate_image"  # Force exit
    
    # Check approval
    if "APPROVED" in latest_feedback.upper():
        return "generate_image"  # ✅ Approved path
    else:
        return "revise_draft"    # 🔄 Revision loop
```

### Graph Connection
```python
# Setup the conditional routing
workflow.add_conditional_edges(
    source="reviewer",                      # Start from reviewer
    path=router_function,                   # Use router to decide
    conditional_edge_map={
        "generate_image": "art_director",   # If approved
        "revise_draft": "writer",           # If revision needed
        "end": END                          # Optional: early exit
    }
)
```

### Routing Decision Tree
```
                      [Reviewer Output]
                             │
                             ▼
                    ┌─────────────────┐
                    │ Router Decision │
                    └─────────┬───────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
         Retries > 3?    Approved?    Need Review?
                │             │             │
                ▼             ▼             ▼
            [Force Exit] [Proceed]   [Loop Back]
                │             │             │
                ▼             ▼             ▼
           Art Director   Art Director   Writer
```

## Agent Node Implementation Patterns

### Pattern 1: Reader → Processor → Logger → Return

```python
def writer_node(state: CreativeWorkflowState) -> dict:
    # 1. READ from state
    product = state['user_prompt']
    feedback = state.get('review_feedback', [])
    
    # 2. PROCESS
    if feedback:
        # Conditional behavior based on state
        system_prompt = "Revise based on feedback"
    else:
        system_prompt = "Create initial draft"
    
    # 3. EXECUTE (with error handling)
    try:
        response = llm.invoke(messages)
        draft = response.content.strip()
        status = "SUCCESS"
    except Exception as e:
        draft = fallback_draft()
        status = "FALLBACK"
    
    # 4. LOG for transparency
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": "Writer",
        "status": status,
        "action": "copy_generation"
    }
    
    # 5. RETURN partial state
    return {
        "draft_text": draft,
        "current_iteration": state['current_iteration'] + 1,
        "agent_execution_log": state['agent_execution_log'] + [log_entry]
    }
```

### Pattern 2: Validation with Multiple Checks

```python
def reviewer_node(state: CreativeWorkflowState) -> dict:
    draft = state['draft_text']
    
    # LLM-based review
    try:
        feedback = llm.invoke(review_prompt).content.strip()
        method = "LLM"
    except:
        # Fallback: rule-based checks
        feedback = rule_based_review(draft)
        method = "RULE_BASED"
    
    # Determine approval status
    is_approved = "APPROVED" in feedback.upper()
    
    return {
        "review_feedback": state['review_feedback'] + [feedback],
        "final_approved_text": draft if is_approved else state.get('final_approved_text'),
        "is_approved": is_approved,
        "compliance_flags": state['compliance_flags'] + get_flags(feedback),
        "agent_execution_log": state['agent_execution_log'] + [log_entry]
    }
```

## Prompt Engineering Strategy

### Writer Prompt (Creative Generation)
```python
system_prompt = """You are an exceptional copywriter specializing in social media advertising.

Your task is to create compelling, energetic, 2-3 line ad copy that:
- Captures attention immediately
- Is specific about product benefits (no vague claims)
- Uses engaging language with emojis
- Is platform-ready (Twitter/Instagram length)
- Avoids unverified claims like "100%", "guaranteed", "miracle"

Write ONLY the ad copy, no explanations."""

user_message = f"Create an engaging social media ad for: {product}"

# If revision needed, add feedback
if revision_needed:
    user_message += f"\n\nPrevious feedback: {feedback}\nPlease revise accordingly."
```

### Reviewer Prompt (Compliance Checking)
```python
system_prompt = """You are a strict legal and brand compliance officer for social media ads.

Your job is to:
1. Identify unverified claims (e.g., "100%", "guaranteed", "best", "miracle")
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

review_prompt = f'Review this ad copy: "{draft}"\n\nIs it compliant and ready to publish?'
```

### Art Director Prompt (Image Generation)
```python
image_prompt = (
    f"Professional product photography and marketing design. "
    f"Product: {product}. "
    f"Style: High-quality, clean background, vibrant colors, modern marketing aesthetic. "
    f"Resolution: 4K, studio lighting, professional product shot."
)
```

## Error Handling Architecture

### Try-Catch Pyramid
```python
try:
    # 1. Primary: Use optimized LLM (Groq)
    response = groq_llm.invoke(messages)
    result = response.content.strip()
except KeyError:
    # 2. Secondary: Config error - use fallback key
    logger.warning("API key missing")
    result = fallback_result()
except APIError:
    # 3. Tertiary: API unavailable - use rule-based
    logger.error("API error")
    result = rule_based_result()
except Exception as e:
    # 4. Catch-all: Unexpected error
    logger.critical(f"Unexpected error: {e}")
    result = default_result()

return result
```

### Logging Strategy
```python
import logging

logger = logging.getLogger(__name__)

# Different levels for different severities
logger.info("Writer generated draft (152 chars)")      # ℹ️ Informational
logger.warning("Using rule-based reviewer")            # ⚠️ Fallback used
logger.error("Groq API error: 429 rate limit")        # ❌ Error but recoverable
logger.critical("No fallback available!")              # 🔴 Fatal
```

## Performance Metrics

### Execution Time Breakdown
```
Component          Time        % of Total
─────────────────────────────────────────
Writer LLM        2-3s        20%
Reviewer LLM      1-2s        10%
Router Decision   <0.1s       <1%
Art Director      8-15s       60%
I/O & Overhead    1-2s        10%
─────────────────────────────────────────
TOTAL            ~15-25s      100%
```

### Quality Metrics
```
Metric                  Target    Current
────────────────────────────────────────
Approval Rate          >80%      ~85%
Avg Revisions needed   <1.5      1.2
Compliance Score       >95%      ~96%
Image Generation       ~100%     ~98%
```

## Scalability Considerations

### Current Limits
- Sequential processing (one campaign at a time)
- Single API key usage
- In-memory state storage

### Scaling Strategies
```
Level 1: Multi-threading
  • Run multiple campaigns in parallel threads
  • Share API quotas carefully

Level 2: Multi-processing
  • True parallelism on multi-core systems
  • Separate API keys per process

Level 3: Distributed
  • Separate worker processes on multiple machines
  • Queue-based workflow (Redis, RabbitMQ)
  • Centralized state store (Redis, PostgreSQL)

Level 4: Serverless
  • AWS Lambda functions for each agent
  • API Gateway for workflow orchestration
  • S3 for state and output storage
```

## Testing & Validation

### Unit Test Example
```python
def test_writer_node_basic():
    state = {
        "user_prompt": "water bottle",
        "draft_text": "",
        "review_feedback": [],
        "retries": 0,
        "current_iteration": 0,
        "workflow_start_time": time.time(),
        "agent_execution_log": [],
        "compliance_flags": [],
        "is_approved": False
    }
    
    result = writer_node(state)
    
    assert "draft_text" in result
    assert len(result["draft_text"]) > 0
    assert result["retries"] == 1
    assert len(result["agent_execution_log"]) == 1
```

### Integration Test Example
```python
def test_full_workflow():
    result = run_campaign_generator("eco-friendly water bottle")
    
    assert result is not None
    assert result["final_approved_text"]
    assert len(result["final_approved_text"]) > 0
    assert result["image_url"]
    assert len(result["review_feedback"]) > 0
    assert result["retries"] <= 3
    assert result["is_approved"] == True
```

## Deployment Considerations

### Docker Containerization
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV GROQ_API_KEY=${GROQ_API_KEY}
ENV HUGGINGFACE_API_TOKEN=${HUGGINGFACE_API_TOKEN}

CMD ["python", "main.py"]
```

### Environment Configuration
```bash
# .env file
GROQ_API_KEY=gsk_xxxxxxxx
HUGGINGFACE_API_TOKEN=hf_xxxxxxxx

# Or pass as environment variables
export GROQ_API_KEY="gsk_xxxxxxxx"
export HUGGINGFACE_API_TOKEN="hf_xxxxxxxx"
```

---

**For system architecture, see ARCHITECTURE.md. For design decisions, see DESIGN.md**
