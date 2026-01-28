#!/usr/bin/env python3
"""
Whisper Dependency Diagnostic Script
Tests all critical dependencies for Whisper to work
"""

import subprocess
import sys

def test_command(cmd, name):
    """Test if a command is available."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ {name}: OK")
            return True
        else:
            print(f"❌ {name}: FAILED")
            print(f"   Error: {result.stderr[:200]}")
            return False
    except FileNotFoundError:
        print(f"❌ {name}: NOT FOUND")
        return False
    except Exception as e:
        print(f"❌ {name}: ERROR - {str(e)[:100]}")
        return False

def test_import(module_name, package_name=None):
    """Test if a Python module can be imported."""
    try:
        __import__(module_name)
        print(f"✅ Python module '{module_name}': OK")
        return True
    except ImportError as e:
        print(f"❌ Python module '{module_name}': NOT FOUND")
        if package_name:
            print(f"   Install with: pip install {package_name}")
        return False
    except Exception as e:
        print(f"⚠️  Python module '{module_name}': WARNING - {str(e)[:100]}")
        return False

def main():
    print("\n" + "="*60)
    print("  WHISPER DEPENDENCY DIAGNOSTIC")
    print("="*60 + "\n")
    
    results = {}
    
    # System-level dependencies
    print("System Dependencies:")
    print("-" * 60)
    results['ffmpeg'] = test_command(['ffmpeg', '-version'], 'ffmpeg')
    results['python'] = test_command([sys.executable, '--version'], 'Python')
    
    # Python packages
    print("\nPython Packages:")
    print("-" * 60)
    results['whisper'] = test_import('whisper', 'openai-whisper')
    results['fastapi'] = test_import('fastapi', 'fastapi')
    results['uvicorn'] = test_import('uvicorn', 'uvicorn')
    results['torch'] = test_import('torch', 'torch')
    results['groq'] = test_import('groq', 'groq')
    
    # GPU Detection
    print("\nOptional (GPU Acceleration):")
    print("-" * 60)
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        if cuda_available:
            print(f"✅ CUDA: AVAILABLE")
            print(f"   GPU: {torch.cuda.get_device_name(0)}")
        else:
            print(f"⚠️  CUDA: NOT AVAILABLE (will use CPU)")
    except:
        print(f"⚠️  CUDA: CANNOT DETECT (will use CPU)")
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY:")
    print("="*60)
    
    critical = ['ffmpeg', 'python', 'whisper']
    critical_ok = all(results.get(k, False) for k in critical)
    
    if critical_ok:
        print("✅ ALL CRITICAL DEPENDENCIES OK - Ready to use Whisper!")
    else:
        print("❌ CRITICAL DEPENDENCIES MISSING:")
        for dep in critical:
            if not results.get(dep, False):
                print(f"   - {dep}")
    
    print("\nTest Result:")
    for dep, status in results.items():
        status_str = "✅ OK" if status else "❌ MISSING"
        print(f"  {dep:15} {status_str}")
    
    print("\n" + "="*60)
    
    if not critical_ok:
        print("\n⚠️  NEXT STEPS:")
        if not results.get('ffmpeg'):
            print("  1. Install ffmpeg:")
            print("     Windows: choco install ffmpeg -y")
            print("     macOS:   brew install ffmpeg")
            print("     Linux:   sudo apt-get install ffmpeg")
        if not results.get('whisper'):
            print("  2. Install Whisper:")
            print("     pip install --upgrade openai-whisper")
        print("  3. Re-run this script to verify")
    
    return 0 if critical_ok else 1

if __name__ == "__main__":
    sys.exit(main())
