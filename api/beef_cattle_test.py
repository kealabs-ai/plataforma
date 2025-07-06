from fastapi import APIRouter

router = APIRouter(
    prefix="/api/beef_cattle_test",
    tags=["Beef Cattle Test"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def test_endpoint():
    """
    Test endpoint to verify if the router is working
    """
    return {"message": "Beef cattle test endpoint is working"}