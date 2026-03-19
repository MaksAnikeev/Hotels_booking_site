from src.schemas.facilities_schemas import FacilitiesGetSchemas, FacilitiesCreateSchemas
from src.services.base_service import BaseService


class FacilitiesService(BaseService):
    async def get_all(
        self,
    ) -> list[FacilitiesGetSchemas]:

        facilities = await self.db.facilities.get_all()
        return facilities

    async def add(
        self, facilities_info: FacilitiesCreateSchemas
    ) -> FacilitiesGetSchemas:

        facility = await self.db.facilities.add(facilities_info)
        return facility
