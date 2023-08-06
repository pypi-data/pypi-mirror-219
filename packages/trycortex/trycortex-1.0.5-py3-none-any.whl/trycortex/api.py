import json
from enum import Enum
import requests
from typing import List, Dict, Union, Any, Tuple

class RetrievedDocument:
    def __init__(
        self,
        source_url: str,
        document_id: str,
        chunks: List[Dict[str, str]]
    ):
        self.source_url = source_url
        self.document_id = document_id
        self.chunks = chunks

class Message:
    def __init__(
        self,
        role: str,
        content: str,
        retrievals: Union[List[RetrievedDocument], None] = None,
        updatedAt: Union[str, None] = None
    ):
        self.role = role
        self.content = content
        self.retrievals = retrievals
        self.updatedAt = updatedAt

class Ok:
    def __init__(self, value):
        self.value = value

    def isOk(self):
        return True

    def isErr(self):
        return False

class Err:
    def __init__(self, error):
        self.error = error

    def isOk(self):
        return False

    def isErr(self):
        return True

class CortexAPIErrorResponse:
    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code

class RunnerAppRunErrorEvent:
    def __init__(self, code: str, message: str):
        self.type = "error"
        self.content = {
            "code": code,
            "message": message
        }

class RunnerAppRunRunStatusEvent:
    def __init__(self, status: str, run_id: str):
        self.type = "run_status"
        self.content = {
            "status": status,
            "run_id": run_id
        }

class RunnerAppRunBlockStatusEvent:
    def __init__(self, block_type: str, name: str, status: str, success_count: int, error_count: int):
        self.type = "block_status"
        self.content = {
            "block_type": block_type,
            "name": name,
            "status": status,
            "success_count": success_count,
            "error_count": error_count
        }

class RunnerAppRunBlockExecutionEvent:
    def __init__(self, block_type: str, block_name: str, execution: List[List[Dict[str, Union[None, str]]]]):
        self.type = "block_execution"
        self.content = {
            "block_type": block_type,
            "block_name": block_name,
            "execution": execution
        }

class RunnerAppRunFinalEvent:
    def __init__(self):
        self.type = "final"

class RunnerAppRunTokensEvent:
    def __init__(
        self,
        block_type: str,
        block_name: str,
        input_index: int,
        map: Union[Dict[str, Union[str, int]], None],
        tokens: Dict[str, Union[str, List[str], List[int]]]
    ):
        self.type = "tokens"
        self.content = {
            "block_type": block_type,
            "block_name": block_name,
            "input_index": input_index,
            "map": map,
            "tokens": tokens
        }

class CortexAPIResponse:
    def __init__(self, value):
        self.value = value

class Result:
    def __init__(self, value):
        self.value = value

class BlockRunConfig:
    def __init__(self, blocks: Dict[str, Any]):
        self.blocks = blocks

class BlockType(Enum):
    INPUT = "input"
    DATA = "data"
    KNOWLEDGE = "knowledge"
    CODE = "code"
    MODEL = "model"
    CHAT = "chat"
    MAP = "map"
    REDUCE = "reduce"
    LOOP = "loop"
    UNTIL = "until"
    SEARCH = "search"
    CURL = "curl"
    BROWSER = "browser"

class RunRunType(Enum):
    DEPLOY = "deploy"
    LOCAL = "local"
    EXECUTE = "execute"
    ALL = "all"

class Status(Enum):
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    ERRORED = "errored"

class BlockStatus:
    def __init__(self, block_type: BlockType, name: str, status: Status, success_count: int, error_count: int):
        self.block_type = block_type
        self.name = name
        self.status = status
        self.success_count = success_count
        self.error_count = error_count

class RunStatus:
    def __init__(self, run: Status, blocks: List[BlockStatus]):
        self.run = run
        self.blocks = blocks


class TraceType:
    def __init__(self, value: Any = None, error: Union[str, None] = None):
        self.value = value
        self.error = error

class RunConfig:
    def __init__(self, blocks: BlockRunConfig):
        self.blocks = blocks

class RunType:
    def __init__(
        self,
        run_id: str,
        created: int,
        run_type: RunRunType,
        app_hash: Union[str, None],
        specification_hash: Union[str, None],
        config: RunConfig,
        status: RunStatus,
        traces: List[Tuple[Tuple[BlockType, str], List[List[TraceType]]]],
        version: Union[int, None] = None,
        results: Union[List[List[Union[Any, None, str]]], None] = None
    ):
        self.run_id = run_id
        self.created = created
        self.run_type = run_type
        self.app_hash = app_hash
        self.specification_hash = specification_hash
        self.config = config
        self.status = status
        self.traces = traces
        self.version = version
        self.results = results

ConfigType = Dict[str, Any]

class CallableParams:
    def __init__(
        self,
        version: Union[int, str],
        config: ConfigType,
        inputs: List[Any],
        blocking: Union[bool, None] = None,
        block_filter: Union[List[Any], None] = None
    ):
        self.version = version
        self.config = config
        self.inputs = inputs
        self.blocking = blocking
        self.block_filter = block_filter

class ChatParams:
    def __init__(
        self,
        version: Union[int, str],
        config: ConfigType,
        inputs: List[Any]
    ):
        self.version = version
        self.config = config
        self.inputs = inputs

class Document:
    def __init__(
        self,
        data_source_id: str,
        created: int,
        document_id: str,
        timestamp: int,
        tags: List[str],
        hash: str,
        text_size: int,
        chunk_count: int,
        chunks: List[Dict[str, Union[str, int, List[Union[None, int]]]]],
        text: Union[str, None] = None,
        source_url: Union[str, None] = None
    ):
        self.data_source_id = data_source_id
        self.created = created
        self.document_id = document_id
        self.timestamp = timestamp
        self.tags = tags
        self.hash = hash
        self.text_size = text_size
        self.chunk_count = chunk_count
        self.chunks = chunks
        self.text = text
        self.source_url = source_url

class CreateDocument:
    def __init__(
        self,
        timestamp: Union[int, None] = None,
        tags:
        List[str] = None,
        text: Union[str, None] = None,
        source_url: Union[str, None] = None
    ):
        self.timestamp = timestamp
        self.tags = tags
        self.text = text
        self.source_url = source_url
    def getJson(self):
        data = {}
        if self.timestamp is not None:
            data["timestamp"] = self.timestamp

        if self.tags is not None:
            data["tags"] = self.tags

        if self.text is not None:
            data["text"] = self.text

        if self.source_url is not None:
            data["source_url"] = self.source_url
        
        return json.dumps(data)


class SharedVisibility:
    PRIVATE = "private"
    PUBLIC = "public"
    UNLISTED = "unlisted"
    DELETED = "deleted"

class HubProvider:
    SLACK = "slack"
    NOTION = "notion"
    WEB = "web"
    MEDIUM = "medium"

class Knowledge:
    def __init__(
        self,
        name: str,
        description: Union[str, None],
        visibility: SharedVisibility,
        config: Union[str, None],
        runnerProjectId: str,
        lastUpdatedAt: Union[str, None],
        hub: Union[Dict[str, Union[str, HubProvider]], None]
    ):
        self.name = name
        self.description = description
        self.visibility = visibility
        self.config = config
        self.runnerProjectId = runnerProjectId
        self.lastUpdatedAt = lastUpdatedAt
        self.hub = hub

class CortexAPI:
    def __init__(self, apiKey: Union[str, None] = None, userId: Union[str, None] = None):
        self.apiKey = apiKey
        self.userId = userId
        self.basePath = 'https://trycortex.ai/api/sdk/p'

    def getIDFromKey(self) -> str:
        config = {
            'headers': {
                'Authorization': f'Bearer {self.apiKey}',
                'Content-Type': 'application/json'
            },
            'method': 'GET',
        }
        endpoint = 'https://trycortex.ai/api/sdk/q/p'
        res = requests.request(**config, url=endpoint)
        return res.json().get('pID')

    def getDocument(self, knowledgeName: str, documentID: str):
        if not self.userId:
            self.userId = self.getIDFromKey()
        config = {
            'headers': {
                'Authorization': f'Bearer {self.apiKey}',
                'Content-Type': 'application/json'
            },
            'method': 'GET',
        }
        endpoint = f'/{self.userId}/knowledge/{knowledgeName}/d/{documentID}'
        response = requests.request(**config, url=self.basePath + endpoint)
        return response.json()

    def uploadDocument(self, knowledgeName: str, documentID: str, document: CreateDocument):
        if not self.userId:
            self.userId = self.getIDFromKey()
        data = document.getJson()
        config = {
            'headers': {
                'Authorization': f'Bearer {self.apiKey}',
                'Content-Type': 'application/json'
            },
            'method': 'POST',
            'data': data,
        }
        endpoint = f'/{self.userId}/knowledge/{knowledgeName}/d/{documentID}'
        response = requests.request(**config, url=self.basePath + endpoint)
        return response.json()

    def deleteDocument(self, knowledgeName: str, documentID: str):
        if not self.userId:
            self.userId = self.getIDFromKey()
        config = {
            'headers': {
                'Authorization': f'Bearer {self.apiKey}',
                'Content-Type': 'application/json'
            },
            'method': 'DELETE',
        }
        endpoint = f'/{self.userId}/knowledge/{knowledgeName}/d/{documentID}'
        response = requests.request(**config, url=self.basePath + endpoint)
        return response.json()

    def runCallable(self, callableID: str, data: CallableParams) -> Dict[str, RunType]:
        if not self.userId:
            self.userId = self.getIDFromKey()
        config = {
            'headers': {
                'Authorization': f'Bearer {self.apiKey}',
                'Content-Type': 'application/json'
            },
            'method': 'POST',
            'data': data,
        }
        endpoint = f'/{self.userId}/a/{callableID}/r'
        response = requests.request(**config, url=self.basePath + endpoint)
        return response.json()

    def runCallableWithStream(self, callableID: str, data: CallableParams) -> Dict[str, RunType]:
        if not self.userId:
            self.userId = self.getIDFromKey()
        config = {
            'headers': {
                'Authorization': f'Bearer {self.apiKey}',
                'Content-Type': 'application/json'
            },
            'method': 'POST',
            'data': {**data, 'stream': True},
        }
        endpoint = f'/{self.userId}/a/{callableID}/r'
        response = requests.request(**config, url=self.basePath + endpoint)
        return response.json()

    def runChatCopilotStream(self, copilotID: str, data: ChatParams) -> requests.Response:
        endpoint = f'/copilot/{copilotID}'
        base = 'https://trycortex.ai/api/sdk'
        response = requests.post(
            url=base + endpoint,
            headers={"Content-Type": "application/json"},
            json=data
        )
        return response

    """ def runChatCopilot(self, copilotID: str, data: ChatParams) -> Dict[str, Any]:
        res = self.runChatCopilotStream(copilotID, data)
        return processStreamedRunResponse(res) """

    def createChatInput(self, messages: List[Message], input: str) -> List[Dict[str, List[Message]]]:
        mes = messages.copy()
        newInput = Message("user", input)
        mes.append(newInput)
        return [{"messages": mes}]

    def createChatConfig(self, projectID: str, knowledgeName: str) -> Dict[str, Any]:
        config = {
            "OUTPUT_STREAM": {"use_stream": True},
            "RETRIEVALS": {"knowledge": [{"project_id": projectID, "data_source_id": knowledgeName}]}
        }
        return config

    def createChatParam(self, version: str, messages: List[Message], input: str, projectID: str, knowledgeName: str) -> ChatParams:
        config = self.createChatConfig(projectID, knowledgeName)
        inputMessages = self.createChatInput(messages, input)
        param = {
            "version": version,
            "config": config,
            "inputs": inputMessages
        }
        return param
