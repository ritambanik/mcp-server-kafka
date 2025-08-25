from __main__ import mcp

@mcp.prompt(
    name="analyze",
    description="Analyze data or text content"
    )
async def analyze_prompt(content: str, focus: str = "general analysis", depth: str = "detailed") -> str:
    """Generate a content analysis prompt"""
    
    depth_instructions = {
        "surface": "Provide a high-level overview with main observations",
        "detailed": "Conduct a thorough analysis with specific examples and insights",
        "comprehensive": "Perform an in-depth analysis covering multiple dimensions and implications"
    }
    
    focus_examples = {
        "trends": "Look for patterns, changes over time, and emerging trends",
        "patterns": "Identify recurring themes, structures, and relationships",
        "sentiment": "Analyze emotional tone, attitudes, and opinions expressed",
        "structure": "Examine organization, flow, and logical arrangement",
        "general analysis": "Provide a well-rounded analysis covering key aspects"
    }
    
    depth_guide = depth_instructions.get(depth, depth_instructions["detailed"])
    focus_guide = focus_examples.get(focus, focus_examples["general analysis"])
    
    prompt_text = f"""Please analyze the following content with a focus on {focus}:

CONTENT TO ANALYZE:
{content}

ANALYSIS PARAMETERS:
- Focus Area: {focus}
- Analysis Depth: {depth}
- Specific Instructions: {focus_guide}
- Detail Level: {depth_guide}

ANALYSIS FRAMEWORK:
1. Key Observations: What stands out most prominently?
2. Detailed Findings: Specific insights related to your focus area
3. Patterns & Relationships: Connections and recurring elements
4. Implications: What do these findings suggest or mean?
5. Recommendations: Actionable insights or next steps (if applicable)

Please provide your analysis following this framework:"""

    return prompt_text