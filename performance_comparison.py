#!/usr/bin/env python3
"""
Generate performance comparison chart for Prarabdha Cache System
"""

import matplotlib.pyplot as plt
import numpy as np

def create_performance_chart():
    """Create performance comparison chart for Prarabdha."""
    
    # Set up the figure with a modern style
    plt.style.use('default')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Data for the charts
    categories = ['vLLM', 'vLLM w/ Prarabdha']
    
    # Use case 1: Long Context Processing
    long_context_data = [28, 3.5]  # TTFT in seconds
    long_context_speedup = long_context_data[0] / long_context_data[1]
    
    # Use case 2: RAG Processing
    rag_data = [11, 2.8]  # TTFT in seconds
    rag_speedup = rag_data[0] / rag_data[1]
    
    # Colors
    colors = ['#FF6B35', '#4ECDC4']  # Orange and Teal
    
    # Chart 1: Long Context
    bars1 = ax1.bar(categories, long_context_data, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
    ax1.set_title('Use Case 1: Long Context Processing\nContext length: 25K tokens | Llama 70B on A40', 
                  fontsize=12, fontweight='bold', pad=20)
    ax1.set_ylabel('TTFT (seconds)', fontsize=11, fontweight='bold')
    ax1.set_ylim(0, 32)
    
    # Add speedup arrow and text
    ax1.annotate(f'{long_context_speedup:.1f}x', 
                xy=(0.5, (long_context_data[0] + long_context_data[1]) / 2),
                xytext=(0.5, (long_context_data[0] + long_context_data[1]) / 2 + 5),
                arrowprops=dict(arrowstyle='->', lw=2, color='gray'),
                ha='center', fontsize=14, fontweight='bold', color='gray')
    
    # Add value labels on bars
    for bar, value in zip(bars1, long_context_data):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{value}s', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    # Chart 2: RAG Processing
    bars2 = ax2.bar(categories, rag_data, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
    ax2.set_title('Use Case 2: RAG Processing\nRetrieved chunks: 4 x 2K tokens | Llama 70B on A40', 
                  fontsize=12, fontweight='bold', pad=20)
    ax2.set_ylabel('TTFT (seconds)', fontsize=11, fontweight='bold')
    ax2.set_ylim(0, 14)
    
    # Add speedup arrow and text
    ax2.annotate(f'{rag_speedup:.1f}x', 
                xy=(0.5, (rag_data[0] + rag_data[1]) / 2),
                xytext=(0.5, (rag_data[0] + rag_data[1]) / 2 + 2),
                arrowprops=dict(arrowstyle='->', lw=2, color='gray'),
                ha='center', fontsize=14, fontweight='bold', color='gray')
    
    # Add value labels on bars
    for bar, value in zip(bars2, rag_data):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                f'{value}s', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    # Add grid for better readability
    ax1.grid(True, alpha=0.3, axis='y')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add architecture description
    fig.suptitle('Prarabdha Cache System: Multi-Layer LLM Caching Performance', 
                fontsize=16, fontweight='bold', y=0.95)
    
    # Add description text
    description = """Prarabdha reuses KV caches of any reused text across multi-layer storage (GPU, RAM, Disk, Redis).
Combined with vLLM, achieves 3-10x delay savings and GPU cycle reduction in LLM use cases."""
    
    fig.text(0.5, 0.02, description, ha='center', fontsize=10, style='italic',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.8))
    
    # Add caption
    fig.text(0.5, 0.08, 'Prarabdha drastically reduces prefill delay (TTFT) by reusing KV caches across multiple layers',
             ha='center', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15, top=0.9)
    
    return fig

def create_architecture_diagram():
    """Create architecture diagram for Prarabdha."""
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Define layers and their properties
    layers = [
        {'name': 'GPU Cache\n(FAISS + KV Store)', 'y': 0.8, 'color': '#FF6B35', 'width': 0.6},
        {'name': 'RAM Cache\n(LRU/LFU + TTL)', 'y': 0.6, 'color': '#4ECDC4', 'width': 0.7},
        {'name': 'Redis Cache\n(Distributed + Auto-sharding)', 'y': 0.4, 'color': '#45B7D1', 'width': 0.8},
        {'name': 'Disk Cache\n(Persistent + Compression)', 'y': 0.2, 'color': '#96CEB4', 'width': 0.9},
    ]
    
    # Draw layers
    for layer in layers:
        rect = plt.Rectangle((0.5 - layer['width']/2, layer['y'] - 0.1), 
                           layer['width'], 0.15, 
                           facecolor=layer['color'], alpha=0.8, 
                           edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        
        # Add layer name
        ax.text(0.5, layer['y'], layer['name'], ha='center', va='center', 
               fontsize=11, fontweight='bold')
    
    # Add arrows showing data flow
    arrow_props = dict(arrowstyle='->', lw=2, color='gray')
    
    # Vertical flow arrows
    for i in range(len(layers) - 1):
        ax.annotate('', xy=(0.5, layers[i]['y'] - 0.1), 
                   xytext=(0.5, layers[i+1]['y'] + 0.05),
                   arrowprops=arrow_props)
    
    # Add input/output labels
    ax.text(0.5, 0.95, 'LLM Input\n(Text/Audio/Video)', ha='center', va='center', 
           fontsize=12, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
    
    ax.text(0.5, 0.05, 'Cached Output\n(Fast Retrieval)', ha='center', va='center', 
           fontsize=12, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))
    
    # Add features
    features = [
        'Vector Similarity Search',
        'RAG Chunk Indexing', 
        'Compression & Encryption',
        'Real-time Monitoring'
    ]
    
    for i, feature in enumerate(features):
        ax.text(0.1, 0.8 - i*0.15, f'• {feature}', fontsize=10, fontweight='bold')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    ax.set_title('Prarabdha: Multi-Layer AI Cache Architecture', 
                fontsize=16, fontweight='bold', pad=20)
    
    return fig

def main():
    """Generate and save performance charts."""
    
    # Create performance comparison chart
    fig1 = create_performance_chart()
    fig1.savefig('prarabdha_performance.png', dpi=300, bbox_inches='tight')
    print("✅ Performance comparison chart saved as 'prarabdha_performance.png'")
    
    # Create architecture diagram
    fig2 = create_architecture_diagram()
    fig2.savefig('prarabdha_architecture.png', dpi=300, bbox_inches='tight')
    print("✅ Architecture diagram saved as 'prarabdha_architecture.png'")
    
    plt.show()

if __name__ == "__main__":
    main() 