from app import app
from models import db
from models import Team

with app.app_context():
    teams = [
        "Team Naveen",
        "Team Shalini",
        "Team Ashitha",
        "Team Rakesh Hariprasad",
        "Team Anirban",
        "Team Vidhya Seetharaman",
        "Team Aftab",
        "Team Prasad",
        "Team Asma",
        "Team Salma"
    ]

    for team_name in teams:

        existing_team = Team.query.filter_by(
            team_name=team_name
        ).first()

        if not existing_team:

            team = Team(
                team_name=team_name
            )

            db.session.add(team)

    db.session.commit()

    print("Teams Added Successfully")
