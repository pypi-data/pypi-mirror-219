from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
  # FIXME: requires TYPE_CHECKING guard in order for source build to work
  import torch


@dataclass
class InferArgs:
  """ Data class for inference arguments. """

  min_new_tokens: int = 0
  """
  Minimum number of new tokens to generate.
  
  If this is set, the `end` argument passed to the session's infer method
   will be interpreted as *a single token*. Special tokens count as an end token.
  """

  max_new_tokens: int = 512
  """
  Maximum number of new tokens to generate
  """

  temperature: float = 1.0
  """ Temperature """

  top_k: int = 0
  """ Top-K parameter. If set, generation uses top-K sampling method. Works with `top_p`. """

  top_p: float = 0.
  """ Top-P parameter. If set, generation uses top-P sampling method. """

  typical_mass: float = 0.
  """ Typical mass parameter. If set, generation will use typical sampling. """

  max_rep_ctx: int = 64
  """ Maximum number of tokens to look back for repetition penalty. """

  rep_penalty: float = 1.0
  """ Repetition penalty, applied to logits for every repeated token before sampling. """

  rng: Optional["torch.Generator"] = None
  """
  The random number generator (torch.Generator) to be used for token sampling.
  Defaults to `None` for the global RNG.
  """

  def __post_init__(self):
    assert self.min_new_tokens >= 0
    assert self.max_new_tokens >= self.min_new_tokens
    assert 0.0 <= self.temperature <= 10.0
    assert 0 <= self.top_k
    assert 0.0 <= self.top_p <= 1.0
    assert 0.0 <= self.typical_mass <= 1.0
    assert 0 <= self.max_rep_ctx
    assert 0.0 <= self.rep_penalty <= 10.0
