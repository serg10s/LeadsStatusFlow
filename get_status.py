import requests
from db.base import LeadData
from sqlalchemy.orm import Session


def get_statuses_from_api():
    url = "https://brokercrm.com/api/getstatuses"  # Exemple url
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # {"email": "fdf@gmail.com", "status": "callback"} exemple response
    else:
        raise Exception('Error statuses')


def save_statuses_to_db(db: Session, leads):

    for items in leads:
        lead = db.query(LeadData).filter_by(email=items["email"]).first()
        if lead:
            new_statuses = list(dict.fromkeys(lead.status + items["status"]))
            lead.status = new_statuses
        db.commit()


def update_lead_statuses(db: Session):
    # get_statuses_api = json.loads(get_statuses_from_api())
    get_statuses_api = {
                        "status": "success",
                        "data":
                        [
                                {"email": "fdf@gmail.com", "status": ["callback", "noanswer", "lowpot"]},
                                {"email": "afa@gmail.com", "status": ["noanswer"]},
                        ]}

    leads = get_statuses_api["data"]
    save_statuses_to_db(db, leads)
