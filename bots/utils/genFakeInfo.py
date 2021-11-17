from datetime import datetime

from kantex.html import Code, Section, SubSection

from .aiohttp import AioHttp


async def genFakeInfo(chkUrl: str):
    rData, resp = await AioHttp.get_json(chkUrl)
    if not resp.status == 200:
        return "API Unreachable", None

    user = rData["results"][0]

    dobTime = datetime.strptime(user["dob"]["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
    userPic = user["picture"]["large"]

    infoText = str(
        Section(
            "Fake User Information",
            str(f"Name: {Code(user['name']['title'])}"),
            str(f"Gender: {Code(user['gender'])}"),
            SubSection(
                "Location",
                str(
                    f"Street: {Code(user['location']['street']['number'])}, {user['location']['street']['name']}",
                ),
                str(f"City: {Code(user['location']['city'])}"),
                str(f"State: {Code(user['location']['state'])}"),
                str(f"Country: {Code(user['location']['country'])}"),
                str(f"Postcode: {Code(user['location']['postcode'])}"),
            ),
            str(f"Email: {Code(user['email'])}"),
            str(f"Date of Birth: {Code(dobTime.strftime('%B %m, %Y'))}"),
            str(f"Age: {Code(user['dob']['age'])}"),
            str(f"Cellphone: {Code(user['cell'])}"),
            str(f"Phone: {Code(user['phone'])}"),
        ),
    )
    return infoText, userPic
