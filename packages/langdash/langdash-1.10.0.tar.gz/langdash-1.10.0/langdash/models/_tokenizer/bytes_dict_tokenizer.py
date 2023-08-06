from typing import List, Union, Optional, Generator, Dict, Callable
from .tokenizer import Tokenizer, BufferedToken


class BytesDictTokenizer(Tokenizer):

  def __init__(
    self,
    encode_func: Callable[..., List[int]],
    decode_func: Callable[[List[int]], str],
    mapping: List[bytes],
  ):
    self.encode_func = encode_func
    self.decode_func = decode_func
    self.mapping = mapping
    self.reverse_mapping: Optional[Dict[bytes, int]] = None

  def encode(self, text: str, add_special_tokens: bool = False) -> List[int]:
    return self.encode_func(text, add_special_tokens=add_special_tokens)

  def decode(self, tokens: List[int]) -> str:
    return self.decode_func(tokens)

  def decode_once(self, token: int) -> Union[str, BufferedToken]:
    token_bytes = self.mapping[token]
    try:
      return token_bytes.decode("utf-8")
    except UnicodeDecodeError:
      return BytesDictBufferedToken(self, token_bytes)

  def tokens_starting_with(self, token_id: int) -> Generator[int, None, None]:
    tokstr = self.mapping[token_id]
    for logits_tokid, logits_tokstr in enumerate(self.mapping):
      if not logits_tokstr.startswith(tokstr):
        yield logits_tokid

  def get_vocab(self):
    if self.reverse_mapping is None:
      self.reverse_mapping = {
        token: idx for idx, token in enumerate(self.mapping)
      }
    return self.reverse_mapping


class BytesDictBufferedToken(BufferedToken):

  def __init__(self, tokenizer: BytesDictTokenizer, token_bytes: bytes):
    self.tokenizer = tokenizer
    self.token_bytes = token_bytes

  def add_token_id(self, token_id: int) -> Optional[str]:
    self.token_bytes += self.tokenizer.mapping[token_id]
    try:
      return self.token_bytes.decode("utf-8")
    except UnicodeDecodeError:
      return None

  def flush(self) -> str:
    return self.token_bytes.decode("utf-8", errors="ignore")
