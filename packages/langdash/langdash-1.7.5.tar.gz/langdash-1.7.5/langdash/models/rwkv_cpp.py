from typing import List, Optional, Tuple
from dataclasses import dataclass
import copy
import os
import sys
import torch
import tokenizers  # type: ignore

from langdash.llm import LLM
from langdash.llm_config import LLMConfig
from langdash.llm_session import LLMGenerationSessionForRawText, LLMState
import langdash.sampling as sampling
from ._mixins.tensor_based_infer_mixin import TensorBasedInferMixin

_rwkv_lib: Optional[str] = None
_rwkv_cpp_folder: Optional[str] = None

RWKV_CPP_COMMIT_DEFAULT = "84634c047a9831b16cdf1cc3f2626e0ef0b2373b"
RWKV_CPP_COMMIT = os.environ.get(
  "LANGDASH_RWKV_CPP_COMMIT", RWKV_CPP_COMMIT_DEFAULT
)
RWKV_CPP_FORCE_RECOMPILE = os.environ.get(
  "LANGDASH_RWKV_CPP_FORCE_RECOMPILE", ""
) == "1"
RWKV_CPP_ENABLE_EVAL_SEQUENCE = os.environ.get(
  "LANGDASH_RWKV_CPP_ENABLE_EVAL_SEQUENCE", ""
) == "1"


def _load_rwkv_import():
  global _rwkv_lib, _rwkv_cpp_folder

  import subprocess
  import shutil

  import langdash
  _rwkv_cpp_folder = os.path.join(
    os.path.dirname(langdash.__file__), "extern/rwkv.cpp"
  )

  force_recompile = RWKV_CPP_FORCE_RECOMPILE

  git = shutil.which("git")

  if not os.path.isdir(_rwkv_cpp_folder):
    print("rwkv.cpp isn't installed, clone and install? (requires git, cmake)")
    do_install = input("Type 'y' (without quotes) to install: ") == "y"
    if not do_install:
      raise ImportError("rwkv.cpp is not installed")
    if git is None:
      raise ImportError("git is needed for compiling rwkv.cpp")

    os.makedirs(_rwkv_cpp_folder, exist_ok=True)

    if not os.path.isdir(os.path.join(_rwkv_cpp_folder, ".git")):
      subprocess.check_call(
        [
          git, "clone", "--recursive",
          "https://github.com/saharNooby/rwkv.cpp", _rwkv_cpp_folder
        ]
      )
    subprocess.check_call(
      [git, "checkout", RWKV_CPP_COMMIT], cwd=_rwkv_cpp_folder
    )
    subprocess.check_call([git, "submodule", "update"], cwd=_rwkv_cpp_folder)

  elif git is not None:
    current_commit = subprocess.check_output(
      [git, "rev-parse", "HEAD"], cwd=_rwkv_cpp_folder, encoding="utf-8"
    ).strip()
    if current_commit != RWKV_CPP_COMMIT:
      subprocess.check_call(
        [git, "pull", "origin", "master"], cwd=_rwkv_cpp_folder
      )
      subprocess.check_call(
        [git, "checkout", RWKV_CPP_COMMIT], cwd=_rwkv_cpp_folder
      )
      subprocess.check_call([git, "submodule", "update"], cwd=_rwkv_cpp_folder)
      force_recompile = True

  if force_recompile:
    try:
      os.unlink(os.path.join(_rwkv_cpp_folder, "CMakeCache.txt"))
    except FileNotFoundError:
      pass

  if "win32" in sys.platform or "cygwin" in sys.platform:
    file_name = "rwkv.dll"
  elif "darwin" in sys.platform:
    file_name = "librwkv.dylib"
  else:
    file_name = "librwkv.so"

  _rwkv_lib = os.path.join(_rwkv_cpp_folder, file_name)

  if force_recompile or not os.path.isfile(_rwkv_lib):

    if os.environ.get("LANGDASH_RWKV_CPP_PATCH_MAX_NODES", "") == "1":
      print("Patching rwkv.cpp's ggml...")
      patch = shutil.which("patch")
      if patch is None:
        raise ImportError("patch is needed for compiling rwkv.cpp")
      with open(
        os.path.join(
          os.path.dirname(langdash.__file__),
          "extern/rwkv-cpp-ggml-max-nodes.patch"
        ), "r"
      ) as patch_file:
        subprocess.run(
          [patch, "-r", "-", "-N", "-p1"],
          input=patch_file.read(),
          text=True,
          cwd=os.path.join(_rwkv_cpp_folder, "ggml"),
          check=False
        )

    cmake = shutil.which("cmake")
    if cmake is None:
      raise ImportError("cmake is needed for compiling rwkv.cpp")
    subprocess.check_call([cmake, "."], cwd=_rwkv_cpp_folder)
    subprocess.check_call(
      [cmake, "--build", ".", "--config", "Release"], cwd=_rwkv_cpp_folder
    )

  sys.path.insert(0, os.path.join(_rwkv_cpp_folder, "rwkv"))


_load_rwkv_import()

import rwkv_cpp_model  # type: ignore
import rwkv_cpp_shared_library  # type: ignore

try:
  import rwkv_tokenizer  # type: ignore
  _rwkv_tokenizer_available = True
except ModuleNotFoundError:
  _rwkv_tokenizer_available = False

sys.path.pop(0)

try:
  from tqdm import tqdm

  def _sequence_progress(v):
    if len(v) < 2:
      return v
    return tqdm(v)
except ImportError:

  def _sequence_progress(v):
    return v


@dataclass
class RwkvCppState(LLMState):
  _logits: Optional[torch.Tensor] = None
  _state: Optional[torch.Tensor] = None
  _next_token: Optional[Tuple[int, str]] = None


class RwkvCppWrapper:

  def __init__(self, llm: "RwkvCppModel"):
    assert _rwkv_lib is not None
    self.model = rwkv_cpp_model.RWKVModel(
      rwkv_cpp_shared_library.RWKVSharedLibrary(_rwkv_lib), llm._model_path,
      **llm._model_kwargs
    )
    self.batch_size = llm._batch_size
    if self.batch_size <= 1:
      self.do_eval_sequence = False
    elif RWKV_CPP_ENABLE_EVAL_SEQUENCE:
      self.do_eval_sequence = hasattr(self.model, "eval_sequence")
    else:
      self.do_eval_sequence = False
    if llm._tokenizer_type == "20B":
      from ._tokenizer.rwkv_tokenizer import RwkvTokenizer
      tokenizer = tokenizers.Tokenizer.from_file(llm._tokenizer_path)
      self.tokenizer = RwkvTokenizer(tokenizer)
    elif llm._tokenizer_type == "world":
      from ._tokenizer.bytes_dict_tokenizer import BytesDictTokenizer
      tokenizer = rwkv_tokenizer.WorldTokenizer(llm._tokenizer_path)
      mapping = [b""] * (len(tokenizer.index_to_token) + 1)
      for k, v in tokenizer.index_to_token.items():
        mapping[k] = v
      self.tokenizer = BytesDictTokenizer(
        encode_func=(lambda text, **_: tokenizer.encode(text)),
        decode_func=(
          lambda tokens, **_: tokenizer.decode_bytes(tokens).
          decode("utf-8", errors="strict")
        ),
        mapping=mapping
      )
    else:
      raise ValueError(f"unknown tokenizer type {llm._tokenizer_type}")
    self.eos_token = 0

  def eval(
    self,
    tokid: int,
    state: torch.Tensor,
    logits_out: Optional[torch.Tensor] = None
  ) -> Tuple[torch.Tensor, torch.Tensor]:
    return self.model.eval(tokid, state, state, logits_out)

  def eval_mult(
    self, tokens: List[int], state: torch.Tensor, logits_out: torch.Tensor
  ) -> Tuple[torch.Tensor, torch.Tensor]:
    if self.do_eval_sequence:
      batch_size = self.batch_size
      for i in _sequence_progress(range(0, len(tokens), batch_size)):
        logits_out, state = self.model.eval_sequence(
          tokens[i:i + batch_size], state, state, logits_out
        )
      return logits_out, state
    else:
      for tokid in _sequence_progress(tokens[:-1]):
        _, state = self.model.eval(tokid, state, state, None)
      logits_out, state = self.model.eval(tokens[-1], state, state, logits_out)
      return logits_out, state


class RwkvCppSession(
  TensorBasedInferMixin,
  LLMGenerationSessionForRawText["RwkvCppModel", RwkvCppState, torch.Tensor]
):
  """
  Session for rwkv.cpp model.
  """

  _logits: Optional[torch.Tensor]
  _state: Optional[torch.Tensor]

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    def load_model(llm: RwkvCppModel):
      return RwkvCppWrapper(llm)

    self._model = self._ld._get_model_internal(self._llm, load_model)
    self._logits, self._state = None, None
    self._next_token = None

  def _eval(self, tokid: int) -> torch.Tensor:
    self._logits, self._state = self._model.eval(
      tokid, self._state, self._logits
    )
    # FIXME: mypy does not infer self._logits to not be None
    return self._logits  # type: ignore

  def _eval_mult(self, tokens: List[int]) -> torch.Tensor:
    self._logits, self._state = self._model.eval_mult(
      tokens, self._state, self._logits
    )
    # FIXME: mypy does not infer self._logits to not be None
    return self._logits  # type: ignore

  def set_state(self, state: Optional[RwkvCppState]):
    if state is None:
      self._logits, self._state = None, None
      self._next_token = None
    else:
      self._logits = copy.deepcopy(state._logits)
      self._state = copy.deepcopy(state._state)
      self._next_token = state._next_token

  def clone_state(self) -> RwkvCppState:
    return RwkvCppState(
      _logits=copy.deepcopy(self._logits),
      _state=copy.deepcopy(self._state),
      _next_token=self._next_token,
    )

  def tokenize(self, text: str, add_special_tokens: bool = False) -> List[int]:
    return self._model.tokenizer.encode(
      text, add_special_tokens=add_special_tokens
    )

  def decode(self, tokids: List[int]) -> str:
    return self._model.tokenizer.decode(tokids)

  def _next_token_logits_raw(self):
    if self._next_token is None:
      if self._logits is None:
        raise ValueError("cannot predict next probability for empty input")
      logits = self._logits
    else:
      logits, _ = self._model.eval(self._next_token[0], self._state)
    return logits

  def next_token_logits(self) -> List[float]:
    return self._next_token_logits_raw().tolist()

  def next_token_probs(self) -> List[float]:
    return sampling.logits_to_probs(self._next_token_logits_raw()).tolist()


class RwkvCppModel(LLM[RwkvCppSession]):
  """
  rwkv.cpp model
  """

  _model_path: str
  _model_kwargs: dict
  _tokenizer_path: str
  _tokenizer_type: str
  _batch_size: int

  Session = RwkvCppSession

  def __init__(
    self,
    model_path: Optional[str] = None,
    tokenizer_path: Optional[str] = None,
    tokenizer_type: str = "20B",
    batch_size: int = 128,
    **model_kwargs
  ):
    """
    Creates a template for the RWKV language model (using the rwkv.cpp library).
  
    You can pass the following environment variables to set compile flags:
  
    * LANGDASH_RWKV_CPP_COMMIT: hash of the commit to compile
    * LANGDASH_RWKV_CPP_FORCE_RECOMPILE: '1' to force recompilation
    * LANGDASH_RWKV_CPP_PATCH_MAX_NODES: '1' to patch the ggml library in rwkv.cpp
    so that large batch_size works (> 1)
  
    These environment variables can be used to set runtime flags:
  
    * LANGDASH_RWKV_CPP_ENABLE_EVAL_SEQUENCE: enable sequence evaluation. This
    feature is locked behind a flag because it requires the ggml library to be patched.
  
    Args:
      model_path (str): Path to the model file.
      tokenizer_path (Optional[str]):
        Path to the tokenizer file.
        Defaults to `None`. If not set, the built-in tokenizer will be used.
      tokenizer_type (str):
        The type of tokenizer to use. Either `"world"` for world models
        or `"20B"` for anything else.
      batch_size (int):
        The batch size for sequence evaluation.
        Must be a positive integer (more than 0).
        If negative, serial evaluation will always be used.
    """
    if "config" in model_kwargs:
      if not isinstance(model_kwargs["config"], LLMConfig):
        raise TypeError("config argument must be LLMConfig")

      config = model_kwargs["config"]
      del model_kwargs["config"]

      self._model_kwargs = {
        "thread_count": None if config.threads == -1 else config.threads,
        "gpu_layer_count": config.gpu_layers,
      }
      self._model_kwargs.update(model_kwargs)
      model_path = config.model
      batch_size = config.batch_size
    else:
      self._model_kwargs = model_kwargs

    if not isinstance(model_path, str):
      raise TypeError("model path must be string")
    self._model_path = model_path
    self._batch_size = batch_size

    if not _rwkv_tokenizer_available and tokenizer_type != "20B":
      raise ValueError("old RWKV tokenizer only supports '20B'")
    self._tokenizer_type = tokenizer_type
    if tokenizer_path is None:
      builtin_tokenizer_paths = {
        "world": "rwkv/rwkv_vocab_v20230424.txt",
        "20B": "rwkv/20B_tokenizer.json",
      }
      assert _rwkv_cpp_folder is not None
      self._tokenizer_path = os.path.join(
        _rwkv_cpp_folder, builtin_tokenizer_paths[self._tokenizer_type]
      )
    else:
      self._tokenizer_path = tokenizer_path
