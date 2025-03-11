import os
import httpx
from fastapi import APIRouter, HTTPException, Request
from core.utils import LOG_FILE
import logging

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

async def forward_request(method: str, path: str, request: Request):
    """Forwards requests to the capacity planner service."""
    target_url = f"{CAPACITY_PLANNER_URL}/{path}"

    try:
        async with httpx.AsyncClient() as client:
            if method == "GET":
                logging.info("GET Request Received")
                response = await client.get(target_url, params=request.query_params)
                logging.info(f'Sending Request to {target_url}')
            elif method == "POST":
                body = await request.json()
                response = await client.post(target_url, json=body)
            else:
                raise HTTPException(status_code=405, detail="Method Not Allowed")

            return response.json()
    except httpx.RequestError:
        raise HTTPException(status_code=500, detail="Failed to reach Capacity Planner service")


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
async def proxy_prepare(request: Request):
    return await forward_request("POST", "prepare", request)


# Route: Proxy POST `/prepare-iac`
@router.post("/prepare-iac")
async def proxy_prepare_iac(request: Request):
    return await forward_request("POST", "prepare-iac", request)
