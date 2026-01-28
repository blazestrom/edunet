"""
Content formatting module for converting generated content into various formats
"""
from typing import Dict
import markdown
from datetime import datetime
from utils.logger import logger

def format_as_markdown(content: Dict) -> str:
    """
    Format content as markdown document.
    
    Args:
        content: Dictionary with keys like 'notes', 'quiz', 'flashcards', 'transcript'
    
    Returns:
        Formatted markdown string
    """
    md = f"# Lecture Notes\n\n"
    md += f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    
    if content.get("course_name"):
        md += f"**Course:** {content['course_name']}\n\n"
    
    if content.get("topic"):
        md += f"**Topic:** {content['topic']}\n\n"
    
    md += "---\n\n"
    
    if content.get("notes"):
        md += "## 📝 Study Notes\n\n"
        md += content["notes"]
        md += "\n\n---\n\n"
    
    if content.get("quiz"):
        md += "## 📋 Quiz Questions\n\n"
        md += content["quiz"]
        md += "\n\n---\n\n"
    
    if content.get("flashcards"):
        md += "## 🎴 Flashcards\n\n"
        md += content["flashcards"]
        md += "\n\n"
    
    if content.get("transcript"):
        md += "---\n\n"
        md += "## 📄 Full Transcript\n\n"
        md += content["transcript"]
        md += "\n"
    
    return md

def format_as_html(content: Dict, theme: str = "light") -> str:
    """
    Convert content to styled HTML document.
    
    Args:
        content: Dictionary with content to format
        theme: Color theme ('light' or 'dark')
    
    Returns:
        HTML string
    """
    md_content = format_as_markdown(content)
    
    # Choose theme colors
    if theme == "dark":
        bg_color = "#1e1e1e"
        text_color = "#e0e0e0"
        heading_color = "#4da6ff"
        code_bg = "#2d2d2d"
    else:
        bg_color = "#ffffff"
        text_color = "#333333"
        heading_color = "#2c3e50"
        code_bg = "#f4f4f4"
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lecture Notes</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
            background-color: {bg_color};
            color: {text_color};
            line-height: 1.8;
            font-size: 16px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        
        h1 {{
            color: {heading_color};
            border-bottom: 4px solid {heading_color};
            padding-bottom: 15px;
            margin-bottom: 30px;
            font-size: 2.5em;
        }}
        
        h2 {{
            color: {heading_color};
            border-bottom: 2px solid {heading_color};
            padding-bottom: 10px;
            margin-top: 40px;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}
        
        h3 {{
            color: {heading_color};
            margin-top: 25px;
            margin-bottom: 15px;
            font-size: 1.3em;
        }}
        
        p {{
            margin-bottom: 15px;
            text-align: justify;
        }}
        
        ul, ol {{
            margin-left: 30px;
            margin-bottom: 15px;
        }}
        
        li {{
            margin-bottom: 8px;
        }}
        
        code {{
            background-color: {code_bg};
            padding: 3px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
        
        pre {{
            background-color: {code_bg};
            padding: 20px;
            border-radius: 6px;
            overflow-x: auto;
            margin: 20px 0;
            border-left: 4px solid {heading_color};
        }}
        
        pre code {{
            background: none;
            padding: 0;
        }}
        
        blockquote {{
            border-left: 5px solid {heading_color};
            padding-left: 20px;
            margin: 20px 0;
            font-style: italic;
            color: #999;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        
        th {{
            background-color: {heading_color};
            color: {bg_color};
            font-weight: bold;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid {heading_color};
            margin: 40px 0;
        }}
        
        em {{
            color: {text_color};
            font-style: italic;
        }}
        
        strong {{
            color: {heading_color};
            font-weight: bold;
        }}
        
        .timestamp {{
            color: #999;
            font-size: 0.9em;
            margin-bottom: 20px;
        }}
        
        @media (max-width: 600px) {{
            .container {{
                padding: 20px 10px;
            }}
            h1 {{
                font-size: 1.8em;
            }}
            h2 {{
                font-size: 1.4em;
            }}
        }}
        
        @media print {{
            body {{
                background-color: white;
                color: black;
            }}
            .container {{
                max-width: 100%;
                padding: 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {markdown.markdown(md_content, extensions=['fenced_code', 'tables', 'toc'])}
    </div>
</body>
</html>"""
    return html

def save_as_text(content: str, output_path: str) -> str:
    """
    Save content as plain text file.
    
    Args:
        content: Text content to save
        output_path: Path where to save the file
    
    Returns:
        Path to saved file
    
    Raises:
        Exception: If file save fails
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"Saved text file: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Error saving text file: {e}")
        raise

def format_as_json(content: Dict) -> str:
    """
    Format content as JSON.
    
    Args:
        content: Content dictionary
    
    Returns:
        JSON string
    """
    import json
    
    formatted = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "course": content.get("course_name", "Unknown"),
            "topic": content.get("topic", "General"),
        },
        "content": {
            "notes": content.get("notes", ""),
            "quiz": content.get("quiz", ""),
            "flashcards": content.get("flashcards", ""),
            "transcript": content.get("transcript", ""),
        }
    }
    
    return json.dumps(formatted, indent=2)

def format_flashcards_for_export(flashcards_text: str) -> Dict:
    """
    Parse flashcard text into structured format.
    
    Args:
        flashcards_text: Flashcard text with Q: and A: format
    
    Returns:
        List of flashcard dicts with 'question' and 'answer' keys
    """
    cards = []
    lines = flashcards_text.split('\n')
    current_question = None
    
    for line in lines:
        line = line.strip()
        if line.startswith('Q:'):
            current_question = line[2:].strip()
        elif line.startswith('A:') and current_question:
            answer = line[2:].strip()
            cards.append({
                "question": current_question,
                "answer": answer
            })
            current_question = None
    
    return cards

def format_quiz_for_export(quiz_text: str) -> Dict:
    """
    Parse quiz text into structured format.
    
    Args:
        quiz_text: Quiz text with Q:, A), B), C), D) format
    
    Returns:
        List of question dicts
    """
    questions = []
    lines = quiz_text.split('\n')
    current_q = None
    
    for line in lines:
        line = line.strip()
        if line.startswith('Q:'):
            if current_q:
                questions.append(current_q)
            current_q = {
                "question": line[2:].strip(),
                "options": [],
                "correct_answer": None,
                "explanation": None
            }
        elif line and current_q and len(line) > 0:
            if line[0] in ['A', 'B', 'C', 'D'] and len(line) > 1 and line[1] == ')':
                current_q["options"].append(line)
            elif line.startswith('Correct Answer:'):
                current_q["correct_answer"] = line.split(':')[1].strip()
            elif line.startswith('Explanation:'):
                current_q["explanation"] = line.split(':', 1)[1].strip()
    
    if current_q:
        questions.append(current_q)
    
    return questions