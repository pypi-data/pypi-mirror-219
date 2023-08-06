import json
import os
from typing import Dict, List
import torch
from transformers import AlbertConfig, AlbertModel, AlbertForMaskedLM
from transformers.models.albert.modeling_albert import AlbertMLMHead


class PartOfSpeechEstimator(AlbertForMaskedLM):
    def __init__(self, config: AlbertConfig):
        # Call grandparents' init
        super(AlbertForMaskedLM, self).__init__(config)

        self.albert = AlbertModel(config, add_pooling_layer=False)
        _config = config.to_dict()
        _config['vocab_size'] = len(_config['parts_of_speech']) + 2
        self.predictions = AlbertMLMHead(AlbertConfig(**_config))

        # Initialize weights and apply final processing
        self.post_init()


class Tagger:
    UNKNOWN_KANJI_ID = 1
    UNKNOWN_NOKANJI_ID = 2
    KANJI_RANGE1 = (int('4E00', 16), int('9FFF', 16))
    KANJI_RANGE2 = (int('3400', 16), int('4DBF', 16))

    def __init__(self, num_threads: int=1):
        this_dir = os.path.dirname(__file__)
        self.config = AlbertConfig.from_json_file(os.path.join(this_dir, 'config.json'))
        self.id_to_pos = ['[PAD]', '前文字と同じ単語内'] + self.config.parts_of_speech
        self.char_to_id = {c: i + 3 for i, c in enumerate(self.config.chars)}

        torch.set_num_interop_threads(num_threads)
        torch.set_num_threads(num_threads)
        self.model = PartOfSpeechEstimator(self.config)
        self.model.cpu()
        self.model.load_state_dict(torch.load(os.path.join(this_dir, 'model.pth')))


    def parse(self, text: str) -> str:
        text = text.strip()
        if len(text) > self.config.max_position_embeddings:
            raise RuntimeError(f"Input text length must be {self.config.max_position_embeddings} or less.")

        model_input = self.encode(text)
        with torch.no_grad():
            session_result = self.model(**model_input).logits.argmax(-1).data[0]
        return self.decode(text, session_result)

    def encode(self, text: str) -> Dict[str, torch.Tensor]:
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

        model_input = {
            'input_ids': torch.tensor([input_ids]),
            'attention_mask': torch.tensor([[1] * len(input_ids)]),
            'token_type_ids': torch.tensor([[0] * len(input_ids)])
        }
        return model_input


    def decode(self, text: str, pos_ids: torch.Tensor) -> str:
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
