GPU usage
=========

Local GPU test
---------------

1) Build and run with NVIDIA GPU:

```
./docker/run_local_gpu.sh \
  ./local-model \
  ./test_input \
  ./outputs \
  dataset.kind=default \
  dataset.img_suffix=.png \
  dataset.pad_out_to_modulo=8 \
  out_ext=.png \
  refine=false \
  model.checkpoint=best_genpref.ckpt
```

RunPod image
------------

Dockerfile for GPU is `docker/Dockerfile.gpu` (CUDA 11.8). Build and push:

```
docker build -t <registry>/comics-inpaint:cu118 -f docker/Dockerfile.gpu .
docker push <registry>/comics-inpaint:cu118
```

Runtime command on RunPod container:

```
python3 /app/bin/predict.py \
  model.path=/data/checkpoint \
  indir=/data/input \
  outdir=/data/output \
  device=cuda \
  model.checkpoint=best_genpref.ckpt \
  dataset.kind=default \
  dataset.img_suffix=.png \
  dataset.pad_out_to_modulo=8 \
  out_ext=.png
```


