"""
Example configurations for different types of campaigns.
Modify these to test various scenarios with the Agentic Media Co-Pilot.
"""

# Example 1: Eco-Friendly Product
EXAMPLE_ECO_PRODUCT = {
    "description": "New eco-friendly water bottle, made from bamboo",
    "expected_tone": "Energetic, environmentally conscious",
    "target_platform": "Instagram, Facebook"
}

# Example 2: Tech Product
EXAMPLE_TECH_PRODUCT = {
    "description": "AI-powered smart watch with 24/7 health monitoring, sleep tracking, and fitness coaching",
    "expected_tone": "Modern, innovative, trustworthy",
    "target_platform": "LinkedIn, Twitter"
}

# Example 3: Food & Beverage
EXAMPLE_FOOD_PRODUCT = {
    "description": "Organic cold-pressed juice blend with superfood ingredients, no added sugar",
    "expected_tone": "Fresh, healthy, vibrant",
    "target_platform": "Instagram, TikTok"
}

# Example 4: Fashion
EXAMPLE_FASHION_PRODUCT = {
    "description": "Handcrafted leather backpack with laptop compartment, designed for urban professionals",
    "expected_tone": "Sophisticated, practical, stylish",
    "target_platform": "Pinterest, Instagram"
}

# Example 5: Service/App
EXAMPLE_SERVICE = {
    "description": "Meditation app with personalized mindfulness exercises and sleep stories",
    "expected_tone": "Calm, supportive, inviting",
    "target_platform": "Facebook, Reddit"
}

# Example 6: Home & Living
EXAMPLE_HOME_PRODUCT = {
    "description": "Smart home security camera with AI motion detection and night vision",
    "expected_tone": "Secure, reliable, cutting-edge",
    "target_platform": "Facebook, YouTube"
}

# Example 7: Beauty & Personal Care
EXAMPLE_BEAUTY_PRODUCT = {
    "description": "Natural skincare serum with vitamin C and hyaluronic acid, cruelty-free",
    "expected_tone": "Luxurious, clean, effective",
    "target_platform": "Instagram, TikTok"
}

# Example 8: Fitness
EXAMPLE_FITNESS_PRODUCT = {
    "description": "Adjustable resistance bands set with workout guide, perfect for home gym",
    "expected_tone": "Motivating, empowering, accessible",
    "target_platform": "YouTube, Instagram"
}

# Example 9: Education
EXAMPLE_EDUCATION_SERVICE = {
    "description": "Online coding bootcamp for beginners, learn Python in 8 weeks with mentorship",
    "expected_tone": "Encouraging, professional, growth-focused",
    "target_platform": "LinkedIn, Twitter"
}

# Example 10: Pet Products
EXAMPLE_PET_PRODUCT = {
    "description": "Automatic pet feeder with portion control and scheduling via smartphone app",
    "expected_tone": "Caring, convenient, modern",
    "target_platform": "Facebook, Instagram"
}


# Collection of all examples for easy iteration
ALL_EXAMPLES = [
    ("Eco-Friendly Product", EXAMPLE_ECO_PRODUCT),
    ("Tech Product", EXAMPLE_TECH_PRODUCT),
    ("Food & Beverage", EXAMPLE_FOOD_PRODUCT),
    ("Fashion", EXAMPLE_FASHION_PRODUCT),
    ("Service/App", EXAMPLE_SERVICE),
    ("Home & Living", EXAMPLE_HOME_PRODUCT),
    ("Beauty & Personal Care", EXAMPLE_BEAUTY_PRODUCT),
    ("Fitness", EXAMPLE_FITNESS_PRODUCT),
    ("Education", EXAMPLE_EDUCATION_SERVICE),
    ("Pet Products", EXAMPLE_PET_PRODUCT),
]


def run_all_examples():
    """
    Run the campaign generator for all example products.
    Useful for testing the system comprehensively.
    """
    from main import run_campaign_generator
    
    results = []
    
    print("\n" + "="*80)
    print("🚀 RUNNING ALL EXAMPLE CAMPAIGNS")
    print("="*80 + "\n")
    
    for i, (category, example) in enumerate(ALL_EXAMPLES, 1):
        print(f"\n{'='*80}")
        print(f"📦 Example {i}/{len(ALL_EXAMPLES)}: {category}")
        print(f"{'='*80}\n")
        
        result = run_campaign_generator(example["description"])
        
        if result:
            results.append({
                "category": category,
                "result": result,
                "metadata": example
            })
        
        print(f"\n✅ Completed {i}/{len(ALL_EXAMPLES)}")
        
        # Add a small delay to avoid rate limiting
        import time
        if i < len(ALL_EXAMPLES):
            print("⏳ Waiting 5 seconds before next campaign...")
            time.sleep(5)
    
    print("\n" + "="*80)
    print("🎉 ALL CAMPAIGNS COMPLETED")
    print("="*80)
    print(f"\n📊 Successfully generated: {len(results)}/{len(ALL_EXAMPLES)} campaigns\n")
    
    return results


def run_single_example(example_name: str):
    """
    Run a specific example by name.
    
    Args:
        example_name: Name of the example (e.g., "Tech Product")
    """
    from main import run_campaign_generator
    
    # Find the example
    example_data = None
    for name, data in ALL_EXAMPLES:
        if name.lower() == example_name.lower():
            example_data = data
            break
    
    if not example_data:
        print(f"❌ Example '{example_name}' not found!")
        print("\nAvailable examples:")
        for name, _ in ALL_EXAMPLES:
            print(f"  • {name}")
        return None
    
    print(f"\n🎯 Running example: {example_name}")
    result = run_campaign_generator(example_data["description"])
    
    return result


if __name__ == "__main__":
    """
    Run examples from command line
    """
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "all":
            run_all_examples()
        elif sys.argv[1] == "list":
            print("\n📋 Available Examples:\n")
            for i, (name, data) in enumerate(ALL_EXAMPLES, 1):
                print(f"{i}. {name}")
                print(f"   Description: {data['description']}")
                print(f"   Tone: {data['expected_tone']}\n")
        else:
            # Try to run a specific example
            run_single_example(sys.argv[1])
    else:
        print("\n📖 Usage:")
        print("  python examples.py all              - Run all examples")
        print("  python examples.py list             - List all examples")
        print("  python examples.py 'Tech Product'   - Run specific example")
        print("\n💡 Or import in your code:")
        print("  from examples import EXAMPLE_TECH_PRODUCT")
        print("  run_campaign_generator(EXAMPLE_TECH_PRODUCT['description'])")
