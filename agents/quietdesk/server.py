from __future__ import annotations

import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from . import store
from .runner import bind_case, start_demo

load_dotenv()

app = FastAPI(title="QuietDesk", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class BindBody(BaseModel):
    item_id: str
    decision: str
    note: str = ""


@app.get("/health")
def health():
    return {"ok": True, "service": "quietdesk"}


@app.post("/shifts/demo")
def demo():
    return start_demo().model_dump()


@app.get("/shifts")
def shifts():
    return [s.model_dump() for s in store.list_shifts()]


@app.get("/shifts/{shift_id}")
def get_shift(shift_id: str):
    try:
        return store.load(shift_id).model_dump()
    except FileNotFoundError:
        raise HTTPException(404, "shift not found") from None


@app.post("/shifts/{shift_id}/bind")
def bind(shift_id: str, body: BindBody):
    try:
        return bind_case(shift_id, body.item_id, body.decision, body.note).model_dump()
    except KeyError:
        raise HTTPException(404, "case not found") from None
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    except FileNotFoundError:
        raise HTTPException(404, "shift not found") from None


def main() -> None:
    import uvicorn

    uvicorn.run(
        "quietdesk.server:app",
        host=os.getenv("QUIETDESK_HOST", "127.0.0.1"),
        port=int(os.getenv("QUIETDESK_PORT", "8787")),
        reload=False,
    )


if __name__ == "__main__":
    main()
