# 🚀 SETUP GUIDE - Creative Media Co-Pilot

Complete step-by-step guide to get the Agentic AI system running locally.

## Prerequisites

- **Python 3.8+** (3.10+ recommended)
- **Git**
- **Free API Keys** (instructions below)
- **~500MB** free disk space

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/agentic-media-pilot.git
cd agentic-media-pilot
```

Or if you have the files locally:

```bash
cd path/to/agentic-media-pilot
```

## Step 2: Create Virtual Environment

### Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Windows (Command Prompt)
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

**Verify activation**: You should see `(venv)` in your terminal prompt.

## Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- `langgraph` - Agent orchestration
- `langchain` - LLM abstractions
- `langchain-groq` - Groq API integration
- `huggingface-hub` - Image generation
- `python-dotenv` - Environment variables
- `Pillow` - Image processing

**Expected time**: 2-3 minutes
**Expected download**: ~200MB

## Step 4: Get API Keys

### 4.1 Groq API Key (for Writer & Reviewer Agents)

1. Visit: https://console.groq.com/keys
2. Sign up (free account, just need email)
3. Create new API key
4. Copy the key (starts with `gsk_`)
5. Save it for the next step

**Why Groq?**
- ⚡ Ultra-fast inference (1-2 seconds vs 5-10 seconds with other providers)
- 💰 Free tier with generous limits
- 🔥 Perfect for real-time feedback loops

### 4.2 Hugging Face API Token (for Image Generation)

1. Visit: https://huggingface.co/settings/tokens
2. Sign up (free account, can use GitHub/Google login)
3. Click "New token"
4. Select "Fine-grained" permissions
5. Click "Create token"
6. Copy the token (starts with `hf_`)
7. Save it for the next step

**Why Hugging Face?**
- 🖼️ Access to FLUX.1-schnell (latest image model)
- 💰 Free tier with inference API
- 📂 Largest open-source model collection

## Step 5: Configure Environment

### Create .env file

**Option A: Manual (Recommended)**

1. In the project directory, create a file named `.env`
2. Copy contents from `.env.example`:
   ```
   GROQ_API_KEY=gsk_your_key_here
   HUGGINGFACE_API_TOKEN=hf_your_token_here
   ```
3. Replace `your_key_here` and `your_token_here` with actual keys
4. Save the file

**Option B: Command Line**

Windows (PowerShell):
```powershell
@"
GROQ_API_KEY=gsk_your_key_here
HUGGINGFACE_API_TOKEN=hf_your_token_here
"@ | Out-File .env -Encoding UTF8
```

macOS/Linux:
```bash
cat > .env << EOF
GROQ_API_KEY=gsk_your_key_here
HUGGINGFACE_API_TOKEN=hf_your_token_here
EOF
```

### Verify Configuration

```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(f'Groq: {'✓' if os.getenv('GROQ_API_KEY') else '✗'}'); print(f'HF Token: {'✓' if os.getenv('HUGGINGFACE_API_TOKEN') else '✗'}')"
```

## Step 6: Test Installation

### Quick Test
```bash
python -c "import langgraph; print('✓ LangGraph installed'); import langchain; print('✓ LangChain installed')"
```

### Run Setup Check
```bash
python utils.py check
```

You should see:
```
🔍 Running Setup Validation...

✅ Python Version: 3.10.x
✅ .env file found
✅ All API keys are configured
✅ All required packages installed

✨ Setup validation complete! Ready to run.
```

## Step 7: Run Your First Campaign

### Interactive Mode
```bash
python main.py
```

Enter a product description when prompted:
```
📦 Enter your product idea or creative prompt: eco-friendly water bottle made with bamboo
```

### Command Line Mode
```bash
python main.py "eco-friendly water bottle made with bamboo"
```

### Expected Output
```
================================================================================
🚀 STARTING CREATIVE CAMPAIGN GENERATION
================================================================================

📦 INPUT PRODUCT: eco-friendly water bottle made with bamboo

────────────────────────────────────────────────────────────────────────────────
📝 [1.1] WRITER AGENT - Draft Generation (Attempt #1)
────────────────────────────────────────────────────────────────────────────────
   ℹ️  Incorporating reviewer feedback for refinement...
   ✓ Draft generated (152 chars)
   📄 Preview: Discover our eco-friendly water bottle, made with sustainable...

...

================================================================================
✅ WORKFLOW COMPLETE
================================================================================

⏱️  Total execution time: 28.3s
🔄 Total iterations: 2
📋 Review cycles: 2

================================================================================
📝 FINAL APPROVED COPY:
================================================================================

Discover our eco-friendly water bottle, made with sustainable bamboo. 
Keeps drinks cold for 24 hours. 💚

================================================================================
🖼️  GENERATED IMAGE:
================================================================================

Generated: campaign_output_1234567890.png

================================================================================
```

## Step 8: Run Demo

See the system in action with multiple campaigns:

```bash
python demo.py
```

### Other Demo Commands

```bash
# Show system architecture
python demo.py architecture

# Show agent specialization
python demo.py specialization

# Show state evolution
python demo.py state

# Show validation loop
python demo.py loop

# Run custom campaign
python demo.py custom "your product description"
```

## Step 9: Explore Examples

```bash
# List all example products
python examples.py list

# Run specific example
python examples.py "Tech Product"

# Run all examples
python examples.py all
```

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'langgraph'"

**Solution**: Install requirements again
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Problem: "GROQ_API_KEY not found"

**Solution**: 
1. Check .env file exists in project root
2. Verify key format (should start with `gsk_`)
3. Try: `python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('GROQ_API_KEY'))"`

### Problem: "API error: 429 Rate Limited"

**Solution**: 
- Groq free tier has rate limits
- Wait a few seconds before running again
- System has fallback mechanisms

### Problem: "HF Token not recognized"

**Solution**:
1. Verify token in `.env` (should start with `hf_`)
2. Token must have "Inference API" permissions
3. Recreate token at https://huggingface.co/settings/tokens

### Problem: "Connection timeout"

**Solution**:
- Check internet connection
- Verify API endpoints are accessible
- Try again (usually resolves)

### Problem: "Image generation failed"

**Solution**:
- Check HUGGINGFACE_API_TOKEN is set
- Verify you have a Hugging Face account
- System will use fallback image URL

## Next Steps

### 1. **Run Your First Campaign**
```bash
python main.py "describe your product here"
```

### 2. **Customize the System**
- Edit system prompts in `main.py`
- Adjust agent temperatures for different behavior
- Add new agents (see DESIGN.md)

### 3. **Integrate with Your Workflow**
- Import functions from `main.py`
- Build a web interface (Flask, FastAPI)
- Create a scheduling system

### 4. **Deploy**
- Dockerize the application
- Deploy to cloud (AWS Lambda, Heroku, etc.)
- Create a REST API

### 5. **Contribute**
- Improve agents
- Add new features
- Help with documentation
- See CONTRIBUTING.md

## Advanced Configuration

### Custom Model Configuration

Edit `main.py` to use different models:

```python
# Use different Groq model
writer_llm = ChatGroq(
    model="mixtral-8x7b-32768",  # Try this model
    temperature=0.75,
)
```

### Adjust Agent Behavior

**More Creative**: Increase temperature
```python
temperature=0.9  # Very creative, more random
```

**More Consistent**: Decrease temperature
```python
temperature=0.3  # Very consistent, deterministic
```

### Change Max Retries

Edit `router_function` in `main.py`:

```python
MAX_RETRIES = 5  # Instead of 3 (allow more iterations)
```

## Performance Optimization

### Run Multiple Campaigns

```python
from main import run_campaign_generator
import concurrent.futures

products = [
    "water bottle",
    "t-shirt",
    "coffee mug"
]

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(run_campaign_generator, products))
```

### Monitor Performance

```bash
# Time a single campaign
time python main.py "test product"

# Profile the code
python -m cProfile -s cumtime main.py "test product"
```

## Documentation

- **ARCHITECTURE.md** - System design and structure
- **DESIGN.md** - Problem solving and design decisions
- **TECHNICAL_OVERVIEW.md** - Implementation details
- **PRESENTATION.md** - Presentation outline

## Support

- 📖 Read the documentation
- 🐛 Check GitHub issues
- 💬 Start a discussion
- 📧 Email support (if available)

## Quick Reference

```bash
# Activate environment
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# Run main application
python main.py

# Run demos
python demo.py

# View examples
python examples.py list

# Check setup
python utils.py check

# Create .env interactively
python utils.py create-env

# Deactivate environment
deactivate
```

---

**Ready to get started? Run `python main.py` now!** 🚀
