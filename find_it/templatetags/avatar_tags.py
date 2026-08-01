from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def user_avatar(user, size=50):
    """TEST: Return a hardcoded red circle SVG to verify the pipeline."""
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">
        <circle cx="{size//2}" cy="{size//2}" r="{size//2}" fill="red" />
    </svg>
    """
    # Clean up the SVG for HTML embedding
    svg = svg.replace('\n', '').replace('\r', '').replace('"', "'")
    return f"data:image/svg+xml;utf8,{svg}"