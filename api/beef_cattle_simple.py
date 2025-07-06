from fastapi import APIRouter

router = APIRouter(
    prefix="/api/beef_cattle_simple",
    tags=["Beef Cattle Simple"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_all_beef_cattle_simple():
    """
    Simple endpoint to test if the router is working
    """
    return {"message": "Simple beef cattle endpoint is working"}