#!/usr/bin/env python3
"""
Example usage of the Prarabdha caching system

This script demonstrates the basic functionality of the caching system
including chat segment caching, RAG search, and statistics.
"""

import json
import time
import numpy as np
from prarabdha import (
    SegmentCacheManager,
    SegmentCacheManagerFactory,
    ChunkIndex,
    AudioCache,
    VideoCache
)

def example_chat_caching():
    """Example of chat segment caching"""
    print("=== Chat Segment Caching Example ===")
    
    # Create cache manager
    cache_manager = SegmentCacheManagerFactory.create_default_manager()
    
    # Example chat segments
    segments = [
        {
            "content": "Hello, how can I help you today?",
            "user_id": "user123",
            "session_id": "session456",
            "timestamp": int(time.time()),
            "model": "gpt-4"
        },
        {
            "content": "I need help with Python programming",
            "user_id": "user123", 
            "session_id": "session456",
            "timestamp": int(time.time()),
            "model": "gpt-4"
        },
        {
            "content": "Sure! What specific Python question do you have?",
            "user_id": "assistant",
            "session_id": "session456", 
            "timestamp": int(time.time()),
            "model": "gpt-4"
        }
    ]
    
    # Cache segments
    for i, segment in enumerate(segments):
        cache_key = cache_manager.cache_segment(segment)
        print(f"Cached segment {i+1} with key: {cache_key}")
    
    # Retrieve segments
    for i, segment in enumerate(segments):
        retrieved = cache_manager.get_segment_with_rag_fallback(segment)
        if retrieved:
            print(f"Retrieved segment {i+1}: {retrieved['content'][:50]}...")
    
    # Get statistics
    stats = cache_manager.get_stats()
    print(f"Cache stats: {stats['hits']} hits, {stats['misses']} misses")
    print()

def example_rag_chunk_indexing():
    """Example of RAG chunk indexing"""
    print("=== RAG Chunk Indexing Example ===")
    
    # Create chunk index
    chunk_index = ChunkIndex()
    
    # Example documents
    documents = [
        {
            "id": "doc1",
            "content": "Python is a high-level programming language. It is known for its simplicity and readability. Python supports multiple programming paradigms including procedural, object-oriented, and functional programming.",
            "metadata": {"author": "John Doe", "topic": "programming"}
        },
        {
            "id": "doc2", 
            "content": "Machine learning is a subset of artificial intelligence. It involves training algorithms to make predictions or decisions based on data. Common techniques include supervised learning, unsupervised learning, and reinforcement learning.",
            "metadata": {"author": "Jane Smith", "topic": "AI"}
        }
    ]
    
    # Add documents to chunk index
    for doc in documents:
        chunk_ids = chunk_index.add_document(
            document_id=doc["id"],
            content=doc["content"],
            metadata=doc["metadata"]
        )
        print(f"Added document {doc['id']} with {len(chunk_ids)} chunks")
    
    # Search for similar chunks
    query = "What is Python programming?"
    similar_chunks = chunk_index.search_similar_chunks(query, k=3)
    
    print(f"Search results for '{query}':")
    for i, (vector_id, similarity, metadata) in enumerate(similar_chunks):
        chunk = chunk_index.get_chunk(metadata.get('chunk_id', ''))
        if chunk:
            print(f"  {i+1}. Similarity: {similarity:.3f}")
            print(f"     Content: {chunk.content[:100]}...")
    
    # Get statistics
    stats = chunk_index.get_stats()
    print(f"Chunk index stats: {stats['total_documents']} documents, {stats['total_chunks']} chunks")
    print()

def example_audio_caching():
    """Example of audio feature caching"""
    print("=== Audio Feature Caching Example ===")
    
    # Create audio cache
    audio_cache = AudioCache()
    
    # Example audio features (simulated)
    audio_features = [
        {
            "audio_id": "audio1",
            "feature_type": "mfcc",
            "features": np.random.rand(13, 100),  # 13 MFCC coefficients, 100 frames
            "metadata": {"duration": 5.0, "sample_rate": 16000}
        },
        {
            "audio_id": "audio2", 
            "feature_type": "spectrogram",
            "features": np.random.rand(128, 256),  # 128 frequency bins, 256 time frames
            "metadata": {"duration": 8.0, "sample_rate": 22050}
        }
    ]
    
    # Cache audio features
    for audio_feat in audio_features:
        feature_key = audio_cache.cache_audio_features(
            audio_id=audio_feat["audio_id"],
            feature_type=audio_feat["feature_type"],
            features=audio_feat["features"],
            metadata=audio_feat["metadata"]
        )
        print(f"Cached audio feature: {feature_key}")
    
    # Retrieve features
    for audio_feat in audio_features:
        retrieved = audio_cache.get_audio_features(
            audio_feat["audio_id"],
            audio_feat["feature_type"]
        )
        if retrieved:
            print(f"Retrieved audio feature: {retrieved.audio_id}:{retrieved.feature_type}")
    
    # Get statistics
    stats = audio_cache.get_stats()
    print(f"Audio cache stats: {stats['total_audio_files']} files, {stats['total_features']} features")
    print()

def example_video_caching():
    """Example of video segment caching"""
    print("=== Video Segment Caching Example ===")
    
    # Create video cache
    video_cache = VideoCache()
    
    # Example video segments (simulated)
    video_segments = [
        {
            "video_id": "video1",
            "segment_id": "seg1",
            "start_frame": 0,
            "end_frame": 150,
            "start_time": 0.0,
            "end_time": 5.0,
            "features": np.random.rand(768),  # Feature vector
            "metadata": {"resolution": "1920x1080", "fps": 30}
        },
        {
            "video_id": "video1",
            "segment_id": "seg2", 
            "start_frame": 150,
            "end_frame": 300,
            "start_time": 5.0,
            "end_time": 10.0,
            "features": np.random.rand(768),
            "metadata": {"resolution": "1920x1080", "fps": 30}
        }
    ]
    
    # Cache video segments
    for segment in video_segments:
        segment_key = video_cache.cache_video_segment(
            video_id=segment["video_id"],
            segment_id=segment["segment_id"],
            start_frame=segment["start_frame"],
            end_frame=segment["end_frame"],
            start_time=segment["start_time"],
            end_time=segment["end_time"],
            features=segment["features"],
            metadata=segment["metadata"]
        )
        print(f"Cached video segment: {segment_key}")
    
    # Retrieve segments
    for segment in video_segments:
        retrieved = video_cache.get_video_segment(
            segment["video_id"],
            segment["segment_id"]
        )
        if retrieved:
            print(f"Retrieved video segment: {retrieved.video_id}:{retrieved.segment_id}")
    
    # Get statistics
    stats = video_cache.get_stats()
    print(f"Video cache stats: {stats['total_videos']} videos, {stats['total_segments']} segments")
    print()

def main():
    """Run all examples"""
    print("Prarabdha Caching System Examples")
    print("=" * 50)
    
    try:
        example_chat_caching()
        example_rag_chunk_indexing()
        example_audio_caching()
        example_video_caching()
        
        print("All examples completed successfully!")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 