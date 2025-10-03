#!/usr/bin/env python3
"""
Model Export Script

Export trained PPO model to ONNX format for efficient inference
on Raspberry Pi or other edge devices.
"""

import argparse
import os
import sys
import torch
import numpy as np
from stable_baselines3 import PPO


def export_to_onnx(model_path, output_path, opset_version=11):
    """
    Export PPO model to ONNX format
    
    Args:
        model_path: Path to trained PPO model (.zip)
        output_path: Output path for ONNX model (.onnx)
        opset_version: ONNX opset version
    """
    print(f"Loading model from: {model_path}")
    model = PPO.load(model_path)
    print("Model loaded successfully!")
    
    # Get the policy network
    policy = model.policy
    policy.eval()
    
    # Create dummy input
    obs_shape = model.observation_space.shape
    dummy_input = torch.randn(1, obs_shape[0])
    
    print(f"\nExporting model to ONNX...")
    print(f"Input shape: {dummy_input.shape}")
    print(f"Output path: {output_path}")
    
    # Export to ONNX
    torch.onnx.export(
        policy,
        dummy_input,
        output_path,
        export_params=True,
        opset_version=opset_version,
        do_constant_folding=True,
        input_names=['observation'],
        output_names=['action'],
        dynamic_axes={
            'observation': {0: 'batch_size'},
            'action': {0: 'batch_size'}
        }
    )
    
    print(f"✓ Model exported successfully to: {output_path}")
    
    # Verify the exported model
    try:
        import onnx
        import onnxruntime as ort
        
        print("\nVerifying exported model...")
        onnx_model = onnx.load(output_path)
        onnx.checker.check_model(onnx_model)
        print("✓ ONNX model is valid")
        
        # Test inference
        print("\nTesting ONNX inference...")
        ort_session = ort.InferenceSession(output_path)
        
        test_input = np.random.randn(1, obs_shape[0]).astype(np.float32)
        ort_inputs = {ort_session.get_inputs()[0].name: test_input}
        ort_outputs = ort_session.run(None, ort_inputs)
        
        print(f"✓ ONNX inference successful")
        print(f"  Input shape: {test_input.shape}")
        print(f"  Output shape: {ort_outputs[0].shape}")
        
    except ImportError:
        print("\nWarning: ONNX or ONNXRuntime not installed. Skipping verification.")
        print("Install with: pip install onnx onnxruntime")


def main():
    parser = argparse.ArgumentParser(
        description="Export trained PPO model to ONNX format"
    )
    
    parser.add_argument(
        "model_path",
        type=str,
        help="Path to trained PPO model (.zip file)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output path for ONNX model (default: model_path with .onnx extension)"
    )
    
    parser.add_argument(
        "--opset-version",
        type=int,
        default=11,
        help="ONNX opset version (default: 11)"
    )
    
    args = parser.parse_args()
    
    # Check if model exists
    if not os.path.exists(args.model_path):
        print(f"Error: Model file not found: {args.model_path}")
        sys.exit(1)
    
    # Determine output path
    if args.output is None:
        output_path = os.path.splitext(args.model_path)[0] + ".onnx"
    else:
        output_path = args.output
    
    # Export model
    export_to_onnx(args.model_path, output_path, args.opset_version)


if __name__ == "__main__":
    main()
