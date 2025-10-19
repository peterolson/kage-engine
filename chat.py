import os
from typing import Callable, Literal, Type, TypeVar
from google import genai
from google.genai import types
from dotenv import load_dotenv
from pydantic import BaseModel
import time
import inspect

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class ChatMessage(BaseModel):
    content: str


class ChatResponse(BaseModel):
    message: ChatMessage


def chat(
    messages: list[dict],
    model: str = "gemini-2.5-flash-preview-05-20",
    format=None,
    max_retries: int = 8,
    backoff_base: float = 1.0,
    backoff_max: float = 30.0,
    max_output_tokens: int | None = None,
    stop_sequences: list[str] | None = None,
    temperature: float | None = 0,
):
    if "lite" in model:
        model = "gemini-2.5-flash-lite-preview-06-17"
    if "pro" in model:
        model = "gemini-2.5-pro"
    if model not in [
        "gemini-2.5-pro-preview-06-05",
        "gemini-2.5-pro",
        "gemini-2.5-flash-lite-preview-06-17",
    ]:
        model = "gemini-2.5-flash"

    config = None
    system_instructions = ""
    for message in messages[:-1]:
        if message.get("role") == "system":
            system_instructions = system_instructions + message.get("content", "")
        if message.get("role") == "user":
            system_instructions = (
                system_instructions
                + "\n\nExample Input:\n"
                + message.get("content", "")
            )
        if message.get("role") == "assistant":
            system_instructions = (
                system_instructions
                + "\n\nExample Output:\n"
                + message.get("content", "")
            )
    config = types.GenerateContentConfig(
        system_instruction=system_instructions if system_instructions else None,
        response_mime_type=("application/json" if format is not None else "text/plain"),
        response_schema=format,
        max_output_tokens=max_output_tokens,
        stop_sequences=stop_sequences,
        temperature=temperature,
        thinking_config=types.ThinkingConfig(thinking_budget=1024),
    )
    contents = messages[-1].get("content", "")
    try:
        response = client.models.generate_content(
            model=model, config=config, contents=contents
        )
        if response.text is None:
            return ChatResponse(message=ChatMessage(content=""))
        return ChatResponse(message=ChatMessage(content=response.text))
    except Exception as e:
        print(f"Error during chat: {e}")
        if "429 RESOURCE_EXHAUSTED" in str(e):
            print(f"Quota exceeded. Exiting...")
            exit(1)
        if max_retries <= 0:
            raise Exception("Maximum retries reached. Unable to process the request.")
        print(f"Retrying... ({max_retries} retries left)")
        time.sleep(min(backoff_base, backoff_max))
        return (
            chat(
                messages=messages,
                model=model,
                format=format,
                max_retries=max_retries - 1,
                backoff_base=backoff_base * 2,
                backoff_max=backoff_max,
            )
            if max_retries > 0
            else ChatResponse(message=ChatMessage(content=""))
        )


T = TypeVar("T", bound=BaseModel)


def chat_with_retry(
    messages: list[dict],
    format: Type[T],
    validation: (
        Callable[[str, T], str | None]
        | Callable[[str, T, str], str | None]
        | Callable[[str, T, str, list[dict[str, str]]], str | None]
    ),
    model: Literal["lite", "medium", "pro"] = "lite",
    base_temperature: float = 0.0,
    allow_failed: bool = False,
) -> T | None:
    model_order = ["lite", "medium", "pro"]
    model_index = model_order.index(model)

    original_input = messages[-1].get("content", "")

    attempts = 0
    max_attempts = 3
    parsed_response = None
    while attempts < max_attempts:
        try:
            response = chat(
                messages,
                model=model_order[model_index],
                format=format,
                temperature=base_temperature + attempts * 0.25,
            )
            parsed_response = format.model_validate_json(response.message.content)
            validation_argcount = len(inspect.signature(validation).parameters)
            if validation_argcount == 2:
                validation_error = validation(original_input, parsed_response)  # type: ignore
            elif validation_argcount == 3:
                validation_error = validation(original_input, parsed_response, model_order[model_index])  # type: ignore
            else:
                validation_error = validation(original_input, parsed_response, model_order[model_index], messages)  # type: ignore
            if not validation_error:
                return parsed_response

            print(f"Validation error: {validation_error}\n{response.message.content}")
            messages.append(
                {
                    "role": "assistant",
                    "content": response.message.content,
                }
            )
            messages.append(
                {
                    "role": "user",
                    "content": f"Your previous response was invalid:\n{validation_error}\n\nPlease try again.\nOriginal input:\n{original_input}",
                }
            )
            attempts += 1
            if attempts >= max_attempts:
                return None

        except Exception as e:
            return None
    if parsed_response and allow_failed:
        return parsed_response
    return None


if __name__ == "__main__":
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "What is the capital of France?",
        },
    ]
    response = chat(messages)
    print(response.message.content)
