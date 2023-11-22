import asyncio
import logging
from fastapi import APIRouter, HTTPException, Request

from ..helper import runtime
from ..middle import apply
from ..request import apply as res_apply

router = APIRouter(
    tags=["apply"],
)


async def async_build(request: Request):
    request_id = request.state.request_id
    extra = {'request_id': request_id}
    logger = runtime.loadLogging(logname='global_logger', level=logging.INFO, extra=extra)
    params = await request.json()
    apply_request = res_apply.RequestApply()
    build = apply.Build(request)
    await build.set_logger(logger)
    await build.set_api_request(apply_request)
    await build.set_params(params)
    await build.run()


@router.post("/apply/build")
async def get_apply_build(request: Request):
    try:
        await async_build(request)
    except Exception as e:
        raise HTTPException(status_code=401, detail="提交申请执行失败")
    return {"message": "ok", "request_id": request.state.request_id}


@router.get("/apply/async_build")
async def get_async_apply_build():
    loop = asyncio.get_event_loop()
    task = loop.create_task(async_build())
    await asyncio.wait([task])
    return {"message": "Hello"}
