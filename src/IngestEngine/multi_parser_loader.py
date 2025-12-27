"""
Enhanced Multi-Format Script Parser
Supports: Final Draft (.fdx), Celtx (.celtx), Fountain (.fountain), PDF (.pdf), and plain text
"""

import re
import io
import tempfile
import os
import json
import zipfile
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging

# Optional imports with fallbacks
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    from PyPDF2 import PdfReader
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BEAUTIFUL_SOUP_AVAILABLE = True
except ImportError:
    BEAUTIFUL_SOUP_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ScriptElement:
    """Individual script element (line)"""
    text: str
    element_type: str  # "scene_heading", "action", "character", "dialogue", "parenthetical", "transition"
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ScriptScene:
    """Complete scene data"""
    header: str
    elements: List[ScriptElement]
    characters: List[str]
    location: str = ""
    time_of_day: str = ""
    scene_number: int = 0
    page_number: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ScriptMetadata:
    """Script metadata"""
    title: str = ""
    author: str = ""
    version: str = ""
    date: str = ""
    contact: str = ""
    copyright: str = ""
    notes: str = ""
    format_type: str = ""

@dataclass
class ScriptData:
    """Complete parsed script data structure"""
    scenes: List[ScriptScene]
    scene_count: int
    characters: List[str]
    metadata: ScriptMetadata
    raw_text: str = ""
    format_info: Dict[str, Any] = field(default_factory=dict)
    processing_stats: Dict[str, Any] = field(default_factory=dict)

class MultiParserLoader:
    """
    Enhanced multi-format script parser with intelligent format detection
    and robust error handling
    """
    
    def __init__(self):
        """Initialize the enhanced multi-format parser"""
        self.supported_formats = {
            "fdx": "Final Draft XML",
            "celtx": "Celtx Project",
            "fountain": "Fountain Markdown",
            "pdf": "PDF Document",
            "txt": "Plain Text",
            "text": "Plain Text",
            "fdxt": "Final Draft Template",
            "fadein": "Fade In",
            "scrivener": "Scrivener"
        }
        
        # Compile regex patterns for performance
        self.patterns = {
            "scene_heading": re.compile(r"^\s*(?:\.)?\s*(INT\.|EXT\.|INT/EXT\.|I/E\.|EST\.).*$", re.IGNORECASE),
            "character": re.compile(r"^\s*([A-Z][A-Z\s\.\'-]+)(?:\s*\(.*\))?\s*$"),
            "dialogue": re.compile(r"^\s*[^A-Z].*$"),  # Non-uppercase lines after character
            "transition": re.compile(r"^\s*(FADE IN:|FADE OUT\.|FADE TO:|CUT TO:|DISSOLVE TO:|SMASH CUT:|MATCH CUT:|WIPE TO:|IRIS IN:|IRIS OUT\.|JUMP CUT:|TIME CUT:|STOCK SHOT:|BACK TO:|FLASHBACK:|FLASH FORWARD:).*$", re.IGNORECASE),
            "parenthetical": re.compile(r"^\s*\(.*\)\s*$"),
            "page_break": re.compile(r"^={3,}$"),
            "forced_uppercase": re.compile(r"^[A-Z][A-Z\s\W]+$"),
            "scene_number": re.compile(r"^(\d+[A-Z]?)\s*$"),
            "clean_whitespace": re.compile(r"\s+")
        }
        
        self.format_detectors = {
            "fdx": self._detect_fdx,
            "celtx": self._detect_celtx,
            "fountain": self._detect_fountain,
            "pdf": self._detect_pdf,
            "fadein": self._detect_fadein
        }
        
    def parse(self, content: Union[str, bytes], file_type: Optional[str] = None, 
              filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse script content with intelligent format detection
        
        Args:
            content: Script content as string or bytes
            file_type: Explicit file type (optional, will be detected)
            filename: Original filename for better detection
            
        Returns:
            Dictionary containing parsed script data
        """
        start_time = datetime.now()
        
        try:
            # Detect format if not provided
            if not file_type and filename:
                file_type = self.detect_format(filename, content)
            elif not file_type:
                file_type = self.detect_format_from_content(content)
            
            file_type = file_type.lower() if file_type else "text"
            
            logger.info(f"Parsing {file_type.upper()} format")
            
            # Parse based on detected format
            if file_type == "fdx":
                result = self._parse_fdx(content)
            elif file_type == "celtx":
                result = self._parse_celtx(content)
            elif file_type == "fountain":
                result = self._parse_fountain(content)
            elif file_type == "pdf":
                result = self._parse_pdf(content)
            elif file_type in ["fadein", "fdxt"]:
                result = self._parse_fadein(content)
            else:  # txt, text, or fallback
                result = self._parse_plaintext(content)
            
            # Add format information
            result["format_info"] = {
                "detected_format": file_type,
                "format_name": self.supported_formats.get(file_type, "Unknown"),
                "detection_method": "explicit" if file_type else "auto"
            }
            
            # Calculate processing stats
            processing_time = (datetime.now() - start_time).total_seconds()
            result["processing_stats"] = {
                "parse_time_seconds": round(processing_time, 3),
                "scenes_per_second": round(result["scene_count"] / processing_time, 2) if processing_time > 0 else 0,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Successfully parsed {result['scene_count']} scenes in {processing_time:.2f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"Parsing failed: {str(e)}")
            
            # Fallback to plain text with error information
            try:
                fallback_result = self._parse_plaintext(content if isinstance(content, str) 
                                                       else content.decode("utf-8", errors="ignore"))
                fallback_result["format_info"] = {
                    "detected_format": "text",
                    "format_name": "Plain Text (Fallback)",
                    "original_format": file_type,
                    "error": str(e)
                }
                fallback_result["processing_stats"] = {
                    "parse_time_seconds": (datetime.now() - start_time).total_seconds(),
                    "fallback_used": True,
                    "error": str(e)
                }
                
                logger.warning(f"Using fallback plain text parser")
                return fallback_result
                
            except Exception as fallback_error:
                logger.critical(f"Fallback parser also failed: {str(fallback_error)}")
                return self._create_error_result(file_type, str(e))
    
    def _parse_fdx(self, content: Union[str, bytes]) -> Dict[str, Any]:
        """Parse Final Draft FDX XML format with full element parsing"""
        try:
            if isinstance(content, bytes):
                content = content.decode("utf-8")
            
            # Parse XML
            root = ET.fromstring(content)
            
            # Extract metadata
            metadata = self._extract_fdx_metadata(root)
            
            # Parse content
            scenes = []
            characters = set()
            all_elements = []
            current_scene = None
            scene_number = 1
            
            # Namespace handling for Final Draft
            namespaces = {"fd": "http://www.finaldraft.com"}
            
            for paragraph in root.findall(".//Paragraph"):
                paragraph_type = paragraph.get("Type", "")
                text_elem = paragraph.find("Text")
                
                if text_elem is not None:
                    text = (text_elem.text or "").strip()
                    
                    if not text:
                        continue
                    
                    # Determine element type
                    element_type = self._classify_fdx_element(paragraph_type, text)
                    element = ScriptElement(text=text, element_type=element_type)
                    all_elements.append(element)
                    
                    # Handle scene headings
                    if paragraph_type == "Scene Heading":
                        if current_scene:
                            current_scene.elements = all_elements
                            scenes.append(current_scene)
                            all_elements = []
                        
                        # Extract location and time from scene heading
                        location, time_of_day = self._parse_scene_heading(text)
                        
                        current_scene = ScriptScene(
                            header=text,
                            elements=[element],
                            characters=[],
                            location=location,
                            time_of_day=time_of_day,
                            scene_number=scene_number
                        )
                        scene_number += 1
                    
                    # Handle character elements
                    elif paragraph_type == "Character":
                        char_name = self._clean_character_name(text)
                        if char_name:
                            characters.add(char_name)
                            if current_scene and char_name not in current_scene.characters:
                                current_scene.characters.append(char_name)
                    
                    # Add to current scene
                    elif current_scene:
                        current_scene.elements.append(element)
            
            # Add last scene
            if current_scene:
                scenes.append(current_scene)
            
            # Convert to dictionary format
            scenes_data = self._scenes_to_dict(scenes)
            
            return {
                "scenes": scenes_data,
                "scene_count": len(scenes),
                "characters": sorted(list(characters)),
                "metadata": metadata.__dict__,
                "format_info": {
                    "parser": "Final Draft XML",
                    "version": "2.0",
                    "element_types_present": list(set([e.element_type for s in scenes for e in s.elements]))
                }
            }
            
        except ET.ParseError as e:
            logger.error(f"FDX XML parsing error: {str(e)}")
            raise ValueError(f"Invalid FDX XML format: {str(e)}")
        except Exception as e:
            logger.error(f"FDX parsing error: {str(e)}")
            raise
    
    def _parse_fountain(self, content: Union[str, bytes]) -> Dict[str, Any]:
        """Parse Fountain format with enhanced scene parsing"""
        try:
            if isinstance(content, bytes):
                content = content.decode("utf-8")
            
            # Extract metadata from Fountain front matter
            metadata, content_body = self._extract_fountain_metadata(content)
            
            lines = content_body.split("\n")
            scenes = []
            characters = set()
            current_scene = None
            scene_number = 1
            current_elements = []
            
            i = 0
            while i < len(lines):
                line = lines[i].rstrip()
                
                # Skip empty lines at scene boundaries
                if not line and not current_scene:
                    i += 1
                    continue
                
                # Scene heading detection
                is_scene_heading = False
                
                # Check for Fountain scene heading (starts with . or INT/EXT)
                if line.startswith("."):
                    line = line[1:].strip()
                    is_scene_heading = True
                elif self.patterns["scene_heading"].match(line):
                    is_scene_heading = True
                
                if is_scene_heading:
                    # Save previous scene
                    if current_scene:
                        current_scene.elements = current_elements
                        scenes.append(current_scene)
                        current_elements = []
                    
                    # Parse new scene
                    location, time_of_day = self._parse_scene_heading(line)
                    
                    current_scene = ScriptScene(
                        header=line,
                        elements=[],
                        characters=[],
                        location=location,
                        time_of_day=time_of_day,
                        scene_number=scene_number
                    )
                    scene_number += 1
                    
                    # Add scene heading element
                    element = ScriptElement(text=line, element_type="scene_heading")
                    current_elements.append(element)
                    current_scene.elements.append(element)
                
                # Character detection (all caps, not too long)
                elif current_scene and self._is_character_line(line):
                    char_name = self._clean_character_name(line)
                    if char_name:
                        characters.add(char_name)
                        if char_name not in current_scene.characters:
                            current_scene.characters.append(char_name)
                    
                    element = ScriptElement(text=line, element_type="character")
                    current_elements.append(element)
                    current_scene.elements.append(element)
                
                # Parenthetical
                elif current_scene and self.patterns["parenthetical"].match(line):
                    element = ScriptElement(text=line, element_type="parenthetical")
                    current_elements.append(element)
                    current_scene.elements.append(element)
                
                # Dialogue (lines after character)
                elif current_scene and line and not line.startswith("[") and not line.startswith("]"):
                    # Check if previous element was character or parenthetical
                    if current_elements and current_elements[-1].element_type in ["character", "parenthetical"]:
                        element = ScriptElement(text=line, element_type="dialogue")
                        current_elements.append(element)
                        current_scene.elements.append(element)
                    else:
                        element = ScriptElement(text=line, element_type="action")
                        current_elements.append(element)
                        current_scene.elements.append(element)
                
                # Action lines
                elif current_scene and line:
                    element = ScriptElement(text=line, element_type="action")
                    current_elements.append(element)
                    current_scene.elements.append(element)
                
                i += 1
            
            # Add last scene
            if current_scene:
                current_scene.elements = current_elements
                scenes.append(current_scene)
            
            # Convert to dictionary format
            scenes_data = self._scenes_to_dict(scenes)
            
            return {
                "scenes": scenes_data,
                "scene_count": len(scenes),
                "characters": sorted(list(characters)),
                "metadata": metadata.__dict__,
                "format_info": {
                    "parser": "Fountain Enhanced",
                    "has_frontmatter": bool(metadata.title),
                    "element_breakdown": self._analyze_element_types(scenes)
                }
            }
            
        except Exception as e:
            logger.error(f"Fountain parsing error: {str(e)}")
            raise
    
    def _parse_pdf(self, content: bytes) -> Dict[str, Any]:
        """Parse PDF files with multiple extraction methods"""
        if not PDFPLUMBER_AVAILABLE and not PYPDF2_AVAILABLE:
            raise ImportError("PDF parsing requires pdfplumber or PyPDF2")
        
        temp_file = None
        try:
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(content)
                temp_file = tmp_file.name
            
            extracted_text = ""
            
            # Try pdfplumber first (better formatting)
            if PDFPLUMBER_AVAILABLE:
                try:
                    with pdfplumber.open(temp_file) as pdf:
                        for page_num, page in enumerate(pdf.pages):
                            text = page.extract_text()
                            if text:
                                # Clean up PDF text
                                text = self._clean_pdf_text(text)
                                extracted_text += text + "\n\n"
                    logger.info(f"Successfully extracted text using pdfplumber")
                except Exception as e:
                    logger.warning(f"pdfplumber extraction failed: {str(e)}")
                    extracted_text = ""
            
            # Fallback to PyPDF2
            if not extracted_text and PYPDF2_AVAILABLE:
                try:
                    with open(temp_file, "rb") as f:
                        pdf_reader = PdfReader(f)
                        for page_num in range(len(pdf_reader.pages)):
                            text = pdf_reader.pages[page_num].extract_text()
                            if text:
                                text = self._clean_pdf_text(text)
                                extracted_text += text + "\n\n"
                    logger.info(f"Successfully extracted text using PyPDF2")
                except Exception as e:
                    logger.warning(f"PyPDF2 extraction failed: {str(e)}")
            
            # Clean up temp file
            if temp_file and os.path.exists(temp_file):
                os.unlink(temp_file)
            
            if not extracted_text:
                raise ValueError("Failed to extract text from PDF")
            
            # Parse as plain text with PDF-specific cleaning
            result = self._parse_plaintext(extracted_text)
            
            # Add PDF-specific metadata
            result["format_info"].update({
                "parser": "PDF Text Extraction",
                "extraction_method": "pdfplumber" if PDFPLUMBER_AVAILABLE else "PyPDF2",
                "character_count": len(extracted_text),
                "estimated_pages": len(re.findall(r"\f", extracted_text)) + 1
            })
            
            return result
            
        except Exception as e:
            # Clean up temp file on error
            if temp_file and os.path.exists(temp_file):
                os.unlink(temp_file)
            logger.error(f"PDF parsing error: {str(e)}")
            raise
    
    def _parse_celtx(self, content: Union[str, bytes]) -> Dict[str, Any]:
        """Parse Celtx format (XML-based project files)"""
        try:
            if isinstance(content, bytes):
                content = content.decode("utf-8")
            
            # Celtx files can be ZIP archives or XML
            if content.startswith("PK"):  # ZIP file header
                return self._parse_celtx_zip(content)
            
            # Try XML parsing
            try:
                if BEAUTIFUL_SOUP_AVAILABLE:
                    return self._parse_celtx_xml_with_bs(content)
                else:
                    return self._parse_celtx_xml_simple(content)
            except:
                # Fallback to plain text extraction
                logger.warning("Celtx XML parsing failed, using text extraction")
                return self._parse_plaintext(content)
                
        except Exception as e:
            logger.error(f"Celtx parsing error: {str(e)}")
            raise
    
    def _parse_celtx_zip(self, content: bytes) -> Dict[str, Any]:
        """Parse Celtx ZIP archive"""
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".celtx") as tmp_file:
                tmp_file.write(content)
                temp_file = tmp_file.name
            
            extracted_text = ""
            
            with zipfile.ZipFile(temp_file, "r") as zip_ref:
                # Look for screenplay files in the archive
                for file_name in zip_ref.namelist():
                    if "screenplay" in file_name.lower() or file_name.endswith(".html"):
                        with zip_ref.open(file_name) as f:
                            file_content = f.read().decode("utf-8", errors="ignore")
                            extracted_text += file_content + "\n"
            
            # Clean up temp file
            os.unlink(temp_file)
            
            # Parse extracted text
            if extracted_text:
                result = self._parse_plaintext(extracted_text)
                result["format_info"]["parser"] = "Celtx ZIP Archive"
                return result
            else:
                raise ValueError("No screenplay found in Celtx archive")
                
        except Exception as e:
            logger.error(f"Celtx ZIP parsing error: {str(e)}")
            raise
    
    def _parse_celtx_xml_with_bs(self, content: str) -> Dict[str, Any]:
        """Parse Celtx XML using BeautifulSoup"""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(content, "xml")
        
        scenes = []
        characters = set()
        
        # Look for scene elements (Celtx-specific structure)
        for scene_elem in soup.find_all(["scene", "div"]):
            header = scene_elem.get("heading", "")
            if not header:
                continue
            
            scene_text = []
            scene_chars = []
            
            # Extract dialogue and characters
            for elem in scene_elem.find_all(["character", "dialogue", "action"]):
                text = elem.get_text(strip=True)
                if text:
                    scene_text.append(text)
                    
                    if elem.name == "character":
                        char_name = self._clean_character_name(text)
                        if char_name:
                            characters.add(char_name)
                            scene_chars.append(char_name)
            
            if scene_text:
                scenes.append({
                    "header": header,
                    "content": scene_text,
                    "characters": scene_chars,
                    "scene_number": len(scenes) + 1
                })
        
        if not scenes:
            # Fallback to plain text extraction
            return self._parse_plaintext(content)
        
        return {
            "scenes": scenes,
            "scene_count": len(scenes),
            "characters": sorted(list(characters)),
            "metadata": ScriptMetadata(format_type="Celtx").__dict__,
            "format_info": {"parser": "Celtx XML (BeautifulSoup)"}
        }
    
    def _parse_celtx_xml_simple(self, content: str) -> Dict[str, Any]:
        """Simple Celtx XML parsing without BeautifulSoup"""
        # Extract text between scene markers
        scenes = []
        characters = set()
        
        # Simple regex-based extraction
        scene_pattern = re.compile(r'<scene[^>]*heading="([^"]*)"[^>]*>(.*?)</scene>', re.DOTALL)
        
        for match in scene_pattern.finditer(content):
            header = match.group(1)
            scene_content = match.group(2)
            
            # Extract lines
            lines = []
            scene_chars = []
            
            # Look for character elements
            char_matches = re.findall(r'<character[^>]*>([^<]+)</character>', scene_content)
            for char_text in char_matches:
                char_name = self._clean_character_name(char_text)
                if char_name:
                    characters.add(char_name)
                    scene_chars.append(char_name)
                    lines.append(char_text)
            
            # Extract other text
            text_matches = re.findall(r'>([^<]+)<', scene_content)
            lines.extend([t.strip() for t in text_matches if t.strip()])
            
            if lines:
                scenes.append({
                    "header": header,
                    "content": lines,
                    "characters": scene_chars,
                    "scene_number": len(scenes) + 1
                })
        
        if not scenes:
            return self._parse_plaintext(content)
        
        return {
            "scenes": scenes,
            "scene_count": len(scenes),
            "characters": sorted(list(characters)),
            "metadata": ScriptMetadata(format_type="Celtx").__dict__,
            "format_info": {"parser": "Celtx XML (Regex)"}
        }
    
    def _parse_fadein(self, content: Union[str, bytes]) -> Dict[str, Any]:
        """Parse Fade In screenplay format"""
        try:
            if isinstance(content, bytes):
                content = content.decode("utf-8")
            
            # Fade In can be XML or plain text
            if content.strip().startswith("<?xml"):
                return self._parse_fadein_xml(content)
            else:
                return self._parse_plaintext(content)
                
        except Exception as e:
            logger.error(f"Fade In parsing error: {str(e)}")
            return self._parse_plaintext(content if isinstance(content, str) 
                                       else content.decode("utf-8", errors="ignore"))
    
    def _parse_fadein_xml(self, content: str) -> Dict[str, Any]:
        """Parse Fade In XML format"""
        try:
            root = ET.fromstring(content)
            
            scenes = []
            characters = set()
            
            # Fade In XML structure
            for scene_elem in root.findall(".//scene"):
                header_elem = scene_elem.find("heading")
                if header_elem is None:
                    continue
                
                header = header_elem.text or ""
                scene_content = []
                scene_chars = []
                
                for elem in scene_elem:
                    if elem.tag == "character":
                        char_text = elem.text or ""
                        char_name = self._clean_character_name(char_text)
                        if char_name:
                            characters.add(char_name)
                            scene_chars.append(char_name)
                        scene_content.append(char_text)
                    elif elem.text:
                        scene_content.append(elem.text.strip())
                
                if scene_content:
                    scenes.append({
                        "header": header,
                        "content": scene_content,
                        "characters": scene_chars,
                        "scene_number": len(scenes) + 1
                    })
            
            if not scenes:
                return self._parse_plaintext(content)
            
            return {
                "scenes": scenes,
                "scene_count": len(scenes),
                "characters": sorted(list(characters)),
                "metadata": ScriptMetadata(format_type="Fade In").__dict__,
                "format_info": {"parser": "Fade In XML"}
            }
            
        except ET.ParseError:
            return self._parse_plaintext(content)
    
    def _parse_plaintext(self, content: Union[str, bytes]) -> Dict[str, Any]:
        """Enhanced plain text parser with smart scene detection"""
        try:
            if isinstance(content, bytes):
                content = content.decode("utf-8", errors="ignore")
            
            # Clean and normalize text
            content = self._normalize_text(content)
            
            lines = content.split("\n")
            scenes = []
            characters = set()
            current_scene = None
            scene_elements = []
            scene_number = 1
            
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                # Skip empty lines between scenes
                if not line and not current_scene:
                    i += 1
                    continue
                
                # Check for scene heading
                is_scene = False
                scene_header = ""
                
                # Multiple scene heading patterns
                if line.startswith("INT.") or line.startswith("EXT.") or line.startswith("INT/EXT."):
                    is_scene = True
                    scene_header = line
                elif line.startswith("SCENE"):
                    # Look ahead for location
                    look_ahead = min(i + 2, len(lines) - 1)
                    for j in range(i, look_ahead):
                        if "INT." in lines[j] or "EXT." in lines[j]:
                            is_scene = True
                            scene_header = lines[j]
                            i = j
                            break
                
                if is_scene:
                    # Save previous scene
                    if current_scene:
                        scenes.append(current_scene)
                    
                    # Parse new scene
                    location, time_of_day = self._parse_scene_heading(scene_header)
                    
                    current_scene = {
                        "header": scene_header,
                        "content": [scene_header],
                        "characters": [],
                        "location": location,
                        "time_of_day": time_of_day,
                        "scene_number": scene_number,
                        "elements": [{"text": scene_header, "type": "scene_heading"}]
                    }
                    scene_number += 1
                    
                    # Reset scene elements
                    scene_elements = [scene_header]
                
                # Character detection in current scene
                elif current_scene and self._is_character_line(line):
                    char_name = self._clean_character_name(line)
                    if char_name:
                        characters.add(char_name)
                        if char_name not in current_scene["characters"]:
                            current_scene["characters"].append(char_name)
                    
                    current_scene["content"].append(line)
                    current_scene["elements"].append({"text": line, "type": "character"})
                
                # Add other content to current scene
                elif current_scene and line:
                    current_scene["content"].append(line)
                    
                    # Classify element type
                    element_type = "action"  # default
                    if self.patterns["parenthetical"].match(line):
                        element_type = "parenthetical"
                    elif any(t in line.upper() for t in ["FADE", "CUT", "DISSOLVE", "SMASH", "MATCH"]):
                        element_type = "transition"
                    
                    current_scene["elements"].append({"text": line, "type": element_type})
                
                i += 1
            
            # Add last scene
            if current_scene:
                scenes.append(current_scene)
            
            # Fallback: if no scenes detected, treat as one scene
            if not scenes and content.strip():
                scenes = [{
                    "header": "SCRIPT",
                    "content": [line for line in content.split("\n") if line.strip()],
                    "characters": list(characters),
                    "scene_number": 1,
                    "elements": [{"text": line, "type": "action"} for line in content.split("\n") if line.strip()]
                }]
            
            return {
                "scenes": scenes,
                "scene_count": len(scenes),
                "characters": sorted(list(characters)),
                "metadata": ScriptMetadata(format_type="Plain Text").__dict__,
                "format_info": {
                    "parser": "Enhanced Plain Text",
                    "detection_method": "scene_heading_patterns",
                    "lines_processed": len(lines)
                }
            }
            
        except Exception as e:
            logger.error(f"Plain text parsing error: {str(e)}")
            return self._create_error_result("text", str(e))
    
    def detect_format(self, filename: str, content: Optional[Union[str, bytes]] = None) -> str:
        """
        Detect script format from filename and optionally content
        
        Args:
            filename: Original filename
            content: Optional file content for content-based detection
            
        Returns:
            Detected format string
        """
        # First, check file extension
        ext = filename.split(".")[-1].lower() if "." in filename else ""
        
        if ext in self.supported_formats:
            if content is not None:
                # Validate with content-based detection
                if self._validate_format(ext, content):
                    return ext
                else:
                    logger.warning(f"Extension {ext} doesn't match content, performing content detection")
            else:
                return ext
        
        # Content-based detection
        if content is not None:
            return self.detect_format_from_content(content)
        
        # Default to plain text
        return "text"
    
    def detect_format_from_content(self, content: Union[str, bytes]) -> str:
        """
        Detect format from content only
        
        Args:
            content: File content
            
        Returns:
            Detected format
        """
        sample = content[:5000] if isinstance(content, str) else content[:5000].decode("utf-8", errors="ignore")
        
        # Check each format
        for format_name, detector in self.format_detectors.items():
            if detector(sample):
                return format_name
        
        # Check for binary PDF
        if isinstance(content, bytes) and content[:4] == b"%PDF":
            return "pdf"
        
        # Default to plain text
        return "text"
    
    def _detect_fdx(self, sample: str) -> bool:
        """Detect Final Draft FDX format"""
        return "<?xml" in sample and ("FinalDraft" in sample or "FDX" in sample or 'ContentType="FinalDraft"' in sample)
    
    def _detect_celtx(self, sample: str) -> bool:
        """Detect Celtx format"""
        return ("<celtx" in sample.lower() or 
                "celtx:" in sample.lower() or 
                "application/vnd.celtx" in sample)
    
    def _detect_fountain(self, sample: str) -> bool:
        """Detect Fountain format"""
        # Check for Fountain front matter
        if sample.strip().startswith("title:"):
            return True
        
        # Check for scene headings
        scene_headings = re.findall(r"^(?:\.\s*)?(INT\.|EXT\.|INT/EXT\.)", sample, re.MULTILINE | re.IGNORECASE)
        return len(scene_headings) > 2  # Multiple scene headings indicate Fountain
    
    def _detect_pdf(self, sample: Union[str, bytes]) -> bool:
        """Detect PDF format"""
        if isinstance(sample, bytes):
            return sample[:4] == b"%PDF"
        return False
    
    def _detect_fadein(self, sample: str) -> bool:
        """Detect Fade In format"""
        return "Fade In" in sample or "fadein" in sample.lower()
    
    def _validate_format(self, format_name: str, content: Union[str, bytes]) -> bool:
        """Validate that content matches the claimed format"""
        if format_name == "fdx":
            return self._detect_fdx(content if isinstance(content, str) else content.decode("utf-8", errors="ignore"))
        elif format_name == "pdf":
            return self._detect_pdf(content)
        # For other formats, assume valid if extension matches
        return True
    
    def _extract_fdx_metadata(self, root: ET.Element) -> ScriptMetadata:
        """Extract metadata from FDX XML"""
        metadata = ScriptMetadata(format_type="Final Draft")
        
        # Look for title
        title_elem = root.find(".//Title")
        if title_elem is not None:
            metadata.title = title_elem.text or ""
        
        # Look for author
        author_elem = root.find(".//Author")
        if author_elem is not None:
            metadata.author = author_elem.text or ""
        
        # Version info
        revision_elem = root.find(".//Revision")
        if revision_elem is not None:
            metadata.version = revision_elem.text or ""
        
        return metadata
    
    def _extract_fountain_metadata(self, content: str) -> Tuple[ScriptMetadata, str]:
        """Extract metadata from Fountain front matter"""
        metadata = ScriptMetadata(format_type="Fountain")
        
        # Check for Fountain front matter (between --- or ===)
        front_matter_match = re.search(r"^(?:---|\+\+\+|\*\*\*)\s*\n(.*?)\n(?:---|\+\+\+|\*\*\*)\s*\n", content, re.DOTALL)
        
        if front_matter_match:
            front_matter = front_matter_match.group(1)
            body_start = front_matter_match.end()
            
            # Parse key-value pairs
            for line in front_matter.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip().lower()
                    value = value.strip()
                    
                    if key == "title":
                        metadata.title = value
                    elif key == "author":
                        metadata.author = value
                    elif key == "date":
                        metadata.date = value
                    elif key == "contact":
                        metadata.contact = value
                    elif key == "copyright":
                        metadata.copyright = value
            
            return metadata, content[body_start:]
        
        return metadata, content
    
    def _classify_fdx_element(self, paragraph_type: str, text: str) -> str:
        """Classify FDX paragraph type to standard element type"""
        type_map = {
            "Scene Heading": "scene_heading",
            "Action": "action",
            "Character": "character",
            "Dialogue": "dialogue",
            "Parenthetical": "parenthetical",
            "Transition": "transition",
            "Shot": "shot",
            "General": "action"
        }
        
        return type_map.get(paragraph_type, "action")
    
    def _parse_scene_heading(self, heading: str) -> Tuple[str, str]:
        """Parse location and time from scene heading"""
        location = ""
        time_of_day = "DAY"  # Default
        
        heading_upper = heading.upper()
        
        # Extract location
        if "INT." in heading_upper:
            location = "INTERIOR"
        elif "EXT." in heading_upper:
            location = "EXTERIOR"
        elif "INT/EXT." in heading_upper or "I/E." in heading_upper:
            location = "INTERIOR/EXTERIOR"
        elif "EST." in heading_upper:
            location = "ESTABLISHING"
        else:
            location = "UNKNOWN"
        
        # Extract time of day
        time_patterns = [
            ("NIGHT", "NIGHT"),
            ("DAY", "DAY"),
            ("MORNING", "MORNING"),
            ("EVENING", "EVENING"),
            ("DAWN", "DAWN"),
            ("DUSK", "DUSK"),
            ("SUNRISE", "DAWN"),
            ("SUNSET", "DUSK"),
            ("CONTINUOUS", "CONTINUOUS"),
            ("LATER", "LATER"),
            ("MOMENTS LATER", "MOMENTS LATER")
        ]
        
        for pattern, time in time_patterns:
            if pattern in heading_upper:
                time_of_day = time
                break
        
        return location, time_of_day
    
    def _clean_character_name(self, text: str) -> str:
        """Clean character name from text"""
        # Remove parentheticals
        text = re.sub(r"\s*\(.*\)\s*", "", text)
        # Clean extra whitespace
        text = self.patterns["clean_whitespace"].sub(" ", text).strip()
        return text
    
    def _is_character_line(self, line: str) -> bool:
        """Check if line is a character name"""
        # Must be mostly uppercase
        if not self.patterns["forced_uppercase"].match(line):
            return False
        
        # Not a scene heading
        if self.patterns["scene_heading"].match(line):
            return False
        
        # Not a transition
        if self.patterns["transition"].match(line):
            return False
        
        # Not too short or too long
        if len(line) < 2 or len(line) > 50:
            return False
        
        # Shouldn't contain certain words
        excluded_words = ["SCENE", "PAGE", "CONTINUED", "FADE", "CUT", "DISSOLVE"]
        if any(word in line.upper() for word in excluded_words):
            return False
        
        return True
    
    def _clean_pdf_text(self, text: str) -> str:
        """Clean text extracted from PDF"""
        # Remove page numbers
        text = re.sub(r"\n\s*\d+\s*\n", "\n", text)
        # Remove header/footer artifacts
        text = re.sub(r"^\s*Screenplay\s*\n", "", text, flags=re.MULTILINE)
        text = re.sub(r"^\s*Page \d+\s*\n", "", text, flags=re.MULTILINE)
        # Normalize whitespace
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\n\s*\n+", "\n\n", text)
        return text.strip()
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for parsing"""
        # Replace smart quotes
        text = text.replace("\u201c", "\"").replace("\u201d", "\"")
        text = text.replace("\u2018", "'").replace("\u2019", "'")
        # Normalize line endings
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        # Remove multiple empty lines
        text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
        return text
    
    def _scenes_to_dict(self, scenes: List[ScriptScene]) -> List[Dict[str, Any]]:
        """Convert ScriptScene objects to dictionary format"""
        scenes_data = []
        for scene in scenes:
            scene_dict = {
                "header": scene.header,
                "content": [e.text for e in scene.elements],
                "elements": [{"text": e.text, "type": e.element_type} for e in scene.elements],
                "characters": scene.characters,
                "location": scene.location,
                "time_of_day": scene.time_of_day,
                "scene_number": scene.scene_number,
                "metadata": scene.metadata
            }
            if scene.page_number:
                scene_dict["page_number"] = scene.page_number
            scenes_data.append(scene_dict)
        return scenes_data
    
    def _analyze_element_types(self, scenes: List[ScriptScene]) -> Dict[str, int]:
        """Analyze distribution of element types"""
        element_counts = {}
        for scene in scenes:
            for element in scene.elements:
                element_counts[element.element_type] = element_counts.get(element.element_type, 0) + 1
        return element_counts
    
    def _create_error_result(self, format_type: str, error: str) -> Dict[str, Any]:
        """Create error result structure"""
        return {
            "scenes": [],
            "scene_count": 0,
            "characters": [],
            "metadata": ScriptMetadata(format_type=format_type).__dict__,
            "format_info": {
                "detected_format": format_type,
                "error": error,
                "parser": "Error"
            },
            "processing_stats": {
                "error": error,
                "success": False
            }
        }

# Singleton instance for easy import
multi_parser = MultiParserLoader()

def load_script(content: Union[str, bytes], file_type: Optional[str] = None, 
                filename: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to load a script using the multi-format parser
    
    Args:
        content: Script content
        file_type: File format type (optional)
        filename: Original filename (optional)
        
    Returns:
        Parsed script data
    """
    return multi_parser.parse(content, file_type, filename)

def detect_file_format(filename: str, content: Optional[Union[str, bytes]] = None) -> str:
    """
    Convenience function to detect file format
    
    Args:
        filename: Name of the file
        content: Optional file content
        
    Returns:
        Detected format string
    """
    return multi_parser.detect_format(filename, content)

def get_supported_formats() -> Dict[str, str]:
    """
    Get dictionary of supported formats and their descriptions
    
    Returns:
        Dictionary of format: description
    """
    return multi_parser.supported_formats.copy()
