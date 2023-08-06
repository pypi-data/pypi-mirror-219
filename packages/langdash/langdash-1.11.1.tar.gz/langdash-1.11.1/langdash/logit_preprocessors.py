from typing import List, Sequence


class LogitPreprocessor:
  """
  Base class for a logit preprocessor.
  """

  def __call__(self, input_ids: List[int], logits: Sequence[int]):
    """
    Preprocesor callback at each generation step.

    Args:
      input_ids (List[int]):
        The list of token ids generated so far.
      logits (Sequence[int]):
        The logit vector for the next generation step. This vector may be modified
        within the function.

    Returns:
      None
    """
    pass
