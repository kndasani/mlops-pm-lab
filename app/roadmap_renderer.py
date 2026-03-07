"""
Roadmap Renderer Module

Generates visual representations of AI strategy roadmaps.
Supports SVG timelines and interactive HTML dashboards.
"""

import json
from typing import Dict, List, Any


def generate_timeline_svg(phases: List[Dict], title: str = "Your AI Strategy Roadmap") -> str:
    """
    Generate a clean, linear SVG timeline visualization of the roadmap phases.
    
    Args:
        phases: List of phase dictionaries from the strategy
        title: Title for the roadmap
        
    Returns:
        SVG string that can be embedded in HTML/Streamlit
    """
    
    num_phases = len(phases)
    # SVG dimensions
    svg_width = 1000
    svg_height = 300
    
    # Timeline positioning
    start_x = 100
    end_x = 900
    timeline_y = 80
    
    # Calculate spacing between phases
    phase_spacing = (end_x - start_x) / (num_phases - 1) if num_phases > 1 else 0
    
    svg_parts = []
    
    # SVG header
    svg_parts.append(f'''<svg width="100%" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" style="background: white;">
    <defs>
        <style>
            .timeline-line {{ stroke: #e0e0e0; stroke-width: 2; }}
            .progress-line {{ stroke: #1a73e8; stroke-width: 3; }}
            .phase-circle {{ fill: white; stroke-width: 3; }}
            .phase-number {{ fill: white; font-weight: bold; font-size: 16px; text-anchor: middle; dominant-baseline: middle; }}
            .phase-label {{ fill: #202124; font-weight: bold; font-size: 13px; text-anchor: middle; }}
            .phase-duration {{ fill: #666; font-size: 11px; text-anchor: middle; }}
            .title {{ fill: #202124; font-size: 18px; font-weight: bold; }}
            .completion-check {{ fill: #28a745; font-weight: bold; font-size: 14px; text-anchor: middle; dominant-baseline: middle; }}
        </style>
    </defs>
    
    <!-- Title -->
    <text x="50" y="25" class="title">{title}</text>
    
    <!-- Background timeline line -->
    <line x1="{start_x}" y1="{timeline_y}" x2="{end_x}" y2="{timeline_y}" class="timeline-line"/>
''')
    
    # Draw each phase
    for idx, phase in enumerate(phases):
        phase_num = phase.get("phase_number", idx + 1)
        phase_name = phase.get("name", f"Phase {phase_num}")[:20]  # Truncate if needed
        duration = phase.get("duration", "")
        
        # Calculate position
        x_pos = start_x + (idx * phase_spacing) if num_phases > 1 else (start_x + end_x) / 2
        
        # Color varies by phase for visual progression
        colors = ["#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4"]
        color = colors[idx % len(colors)]
        
        # Draw circle
        svg_parts.append(f'''
    <!-- Phase {phase_num} -->
    <circle cx="{x_pos}" cy="{timeline_y}" r="20" class="phase-circle" stroke="{color}"/>
    <text x="{x_pos}" y="{timeline_y}" class="phase-number">{phase_num}</text>
    
    <!-- Phase label and duration -->
    <text x="{x_pos}" y="{timeline_y + 50}" class="phase-label">{phase_name}</text>
    <text x="{x_pos}" y="{timeline_y + 70}" class="phase-duration">{duration}</text>
''')
    
    # Draw progress line up to the last phase
    if num_phases > 1:
        last_x = start_x + ((num_phases - 1) * phase_spacing)
        svg_parts.append(f'''
    <!-- Progress indicator line -->
    <line x1="{start_x}" y1="{timeline_y}" x2="{last_x}" y2="{timeline_y}" class="progress-line"/>
''')
    
    # Draw completion checkmark at the end
    final_x = start_x + ((num_phases - 1) * phase_spacing) if num_phases > 1 else (start_x + end_x) / 2
    svg_parts.append(f'''
    <!-- Completion indicator -->
    <text x="{final_x + 50}" y="{timeline_y - 5}" class="completion-check">✓ Complete</text>
''')
    
    # Close SVG
    svg_parts.append('</svg>')
    
    return ''.join(svg_parts)


def generate_metrics_card(success_metrics: List[str], quick_wins: List[str]) -> str:
    """
    Generate an HTML card showing success metrics and quick wins.
    """
    metrics_html = '<div style="padding: 20px; background: #f8f9fa; border-radius: 8px; margin: 20px 0;">'
    metrics_html += '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">'
    
    # Quick Wins
    metrics_html += '''
    <div>
        <h3 style="margin-top: 0; color: #1a73e8;">⚡ Quick Wins (First Month)</h3>
        <ul style="margin: 0; padding-left: 20px;">
    '''
    for win in quick_wins[:3]:
        metrics_html += f'<li style="margin: 8px 0; color: #202124;">{win}</li>'
    metrics_html += '</ul></div>'
    
    # Success Metrics
    metrics_html += '''
    <div>
        <h3 style="margin-top: 0; color: #1a73e8;">📊 Success Metrics</h3>
        <ul style="margin: 0; padding-left: 20px;">
    '''
    for metric in success_metrics[:3]:
        metrics_html += f'<li style="margin: 8px 0; color: #202124;">{metric}</li>'
    metrics_html += '</ul></div></div></div>'
    
    return metrics_html


def generate_risk_mitigation_table(risks: List[Dict]) -> str:
    """
    Generate an HTML table for risks and mitigation strategies.
    """
    if not risks:
        return ""
    
    html = '<div style="margin: 20px 0;"><h3 style="color: #1a73e8;">⚠️ Risks & Mitigation</h3>'
    html += '<table style="width: 100%; border-collapse: collapse;">'
    html += '<tr style="background: #e8f0fe;"><th style="padding: 12px; text-align: left; border: 1px solid #dfe1e5;">Risk</th><th style="padding: 12px; text-align: left; border: 1px solid #dfe1e5;">Mitigation Strategy</th></tr>'
    
    for risk in risks[:5]:  # Show top 5 risks
        risk_text = risk.get("risk", "Unknown risk")
        mitigation = risk.get("mitigation", "TBD")
        html += f'''<tr>
            <td style="padding: 12px; border: 1px solid #dfe1e5; color: #d32f2f; font-weight: 500;">{risk_text}</td>
            <td style="padding: 12px; border: 1px solid #dfe1e5; color: #1976d2;">{mitigation}</td>
        </tr>'''
    
    html += '</table></div>'
    return html


def generate_phase_details_accordion(phases: List[Dict]) -> str:
    """
    Generate interactive accordion cards for expanding phase details.
    
    Args:
        phases: List of phase dictionaries from the strategy
        
    Returns:
        HTML string with expandable phase cards
    """
    
    html_parts = []
    html_parts.append('<div style="margin-top: 0;">')
    
    for idx, phase in enumerate(phases, 1):
        phase_num = phase.get("phase_number", idx)
        phase_name = phase.get("name", f"Phase {phase_num}")
        duration = phase.get("duration", "2-4 weeks")
        goal = phase.get("goal", "")
        description = phase.get("description", "")
        key_activities = phase.get("key_activities", [])
        milestones = phase.get("milestones", [])
        tools = phase.get("tools_or_approaches", [])
        success = phase.get("success_criteria", "")
        resources = phase.get("resources_needed", "")
        
        # Color coding for phases
        colors = ["#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4"]
        color = colors[(phase_num - 1) % len(colors)]
        
        html_parts.append(f'''
    <details style="margin-bottom: 15px; border: 2px solid {color}; border-radius: 8px; overflow: hidden;">
        <summary style="background-color: {color}; color: white; padding: 15px; cursor: pointer; font-weight: bold; font-size: 15px; user-select: none; display: flex; justify-content: space-between; align-items: center;">
            <span>▶ Phase {phase_num}: {phase_name} <span style="font-weight: normal; font-size: 13px;">({duration})</span></span>
            <span style="font-size: 12px; opacity: 0.9;">Click to expand</span>
        </summary>
        <div style="padding: 20px; background-color: #f8f9fa;">
''')
        
        if goal:
            html_parts.append(f'<div style="margin-bottom: 15px; padding: 12px; background-color: white; border-left: 4px solid {color}; border-radius: 4px;"><strong style="color: #202124;">🎯 Goal:</strong><p style="margin: 8px 0 0 0; color: #555;">{goal}</p></div>')
        
        if description:
            html_parts.append(f'<p style="margin-bottom: 15px; color: #333; line-height: 1.6;"><strong>📝 Overview:</strong><br>{description}</p>')
        
        if key_activities:
            html_parts.append('<div style="margin-bottom: 15px;">')
            html_parts.append(f'<strong style="color: #202124;">✓ Key Activities:</strong>')
            html_parts.append('<ul style="margin: 10px 0; padding-left: 25px; color: #555;">')
            for activity in key_activities:
                html_parts.append(f'<li style="margin: 6px 0; line-height: 1.5;">{activity}</li>')
            html_parts.append('</ul>')
            html_parts.append('</div>')
        
        if tools:
            html_parts.append('<div style="margin-bottom: 15px;">')
            html_parts.append(f'<strong style="color: #202124;">🛠️ Tools & Technologies:</strong>')
            html_parts.append('<ul style="margin: 10px 0; padding-left: 25px; color: #555;">')
            for tool in tools:
                html_parts.append(f'<li style="margin: 6px 0; line-height: 1.5;">{tool}</li>')
            html_parts.append('</ul>')
            html_parts.append('</div>')
        
        if milestones:
            html_parts.append('<div style="margin-bottom: 15px;">')
            html_parts.append(f'<strong style="color: #202124;">📍 Milestones:</strong>')
            html_parts.append('<ul style="margin: 10px 0; padding-left: 25px; color: #555;">')
            for milestone in milestones:
                html_parts.append(f'<li style="margin: 6px 0; line-height: 1.5;">{milestone}</li>')
            html_parts.append('</ul>')
            html_parts.append('</div>')
        
        if success:
            html_parts.append(f'<div style="margin-bottom: 15px; padding: 12px; background-color: #e8f5e9; border-left: 4px solid #4caf50; border-radius: 4px;"><strong style="color: #2e7d32;">✓ Success Criteria:</strong><p style="margin: 8px 0 0 0; color: #333;">{success}</p></div>')
        
        if resources:
            html_parts.append(f'<div style="padding: 12px; background-color: #e3f2fd; border-left: 4px solid #2196f3; border-radius: 4px;"><strong style="color: #1565c0;">📦 Resources Needed:</strong><p style="margin: 8px 0 0 0; color: #333;">{resources}</p></div>')
        
        html_parts.append('</div>')
        html_parts.append('</details>')
    
    html_parts.append('</div>')
    
    return ''.join(html_parts)


def generate_dashboard_html(strategy: Dict) -> str:
    """
    Generate a complete HTML dashboard for the strategy.
    Returns HTML string that can be displayed in Streamlit with st.components.html()
    """
    
    analysis = strategy.get("context_analysis", {})
    roadmap = strategy.get("roadmap", {})
    
    html = f'''
<div style="max-width: 1400px; margin: 0 auto; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
    
    <!-- Header Section -->
    <div style="background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%); color: white; padding: 40px; border-radius: 8px; margin-bottom: 30px;">
        <h1 style="margin: 0 0 10px 0; font-size: 32px;">Your Personalized AI Strategy</h1>
        <p style="margin: 0; font-size: 16px; opacity: 0.9;">{analysis.get('inferred_role', 'AI Enthusiast')} • {analysis.get('context_type', 'Personal Development').title()}</p>
    </div>
    
    <!-- Summary Section -->
    <div style="background: white; padding: 25px; border-radius: 8px; border: 1px solid #dfe1e5; margin-bottom: 30px;">
        <h2 style="margin-top: 0; color: #202124;">Your Strategic Direction</h2>
        <p style="font-size: 16px; color: #3c4043; line-height: 1.6;">{roadmap.get('strategy_summary', 'Your personalized strategy has been created.')}</p>
    </div>
    
    <!-- Timeline Visualization (with horizontal scroll) -->
    <div style="background: white; padding: 25px; border-radius: 8px; border: 1px solid #dfe1e5; margin-bottom: 30px; overflow-x: auto;">
        <h2 style="margin-top: 0; color: #202124;">Phased Implementation Timeline</h2>
        <div style="min-width: 100%; overflow-x: auto; padding-bottom: 20px;">
            {generate_timeline_svg(roadmap.get('phases', []))}
        </div>
    </div>
    
    <!-- Metrics Section -->
    <div style="background: white; border-radius: 8px; border: 1px solid #dfe1e5; margin-bottom: 30px; overflow: hidden;">
        {generate_metrics_card(roadmap.get('success_metrics', []), roadmap.get('quick_wins', []))}
    </div>
    
    <!-- Phase Details -->
    <div style="background: white; padding: 25px; border-radius: 8px; border: 1px solid #dfe1e5; margin-bottom: 30px;">
        <h2 style="margin-top: 0; color: #202124;">Phase Details</h2>
        {generate_phase_details_accordion(roadmap.get('phases', []))}
    </div>
    
    <!-- Risks & Mitigation -->
    <div style="background: white; padding: 25px; border-radius: 8px; border: 1px solid #dfe1e5; margin-bottom: 30px;">
        {generate_risk_mitigation_table(roadmap.get('risks_and_mitigation', []))}
    </div>
    
    <!-- Challenges Analysis -->
    <div style="background: #fff3cd; padding: 25px; border-radius: 8px; border-left: 4px solid #ffc107; margin-bottom: 30px;">
        <h3 style="margin-top: 0; color: #856404;">Your Key Challenges</h3>
        <ul style="margin: 0; padding-left: 20px; color: #856404;">
'''
    
    for challenge in analysis.get('key_challenges', []):
        html += f'<li style="margin: 8px 0;">{challenge}</li>'
    
    html += '''
        </ul>
    </div>
    
    <!-- AI Opportunities -->
    <div style="background: #d4edda; padding: 25px; border-radius: 8px; border-left: 4px solid #28a745; margin-bottom: 30px;">
        <h3 style="margin-top: 0; color: #155724;">Your AI Opportunities</h3>
        <ul style="margin: 0; padding-left: 20px; color: #155724;">
'''
    
    for opportunity in analysis.get('potential_ai_applications', []):
        html += f'<li style="margin: 8px 0;">{opportunity}</li>'
    
    html += '''
        </ul>
    </div>
    
</div>
'''
    
    return html


if __name__ == "__main__":
    # Example usage
    example_strategy = {
        "context_analysis": {
            "context_type": "personal",
            "primary_goal": "Learn AI and apply to teaching",
            "inferred_role": "High School Teacher",
            "key_challenges": ["No technical background", "Limited time"],
            "potential_ai_applications": ["Personalized grading", "Content generation"],
            "maturity_estimate": "beginner"
        },
        "roadmap": {
            "strategy_summary": "Start with foundational knowledge, then apply to specific teaching workflows.",
            "phases": [
                {
                    "phase_number": 1,
                    "name": "Foundation",
                    "duration": "3 weeks",
                    "goal": "Understand AI fundamentals",
                    "key_activities": ["Online course", "Explore tools"],
                    "tools_or_approaches": ["ChatGPT", "YouTube tutorials"],
                    "success_criteria": "Can explain 3 AI concepts",
                    "resources_needed": "5 hours/week"
                }
            ],
            "success_metrics": ["Student feedback improved"],
            "quick_wins": ["First ChatGPT prompt"],
            "risks_and_mitigation": [{"risk": "Time constraint", "mitigation": "Start small"}]
        }
    }
    
    html = generate_dashboard_html(example_strategy)
    with open("/tmp/roadmap_dashboard.html", "w") as f:
        f.write(html)
    print("Dashboard generated at /tmp/roadmap_dashboard.html")
