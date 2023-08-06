"""
LLAMA HUB.
"""
import traceback
import secrets
import time
import sys

from loguru import logger
logger.remove(None)
logger.add("logs/{time:YYYY-MM-DD}.log",level = 'DEBUG', format = "{time:YYYY-MM-DD HH:mm:ss} | {level:<8} |{line:<3}|{file:<25} | {message}",rotation="10 MB")
loguru_format = "<cyan>{time:YYYY-MM-DD HH:mm:ss}</cyan>|<level>{level:<8}|{file:<25}|{line:<3}></level>{message}"
logger.add(sys.stdout,level = 'DEBUG', format = loguru_format)
logger.level("INFO", color="<green>")


from . import is_true
from .choice import reduce_choice
from .model import load_model

# Configurations from environment variables.
from . import MODEL
from . import MODEL_REVISION
from . import MODEL_CACHE_DIR
from . import MODEL_LOAD_IN_8BIT
from . import MODEL_LOAD_IN_4BIT
from . import MODEL_LOCAL_FILES_ONLY
from . import MODEL_TRUST_REMOTE_CODE
from . import MODEL_HALF_PRECISION
from . import SERVER_MODEL_NAME
from . import COMPLETION_MAX_PROMPT
from . import COMPLETION_MAX_TOKENS
from . import COMPLETION_MAX_N
from . import COMPLETION_MAX_LOGPROBS

# Load the language model to be served.
stream_model = None
def load_stream_model(model=MODEL,load_in_8bit=MODEL_LOAD_IN_8BIT):
    global stream_model
    logger.info(f"Loading model {MODEL} in 8bit: {load_in_8bit}")
    stream_model = load_model(
        name_or_path=model,
        revision=MODEL_REVISION,
        cache_dir=MODEL_CACHE_DIR,
        load_in_8bit=load_in_8bit,
        load_in_4bit=MODEL_LOAD_IN_4BIT,
        local_files_only=MODEL_LOCAL_FILES_ONLY,
        trust_remote_code=MODEL_TRUST_REMOTE_CODE,
        half_precision=MODEL_HALF_PRECISION,
    )
    logger.info(f"Model {MODEL} finished loading")

# schema = {
#         "prompt": str,
#         "min_tokens": int,
#         "max_tokens": int,
#         "temperature": float,
#         "top_p": float,
#         "n": int,
#         "stream": bool,
#         "logprobs": int,
#         "echo": bool,
#     }
def create_completion(options):
    """Create a completion for the provided prompt and parameters."""
    if "prompt" not in options:
        logger.warning("prompt not specified")
        options["prompt"] = ""

    
    # Limit maximum resource usage.
    # if len(options["prompt"]) > COMPLETION_MAX_PROMPT:
    #     logger.warning("prompt truncated to {} chars from {}", COMPLETION_MAX_PROMPT, len(options["prompt"]))
    #     options["prompt"] = options["prompt"][:COMPLETION_MAX_PROMPT]
    if options.get("min_tokens", 0) > COMPLETION_MAX_TOKENS:
        options["min_tokens"] = COMPLETION_MAX_TOKENS
    if options.get("max_tokens", 0) > COMPLETION_MAX_TOKENS:
        options["max_tokens"] = COMPLETION_MAX_TOKENS
    if options.get("n", 0) > COMPLETION_MAX_N:
        options["n"] = COMPLETION_MAX_N
    if options.get("logprobs", 0) > COMPLETION_MAX_LOGPROBS:
        options["logprobs"] = COMPLETION_MAX_LOGPROBS

    # Create response body template.
    template = {
        "id": f"cmpl-{secrets.token_hex(12)}",
        "object": "text_completion",
        "created": round(time.time()),
        "model": SERVER_MODEL_NAME,
        "choices": [],
    }
    logger.debug("options: {}", options)
    try:
        # Return in event stream or plain JSON.
        logger.info("Generating completion")
        return create_completion_json(options, template)
    except Exception as e:
        logger.exception(traceback.TracebackException.from_exception(e))
        logger.error(f"Error generating completion: {e}", exc_info=True)
        return str({"error": str(e)})

def create_completion_json(options, template):
    """Return text completion results in plain JSON."""

    # Tokenize the prompt beforehand to count token usage.
    logger.info("Tokenizing prompt")
    options["prompt"] = stream_model.tokenize(options["prompt"],trim_to=COMPLETION_MAX_PROMPT)
    prompt_tokens = stream_model.get_tokens_count(options["prompt"])
    completion_tokens = 0

    # Add data to the corresponding buffer according to the index.
    buffers = {}
    for choice in stream_model(**options):
        completion_tokens += 1
        index = choice["index"]
        if index not in buffers:
            buffers[index] = []
        buffers[index].append(choice)

    #clear options to save memory
    options.clear()

    # Merge choices with the same index.
    data = template.copy()
    for _, buffer in buffers.items():
        if buffer:
            data["choices"].append(reduce_choice(buffer))

    # Include token usage info.
    data["usage"] = {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens,
    }

    return data


def main():
    """Start serving API requests."""
    load_stream_model()
    


if __name__ == "__main__":
    main()
