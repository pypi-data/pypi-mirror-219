from typing import TypedDict

class WorkflowRun(TypedDict):
    id: str
    status: str
    createdAt: str
    dateStarted: str
    dateEnded: str
    logs: str
    errorLogs: str
    payload: str
