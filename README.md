# M-MAD: Multidimensional Multi-Agent Debate for Advanced Machine Translation Evaluation

The code for M-MAD will be released upon acceptance of the paper. Stay tuned for updates!

## **🤖** About M-MAD<a name="about"></a>

The **M-MAD** framework is a systematic LLM-based multi-agent framework for advanced LLM-as-a-judge MT evaluation. It operates in three stages:

1. **Dimension Partition**: Decomposing the heuristic MQM annotation guideline into distinct dimensions for independent LLM-as-a-judge assessments.
2. **Multi-Agent Debate**: Conducting multi-agent debates within each dimension, harnessing LLMs' inherent knowledge, reasoning, and collaborative abilities.
3. **Final Judgement**: Synthesizing the debated outcomes through a final judge agent to produce a comprehensive evaluation judgment.

![framework.png](asset/framework.png)

## **📄** Paper

For a detailed explanation of the M-MAD framework, please refer to the paper:  
[Multidimensional Multi-Agent Debate for Advanced Machine Translation Evaluation (arXiv)](https://arxiv.org/pdf/2412.20127)

## **💻** Running the Code
### Stage 1 (Dimension Partition)

```bash
sh run_stage1.sh
```

### Stage 2 & 3 (Muti-Agent Debate & Final Judgement)

To run the meta-evaluation for the metrics, execute the following file:

```bash
sh run_stage2_3.sh
```

### Meta-evaluation

To run the meta-evaluation for the metrics, execute the following file:

```bash
wmt23_metrics.ipynb
```

## Citation

```
@article{feng2024mmad,
  title={M-MAD: Multidimensional Multi-Agent Debate Framework for Fine-grained Machine Translation Evaluation},
  author={Feng, Zhaopeng and Su, Jiayuan and Zheng, Jiamei and Ren, Jiahan and Zhang, Yan and Wu, Jian and Wang, Hongwei and Liu, Zuozhu},
  journal={arXiv preprint arXiv:2412.20127},
  year={2024}
}
```