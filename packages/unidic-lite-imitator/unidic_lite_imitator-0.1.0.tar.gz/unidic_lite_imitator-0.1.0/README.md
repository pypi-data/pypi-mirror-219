# Unidic Lite Imitator

This package imitates Japanese morphological analysis of mecab and unidic_lite with a small onnx model.  
You can add tokenization and part-of-speech estimation to your environment  
with only 2MB additoinal disk space if you already have onnxruntime in your environment.

## Installation

```
$ pip install unidic_lite_imitator
```

## Usage Examples

```python
>> import unidic_lite_imitator
>> tagger = unidic_lite_imitator.Tagger()
>> sample_text = '使い方のサンプルです。'
>> tagger.parse(sample_text)
[('使い', '動詞'), ('方', '接尾辞'), ('の', '助詞'), ('サンプル', '名詞'), ('です', '助動詞'), ('。', '補助記号')]
```

Input string length must be 192 or less.
