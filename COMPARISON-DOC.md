
Исследование качества решения NER open source и proprietary моделей

| model name | Jaccard similarity | type | Inference | Cost prompt (1M), rub | Cost answer (1M), rub |
|------------|---------------------|------|------|------|------|
| claude-3.5-sonnet | 0.63 | proprietary | bothub | 405 | 2025 |
| mistral-large-latest | 0.47 | proprietary | mistral | 197 | 591
| o3-mini | 0.45 | proprietary | bothub | 148,5 | 594 |
| ministral-3b-latest | 0.43 | proprietary | mistral | 3,53 | 3,53
| llama-3.1-405b-instruct | 0.52 | open source | bothub | 108 | 108 |
| qwen-2.5-7b-instruct | 0.49 | open source | bothub | 3,375 | 6,75 |
| llama-3.3-70b-instruct | 0.46 | open source | bothub | 16,2 | 40,5 |
| llama-3.1-8b-instruct | 0.36 | open source | bothub | 0 | 0 |
| gemma-2-2b-it | 0.28 | open source | local | 0 | 0 |
| deepseek-r1-distill-qwen-1.5b | 0.13 | open source | local | 0 | 0 |
| ministral-3b-instruct | 0.00 | open source | local | 0 | 0 |