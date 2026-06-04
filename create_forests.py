from app import app
from models import db
from models import Team
from models import Forest

with app.app_context():

    teams = Team.query.all()

    for team in teams:

        existing_forest = Forest.query.filter_by(
            team_id=team.id
        ).first()

        if existing_forest:
            print(f"Forest already exists for {team.team_name}")
            continue

        forest = Forest(
            team_id=team.id,
            water_count=0,
            tree_count=0,
            current_stage="Seed"
        )

        db.session.add(forest)

    db.session.commit()

    print("Forest creation completed")
