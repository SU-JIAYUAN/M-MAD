# M-MAD: Multidimensional Multi-Agent Debate for Advanced Machine Translation Evaluation

## **🤖** About M-MAD<a name="about"></a>

The **M-MAD** framework is a systematic LLM-based multi-agent framework for advanced LLM-as-a-judge MT evaluation. It operates in three stages:


1. **Dimension Partition**: Decomposing the heuristic MQM annotation guideline into distinct dimensions for independent LLM-as-a-judge assessments.
2. **Multi-Agent Debate**: conducting multi-agent debates within each dimension, harnessing LLMs' inherent knowledge, reasoning, and collaborative abilities.
3. **Final Judgement**: synthesizing the debated outcomes through a final judge agent to produce a comprehensive evaluation judgment.

![framework.png](asset/framework.png)

## Meta-evaluation
To run the meta-evaluation for the metrics, execute the following file:
```bash
/mt-metrics-eval/mt_metrics_eval/wmt23_metrics.ipynb
```