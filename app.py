from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

def get_player_info(uid, region):
    url = f"https://aditya-info-v11op.onrender.com/player-info?uid={uid}&region={region}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"حدث خطأ أثناء الاتصال: {e}"}

def unix_to_datetime(unix_timestamp):
    if unix_timestamp and unix_timestamp != "0":
        return datetime.utcfromtimestamp(int(unix_timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    else:
        return "غير متوفر"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uid = request.form.get("uid", "").strip()
        region = request.form.get("region", "").strip().upper()
        if not uid or not region:
            return render_template("result.html", uid=uid, region=region, data=None, error="يجب إدخال جميع الحقول.")

        raw_data = get_player_info(uid, region)

        if "player_info" not in raw_data:
            return render_template("result.html", uid=uid, region=region, data=None, error="لا توجد بيانات لهذا الحساب.")

        info = raw_data["player_info"]

        basic = info.get("basicInfo", {})
        pet = info.get("petInfo", {})
        social = info.get("socialInfo", {})
        profile = info.get("profileInfo", {})
        clan = info.get("clanBasicInfo", {})

        # رابط صورة اللباس الجديدة
        outfit_image_url = f"https://aditya-outfit-v11op.onrender.com/outfit-image?uid={uid}&region={region}"

        organized_data = {
            # Basic Info
            "nickname": basic.get("nickname", "غير متوفر"),
            "accountId": basic.get("accountId", "غير متوفر"),
            "region": basic.get("region", "غير متوفر"),
            "level": basic.get("level", "غير متوفر"),
            "liked": basic.get("liked", "غير متوفر"),
            "rankingPoints": basic.get("rankingPoints", "غير متوفر"),
            "rank": basic.get("rank", "غير متوفر"),
            "createAt": unix_to_datetime(basic.get("createAt", "0")),
            "lastLoginAt": unix_to_datetime(basic.get("lastLoginAt", "0")),
            "bannerId": basic.get("bannerId", "غير متوفر"),
            "badgeId": basic.get("badgeId", "غير متوفر"),
            "headPic": basic.get("headPic", "غير متوفر"),

            # Pet Info
            "petName": pet.get("name", "غير متوفر"),
            "petLevel": pet.get("level", "غير متوفر"),
            "petExp": pet.get("exp", "غير متوفر"),

            # Profile Info
            "avatarId": profile.get("avatarId", "غير متوفر"),
            "clothes": profile.get("clothes", []),
            "equipedSkills": profile.get("equipedSkills", []),
            "isSelected": profile.get("isSelected", False),
            "isSelectedAwaken": profile.get("isSelectedAwaken", False),

            # Social Info
            "language": social.get("language", "غير متوفر"),
            "gender": social.get("gender", "غير متوفر"),
            "signature": social.get("signature", "غير متوفر"),

            # Clan Info
            "clanName": clan.get("name", "غير متوفر"),
            "clanId": clan.get("clanId", "غير متوفر"),
            "clanRole": clan.get("role", "غير متوفر"),

            # Outfit Image
            "outfit_image_url": outfit_image_url
        }

        return render_template("result.html", uid=uid, region=region, data=organized_data, error=None)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
