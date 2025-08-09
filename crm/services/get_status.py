from db.base import LeadModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import aiohttp


async def get_statuses_from_api(url): # example: get data from broker 
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            try:
                data = await response.json()
            except:
                raise Exception('Error statuses')
            else:
                return data

async def save_statuses_to_db(session: AsyncSession, leads):
    for items in leads:
        lead_select = await session.execute(select(LeadModel).where(LeadModel.email == items["email"]))
        lead = lead_select.scalar_one_or_none()
        if lead:
            new_statuses = list(dict.fromkeys(lead.status + items["status"]))
            lead.status = new_statuses
        await session.commit()


async def update_lead_statuses(session: AsyncSession):
    # get_statuses_api = await get_statuses_from_api(url)
    get_statuses_api = {
                        "status": "success",
                        "data":
                        [
                                {"email": "name@gmail.com", "status": ["callback", "noanswer", "lowpot"]},
                                {"email": "test@gmail.com", "status": ["noanswer"]},
                        ]}

    leads = get_statuses_api["data"]
    await save_statuses_to_db(session, leads)
