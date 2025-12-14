# Troubleshooting Guide

## GPU Issues

### Issue: CUDA Image Not Found During Build

**Problem**:
```
docker-compose -f infrastructure/docker/docker-compose.yml build --no-cache
...
ERROR [rag-service internal] load metadata for docker.io/nvidia/cuda:12.1-devel-ubuntu20.04
failed to resolve source metadata for docker.io/nvidia/cuda:12.1-devel-ubuntu20.04: not found
```

**Cause**:
- The specified CUDA base image (`nvidia/cuda:12.1-devel-ubuntu20.04`) does not exist in Docker Hub
- CUDA version mismatch between Dockerfile and available images

**Solution**:
1. **Use the correct CUDA image**:
   ```bash
   docker pull nvidia/cuda:12.6.0-devel-ubuntu22.04
   ```
   
2. **Verify the image is available**:
   ```bash
   docker images | grep nvidia/cuda
   ```
   
3. **Ensure PyTorch dependencies match the CUDA version**:
   ```dockerfile
   FROM nvidia/cuda:12.6.0-devel-ubuntu22.04 AS base-deps
   
   ARG TORCH_VERSION=2.7.1
   ARG CUDA_TAG=cu126
   
   RUN python3.11 -m pip install --no-cache-dir \
       torch==${TORCH_VERSION}+${CUDA_TAG} \
       torchvision==0.22.1+${CUDA_TAG} \
       torchaudio==${TORCH_VERSION}+${CUDA_TAG} \
       --index-url https://download.pytorch.org/whl/${CUDA_TAG}
   ```

4. **Verify GPU functionality**:
   ```bash
   docker run --rm --gpus all nvidia/cuda:12.6.0-devel-ubuntu22.04 nvidia-smi
   ```
   
5. **Then proceed with the build**:
   ```bash
   docker-compose -f infrastructure/docker/docker-compose.yml build --no-cache
   ```

**Note**: Always check the [NVIDIA Container Catalog](https://catalog.ngc.nvidia.com/containers) for available CUDA images before building.

### Issue: Video Card Model Detection

**Problem**:
GPU detected as `NVIDIA GeForce RTX 4060` instead of `NVIDIA GeForce RTX 4060 Ti` in container.

**Explanation**:
- This is normal behavior. NVIDIA uses the same device ID for the entire 4060 series
- Both RTX 4060 and RTX 4060 Ti are based on the AD107 chip
- The driver automatically applies optimal settings for your Ti variant
- Performance is not affected

**Verification**:
- Check VRAM: RTX 4060 Ti has 8GB, same as standard 4060
- Monitor GPU utilization - it will reflect the actual Ti performance
- The difference is in clock speeds and power limits, handled by the driver

---

## RAG Service Issues

### Issue: Long Initial Startup Time

**Problem**:
RAG service takes a long time to start (30+ minutes) during first run.

**Cause**:
- First-time indexing of PDF books (PHB, DMG, SRD)
- Generation of embeddings for all text chunks
- Resource-intensive process using CPU/GPU

**Solution**:
- Wait for completion - this happens only once
- Ensure chroma.db directory is mounted as a volume for persistence
- Subsequent startups will be fast

---

## Docker Issues

### Issue: Environment Variable Warnings

**Problem**:
```
time="2025-12-14T11:20:59+03:00" level=warning msg="The \"MINIO_ROOT_USER\" variable is not set. Defaulting to a blank string."
```

**Solution**:
Create a `.env` file in the project root:
```env
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
POSTGRES_USER=ai_dnd_user
POSTGRES_PASSWORD=ai_dnd_pass
POSTGRES_DB=ai_dnd
```

This eliminates warnings and ensures consistent configuration.