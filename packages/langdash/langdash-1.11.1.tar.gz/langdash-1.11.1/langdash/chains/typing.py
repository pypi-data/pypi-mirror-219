from typing import Dict, Any, Callable

Type = Callable[[str], Any]
TypeDict = Dict[str, Type]


class Mapping:
  """
  Helper type for mapping string into value.
  """

  def __init__(self, mapping: Dict[str, Any]):
    self.mapping = mapping

  def __call__(self, input: str):
    return self.mapping[input]
