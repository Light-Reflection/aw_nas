A Surgery of the Neural Architecture Evaluators
--------

### Run one-shot training on NAS-Bench-201

#### Train one-shot models

`cp examples/research/surgery/data/* $AWNAS/nasbench-201/`

`awnas search --gpu 0 --seed [random seed] --save-every 50 --train-dir results/oneshot-example/ examples/research/surgery/oneshot.yaml`

One can modify the configurations in `oneshot.yaml`, for example, 1) To use N architecture samples in every supernet update, change `evaluator_cfg.mepa_samples` to N; 2) To use de-isomorphism sampling, add `deiso: true` and the architecture list file in the controller component cfg, as follows

```
controller_type: nasbench-201-rs
controller_cfg:
  rollout_type: nasbench-201
  deiso: true
  text_file: examples/research/surgery/data/non-isom.txt
  mode: eval
```

#### Derive samples on one-shot models

`awnas derive --load results/oneshot-example/1000/ --out-file results/oneshot-example/derive_results.yaml --gpu 0 -n 6466 --test --seed [random seed] --runtime-save examples/research/surgery/oneshot_derive.yaml`

#### Get the evaluation results

`python evaluation.py results/oneshot-example/derive_results.yaml --type iso`

> Note that, several data files are used in the evaluation script and the de-isomorphism sampling (`examples/research/surgery/data/non-isom.txt`). These files (`non-isom.txt`, `iso_dict.yaml`, `iso_dict.txt`, `deiso_dict.txt`) should be downloaded from [this url](https://cloud.tsinghua.edu.cn/d/97a8f29e58cc4e87a3d3/).

### Run predictor training on NAS-Bench-201
