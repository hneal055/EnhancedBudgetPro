# Phase 13.0 - Emotional Intelligence Layer

**Status:** 🚧 In Development  
**Version:** 13.0.0 (Phase 13.1 - Hybrid MVP)  
**Start Date:** December 14, 2025  
**Approach:** Option C - Hybrid (Fast MVP → Proprietary Refinement)

---

## 🎯 Strategic Vision

Transform EnhancedBudgetPro into **PilotForgeAI** by adding emotional intelligence - the missing 10% that creates a category-defining moat.

**Core Insight:** Understanding a script's emotional DNA enables:
- Emotion-aware scheduling (high-intensity scenes require more time)
- Character emotional arc tracking (schedule sensitive scenes carefully)
- Crew fatigue prediction (cumulative emotional load)
- Budget adjustments for emotional complexity

---

## 📊 Two-Phase Approach

### Phase 13.1 - Fast MVP (Weeks 1-6)
**Goal:** Integrate proven NLP for immediate value

**Technology Stack:**
- HuggingFace Transformers (j-hartmann/emotion-english-distilroberta-base)
- 7 emotion categories: joy, sadness, anger, fear, surprise, disgust, neutral
- 95%+ accuracy on general text
- Fast inference (<100ms per line)

**Deliverables:**
- Week 1-2: Emotion detection engine
- Week 3-4: Integration with IngestEngine pipeline
- Week 5-6: Emotional Intelligence UI page

### Phase 13.2 - Proprietary Refinement (Months 2-6)
**Goal:** Build domain-specific competitive moat

**Custom Capabilities:**
- 25+ film/TV-specific emotions (betrayal, longing, dread, euphoria)
- Sarcasm and subtext detection
- Genre-aware emotion interpretation
- Character voice consistency tracking
- Ensemble emotional dynamics

**Timeline:**
- Months 2-4: Collect training data, label scripts
- Months 5-6: Train custom model, replace base layer

---

## 🏗️ Architecture

### Data Flow

```
Script Input (FDX/Fountain/PDF)
    ↓
IngestEngine (existing)
    ↓ {scenes, characters, dialogue, action}
    ↓
EmotionEngine (NEW) ← HuggingFace Transformers
    ↓ {line, character, emotion, intensity}
    ↓
EmotionalIntelligence (NEW)
    ↓ {character_arcs, scene_intensity, tension_patterns}
    ↓
AI Producer Mode (Phase 12.0 - enhanced)
    ↓ Emotion-aware insights
    ↓
UI Dashboard (NEW: Phase 13 page)
```

### Module Structure

```
src/
├── IngestEngine/           # Existing - no changes
├── AnalysisEngine/
│   ├── emotion_engine.py           # NEW: Core emotion detection
│   ├── emotional_intelligence.py   # NEW: Arc tracking, analytics
│   └── insight_engine.py           # ENHANCED: Add emotion insights
├── EmotionEngine/          # NEW MODULE
│   ├── __init__.py
│   ├── detector.py         # HuggingFace integration
│   ├── analyzer.py         # Scene-level analysis
│   ├── arc_tracker.py      # Character emotional arcs
│   └── models/             # Model cache
└── ExportEngine/           # ENHANCED: Add emotion exports

pages/
├── 13_AI_Producer_Mode.py  # ENHANCED: Add emotion insights
└── 14_Emotional_Intelligence.py  # NEW: Emotion dashboard
```

---

## 🎨 Phase 13.1 Technical Specification

### 1. EmotionEngine Core

**File:** `src/EmotionEngine/detector.py`

```python
from transformers import pipeline
from typing import Dict, List

class EmotionDetector:
    """
    HuggingFace-based emotion detection (Phase 13.1)
    Will be replaced/augmented with proprietary model in Phase 13.2
    """
    
    def __init__(self):
        # Load pre-trained model
        self.classifier = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            return_all_scores=True
        )
    
    def detect_emotion(self, text: str) -> Dict[str, float]:
        """
        Returns: {
            'emotion': 'anger',
            'intensity': 0.87,
            'all_scores': {
                'joy': 0.03, 'sadness': 0.05, 'anger': 0.87,
                'fear': 0.02, 'surprise': 0.01, 'disgust': 0.01, 'neutral': 0.01
            }
        }
        """
        
    def detect_batch(self, texts: List[str]) -> List[Dict]:
        """Batch processing for performance"""
```

### 2. Emotional Intelligence Analytics

**File:** `src/AnalysisEngine/emotional_intelligence.py`

```python
class EmotionalIntelligence:
    """
    Scene-level and character-level emotional analytics
    """
    
    def analyze_character_arc(self, character: str, scenes: List[Dict]) -> Dict:
        """
        Returns: {
            'character': 'Character A',
            'dominant_emotions': ['anger', 'fear'],
            'arc_type': 'redemption',  # or 'tragedy', 'growth', etc.
            'emotional_journey': [
                {'scene': 1, 'emotion': 'anger', 'intensity': 0.8},
                {'scene': 5, 'emotion': 'fear', 'intensity': 0.6},
                ...
            ],
            'arc_peaks': [7, 23, 45]  # Scene numbers with high intensity
        }
        """
    
    def analyze_scene_intensity(self, scene: Dict) -> Dict:
        """
        Returns: {
            'scene_id': 'scene_12',
            'emotional_intensity': 0.85,  # 0-1 scale
            'dominant_emotion': 'fear',
            'tension_level': 'HIGH',  # LOW/MEDIUM/HIGH/CRITICAL
            'complexity_score': 0.72,  # Multiple emotions = higher
            'dialogue_emotion_avg': 0.80,
            'action_emotion_avg': 0.65
        }
        """
    
    def detect_emotional_patterns(self, scenes: List[Dict]) -> Dict:
        """
        Returns: {
            'pattern_type': 'escalating_tension',  # or 'roller_coaster', 'flat', etc.
            'peak_scenes': [12, 34, 67],
            'valley_scenes': [5, 23, 45],
            'overall_intensity': 0.68,
            'genre_match': 'thriller'  # Based on emotion distribution
        }
        """
```

### 3. Integration with IngestEngine

**File:** `src/ScriptIngest.py` (enhanced)

```python
def run_full_analysis(script_path, output_dir, enable_emotion=True):
    """
    Enhanced with emotion detection (opt-in for Phase 13.1)
    """
    
    # Existing pipeline
    data = router.route_file(script_path)
    intel = character_intelligence(data)
    density = scene_density_analysis(data)
    
    # NEW: Emotion detection (Phase 13.1)
    if enable_emotion:
        from src.EmotionEngine.detector import EmotionDetector
        from src.AnalysisEngine.emotional_intelligence import EmotionalIntelligence
        
        detector = EmotionDetector()
        ei = EmotionalIntelligence()
        
        # Add emotions to each line
        emotion_data = detector.analyze_script(data)
        
        # Compute analytics
        character_arcs = ei.analyze_all_characters(emotion_data)
        scene_intensities = ei.analyze_all_scenes(emotion_data)
        patterns = ei.detect_emotional_patterns(emotion_data)
        
        results['emotions'] = emotion_data
        results['character_arcs'] = character_arcs
        results['scene_intensities'] = scene_intensities
        results['emotional_patterns'] = patterns
```

### 4. Enhanced AI Producer Mode

**File:** `src/AnalysisEngine/insight_engine.py` (enhanced)

Add new category: `EMOTIONAL = "emotional"`

```python
def _analyze_emotional_complexity(self, session_state: Dict):
    """NEW: Emotional intelligence insights"""
    
    scene_intensities = session_state.get("scene_intensities", {})
    character_arcs = session_state.get("character_arcs", {})
    schedule = session_state.get("schedule", {})
    
    # Insight: High-intensity scenes clustered together
    if self._detect_intensity_clustering(scene_intensities, schedule):
        self.insights.append(ProducerInsight(
            category=InsightCategory.EMOTIONAL,
            severity=InsightSeverity.WARNING,
            title="High-Intensity Scenes Clustered",
            description="3 emotionally intense scenes scheduled back-to-back on Day 7",
            data_points={
                "affected_scenes": [12, 13, 14],
                "avg_intensity": 0.87,
                "day": 7
            },
            recommendation="Consider spacing intense scenes across multiple days to prevent cast/crew burnout."
        ))
    
    # Insight: Character emotional arc peak scheduling
    for character, arc in character_arcs.items():
        peak_scenes = arc.get("arc_peaks", [])
        if self._check_peak_scheduling(peak_scenes, schedule):
            self.insights.append(ProducerInsight(
                category=InsightCategory.EMOTIONAL,
                severity=InsightSeverity.INFO,
                title=f"Emotional Arc Peak: {character}",
                description=f"{character}'s emotional journey peaks in Scene {peak_scenes[0]}",
                recommendation="Schedule extra time for this scene - actor will need emotional preparation."
            ))
```

---

## 📊 Data Contracts

### Emotion Detection Output

```python
{
    "line_id": "scene_1_line_3",
    "scene_id": "scene_1",
    "character": "Character A",
    "text": "I can't believe you did this to me!",
    "line_type": "dialogue",  # or "action"
    "emotion": {
        "primary": "anger",
        "intensity": 0.87,
        "secondary": "betrayal",  # Phase 13.2
        "all_scores": {
            "joy": 0.03,
            "sadness": 0.05,
            "anger": 0.87,
            "fear": 0.02,
            "surprise": 0.01,
            "disgust": 0.01,
            "neutral": 0.01
        }
    }
}
```

### Character Emotional Arc

```python
{
    "character": "Character A",
    "total_lines": 145,
    "dominant_emotions": ["anger", "fear", "sadness"],
    "arc_type": "redemption",  # ML-inferred
    "emotional_journey": [
        {"scene": 1, "emotion": "anger", "intensity": 0.8},
        {"scene": 5, "emotion": "anger", "intensity": 0.7},
        {"scene": 12, "emotion": "fear", "intensity": 0.9},  # PEAK
        {"scene": 20, "emotion": "sadness", "intensity": 0.6},
        {"scene": 35, "emotion": "joy", "intensity": 0.7}  # Resolution
    ],
    "arc_peaks": [12, 34],  # High-intensity moments
    "arc_valleys": [5, 28],  # Low-intensity moments
    "emotional_range": 0.85,  # 0-1, diversity of emotions
    "consistency_score": 0.92  # Voice consistency
}
```

### Scene Emotional Intensity

```python
{
    "scene_id": "scene_12",
    "heading": "INT. APARTMENT - NIGHT",
    "emotional_intensity": 0.87,  # 0-1 average of all lines
    "tension_level": "HIGH",  # LOW/MEDIUM/HIGH/CRITICAL
    "dominant_emotion": "fear",
    "emotion_distribution": {
        "fear": 0.65,
        "anger": 0.25,
        "sadness": 0.10
    },
    "complexity_score": 0.72,  # Multiple emotions = complex
    "dialogue_lines": 24,
    "action_lines": 8,
    "characters_present": ["A", "B", "C"],
    "estimated_shoot_time_multiplier": 1.3  # High intensity = more takes
}
```

---

## 🎨 UI Components (Phase 13.1)

### Page 14: Emotional Intelligence Dashboard

**Features:**
1. **Character Emotional Arcs** (Line charts)
2. **Scene Intensity Heatmap** (Color-coded stripboard)
3. **Emotion Distribution** (Pie charts per character)
4. **Tension Patterns** (Story-wide intensity curve)
5. **High-Risk Emotional Scenes** (Table with recommendations)

### Enhanced AI Producer Mode (Page 13)

**New Insight Category: Emotional**
- Intensity clustering warnings
- Character arc peak notifications
- Crew fatigue predictions
- Budget impact estimates

---

## 🧪 Testing Strategy

### Phase 13.1 Tests

```bash
# Unit tests
test_emotion_detector.py      # Test HuggingFace integration
test_emotional_intelligence.py # Test analytics logic
test_arc_detection.py          # Test character arc inference

# Integration tests
test_phase_13_1_integration.py # Full pipeline with emotions

# Validation
test_emotion_accuracy.py       # Compare against labeled data
```

### Test Scripts
- `samples/test_emotional_script.fountain` - High-intensity scenes
- `samples/test_character_arc.fdx` - Clear redemption arc
- `samples/test_flat_emotions.txt` - Low emotional variance

---

## 📦 Dependencies

### New Requirements (Phase 13.1)

```txt
# Emotion Detection
transformers>=4.35.0
torch>=2.1.0  # or tensorflow>=2.14.0
sentencepiece>=0.1.99

# Visualization
plotly>=5.18.0  # Already included
seaborn>=0.13.0  # For emotion heatmaps
```

### Model Download
First run will download ~500MB model from HuggingFace Hub

---

## 🚀 Implementation Timeline

### Week 1-2: Emotion Detection Engine
- Day 1-2: Setup EmotionEngine module structure
- Day 3-5: Integrate HuggingFace model
- Day 6-8: Build batch processing pipeline
- Day 9-10: Unit tests and validation

### Week 3-4: Integration & Analytics
- Day 11-13: Integrate with IngestEngine
- Day 14-16: Build emotional_intelligence.py analytics
- Day 17-18: Character arc detection logic
- Day 19-20: Scene intensity calculations

### Week 5-6: UI & Insights
- Day 21-23: Build Emotional Intelligence dashboard (Page 14)
- Day 24-26: Enhance AI Producer Mode with emotion insights
- Day 27-28: Add emotion exports (CSV/Excel)
- Day 29-30: End-to-end testing and documentation

---

## 🎯 Success Metrics (Phase 13.1)

### Technical
- ✅ Emotion detection accuracy >90% on test scripts
- ✅ Batch processing <5s for 120-page script
- ✅ Character arc detection matches manual labels 85%+
- ✅ Scene intensity correlates with manual ratings 0.8+ R²

### User Value
- ✅ Producers find 3+ actionable emotional insights per script
- ✅ Scheduling adjustments based on emotional intensity
- ✅ Budget estimates account for emotional complexity
- ✅ Clear ROI story for pilot customers

---

## 🔮 Phase 13.2 Preview (Proprietary Layer)

**What Makes It Proprietary:**
1. **25+ Film-Specific Emotions:** betrayal, dread, longing, euphoria, desperation
2. **Sarcasm Detection:** "Oh, that's just great" → anger, not joy
3. **Subtext Analysis:** "I'm fine" → fear/sadness (context-aware)
4. **Genre Calibration:** Same line reads differently in comedy vs. thriller
5. **Ensemble Dynamics:** Track emotional interplay between characters

**Training Data Sources:**
- Labeled film/TV scripts (purchase or license)
- IMDb scene descriptions with emotion tags
- Screenplay databases with critic reviews
- User feedback from Phase 13.1 usage

**Model Architecture:**
- Fine-tuned RoBERTa or GPT-based model
- Custom emotion taxonomy (25 categories)
- Context window: full scene (not just line)
- Multi-task learning: emotion + intensity + subtext

---

## 💰 Business Impact

### Phase 13.1 (MVP)
**Value Proposition:**
"The only production system that schedules based on emotional intensity, not just scene count."

**Use Cases:**
- Identify emotionally draining shoot days
- Budget for high-intensity scene complexity
- Protect actor mental health

### Phase 13.2 (Proprietary)
**Value Proposition:**
"PilotForgeAI's proprietary emotional intelligence understands your story better than human script supervisors."

**Competitive Moat:**
- No competitors have domain-specific emotion models
- Training data is expensive and time-consuming
- Network effects: more usage → better model

---

## 📝 Documentation Deliverables

- [x] Technical specification (this document)
- [ ] API reference for EmotionEngine
- [ ] Integration guide for existing modules
- [ ] User guide for Emotional Intelligence page
- [ ] Training guide for Phase 13.2 model

---

**Phase 13.0 Status:** 🚧 Week 1 Starting  
**Phase 13.1 Target:** MVP in 6 weeks  
**Phase 13.2 Target:** Proprietary model in 6 months

*"Understanding emotion is understanding story. Understanding story is understanding production."*
