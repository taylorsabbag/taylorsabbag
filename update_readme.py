import feedparser
import datetime
import re

# Function to truncate description and remove HTML tags
def clean_description(desc, length=100):
    # Remove HTML tags
    clean = re.compile('<.*?>')
    desc = re.sub(clean, '', desc)
    # Truncate and add ellipsis if needed
    if len(desc) > length:
        return desc[:length] + "..."
    return desc

# Read the RSS feed
feed = feedparser.parse('https://www.taylorsabbag.dev/rss')

# Prepare the new table content
table_content = """## Things I've Written

*Behold, my digital scrolls of wisdom! These mystical texts are automatically summoned from my personal grimoire through ancient RSS enchantments:*

| 📜 Scroll Title | 🌟 Date of Enchantment | 🔮 Magical Synopsis |
|-----------------|----------------------|-------------------|
"""

# Add up to 5 most recent posts
for entry in feed.entries[:5]:
    try:
        # Try the original format first
        date = datetime.datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d')
    except ValueError:
        try:
            # Try the GMT format
            date = datetime.datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S GMT').strftime('%Y-%m-%d')
        except ValueError:
            # If both fail, just use the raw date or a fallback
            date = entry.published.split('T')[0] if 'T' in entry.published else entry.published
    
    # Clean and format the description
    description = clean_description(entry.description)
    
    # Add the table row
    table_content += f"| [{entry.title}]({entry.link}) | {date} | {description} |\n"

# Read the current README
with open('README.md', 'r', encoding='utf-8') as f:
    readme_content = f.read()

# Find and replace the blog posts section
# You'll need to adjust these patterns based on your README structure
pattern = r'## Things I\'ve Written.*?(?=##|$)'
if '## Things I\'ve Written' in readme_content:
    new_content = re.sub(pattern, table_content, readme_content, flags=re.DOTALL)
else:
    new_content = readme_content + '\n' + table_content

# Write the updated README
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(new_content)
