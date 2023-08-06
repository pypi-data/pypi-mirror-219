import json
import os
from typing import Dict, List
import numpy
import onnxruntime as ort


class Tagger:
    UNKNOWN_KANJI_ID = 1
    UNKNOWN_NOKANJI_ID = 2
    KANJI_RANGE1 = (int('4E00', 16), int('9FFF', 16))
    KANJI_RANGE2 = (int('3400', 16), int('4DBF', 16))
    OUTPUT_NAME = '408'

    def __init__(self, num_threads: int=1):
        this_dir = os.path.dirname(__file__)
        with open(os.path.join(this_dir, 'config.json')) as fp:
            self.config = json.load(fp)
        self.id_to_pos = ['[PAD]', '前文字と同じ単語内'] + self.config['parts_of_speech']
        self.char_to_id = {c: i + 3 for i, c in enumerate(self.config['chars'])}

        session_options = ort.SessionOptions()
        session_options.intra_op_num_threads = 1
        session_options.inter_op_num_threads = 1
        model_file = os.path.join(this_dir, 'model.onnx')
        self.ort_session = ort.InferenceSession(model_file, session_options)

        self.token_type_ids = numpy.array([[0] * self.config['max_position_embeddings']], dtype=numpy.int64)

    def parse(self, text: str) -> str:
        text = text.strip()
        if len(text) > self.config['max_position_embeddings']:
            raise RuntimeError(f"Input text length must be {self.config['max_position_embeddings']} or less.")

        session_input = self.encode(text)
        session_result = self.ort_session.run([self.OUTPUT_NAME], session_input)
        return self.decode(text, session_result[0][0])

    def encode(self, text: str) -> Dict[str, numpy.ndarray]:
        input_ids = []
        for c in text:
            if c in self.char_to_id:
                input_ids.append(self.char_to_id[c])
                continue
            _c = ord(c)
            if self.KANJI_RANGE1[0] <= _c <= self.KANJI_RANGE1[1] or self.KANJI_RANGE2[0] <= _c <= self.KANJI_RANGE2[1]:
                input_ids.append(self.UNKNOWN_KANJI_ID)
            else:
                input_ids.append(self.UNKNOWN_NOKANJI_ID)

        input_length = len(input_ids)
        padding_length = self.config['max_position_embeddings'] - input_length
        input_ids += [0] * padding_length
        attention_mask = [1] * input_length + [0] * padding_length
        session_input = {
            'input.1': numpy.array([input_ids], dtype=numpy.int64),
            'onnx::Unsqueeze_1': numpy.array([attention_mask], dtype=numpy.int64),
            'input.3': self.token_type_ids
        }
        return session_input


    def decode(self, text: str, pos_ids: numpy.ndarray) -> str:
        tokens = []
        word = []
        pos = ''
        for char, pos_id in zip(text, pos_ids):
            if pos_id == 0:
                if pos:
                    tokens.append((''.join(word), pos))
                    pos = ''
                    word = []
                tokens.append((' ', '[PAD]'))
            elif pos_id == 1:
                word.append(char)
            else:
                if pos:
                    tokens.append((''.join(word), pos))
                word = [char]
                pos = self.id_to_pos[pos_id]
        if pos:
            tokens.append((''.join(word), pos))
        return tokens
