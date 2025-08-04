#!/usr/bin/env python3
"""
Multimodal Caching Demo
Demonstrates the comprehensive multimodal caching system
"""

import numpy as np
import time
from prarabdha.multimodal_cache_manager import MultimodalCacheManager
from prarabdha.advanced_multimodal_cache import AdvancedMultimodalCache


def demo_multimodal_caching():
    """Demo basic multimodal caching."""
    print("🚀 Multimodal Caching Demo")
    print("=" * 50)
    
    # Initialize cache manager
    cache = MultimodalCacheManager(similarity_threshold=0.85)
    
    # Cache text content
    print("\n📝 Caching text content...")
    text_result = cache.cache_text(
        "Explain quantum computing",
        "Quantum computing uses quantum mechanical phenomena to process information...",
        {"topic": "quantum", "difficulty": "intermediate"}
    )
    print(f"✅ Cached text: {text_result['entry_id']}")
    
    # Cache video frame
    print("\n🎥 Caching video frame...")
    frame = np.random.rand(224, 224, 3)  # Simulated video frame
    video_result = cache.cache_video_frame(
        frame,
        "A person walking in a park",
        {"scene": "outdoor", "action": "walking"}
    )
    print(f"✅ Cached video: {video_result['entry_id']}")
    
    # Cache audio segment
    print("\n🎵 Caching audio segment...")
    waveform = np.random.rand(16000)  # 1 second audio at 16kHz
    audio_result = cache.cache_audio_segment(
        waveform,
        16000,
        "Speech about artificial intelligence",
        {"content": "speech", "topic": "AI"}
    )
    print(f"✅ Cached audio: {audio_result['entry_id']}")
    
    # Test retrieval
    print("\n🔍 Testing retrieval...")
    
    # Text retrieval
    text_response = cache.get_text("Explain quantum computing")
    print(f"📝 Text response: {text_response[:50]}...")
    
    # Video retrieval
    video_response = cache.get_video_frame(frame)
    print(f"🎥 Video response: {video_response}")
    
    # Audio retrieval
    audio_response = cache.get_audio_segment(waveform, 16000)
    print(f"🎵 Audio response: {audio_response}")
    
    # Cross-modal search
    print("\n🔍 Cross-modal search...")
    results = cache.cross_modal_search("person", modality='all')
    print(f"Found {len(results)} results for 'person'")
    
    # Get statistics
    stats = cache.get_stats()
    print(f"\n📊 Cache Statistics:")
    print(f"  Total entries: {stats['total_entries']}")
    print(f"  Hit rate: {stats['hit_rate']:.2%}")
    print(f"  Text hits: {stats['text_hits']}")
    print(f"  Video hits: {stats['video_hits']}")
    print(f"  Audio hits: {stats['audio_hits']}")
    print(f"  Cross-modal hits: {stats['cross_modal_hits']}")


def demo_advanced_features():
    """Demo advanced features including prefill reuse and adaptive TTL."""
    print("\n🚀 Advanced Features Demo")
    print("=" * 50)
    
    # Initialize advanced cache
    advanced_cache = AdvancedMultimodalCache(
        max_memory_gb=32.0,
        similarity_threshold=0.85,
        enable_prefill_reuse=True,
        enable_adaptive_ttl=True,
        enable_heavy_input=True
    )
    
    # Simulate token prefill reuse
    print("\n🔄 Token Prefill Reuse Demo...")
    
    # Create sample tokens and KV cache
    tokens = [1000, 1001, 1002, 1003, 1004]
    kv_cache = {
        'layer_0': np.random.rand(32, 768).astype(np.float32),
        'layer_1': np.random.rand(32, 768).astype(np.float32)
    }
    
    # Cache with prefill
    prefill_result = advanced_cache.cache_text_with_prefill(
        prompt="Explain quantum computing",
        response="Quantum computing uses quantum mechanical phenomena...",
        tokens=tokens,
        kv_cache=kv_cache,
        user_id="user_123",
        session_id="session_456",
        user_priority=2,
        metadata={"topic": "quantum", "complexity": "high"}
    )
    print(f"✅ Cached with prefill: {prefill_result['entry_id']}")
    
    # Retrieve with prefill
    retrieved = advanced_cache.get_text_with_prefill(
        prompt="Explain quantum computing",
        tokens=tokens,
        user_id="user_123"
    )
    
    if retrieved:
        print(f"🔄 Retrieved with prefill reuse:")
        print(f"  Response: {retrieved['response'][:50]}...")
        print(f"  Cache type: {retrieved['cache_type']}")
        if 'prefix_tokens' in retrieved:
            print(f"  Prefix tokens: {len(retrieved['prefix_tokens'])}")
        if 'kv_cache' in retrieved:
            print(f"  KV cache layers: {len(retrieved['kv_cache'])}")
    
    # Test adaptive TTL
    print("\n⏰ Adaptive TTL Demo...")
    
    # Cache with different priorities
    high_priority_result = advanced_cache.cache_text_with_prefill(
        prompt="Important system configuration",
        response="System configuration details...",
        tokens=[2000, 2001, 2002],
        kv_cache={'layer_0': np.random.rand(32, 768).astype(np.float32)},
        user_id="admin",
        user_priority=5,  # High priority
        metadata={"type": "system", "priority": "high"}
    )
    
    low_priority_result = advanced_cache.cache_text_with_prefill(
        prompt="Temporary debug info",
        response="Debug information...",
        tokens=[3000, 3001],
        kv_cache={'layer_0': np.random.rand(32, 768).astype(np.float32)},
        user_id="developer",
        user_priority=1,  # Low priority
        metadata={"type": "debug", "priority": "low"}
    )
    
    print(f"✅ High priority TTL: {high_priority_result.get('ttl_prediction', 'N/A')}s")
    print(f"✅ Low priority TTL: {low_priority_result.get('ttl_prediction', 'N/A')}s")
    
    # Test heavy input optimization
    print("\n⚡ Heavy Input Optimization Demo...")
    
    # Batch operations
    batch_data = [
        ("What is machine learning?", "Machine learning is a subset of AI..."),
        ("Explain neural networks", "Neural networks are computational models..."),
        ("What is deep learning?", "Deep learning uses multiple layers..."),
        ("Explain computer vision", "Computer vision enables machines to see..."),
        ("What is NLP?", "Natural Language Processing enables...")
    ]
    
    if advanced_cache.heavy_input_cache:
        batch_results = advanced_cache.heavy_input_cache.batch_put(batch_data)
        print(f"✅ Batch cached {len(batch_results)} items")
        
        # Batch retrieval
        prompts = ["What is machine learning?", "Explain neural networks"]
        responses = advanced_cache.heavy_input_cache.batch_get(prompts)
        print(f"🔄 Batch retrieved {len(responses)} responses")
    
    # Get comprehensive statistics
    stats = advanced_cache.get_stats()
    print(f"\n📊 Advanced Cache Statistics:")
    print(f"  Total entries: {stats['total_entries']}")
    print(f"  Hit rate: {stats['hit_rate']:.2%}")
    print(f"  Prefill hits: {stats['prefill_hits']}")
    print(f"  Adaptive TTL hits: {stats['adaptive_ttl_hits']}")
    print(f"  Heavy input hits: {stats['heavy_input_hits']}")
    print(f"  Multimodal hits: {stats['multimodal_hits']}")
    
    # Feature status
    features = stats['features_enabled']
    print(f"\n🔧 Features Enabled:")
    print(f"  Prefill reuse: {features['prefill_reuse']}")
    print(f"  Adaptive TTL: {features['adaptive_ttl']}")
    print(f"  Heavy input: {features['heavy_input']}")


def demo_performance_comparison():
    """Demo performance comparison between different cache types."""
    print("\n⚡ Performance Comparison Demo")
    print("=" * 50)
    
    # Test different cache configurations
    configs = [
        ("Basic", MultimodalCacheManager(similarity_threshold=0.85)),
        ("Advanced", AdvancedMultimodalCache(
            max_memory_gb=32.0,
            similarity_threshold=0.85,
            enable_prefill_reuse=True,
            enable_adaptive_ttl=True,
            enable_heavy_input=True
        ))
    ]
    
    test_prompts = [
        "Explain quantum computing",
        "What is machine learning?",
        "How do neural networks work?",
        "Explain computer vision",
        "What is natural language processing?"
    ]
    
    for name, cache in configs:
        print(f"\n🧪 Testing {name} Cache...")
        
        start_time = time.time()
        
        # Cache operations
        for i, prompt in enumerate(test_prompts):
            if hasattr(cache, 'cache_text'):
                cache.cache_text(prompt, f"Response {i+1} for {prompt}")
            elif hasattr(cache, 'cache_text_with_prefill'):
                tokens = [1000 + i, 1001 + i, 1002 + i]
                kv_cache = {'layer_0': np.random.rand(32, 768).astype(np.float32)}
                cache.cache_text_with_prefill(
                    prompt, f"Response {i+1} for {prompt}",
                    tokens, kv_cache, "test_user"
                )
        
        cache_time = time.time() - start_time
        
        # Retrieval operations
        start_time = time.time()
        hits = 0
        for prompt in test_prompts:
            if hasattr(cache, 'get_text'):
                result = cache.get_text(prompt)
            elif hasattr(cache, 'get_text_with_prefill'):
                tokens = [1000, 1001, 1002]
                result = cache.get_text_with_prefill(prompt, tokens, "test_user")
            if result:
                hits += 1
        
        retrieval_time = time.time() - start_time
        
        # Get stats
        stats = cache.get_stats()
        
        print(f"  Cache time: {cache_time:.4f}s")
        print(f"  Retrieval time: {retrieval_time:.4f}s")
        print(f"  Hit rate: {stats.get('hit_rate', 0):.2%}")
        print(f"  Total entries: {stats.get('total_entries', 0)}")


def main():
    """Run all demos."""
    print("🎯 Prarabdha Multimodal Caching System Demo")
    print("=" * 60)
    
    try:
        # Basic multimodal caching
        demo_multimodal_caching()
        
        # Advanced features
        demo_advanced_features()
        
        # Performance comparison
        demo_performance_comparison()
        
        print("\n✅ All demos completed successfully!")
        print("\n🚀 Key Features Demonstrated:")
        print("  • Multimodal caching (text, video, audio)")
        print("  • Cross-modal search capabilities")
        print("  • Token prefill reuse with KV cache")
        print("  • Adaptive TTL with ML-based prediction")
        print("  • Heavy input optimization with batch operations")
        print("  • Intelligent eviction and semantic clustering")
        print("  • Real-time performance monitoring")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 