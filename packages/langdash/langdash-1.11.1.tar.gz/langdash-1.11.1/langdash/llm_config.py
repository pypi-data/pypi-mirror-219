from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class LLMConfig:
  """
  Data class used to store unified LLM config.
  
  Attributes:
    model (Optional[str]):
      The name, or the path of the model. Defaults to `None`.
    batch_size (int):
      The number of tokens per batch size for inference.
      Defaults to -1 for auto.
    threads (int):
      The number of threads used for inference.
      Defaults to -1 for auto.
    context_length (int):
      The number of tokens used for context.
      Defaults to -1 for auto.
    gpu_layers (int):
      The number of layers to run on GPU.
      Defaults to 0.
  """

  model: Optional[str] = None
  batch_size: int = -1
  threads: int = -1
  context_length: int = -1
  gpu_layers: int = 0