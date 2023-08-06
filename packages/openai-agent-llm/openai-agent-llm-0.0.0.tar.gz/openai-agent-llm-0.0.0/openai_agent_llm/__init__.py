import json
import secrets
from typing import Generator, Optional, Union, Dict, List, Any
import time
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from loguru import logger
from starlette.requests import Request

from openai_agent_llm.constants import ErrorCode
from openai_agent_llm.protocol import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionResponseStreamChoice,
    ChatCompletionStreamResponse,
    ChatMessage,
    ChatCompletionResponseChoice,
    CompletionRequest,
    CompletionResponse,
    CompletionResponseChoice,
    DeltaMessage,
    CompletionResponseStreamChoice,
    CompletionStreamResponse,
    ErrorResponse,
    ModelCard,
    ModelList,
    ModelPermission,
    UsageInfo,
    EmbeddingsResponse,
    EmbeddingsRequest,
)

server_error_msg = (
    "**NETWORK ERROR DUE TO HIGH TRAFFIC. PLEASE REGENERATE OR REFRESH THIS PAGE.**"
)


# 定义错误resp
def create_error_response(code: int, message: str) -> JSONResponse:
    return JSONResponse(
        ErrorResponse(message=message, code=code).dict(), status_code=500
    )


# 检查请求参数
def check_requests(request) -> Optional[JSONResponse]:
    # Check all params
    if request.max_tokens is not None and request.max_tokens <= 0:
        return create_error_response(
            ErrorCode.PARAM_OUT_OF_RANGE,
            f"{request.max_tokens} is less than the minimum of 1 - 'max_tokens'",
        )
    if request.n is not None and request.n <= 0:
        return create_error_response(
            ErrorCode.PARAM_OUT_OF_RANGE,
            f"{request.n} is less than the minimum of 1 - 'n'",
        )
    if request.temperature is not None and request.temperature < 0:
        return create_error_response(
            ErrorCode.PARAM_OUT_OF_RANGE,
            f"{request.temperature} is less than the minimum of 0 - 'temperature'",
        )
    if request.temperature is not None and request.temperature > 2:
        return create_error_response(
            ErrorCode.PARAM_OUT_OF_RANGE,
            f"{request.temperature} is greater than the maximum of 2 - 'temperature'",
        )
    if request.top_p is not None and request.top_p < 0:
        return create_error_response(
            ErrorCode.PARAM_OUT_OF_RANGE,
            f"{request.top_p} is less than the minimum of 0 - 'top_p'",
        )
    if request.top_p is not None and request.top_p > 1:
        return create_error_response(
            ErrorCode.PARAM_OUT_OF_RANGE,
            f"{request.top_p} is greater than the maximum of 1 - 'temperature'",
        )
    if request.stop is not None and (
            not isinstance(request.stop, str) and not isinstance(request.stop, list)
    ):
        return create_error_response(
            ErrorCode.PARAM_OUT_OF_RANGE,
            f"{request.stop} is not valid under any of the given schemas - 'stop'",
        )

    return None


# 获取生成参数
def get_gen_params(
        model_name: str,
        messages: Union[str, List[Dict[str, str]]],
        *,
        temperature: float,
        top_p: float,
        max_tokens: Optional[int],
        echo: Optional[bool],
        stream: Optional[bool],
        stop: Optional[Union[str, List[str]]] = None,
) -> Dict[str, Any]:
    if not max_tokens:
        max_tokens = 1024

    gen_params = {
        "model": model_name,
        "prompt": messages,
        "temperature": temperature,
        "top_p": top_p,
        "max_new_tokens": max_tokens,
        "echo": echo,
        "stream": stream,
    }

    if stop is not None:
        if isinstance(stop, str):
            stop = [stop]

        gen_params["stop"] = gen_params["stop"] + stop if "stop" in gen_params else stop

    logger.debug(f"==== request ====\n{gen_params}")
    return gen_params


class ModelServer:
    model_name = ""
    http_request: Request = None

    def __init__(self):
        pass

    def infer(self, params):
        return []

    def generate_stream_response(self, params):
        try:
            for output in self.infer(params):
                ret = {
                    "text": output["text"],
                    "error_code": 0,
                }
                if "usage" in output:
                    ret["usage"] = output["usage"]
                if "finish_reason" in output:
                    ret["finish_reason"] = output["finish_reason"]
                if "logprobs" in output:
                    ret["logprobs"] = output["logprobs"]
                yield ret

        except (ValueError, RuntimeError, Exception) as e:
            logger.exception(e)
            ret = {
                "text": f"{server_error_msg}\n\n({e})",
                "error_code": ErrorCode.INTERNAL_ERROR,
            }
            yield ret

    def generate_response(self, params) -> Union[dict, list]:
        try:
            ret = {"text": "", "error_code": 0}
            output = {}
            text = ""
            for output in self.infer(params):
                text += output["text"]
            ret["text"] = text

            if "usage" in output:
                ret["usage"] = output["usage"]
            if "finish_reason" in output:
                ret["finish_reason"] = output["finish_reason"]
            if "logprobs" in output:
                ret["logprobs"] = output["logprobs"]

        except (ValueError, RuntimeError, Exception) as e:
            logger.exception(e)
            ret = {
                "text": f"{server_error_msg}\n\n({e})",
                "error_code": ErrorCode.INTERNAL_ERROR,
            }
        return ret

    def get_embeddings(self, params):
        try:
            # todo:对接模型,获取embedding
            embedding = []
            token_num = 0
            ret = {
                "embedding": embedding,
                "token_num": token_num,
            }
        except (ValueError, RuntimeError, Exception) as e:
            ret = {
                "text": f"{server_error_msg}\n\n({e})",
                "error_code": ErrorCode.INTERNAL_ERROR,
            }
        return ret

    @property
    def stop(self):
        return


async def generate_completion_stream_generator(request: CompletionRequest, model_server: ModelServer):
    model_name = request.model
    _id = f"cmpl-{secrets.token_hex(12)}"
    finish_stream_events = []

    for text in request.prompt:
        for i in range(request.n):
            previous_text = ""
            payload = get_gen_params(
                request.model,
                text,
                temperature=request.temperature,
                top_p=request.top_p,
                max_tokens=request.max_tokens,
                echo=request.echo,
                stream=request.stream,
                stop=request.stop,
            )

            for content in model_server.generate_stream_response(payload):
                if content["error_code"] != 0:
                    yield f"data: {json.dumps(content, ensure_ascii=False)}\n\n"
                    yield "data: [DONE]\n\n"
                    return

                decoded_unicode = content["text"].replace("\ufffd", "")
                # delta_text = decoded_unicode[len(previous_text):]
                delta_text = decoded_unicode
                previous_text = decoded_unicode

                choice_data = CompletionResponseStreamChoice(
                    index=i,
                    text=delta_text,
                    logprobs=content.get("logprobs", None),
                    finish_reason=content.get("finish_reason", None),
                )
                chunk = CompletionStreamResponse(
                    id=_id, object="text_completion", choices=[choice_data], model=model_name
                )
                if len(delta_text) == 0:
                    if content.get("finish_reason", None) is not None:
                        finish_stream_events.append(chunk)
                    continue

                yield f"data: {chunk.json(exclude_unset=True, ensure_ascii=False)}\n\n"

    # There is not "content" field in the last delta message, so exclude_none to exclude field "content".
    for finish_chunk in finish_stream_events:
        yield f"data: {finish_chunk.json(exclude_unset=True, ensure_ascii=False)}\n\n"

    yield "data: [DONE]\n\n"


async def chat_completion_stream_generator(
        model_name: str, gen_params: Dict[str, Any], n: int,
        model_server: ModelServer
) -> Generator[str, Any, None]:
    """
    Event stream format:
    https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#event_stream_format
    """
    _id = f"chatcmpl-{secrets.token_hex(12)}"
    finish_stream_events = []
    for i in range(n):
        # First chunk with role
        choice_data = ChatCompletionResponseStreamChoice(
            index=i,
            delta=DeltaMessage(role="assistant"),
            finish_reason=None,
        )
        chunk = ChatCompletionStreamResponse(
            id=_id, choices=[choice_data], model=model_name
        )
        yield f"data: {chunk.json(exclude_unset=True, ensure_ascii=False)}\n\n"

        previous_text = ""
        for content in model_server.generate_stream_response(gen_params):
            if content["error_code"] != 0:
                yield f"data: {json.dumps(content, ensure_ascii=False)}\n\n"
                yield "data: [DONE]\n\n"
                return

            decoded_unicode = content["text"].replace("\ufffd", "")
            # delta_text = decoded_unicode[len(previous_text):]
            delta_text = decoded_unicode
            previous_text = decoded_unicode

            if len(delta_text) == 0:
                delta_text = None
            choice_data = ChatCompletionResponseStreamChoice(
                index=i,
                delta=DeltaMessage(content=delta_text),
                finish_reason=content.get("finish_reason", None),
            )
            chunk = ChatCompletionStreamResponse(
                id=_id, choices=[choice_data], model=model_name
            )

            if delta_text is None:
                if content.get("finish_reason", None) is not None:
                    finish_stream_events.append(chunk)
                continue

            yield f"data: {chunk.json(exclude_unset=True, ensure_ascii=False)}\n\n"

    # There is not "content" field in the last delta message, so exclude_none to exclude field "content".
    for finish_chunk in finish_stream_events:
        yield f"data: {finish_chunk.json(exclude_none=True, ensure_ascii=False)}\n\n"

    yield "data: [DONE]\n\n"


class LLMAPI(FastAPI):
    model_server = None

    def init(self, model_server_class=ModelServer):
        self.model_server_class = model_server_class
        self.add_api_route("/v1/models", endpoint=self.show_available_models)
        self.add_api_route("/v1/chat/completions", endpoint=self.create_chat_completion, methods=["post"])
        self.add_api_route("/v1/completions", endpoint=self.create_completion, methods=["post"])
        self.add_api_route("/v1/embeddings", endpoint=self.create_embeddings, methods=["post"])
        self.middleware('http')(self.catch_exceptions_middleware)

    async def catch_exceptions_middleware(self, request, call_next):
        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception(e)
        else:
            return response

    async def create_chat_completion(self, http_request: Request, request: ChatCompletionRequest):
        """Creates a completion for the chat message"""
        model_server = self.model_server_class()
        model_server.http_request = http_request
        error_check_ret = check_requests(request)
        if error_check_ret is not None:
            return error_check_ret

        gen_params = get_gen_params(
            request.model,
            request.messages,
            temperature=request.temperature,
            top_p=request.top_p,
            max_tokens=request.max_tokens,
            echo=False,
            stream=request.stream,
            stop=request.stop,
        )

        if request.stream:
            generator = chat_completion_stream_generator(
                request.model, gen_params, request.n, model_server=model_server
            )
            return StreamingResponse(generator, media_type="text/event-stream")

        choices = []
        usage = UsageInfo()
        for i in range(request.n):
            content = model_server.generate_response(gen_params)
            if content["error_code"] != 0:
                return create_error_response(content["error_code"], content["text"])

            choices.append(
                ChatCompletionResponseChoice(
                    index=i,
                    message=ChatMessage(role="assistant", content=content["text"]),
                    finish_reason=content.get("finish_reason", "stop"),
                )
            )

            task_usage = UsageInfo.parse_obj(content["usage"])
            for usage_key, usage_value in task_usage.dict().items():
                setattr(usage, usage_key, getattr(usage, usage_key) + usage_value)

        return ChatCompletionResponse(model=request.model, choices=choices, usage=usage)

    async def create_completion(self, http_request: Request, request: CompletionRequest):
        model_server = self.model_server_class()
        model_server.http_request = http_request
        error_check_ret = check_requests(request)
        if error_check_ret is not None:
            return error_check_ret
        start_time = time.time()
        if isinstance(request.prompt, str):
            request.prompt = [request.prompt]

        if request.stream:
            generator = generate_completion_stream_generator(request, model_server=model_server)
            return StreamingResponse(generator, media_type="text/event-stream")
        else:
            text_completions = []
            for text in request.prompt:
                gen_params = get_gen_params(
                    request.model,
                    text,
                    temperature=request.temperature,
                    top_p=request.top_p,
                    max_tokens=request.max_tokens,
                    echo=request.echo,
                    stream=request.stream,
                    stop=request.stop,
                )
                for i in range(request.n):
                    content = model_server.generate_response(gen_params)
                    text_completions.append(content)

            choices = []
            usage = UsageInfo()
            for i, content in enumerate(text_completions):
                if content["error_code"] != 0:
                    return create_error_response(content["error_code"], content["text"])

                choices.append(
                    CompletionResponseChoice(
                        index=i,
                        text=content["text"],
                        logprobs=content.get("logprobs", None),
                        finish_reason=content.get("finish_reason", "stop"),
                    )
                )

                task_usage = UsageInfo.parse_obj(content["usage"])
                for usage_key, usage_value in task_usage.dict().items():
                    setattr(usage, usage_key, getattr(usage, usage_key) + usage_value)
            logger.info(f"consume time  = {(time.time() - start_time)}s, response = {str(choices)}")
            return CompletionResponse(
                model=request.model, choices=choices, usage=UsageInfo.parse_obj(usage)
            )

    async def show_available_models(self, http_request: Request):
        model_cards = []
        model_list = ["xxx"]
        for m in model_list:
            model_cards.append(ModelCard(id=m, root=m, permission=[ModelPermission()]))
        return ModelList(data=model_cards)

    async def create_embeddings(self, http_request: Request, request: EmbeddingsRequest):
        """Creates embeddings for the text"""
        # todo:对接模型
        data, token_num = [], 0

        return EmbeddingsResponse(
            data=data,
            model=request.model,
            usage=UsageInfo(
                prompt_tokens=token_num,
                total_tokens=token_num,
                completion_tokens=None,
            ),
        ).dict(exclude_none=True)
