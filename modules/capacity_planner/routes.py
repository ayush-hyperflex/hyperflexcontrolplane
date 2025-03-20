import os
import httpx
from fastapi import APIRouter, HTTPException, Request, Query, Body
from core.utils import LOG_FILE
import logging
from typing import Optional, Dict, Any
import traceback

CAPACITY_PLANNER_URL = os.getenv("CAPACITY_PLANNER_URL", "http://capacity-planner:3000/api/v1/capacity-planning")
router = APIRouter()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),  # Save logs to file
        logging.StreamHandler()  # Print logs to stdout (for Docker)
    ]
)


async def forward_request(method: str, path: str, request: Request, query_params: Optional[dict] = None,
                          body: Optional[dict] = None):
    """Forwards requests to the capacity planner service."""
    target_url = f"{CAPACITY_PLANNER_URL}/{path}"
    logging.info(f'Request  Received on {target_url}')
    # try:
    async with httpx.AsyncClient(verify=False,timeout=300) as client:
        if method == "GET":
            logging.info("GET Request Received")
            response = await client.get(target_url, params=query_params if query_params else None)
            logging.info(f'Sending Request to {target_url}')
        elif method == "POST":
            if body is not None:
                body= body
            elif body:
                body = request.body()
            else:
                body= None
            response = await client.post(target_url, json=body)
            logging.info(f"{response.text},{response.status_code}")
        else:
            raise HTTPException(status_code=405, detail="Method Not Allowed")
        return response.json()
    # except httpx.RequestError:
    #     error_message = traceback.format_exc()
    #     # logging.error(f"Exception details:\n, {error_message}" , error_message)
    #     raise HTTPException(status_code=500, detail="Failed to reach Capacity Planner service")


@router.post("/deployments")
async def proxy_deployments(request: Request):
    return await forward_request("POST", "deployments", request)


# Route: Proxy GET `/regions`
@router.get("/regions")
async def proxy_regions(request: Request):
    logging.info('In Proxy Regions')
    return await forward_request("GET", "regions", request)


# Route: Proxy GET `/hardware-profiles`
@router.get("/hardware-profiles")
async def proxy_hardware_profiles(request: Request):
    return await forward_request("GET", "hardware-profiles", request)


# Route: Proxy GET `/elasticsearch/versions`
@router.get("/elasticsearch/versions")
async def proxy_elasticsearch_versions(request: Request):
    return await forward_request("GET", "elasticsearch/versions", request)


# Route: Proxy POST `/prepare`
@router.post("/prepare")
async def proxy_prepare(request: Request,query_params: Optional[str] = Query(None, description="Optional query parameters"),
    body: Dict[str, Any] = Body(None, description="Optional raw JSON request body")):
    return await forward_request("POST", "prepare", request,query_params,body)


# Route: Proxy POST `/prepare-iac`
@router.post("/prepare-iac")
async def proxy_prepare_iac(request: Request):
    return await forward_request("POST", "prepare-iac", request)
