#!/usr/bin/env python3
"""
Simple example demonstrating the clean import interface for Prarabdha caching system

This shows how users can import specific cache classes directly from their modules.
"""

import time
import numpy as np

# Clean imports as requested
from prarabdha.chats import ChatCache
from prarabdha.audio import audioCache
from prarabdha.video import videoCache
from prarabdha.rag import RAGCache

def demo_chat_caching():
    """Demonstrate chat caching with clean import"""
    print("=== Chat Caching Demo ===")
    
    # Create chat cache
    chat_cache = ChatCache()
    
    # Cache a chat segment
    segment = {
        "content": "Hello, how can I help you with Python programming?",
        "user_id": "user123",
        "session_id": "session456",
        "timestamp": int(time.time()),
        "model": "gpt-4"
    }
    
    cache_key = chat_cache.cache_segment(segment)
    print(f"Cached chat segment with key: {cache_key}")
    
    # Retrieve the segment
    retrieved = chat_cache.get_segment_with_rag_fallback(segment)
    if retrieved:
        print(f"Retrieved: {retrieved['content']}")
    
    # Get stats
    stats = chat_cache.get_stats()
    print(f"Chat cache hit rate: {stats['hit_rate']:.2%}")
    print()

def demo_audio_caching():
    """Demonstrate audio caching with clean import"""
    print("=== Audio Caching Demo ===")
    
    # Create audio cache
    audio_cache = audioCache()
    
    # Cache audio features
    features = np.random.rand(13, 100)  # MFCC features
    feature_key = audio_cache.cache_audio_features(
        audio_id="audio1",
        feature_type="mfcc",
        features=features,
        metadata={"duration": 5.0, "sample_rate": 16000}
    )
    print(f"Cached audio features with key: {feature_key}")
    
    # Retrieve features
    retrieved = audio_cache.get_audio_features("audio1", "mfcc")
    if retrieved:
        print(f"Retrieved audio features shape: {retrieved.features.shape}")
    
    # Get stats
    stats = audio_cache.get_stats()
    print(f"Audio cache: {stats['total_audio_files']} files, {stats['total_features']} features")
    print()

def demo_video_caching():
    """Demonstrate video caching with clean import"""
    print("=== Video Caching Demo ===")
    
    # Create video cache
    video_cache = videoCache()
    
    # Cache video segment
    segment_key = video_cache.cache_video_segment(
        video_id="video1",
        segment_id="seg1",
        start_frame=0,
        end_frame=150,
        start_time=0.0,
        end_time=5.0,
        features=np.random.rand(768),
        metadata={"resolution": "1920x1080", "fps": 30}
    )
    print(f"Cached video segment with key: {segment_key}")
    
    # Retrieve segment
    retrieved = video_cache.get_video_segment("video1", "seg1")
    if retrieved:
        print(f"Retrieved video segment: {retrieved.video_id}:{retrieved.segment_id}")
    
    # Get stats
    stats = video_cache.get_stats()
    print(f"Video cache: {stats['total_videos']} videos, {stats['total_segments']} segments")
    print()

def demo_rag_caching():
    """Demonstrate RAG caching with clean import"""
    print("=== RAG Caching Demo ===")
    
    # Create RAG cache
    rag_cache = RAGCache()
    
    # Add document
    chunk_ids = rag_cache.add_document(
        document_id="doc1",
        content="Python is a high-level programming language known for its simplicity and readability.",
        metadata={"author": "John Doe", "topic": "programming"}
    )
    print(f"Added document with {len(chunk_ids)} chunks")
    
    # Search similar chunks
    similar_chunks = rag_cache.search_similar_chunks("What is Python?", k=2)
    print(f"Found {len(similar_chunks)} similar chunks")
    
    for i, (vector_id, similarity, metadata) in enumerate(similar_chunks):
        chunk = rag_cache.get_chunk(metadata.get('chunk_id', ''))
        if chunk:
            print(f"  {i+1}. Similarity: {similarity:.3f}")
            print(f"     Content: {chunk.content[:50]}...")
    
    # Get stats
    stats = rag_cache.get_stats()
    print(f"RAG cache: {stats['total_documents']} documents, {stats['total_chunks']} chunks")
    print()

def main():
    """Run all demos"""
    print("Prarabdha Clean Import Interface Demo")
    print("=" * 50)
    
    try:
        demo_chat_caching()
        demo_audio_caching()
        demo_video_caching()
        demo_rag_caching()
        
        print("All demos completed successfully!")
        print("\nImport examples:")
        print("from prarabdha.chats import ChatCache")
        print("from prarabdha.audio import audioCache")
        print("from prarabdha.video import videoCache")
        print("from prarabdha.rag import RAGCache")
        
    except Exception as e:
        print(f"Error running demos: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 