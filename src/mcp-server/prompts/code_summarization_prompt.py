from __main__ import mcp

@mcp.prompt(
    name="summarize",
    description="Create a summary of provided text"
   )
async def summarize_prompt(text: str, length: str = "medium", style: str = "paragraph") -> str:
    """Generate a text summarization prompt"""
    
    length_instructions = {
        "short": "Keep the summary to 1-2 sentences maximum",
        "medium": "Provide a concise summary in 2-4 sentences",
        "long": "Create a detailed summary in 1-2 paragraphs"
    }
    
    style_instructions = {
        "bullet-points": "Format the summary as clear bullet points",
        "paragraph": "Write the summary as flowing paragraphs",
        "executive": "Structure as an executive summary with key takeaways"
    }
    
    length_guide = length_instructions.get(length, length_instructions["medium"])
    style_guide = style_instructions.get(style, style_instructions["paragraph"])
    
    prompt_text = f"""Please create a {length} summary of the following text using {style} format:

TEXT TO SUMMARIZE:
{text}

SUMMARY REQUIREMENTS:
- {length_guide}
- {style_guide}
- Focus on the most important information
- Maintain the original meaning and context
- Use clear, accessible language

Please provide your summary now:"""

    return prompt_text