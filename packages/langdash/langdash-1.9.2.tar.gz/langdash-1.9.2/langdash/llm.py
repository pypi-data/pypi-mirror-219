from typing import TypeVar, Generic, Type, TYPE_CHECKING
from enum import Flag, auto


class LLMCapability(Flag):
  """
  Flag representing the capabilities of a language model.
  """
  Generative = auto()
  Embedding = auto()


if TYPE_CHECKING:
  from langdash.llm_session import LLMSession, LLMEmbeddingSession
  T_LLMSession = TypeVar("T_LLMSession", bound=LLMSession)
  T_LLMEmbeddingSession = TypeVar(
    "T_LLMEmbeddingSession", bound=LLMEmbeddingSession
  )
else:
  T_LLMSession = TypeVar("T_LLMSession")
  T_LLMEmbeddingSession = TypeVar("T_LLMEmbeddingSession")


class LLM(Generic[T_LLMSession]):
  """
  A language model class for inference.
  """
  Session: Type["T_LLMSession"]

  def session(self, *args, **kwargs) -> "T_LLMSession":
    """
    Create a new session for the given model.
    
    Args:
      default_infer_args (InferArgs):
        Default arguments for the inference.
      track_called_nodes (bool):
        Whether to track called nodes. Defaults to `False`.
      token_healing (bool):
        Whether to enable token healing. Defaults to `True`.
      event_handlers (Optional[LLMGenerationSessionEvents]):
        Event handlers for prompt events. Defaults to `None`.

    Returns:
      A new session object.
    """
    return self.__class__.Session(llm=self, *args, **kwargs)

  @property
  def capability(self) -> LLMCapability:
    """
    Returns the capability of the language model.
    """
    return LLMCapability.Generative


class EmbeddingLLM(LLM[T_LLMEmbeddingSession]):
  """
  A language model class for generating embeddings.
  """

  @property
  def capability(self) -> LLMCapability:
    return LLMCapability.Embedding
