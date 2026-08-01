import random
import html

# Your custom color palette
COLOR_PALETTE = [
    "#7cad79",  # Light green
    "#456149",  # Dark green
    "#d4d0a7",  # Light beige
    "#478593",  # Teal
    "#385575",  # Dark blue
    "#6A0DAD",  # Purple
    "#1E3A8A",  # Dark blue
    "#20B2AA",  # Teal
    "#E6E6FA",  # Light purple
]

def get_random_colors(n=3, seed=None):
    """Return `n` random colors from the palette, optionally seeded for consistency."""
    if seed is not None:
        random.seed(seed)
    return random.sample(COLOR_PALETTE, n)

def generate_avatar_svg(user_id, size=200):
    """Generate a random SVG avatar for a user."""
    colors = get_random_colors(3, seed=user_id)
    color1, color2, color3 = colors

    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">
        <circle cx="{size//2}" cy="{size//2}" r="{size//2}" fill="{color1}" />
        <circle cx="{size//2}" cy="{size//2}" r="{size//3}" fill="{color2}" />
        <circle cx="{size//2}" cy="{size//2}" r="{size//6}" fill="{color3}" />
        <path d="M0,0 L{size},{size} M{size},0 L0,{size}" stroke="white" stroke-width="10" opacity="0.3" />
    </svg>
    """
    # Remove newlines and escape quotes for HTML embedding
    svg = svg.replace('\n', '').replace('\r', '').replace('"', "'")
    return svg