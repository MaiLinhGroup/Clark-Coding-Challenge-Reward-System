import re
from collections import deque
from fastapi import FastAPI, UploadFile, HTTPException


description = """
ClarkCodingChallenge-RewardSystem API helps you to calculate the score for each user that they gain through direct and indirect referrals. 🚀

## Confirmed Invitations

You can **calculate the score for confirmed invitations** for all participating users.
"""

app = FastAPI(
    title="ClarkCodingChallenge-RewardSystem",
    description=description,
    version="0.0.1",
    contact={
        "name": "Mai Linh Nguyen",
        "url": "https://github.com/MaiLinhGroup",
        "email": "MaiLinhGroup@users.noreply.github.com",
    },
    )

# routes layer
@app.get("/")
async def health_check():
    return {"Hello": "World"}

@app.post(
    "/confirmed-invitations/scores",
    summary="Calculate the score for confirmed invitations",
    description="For each confirmed invitation, the user who refer/invite the new user to the system receives points. The endpoint calculates the score for each user that they achieve through direct and indirect referrals.",
)
async def calculate_score(file: UploadFile):
    contents = await file.read()
    events = contents.decode().split('\n')

    if len(events) == 1 and events[0] == '':
        raise HTTPException(status_code=400, detail="Input file is empty")

    timestamp = r'^([1]\d|[2][0])(\d{2})-([0]\d|[1][0-2])-(0[1-9]|[12]\d|3[01])\s((0\d|1\d|2[0-3])):(0\d|[1-5]\d)'
    pattern = re.compile(timestamp)
    try:
        events.sort(key=lambda x: re.search(pattern,x).group())
    except AttributeError as e:
        raise HTTPException(status_code=400, detail="Timestamp in input file is not in the correct format") from e

    return await _calculate_score_v2(events)
    

# service layer
async def _calculate_score(events: list[str]) -> dict:
    # key: invitee, value: inviter
    referral_record = {}
    # key: inviter, value: score for confirmed invitation
    scoring = {}

    # should match either "<inviter> recommends <invitee>" or "<invitee> accepts"
    recommendation = r'(?P<P1>[A-Z])\s{1}recommends\s{1}(?P<P2>[A-Z])$'
    accept = r'(?P<P3>[A-Z])\s{1}accepts$'
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


async def reward_referrals(scoring: dict, referral_record: dict, woo: str, k: int) -> None:
    beneficiary = referral_record.get(woo)
    if beneficiary is not None:
        scoring[beneficiary] = scoring.get(beneficiary, 0) + 0.5 ** k
        await reward_referrals(scoring, referral_record, beneficiary, k + 1)
    return
        
### alternative implementation with deque (double ended queue aka Python's version of linked list)
async def _calculate_score_v2(events: list[str]) -> dict:
    # list of referrals
    referral_graphs = []
    recommendation = r'(?P<P1>[A-Z])\s{1}recommends\s{1}(?P<P2>[A-Z])$'
    pattern = re.compile(recommendation)
    for event in events:
        recomm_match = re.search(pattern, event)
        if recomm_match is not None and is_first_invitation_for(recomm_match['P2'], referral_graphs):
            referral_graphs.append(deque([recomm_match['P1'],recomm_match['P2']]))
            
    # find confirmed invitations
    scoring = {}
    accept = r'(?P<P3>[A-Z])\s{1}accepts$'
    pattern = re.compile(accept)
    for latest_event in reversed(events):
        accept_match = re.search(pattern, latest_event)
        if accept_match is not None:
            await sum_up_score(accept_match['P3'], referral_graphs, scoring, 0)

    return scoring

async def sum_up_score(confirmed_invitee: str, referral_graphs: list, scoring: dict, k: int) -> None:
    for r in referral_graphs:
        if r[-1] == confirmed_invitee:
            beneficiary = r[0]
            scoring[beneficiary] = scoring.get(beneficiary, 0) + 0.5 ** k
            await sum_up_score(beneficiary, referral_graphs, scoring, k + 1)
    return

def is_first_invitation_for(invitee: str, referral_graphs: list) -> bool:
    return all(r[-1] != invitee for r in referral_graphs)