import json
import math

# Load your JSON file
with open('projects.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

# Build a card (inner <table>)
def build_card(c):
    if not c["title"]:
        return "<td></td>"

    # Truncate description and keywords to ensure consistent height
    # Based on: "DeepGit: Exploration and Discovery of Research Software with Human-Curated Graphs" = 95 chars
    # Based on: "Query Language, SQL" = 19 chars
    max_description_length = 100  # Increased for wider cards
    max_keywords_length = 30     # Increased for wider cards
    
    description = c["description"]
    if len(description) > max_description_length:
        description = description[:max_description_length-3] + "..."
    
    keywords = c["keywords"]
    if len(keywords) > max_keywords_length:
        keywords = keywords[:max_keywords_length-3] + "..."

    # handle stars
    if c["stars"] == "private":
        stars_display = '<img src="https://cdn.jsdelivr.net/gh/Readme-Workflows/Readme-Icons@main/icons/octicons/RequestedChanges.svg" width="20px" alt="Private Repository" align="center">'
    else:
        stars_display = f'<img src="https://cdn.jsdelivr.net/gh/Readme-Workflows/Readme-Icons@main/icons/octicons/StarredRepositoryYellow.svg" width="20px" alt="GitHub stars" align="center"> {c["stars"]}'

    # handle paper link icon
    paper_icon = ""
    if c["paper_link"]:
        paper_icon = f'''
<td align="center" style="padding: 10px;">
  <a href="{c["paper_link"]}">
    <img src="https://cdn.jsdelivr.net/gh/Readme-Workflows/Readme-Icons@main/icons/octicons/Wiki.svg" width="20px" alt="Paper" align="center">
  </a>
</td>'''
    else:
        paper_icon = '<td align="center" valign="middle" style="padding: 10px;"></td>'

    # build the icons row with two cells: paper + stars
    icons_row = f'''
<tr height="40px">
  {paper_icon}
  <td align="center" style="padding: 10px;">
    {stars_display}
  </td>
</tr>'''

    # build inner table
    inner_table = f'''
<table>
  <tr height="100px">
    <td colspan="4" align="center" valign="middle">
      <a href="{c["link"]}">
        <img src="{c["logo_img"]}" width="{c["logo_width"]}" height="{c["logo_height"]}" style="object-fit: cover;" />
      </a>
    </td>
  </tr>
  <tr height="120px">
    <td width="250px" colspan="4" valign="top" style="padding: 10px; font-size: 12px;">
      <a href="{c["link"]}"><strong>{c["title"]}</strong></a>: {description}
      <br><br>{keywords}
    </td>
  </tr>
  {icons_row}
</table>
'''
    return f"<td>{inner_table}</td>"

# Build rows of 3 cards each
rows_html = []
for i in range(0, len(cards), 3):
    row_cards = cards[i:i+3]
    # pad with empty cards if needed
    while len(row_cards) < 3:
        row_cards.append({"title": "", "logo_img": "", "logo_width": 80, "logo_height": 80, "link": "", "description": "", "keywords": "", "paper_link": "", "stars": ""})
    cells_html = "\n".join(build_card(c) for c in row_cards)
    rows_html.append(f'<tr height="320px">\n{cells_html}\n</tr>')

# Create the header content
header_content = """## Hi there, I am [Yilin Xia](https://yilinxia.com/)

I am a Ph.D. student advised by Dr. Bertram Ludäscher and Dr. Matthew Turk in the School of Information Sciences at the University of Illinois at Urbana-Champaign.

I am broadly interested in Data Management, Knowledge Representation & Reasoning, and Data Visualization aiming to address data challenges through a Declarative Approach. My research is supported in part by GitHub Secure Open Source Fund, Google Academic Research Grants, Gemini Academic Program, and NumFOCUS Small Development Grants.

"""

# Wrap in outer table
html_output = "<table>\n" + "\n".join(rows_html) + "\n</table>"

# Combine header and table
full_output = header_content + html_output

# Write to README.md
with open('README.md', 'w', encoding='utf-8') as out:
    out.write(full_output)

print("README.md generated successfully!")
