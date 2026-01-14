"""NLP service for text processing and summarization (FREE)"""
import os
import re
import asyncio
from collections import Counter
from dotenv import load_dotenv

load_dotenv()


def clean_transcript(text: str) -> str:
    """
    Clean transcript by removing filler words and fixing formatting
    
    Args:
        text: Raw transcript text
        
    Returns:
        Cleaned transcript text
    """
    # Remove common filler words
    filler_words = [
        r'\bum\b', r'\buh\b', r'\blike\b', r'\byou know\b', 
        r'\bso\b', r'\bbasically\b', r'\bactually\b'
    ]
    
    cleaned = text
    for filler in filler_words:
        cleaned = re.sub(filler, '', cleaned, flags=re.IGNORECASE)
    
    # Remove extra spaces
    cleaned = re.sub(r'\s+', ' ', cleaned)
    
    # Fix spacing around punctuation
    cleaned = re.sub(r'\s+([.,!?])', r'\1', cleaned)
    
    return cleaned.strip()


async def generate_summary(transcript: str) -> dict:
    """
    Generate meeting summary using extractive summarization
    
    Args:
        transcript: Meeting transcript text
        
    Returns:
        dict with 'summary', 'key_points', and 'action_items'
    """
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, _generate_summary_sync, transcript)
        return result
    
    except Exception as e:
        raise Exception(f"Summarization failed: {str(e)}")


def _generate_summary_sync(transcript: str) -> dict:
    """Synchronous summarization helper using extractive method"""
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', transcript)
    sentences = [s.strip() for s in sentences if len(s.strip().split()) > 3]
    
    if not sentences:
        return {
            "summary": "No content to summarize",
            "key_points": ["No content available"],
            "action_items": ["No action items found"]
        }
    
    # Extract top sentences for summary (first, middle, last significant sentences)
    num_sentences = min(5, len(sentences))
    summary_sentences = []
    
    if len(sentences) > 0:
        summary_sentences.append(sentences[0])  # First sentence
    if len(sentences) > 2:
        summary_sentences.append(sentences[len(sentences)//2])  # Middle
    if len(sentences) > 1:
        summary_sentences.append(sentences[-1])  # Last
    
    # Score remaining sentences by word frequency
    words = ' '.join(sentences).lower().split()
    word_freq = Counter(words)
    
    # Remove common words
    stop_words = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but', 'in', 'with', 'to', 'for', 'of', 'as', 'by', 'from'}
    for word in stop_words:
        word_freq.pop(word, None)
    
    # Get most important sentences based on word frequency
    sentence_scores = []
    for sentence in sentences:
        score = sum(word_freq.get(word.lower(), 0) for word in sentence.split())
        sentence_scores.append((score, sentence))
    
    # Sort and get top sentences
    sentence_scores.sort(reverse=True)
    top_sentences = [s[1] for s in sentence_scores[:num_sentences]]
    
    full_summary = '. '.join(summary_sentences[:3]) + '.'
    
    # Extract key points (sentences with keywords)
    key_points = _extract_key_points(transcript)
    
    # Extract action items (sentences with action verbs)
    action_items = _extract_action_items(transcript)
    
    return {
        "summary": full_summary,
        "key_points": key_points,
        "action_items": action_items
    }


def _extract_key_points(text: str) -> list[str]:
    """Extract key points from text"""
    sentences = re.split(r'[.!?]+', text)
    keywords = ['important', 'key', 'main', 'significant', 'critical', 'essential', 
                'decided', 'agreed', 'concluded', 'discussed']
    
    key_points = []
    for sentence in sentences:
        sentence = sentence.strip()
        if any(keyword in sentence.lower() for keyword in keywords) and len(sentence.split()) > 5:
            key_points.append(sentence)
            if len(key_points) >= 5:  # Limit to top 5
                break
    
    return key_points if key_points else ["No specific key points identified"]


def _extract_action_items(text: str) -> list[str]:
    """Extract action items from text"""
    sentences = re.split(r'[.!?]+', text)
    action_verbs = ['will', 'should', 'need to', 'must', 'have to', 'going to',
                   'plan to', 'follow up', 'schedule', 'assign', 'complete']
    
    action_items = []
    for sentence in sentences:
        sentence = sentence.strip()
        if any(verb in sentence.lower() for verb in action_verbs) and len(sentence.split()) > 5:
            action_items.append(sentence)
            if len(action_items) >= 5:  # Limit to top 5
                break
    
    return action_items if action_items else ["No specific action items identified"]
