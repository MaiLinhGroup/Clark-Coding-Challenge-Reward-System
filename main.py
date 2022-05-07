import re
from fastapi import FastAPI, UploadFile

app = FastAPI()

# routes layer
@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/scoring")
async def calculate_score(file: UploadFile):
    contents = await file.read()
    return await _calculate_score(contents.decode().split('\n'))

# service layer
async def _calculate_score(events: list[str]):
    # key: invitee, value: inviter
    referral_record = {}
    # key: inviter, value: score for confirmed invitation
    scoring = {}

    # should match either "<inviter> recommends <invitee>" or "<invitee> accepts"
    recommendation = '(?P<P1>[A-Z])\s{1}recommends\s{1}(?P<P2>[A-Z])$'
    accept = '(?P<P3>[A-Z])\s{1}accepts$'
    pattern = re.compile(f'{recommendation}|{accept}')

    for event in events:
        match = re.search(pattern, event)
        if match is not None:
            if match['P1'] is not None and match['P2'] is not None and referral_record.get(match['P2']) is None:
                # only the first invitation counts
                referral_record[match['P2']] = match['P1']
            else:
                await reward_referrals(scoring, referral_record, match['P3'], 0)
    return scoring


async def reward_referrals(scoring: dict, referral_record: dict, woo: str, k: int):
    beneficiary = referral_record.get(woo)
    if beneficiary is not None:
        scoring[beneficiary] = scoring.get(beneficiary, 0) + 0.5 ** k
        return await reward_referrals(scoring, referral_record, beneficiary, k + 1)
    return