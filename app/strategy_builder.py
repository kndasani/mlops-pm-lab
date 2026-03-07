"""
Strategy Builder Module

Enables users to build personalized AI strategies for their unique contexts.
Supports personal goals, professional development, organizational initiatives,
and creative endeavors.
"""

import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime, timedelta

load_dotenv()

# ============================================================================
# CONTEXT ANALYSIS & STRATEGY GENERATION
# ============================================================================

CONTEXT_ANALYZER_TEMPLATE = """
Analyze the following user context and extract detailed, accurate information to build a personalized AI strategy.
Be VERY specific about their role, industry, and goals - do NOT make generic assumptions.

User Context: {context}

Please respond with a JSON object containing:
{{
    "context_type": "personal|freelancer|small_business|enterprise|educator|creative",
    "primary_goal": "precise statement of what they specifically want to achieve",
    "inferred_role": "their exact role or business (e.g., 'Bookstore Owner', 'Private Math Tutor', 'Social Media Freelancer')",
    "industry_or_field": "their specific industry/field",
    "key_challenges": ["list", "of", "specific", "obstacles", "they", "face"],
    "potential_ai_applications": ["list", "of", "specific", "relevant", "ai", "use", "cases"],
    "maturity_estimate": "no_experience|beginner|intermediate|advanced",
    "follow_up_questions": [
        "question to clarify their expectations",
        "question about their AI knowledge/comfort level",
        "question about their constraints or concerns"
    ]
}}

Be VERY specific. If they mention being a bookstore owner wanting to increase sales, YOUR inferred_role should be "Bookstore Owner", 
NOT "AI Enthusiast" or generic "Professional". Focus on their ACTUAL stated context, not assumptions."""


ROADMAP_GENERATOR_TEMPLATE = """
Create a highly personalized, practical AI adoption roadmap for this person based on their specific situation and conversation.

User Role: {context_type}
Their Specific Goal: {primary_goal}
What They Told Us: {resources}

---

Generate a JSON roadmap with 3-4 concrete phases tailored to their exact context. Each phase should be:
1. Practical and achievable given their situation (not generic corporate speak)
2. Build on the previous phase
3. Include SPECIFIC AI tools/approaches relevant to their industry/role
4. Have clear success criteria they can actually measure
5. Realistic timeline based on their stated situation

For example, if they're a bookstore owner with limited tech knowledge, suggest:
- Phase 1: Explore specific AI tools that help with book recommendations
- Not: "Conduct organizational assessment and AI readiness evaluation"

Format:
{{
    "strategy_summary": "2-3 sentences tailored to their specific context and goals",
    "phases": [
        {{
            "phase_number": 1,
            "name": "Phase name specific to their context",
            "duration": "realistic timeframe",
            "goal": "specific, measurable goal for this phase",
            "key_activities": ["activity 1", "activity 2", "activity 3"],
            "tools_or_approaches": ["specific tool names or approaches"],
            "success_criteria": "How they'll know this worked in their context",
            "resources_needed": "What's realistically needed"
        }}
    ],
    "success_metrics": ["Their stated success metrics"],
    "quick_wins": ["achievable", "wins", "in", "first", "2-4", "weeks"],
    "risks_and_mitigation": [
        {{"risk": "described in their context", "mitigation": "practical solution for them"}}
    ]
}}

Make it personal, specific, and practical. Avoid corporate jargon."""


def analyze_context(user_context: str) -> dict:
    """
    Analyze user's context description to extract key strategic information.
    Returns dictionary with context type, goals, challenges, and opportunities.
    """
    prompt_template = ChatPromptTemplate.from_template(CONTEXT_ANALYZER_TEMPLATE)
    prompt = prompt_template.format(context=user_context)
    
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
    )
    
    response = model.invoke(prompt)
    
    # Parse JSON response
    try:
        analysis = json.loads(response.content)
    except json.JSONDecodeError:
        # Fallback if response isn't valid JSON
        analysis = {
            "context_type": "professional",
            "primary_goal": user_context[:100],
            "inferred_role": "AI Enthusiast",
            "key_challenges": ["Getting Started"],
            "potential_ai_applications": ["General AI Exploration"],
            "maturity_estimate": "beginner"
        }
    
    return analysis


def generate_roadmap(
    context_type: str,
    primary_goal: str,
    conversation_context: str = "",
) -> dict:
    """
    Generate a personalized AI strategy roadmap based on user's situation.
    Returns a dictionary with phases, success criteria, and recommended approaches.
    """
    prompt_template = ChatPromptTemplate.from_template(ROADMAP_GENERATOR_TEMPLATE)
    prompt = prompt_template.format(
        context_type=context_type,
        primary_goal=primary_goal,
        resources=conversation_context
    )
    
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
    )
    
    response = model.invoke(prompt)
    
    # Parse JSON response with better error handling
    roadmap = None
    try:
        # Try to extract JSON from response
        response_text = response.content
        
        # Try to find JSON object in the response
        import re
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            roadmap = json.loads(json_str)
            
            # Validate that we have phases
            if 'phases' in roadmap and len(roadmap.get('phases', [])) > 0:
                print(f"✓ Generated {len(roadmap['phases'])} phases")
                return roadmap
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
    except Exception as e:
        print(f"Error parsing roadmap: {e}")
    
    # If JSON parsing failed or no phases, create a multi-phase fallback
    print("⚠ Using fallback roadmap with 3 phases")
    roadmap = {
        "strategy_summary": f"Your personalized AI journey for {primary_goal}. Start with foundations, then apply to your specific context.",
        "phases": [
            {
                "phase_number": 1,
                "name": "Foundation & Assessment",
                "duration": "2-3 weeks",
                "goal": "Understand AI basics and assess your specific needs",
                "key_activities": ["Research relevant AI tools for your context", "Identify your top 3 AI use cases", "Learn from practical examples"],
                "tools_or_approaches": ["ChatGPT for exploration", "Industry-specific AI tools", "Online resources and tutorials"],
                "success_criteria": "Can clearly explain how AI applies to your specific situation",
                "resources_needed": "5-10 hours of learning time, free tools available"
            },
            {
                "phase_number": 2,
                "name": "First Implementation",
                "duration": "3-4 weeks",
                "goal": "Try AI on your highest-priority use case",
                "key_activities": ["Set up your chosen AI tool", "Run 2-3 small experiments", "Document what works and what doesn't"],
                "tools_or_approaches": ["Your chosen AI platform", "Small-scale pilots", "Team feedback collection"],
                "success_criteria": "Successfully completed 1-2 small AI tasks with measurable results",
                "resources_needed": "Weekly time commitment, potential tool subscription"
            },
            {
                "phase_number": 3,
                "name": "Scale & Optimize",
                "duration": "4-6 weeks",
                "goal": "Expand to additional use cases and optimize processes",
                "key_activities": ["Apply learnings to secondary use cases", "Develop workflows and guidelines", "Train yourself or your team"],
                "tools_or_approaches": ["Proven AI tools", "Standard workflows", "Knowledge documentation"],
                "success_criteria": "Operating AI tools confidently with clear ROI",
                "resources_needed": "Ongoing support and tools"
            }
        ],
        "success_metrics": ["Successfully using AI for your stated goal", "Measurable improvement in efficiency or outcomes", "Confidence in using AI tools"],
        "quick_wins": ["First AI tool exploration completed", "Generated your first AI output", "Identified one practical application"],
        "risks_and_mitigation": [
            {"risk": "Tool complexity or learning curve", "mitigation": "Start simple, use tutorials, leverage free tools first"},
            {"risk": "Results not meeting expectations", "mitigation": "Adjust approach, try different tools, gather feedback"},
            {"risk": "Integration with existing processes", "mitigation": "Plan integration carefully, test small before scaling"}
        ]
    }
    
    return roadmap


def build_strategy(
    user_context: str,
    resources: str = "",
    timeline: str = "",
    constraints: str = "",
    success_metrics: str = ""
) -> dict:
    """
    Complete strategy building workflow:
    1. Analyze user context
    2. Generate personalized roadmap
    3. Return full strategy package
    """
    # Step 1: Analyze context
    analysis = analyze_context(user_context)
    
    # Step 2: Generate roadmap based on analysis
    # Note: we pass the full user context as conversation_context instead of breaking it into pieces
    roadmap = generate_roadmap(
        context_type=analysis.get("context_type", "professional"),
        primary_goal=analysis.get("primary_goal", user_context[:100]),
        conversation_context=user_context  # Pass full context instead of resources/timeline/constraints
    )
    
    # Step 3: Combine into full strategy package
    strategy = {
        "created_at": datetime.now().isoformat(),
        "context_analysis": analysis,
        "roadmap": roadmap,
        "user_inputs": {
            "context": user_context,
            "resources": resources,
            "timeline": timeline,
            "constraints": constraints,
            "success_metrics": success_metrics
        }
    }
    
    return strategy


def strategy_to_markdown(strategy: dict) -> str:
    """
    Convert strategy object to a readable markdown document.
    Can be exported or displayed to user.
    """
    analysis = strategy["context_analysis"]
    roadmap = strategy["roadmap"]
    
    md = []
    md.append("# Your Personalized AI Strategy\n")
    md.append(f"*Generated: {strategy['created_at']}*\n")
    
    # Executive Summary
    md.append("## Executive Summary\n")
    md.append(f"**Your Goal:** {analysis.get('primary_goal', 'AI Integration')}\n")
    md.append(f"**Your Role:** {analysis.get('inferred_role', 'AI Enthusiast')}\n")
    md.append(f"**Strategy:** {roadmap.get('strategy_summary', 'Phased approach to AI adoption')}\n")
    
    # Context & Challenges
    md.append("\n## Your Situation\n")
    md.append("**Key Challenges:**\n")
    for challenge in analysis.get("key_challenges", []):
        md.append(f"- {challenge}\n")
    
    md.append("\n**AI Opportunities for Your Context:**\n")
    for app in analysis.get("potential_ai_applications", []):
        md.append(f"- {app}\n")
    
    # Quick Wins
    md.append("\n## Quick Wins (First Month)\n")
    for win in roadmap.get("quick_wins", []):
        md.append(f"- {win}\n")
    
    # Phased Roadmap
    md.append("\n## Your Phased Roadmap\n")
    for phase in roadmap.get("phases", []):
        md.append(f"\n### Phase {phase.get('phase_number', 1)}: {phase.get('name', 'Phase')}\n")
        md.append(f"**Duration:** {phase.get('duration', '2-4 weeks')}\n")
        md.append(f"**Goal:** {phase.get('goal', 'TBD')}\n")
        
        md.append("\n**Key Activities:**\n")
        for activity in phase.get("key_activities", []):
            md.append(f"- {activity}\n")
        
        md.append("\n**Tools & Approaches:**\n")
        for tool in phase.get("tools_or_approaches", []):
            md.append(f"- {tool}\n")
        
        md.append(f"\n**Success Criteria:** {phase.get('success_criteria', 'TBD')}\n")
        md.append(f"**Resources Needed:** {phase.get('resources_needed', 'TBD')}\n")
    
    # Success Metrics
    md.append("\n## Overall Success Metrics\n")
    for metric in roadmap.get("success_metrics", []):
        md.append(f"- {metric}\n")
    
    # Risks & Mitigation
    if roadmap.get("risks_and_mitigation"):
        md.append("\n## Potential Risks & How to Address Them\n")
        for risk_item in roadmap.get("risks_and_mitigation", []):
            md.append(f"- **{risk_item.get('risk', 'Risk')}:** {risk_item.get('mitigation', 'TBD')}\n")
    
    return "\n".join(md)


if __name__ == "__main__":
    # Example usage
    context = "I'm a high school English teacher wanting to use AI to personalize feedback for student essays."
    resources = "5 hours per week, $50 budget, no AI experience"
    timeline = "3 months"
    constraints = "Must maintain academic integrity, school approval needed"
    metrics = "Students report better feedback quality, essays improve, teacher time saved"
    
    strategy = build_strategy(context, resources, timeline, constraints, metrics)
    print(json.dumps(strategy, indent=2))
    print("\n" + "="*80 + "\n")
    print(strategy_to_markdown(strategy))
