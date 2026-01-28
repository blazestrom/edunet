"""
Content exporter module for saving generated content in multiple formats
"""
import os
from typing import Dict, List
from pathlib import Path
from fpdf import FPDF
from output.formatter import (
    format_as_markdown, 
    format_as_html, 
    format_as_json,
    save_as_text
)
from utils.logger import logger

class PDFExporter(FPDF):
    """Custom PDF exporter with formatted headers and footers"""
    
    def __init__(self, title: str = "Lecture Notes"):
        super().__init__()
        self.title = title
    
    def header(self):
        """Add header to each page"""
        self.set_font('Arial', 'B', 16)
        self.set_text_color(44, 62, 80)
        self.cell(0, 10, self.title, 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        """Add footer with page number"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def chapter_title(self, title: str):
        """Add chapter title"""
        self.set_font('Arial', 'B', 14)
        self.set_text_color(44, 62, 80)
        self.set_fill_color(224, 240, 255)
        self.cell(0, 10, title, 0, 1, fill=True)
        self.ln(3)
    
    def chapter_body(self, body: str, max_width: int = 0):
        """Add chapter body text"""
        self.set_font('Arial', '', 11)
        self.set_text_color(50, 50, 50)
        
        # Handle long text that might exceed page width
        for line in body.split('\n'):
            self.multi_cell(0, 6, line.strip())
        
        self.ln()
    
    def add_section(self, title: str, content: str):
        """Add a complete section with title and content"""
        if content and content.strip():
            self.chapter_title(title)
            self.chapter_body(content)

def export_as_pdf(content: Dict, output_path: str, title: str = "Lecture Notes") -> str:
    """
    Export content as PDF file.
    
    Args:
        content: Dictionary containing notes, quiz, flashcards, transcript
        output_path: Path where to save the PDF file
        title: Title for the PDF document
    
    Returns:
        Path to saved PDF file
    
    Raises:
        Exception: If PDF creation fails
    """
    try:
        logger.info(f"Creating PDF: {output_path}")
        
        pdf = PDFExporter(title=title)
        pdf.add_page()
        
        # Add metadata
        if content.get("course_name"):
            pdf.chapter_body(f"Course: {content['course_name']}")
        if content.get("topic"):
            pdf.chapter_body(f"Topic: {content['topic']}")
        
        # Add study notes
        if content.get("notes"):
            pdf.add_section("📝 Study Notes", content["notes"][:5000])  # Limit for PDF
        
        # Add quiz questions
        if content.get("quiz"):
            pdf.add_page()
            pdf.add_section("📋 Quiz Questions", content["quiz"][:5000])
        
        # Add flashcards
        if content.get("flashcards"):
            pdf.add_page()
            pdf.add_section("🎴 Flashcards", content["flashcards"][:5000])
        
        # Create output directory if needed
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        pdf.output(output_path)
        logger.info(f"✓ PDF saved successfully: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error creating PDF: {e}")
        raise

def export_content(content: Dict, output_dir: str, base_filename: str, formats: List[str] = None) -> Dict[str, str]:
    """
    Export content in multiple formats.
    
    Args:
        content: Dictionary with 'notes', 'quiz', 'flashcards', 'transcript'
        output_dir: Directory to save output files
        base_filename: Base name for output files (without extension)
        formats: List of formats to export as ['md', 'html', 'pdf', 'txt', 'json']
    
    Returns:
        Dictionary mapping format name to file path
    
    Raises:
        Exception: If export fails
    """
    if formats is None:
        formats = ['md', 'html', 'pdf']
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    output_files = {}
    
    try:
        # Export as Markdown
        if 'md' in formats:
            logger.info("Exporting as Markdown...")
            md_content = format_as_markdown(content)
            md_path = os.path.join(output_dir, f"{base_filename}.md")
            save_as_text(md_content, md_path)
            output_files['markdown'] = md_path
            logger.debug(f"✓ Markdown exported: {md_path}")
        
        # Export as HTML
        if 'html' in formats:
            logger.info("Exporting as HTML...")
            html_content = format_as_html(content)
            html_path = os.path.join(output_dir, f"{base_filename}.html")
            save_as_text(html_content, html_path)
            output_files['html'] = html_path
            logger.debug(f"✓ HTML exported: {html_path}")
        
        # Export as PDF
        if 'pdf' in formats:
            logger.info("Exporting as PDF...")
            pdf_path = os.path.join(output_dir, f"{base_filename}.pdf")
            export_as_pdf(content, pdf_path, title=base_filename)
            output_files['pdf'] = pdf_path
            logger.debug(f"✓ PDF exported: {pdf_path}")
        
        # Export as plain text
        if 'txt' in formats:
            logger.info("Exporting as plain text...")
            txt_content = content.get('transcript', '') or content.get('notes', '')
            txt_path = os.path.join(output_dir, f"{base_filename}.txt")
            save_as_text(txt_content, txt_path)
            output_files['txt'] = txt_path
            logger.debug(f"✓ Text exported: {txt_path}")
        
        # Export as JSON
        if 'json' in formats:
            logger.info("Exporting as JSON...")
            json_content = format_as_json(content)
            json_path = os.path.join(output_dir, f"{base_filename}.json")
            save_as_text(json_content, json_path)
            output_files['json'] = json_path
            logger.debug(f"✓ JSON exported: {json_path}")
        
        logger.info(f"✓ All formats exported successfully. Total formats: {len(output_files)}")
        return output_files
        
    except Exception as e:
        logger.error(f"Error during content export: {e}")
        raise

def export_individual_sections(content: Dict, output_dir: str, base_filename: str) -> Dict[str, str]:
    """
    Export each section (notes, quiz, flashcards) as separate files.
    
    Args:
        content: Content dictionary
        output_dir: Output directory
        base_filename: Base filename
    
    Returns:
        Dictionary mapping section names to file paths
    """
    os.makedirs(output_dir, exist_ok=True)
    output_files = {}
    
    try:
        # Export notes
        if content.get("notes"):
            notes_path = os.path.join(output_dir, f"{base_filename}_notes.md")
            save_as_text(content["notes"], notes_path)
            output_files['notes'] = notes_path
            logger.info(f"✓ Notes exported: {notes_path}")
        
        # Export quiz
        if content.get("quiz"):
            quiz_path = os.path.join(output_dir, f"{base_filename}_quiz.md")
            save_as_text(content["quiz"], quiz_path)
            output_files['quiz'] = quiz_path
            logger.info(f"✓ Quiz exported: {quiz_path}")
        
        # Export flashcards
        if content.get("flashcards"):
            cards_path = os.path.join(output_dir, f"{base_filename}_flashcards.md")
            save_as_text(content["flashcards"], cards_path)
            output_files['flashcards'] = cards_path
            logger.info(f"✓ Flashcards exported: {cards_path}")
        
        # Export transcript
        if content.get("transcript"):
            transcript_path = os.path.join(output_dir, f"{base_filename}_transcript.txt")
            save_as_text(content["transcript"], transcript_path)
            output_files['transcript'] = transcript_path
            logger.info(f"✓ Transcript exported: {transcript_path}")
        
        return output_files
        
    except Exception as e:
        logger.error(f"Error exporting individual sections: {e}")
        raise
        
        logger.info(f"Exported {len(output_files)} files")
        return output_files
        
    except Exception as e:
        logger.error(f"Error exporting content: {e}")
        raise