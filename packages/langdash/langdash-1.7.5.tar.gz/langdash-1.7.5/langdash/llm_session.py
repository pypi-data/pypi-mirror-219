from typing import TypeVar, Generic, Optional, List, Generator, Union, Tuple, TYPE_CHECKING
import copy

from langdash.response import RespInfer
from langdash.chains import CalledNode, LDNodeArgs, LDNode
from langdash.infer import InferArgs
from langdash.llm import LLM

if TYPE_CHECKING:
  from langdash.core import Langdash

T_LLM = TypeVar("T_LLM", bound=LLM)


class LLMSession(Generic[T_LLM]):
  """
  Base class for a session for a language model.
  """

  def __init__(self, llm: T_LLM, ld: "Langdash"):
    self._ld = ld
    self._llm = llm

  def clone(self) -> "LLMSession":
    """
    Clone the current session.
    """
    raise NotImplementedError("clone")


class LLMState:
  """
  A state class for a language model.
  """
  pass


T_LLMState = TypeVar("T_LLMState", bound=LLMState)


class LLMGenerationSessionEvents:

  def on_before_node_append(
    self, node: LDNode, args: LDNodeArgs, tokens_used: int,
    session: "LLMGenerationSession"
  ) -> Optional[bool]:
    """
    Event handler which fires after the node is run, but before node is appended to list of called nodes.
    
    Args:
      node (LDNode): The node being added
      args (LDNodeArgs): The arguments of the node
      tokens_used (int): Number of tokens the node used
      session (LLMGenerationSession): The current session
    
    Returns:
      `None` or `True` if node should be appended, otherwise `False` if node should not be appended.
    """
    return None


class LLMGenerationSession(LLMSession, Generic[T_LLM, T_LLMState]):
  """ Generation session for a language model. """

  default_infer_args: InferArgs
  """ Default inference arguments. """

  called_nodes: Optional[List[CalledNode]]
  """
  List of called nodes.
  
  If `track_called_nodes` is set to `False` in constructor, then this will be `None`.
  """

  # Event handlers
  event_handlers: Optional[LLMGenerationSessionEvents]

  def __init__(
    self,
    llm: T_LLM,
    ld: "Langdash",
    default_infer_args: InferArgs = InferArgs(),
    track_called_nodes: bool = False,
    token_healing: bool = True,
    event_handlers: Optional[LLMGenerationSessionEvents] = None,
  ):
    super().__init__(llm, ld)
    self.default_infer_args = default_infer_args
    self.called_nodes = ([] if track_called_nodes else None)
    self.token_healing = token_healing
    self._tokens_counter = 0
    self.tokens_used = 0
    self.event_handlers = event_handlers

  def set_state(self, state: Optional[T_LLMState]):
    """
    Set the state of the language model.

    Args:
      state (Optional[T_LLMState]):
        The state of the language model, or None to clear the state.
    """
    raise NotImplementedError("set_state")

  def clone_state(self) -> T_LLMState:
    """
    Clone the current state of the language model.
    
    Returns:
      (T_LLMState) The current state as an object.
    """
    raise NotImplementedError("clone_state")

  def clone(self) -> "LLMGenerationSession":
    """
    Clone the current session.
    
    Returns:
      (LLMGenerationSession) A new generation session with the same arguments.
    """
    session = self.__class__(
      llm=self._llm,
      ld=self._ld,
      default_infer_args=self.default_infer_args,
      track_called_nodes=False,
      token_healing=self.token_healing,
      event_handlers=self.event_handlers,
    )
    session.set_state(self.clone_state())
    if self.called_nodes is not None:
      session.called_nodes = copy.copy(self.called_nodes)
    return session

  def _append_called_chain(
    self, node: LDNode, args: LDNodeArgs, tokens_used: int
  ):
    if self.event_handlers is not None:
      if self.event_handlers.on_before_node_append(
        node, args, tokens_used, self
      ) is False:
        return
    if self.called_nodes is not None:
      self.called_nodes.append(
        CalledNode(node=node, args=args, tokens_used=tokens_used)
      )
    self.tokens_used += tokens_used

  def tokenize(self, text: str, add_special_tokens: bool = False) -> List[int]:
    """
    Tokenize the given text into a list of tokens.

    Args:
      text (str): The text to tokenize.
      add_special_tokens (bool): Whether to add special tokens to the output.

    Returns:
      (List[int]) The list of tokens.
    """
    raise NotImplementedError("tokenize")

  def decode(self, tokids: List[int]) -> str:
    raise NotImplementedError("decode")

  def next_token_logits(self) -> List[float]:
    """
    Returns the logits for next token.
    """
    raise NotImplementedError("next_token_logits")

  def next_token_probs(self) -> List[float]:
    """
    Returns the probabilities for next token.
    """
    raise NotImplementedError("next_token_probs")

  def flush_token(self):
    raise NotImplementedError("flush_token")

  def _infer(
    self, end: Optional[Union[str, int]], args: InferArgs, end_is_token: bool
  ) -> Generator[RespInfer, None, None]:
    raise NotImplementedError("_infer")

  def infer(
    self,
    end: Optional[Union[str, int]],
    args: Optional[InferArgs] = None,
    end_is_token: bool = False,
  ) -> Generator[RespInfer, None, None]:
    """
    Infer the next tokens from the input sequence.

    Args:
      end (Optional[Union[str, int]]):
        The end of the output sequence.
        If set to `None`, the output sequence will be generated until the maximum number of tokens is reached.
        
        Defaults to `None`.
      args (Optional[InferArgs]):
        Optional inference parameters. Defaults to `None`.
      end_is_token (bool):
        If true, then the end string will be interpreted as a token. Defaults to `False`.
        
    Returns:
      (Generator[RespInfer, None, None]) Generator yielding inference events.
    """
    if not args:
      args = self.default_infer_args
    yield from self._infer(end=end, args=args, end_is_token=end_is_token)

  def inject(
    self,
    text: Union[str, int, List[int]],
    add_special_tokens: bool = False
  ) -> int:
    raise NotImplementedError("inject")

  def get_context_length(self) -> int:
    """
    Returns the context length of the model, or zero for models that don't support one.
    """
    return 0


T_Tensor = TypeVar("T_Tensor")


class LLMGenerationSessionForRawText(
  LLMGenerationSession, Generic[T_LLM, T_LLMState, T_Tensor]
):
  """ Generation session for a language model that processes raw text. """

  _logits: Optional[T_Tensor]
  _next_token: Optional[Tuple[int, str]]

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._logits = None
    self._next_token = None

  def _eval(self, tokid: int) -> T_Tensor:
    raise NotImplementedError("_eval")

  def _eval_mult(self, tokens: List[int]):
    assert tokens, "tokens must not be empty"
    for tokid in tokens:
      logits = self._eval(tokid)
    return logits

  def flush_token(self):
    """
    Flushes the previous token into the language model if healing is enabled.
    
    **Warning:** unexpected behavior if the previous token is a "boundary" token,
    like the space `' '` token.
    """
    if self._next_token is None:
      return
    self.inject(self._next_token[0])
    self._next_token = None

  def next_token_probs(self, *args, **kwargs) -> List[float]:
    raise NotImplementedError("next_token_probs")

  def _on_first_inject(self):
    return

  def inject(
    self,
    text: Union[str, int, List[int]],
    add_special_tokens: bool = False
  ) -> int:
    if isinstance(text, str):
      tokens = self.tokenize(text, add_special_tokens=add_special_tokens)
    elif isinstance(text, int):
      tokens = [text]
    else:
      assert (isinstance(text, list))
      tokens = text
    if not tokens:
      return 0

    if self._logits is None:
      self._on_first_inject()

    num_toks = 0

    if self.token_healing:
      if self._next_token is not None:
        tokid, _ = self._next_token
        tokens = self.tokenize(
          self.decode([tokid, *tokens]), add_special_tokens=add_special_tokens
        )
      if len(tokens) > 1:
        self._logits = self._eval_mult(tokens[:-1])
        num_toks += len(tokens) - 1
      self._next_token = (tokens[-1], self.decode([tokens[-1]]))
    else:
      if self._next_token is not None:
        tokid, tokstr = self._next_token
        self._eval(tokid)
        num_toks += 1
      self._logits = self._eval_mult(tokens)
      num_toks += len(tokens)

    return num_toks


T_Embedding = TypeVar("T_Embedding")


class LLMEmbeddingSession(LLMSession, Generic[T_LLM, T_Embedding]):
  """ Session for a language model that outputs an embedding for raw text. """

  def __init__(self, llm: T_LLM, ld: "Langdash"):
    self._ld = ld
    self._llm = llm

  def embedding_size(self) -> int:
    """
    Returns the embedding size of the model.
    """
    raise NotImplementedError("embedding_size")

  def embed(self, documents: List[str]) -> T_Embedding:
    """
    Infer the embedding of a list of text.
    
    Args:
      documents (List[str]): The text to be embedded.
      
    Returns:
      The embedding vector of the text.
    """
    raise NotImplementedError("infer")
