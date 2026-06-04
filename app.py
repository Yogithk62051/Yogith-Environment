from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import session

from datetime import datetime, timedelta

from models import db
from models import Team
from models import Forest
from models import User

from tree_logic import get_stage
from tree_image import get_tree_image
from models import CompletedTree
from flask import session
import os




app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY",
    "development_secret"
)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:///environment.db"
)
db.init_app(app)
with app.app_context():
    db.create_all()

# ==========================
# Home Page
# ==========================

@app.route("/")
def home():

    return render_template(
        "home.html"
    )


@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form["name"]

        email = request.form["email"]

        password = request.form["password"]

        team_name = request.form["team"]
        print("SELECTED TEAM:", team_name)
        print("ALL TEAMS:", [t.team_name for t in Team.query.all()])
        team = Team.query.filter_by(
            team_name=team_name
        ).first()


        if not team:

            return "Team not found"

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            return redirect("/login")

        user = User(
            name=name,
            email=email,
            password=password,
            team_id=team.id
        )

        db.session.add(user)

        db.session.commit()

        return redirect("/login")

    return render_template(
        "register.html"
    )
# ==========================
# Login Page
# ==========================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]

        user = User.query.filter_by(
            email=email
        ).first()

        if not user:

            return "User not found"

        if user.password != password:

            return "Invalid password"

        session["user_id"] = user.id

        return redirect(
            f"/forest/{user.team_id}"
        )

    return render_template(
        "login.html"
    )
# ==========================
# Logout
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

# ==========================
# Team Lobby
# ==========================

@app.route("/team/<int:team_id>")
def team(team_id):

    team = Team.query.get_or_404(
        team_id
    )

    return render_template(
        "team_lobby.html",
        team=team
    )


# ==========================
# Team Forest
# ==========================

@app.route("/forest/<int:team_id>")
def forest(team_id):

    team = Team.query.get_or_404(
        team_id
    )

    if len(team.users) == 0:

        return f"No users found in team {team.team_name}"

    user = User.query.get(
        session.get("user_id")
    )
    if not user:
        return redirect("/login")

    print("================================")
    print("SESSION USER ID:", session.get("user_id"))
    print("CURRENT USER:", user.name)
    print("BUCKET:", user.water_bucket)
    print("==")

    remaining_seconds = 0

    # Bucket Refill Logic

    if user.water_bucket == 0 and user.last_watered:

        time_passed = (
            datetime.now()
            - user.last_watered
        )

        if time_passed >= timedelta(
            seconds=30
        ):

            user.water_bucket = 1

            db.session.commit()

        else:

            remaining_seconds = (
                30-
                int(
                    time_passed.total_seconds()
                )
            )

    forest = Forest.query.filter_by(
        team_id=team.id
    ).first()

    if not forest:

        return f"No forest found for team {team.team_name}"

    tree_image = get_tree_image(
        forest.current_stage
    )

    return render_template(
        "dashboard.html",
        team=team,
        forest=forest,
        user=user,
        remaining_seconds=remaining_seconds,
        tree_image=tree_image
    )


# ==========================
# Water Plant
# ==========================

@app.route(
    "/water/<int:team_id>",
    methods=["POST"]
)
def water(team_id):

    team = Team.query.get_or_404(
        team_id
    )

    if len(team.users) == 0:

        return redirect(
            f"/forest/{team.id}"
        )

    user = User.query.get(
        session.get("user_id")
    )

    forest = Forest.query.filter_by(
        team_id=team.id
    ).first()

    if not forest:

        return redirect(
            f"/forest/{team.id}"
        )

    if user.water_bucket == 0:

        return redirect(
            f"/forest/{team.id}"
        )

    # Water Tree

    forest.water_count += 1

    forest.current_stage = get_stage(
        forest.water_count
    )

    # Consume Bucket

    user.water_bucket = 0

    user.last_watered = datetime.now()

    # Tree Cycle Complete

    if forest.water_count > 6:
        forest.tree_count += 1

        completed_tree = CompletedTree(

            team_id=team.id,

            user_name=user.name,

            tree_image="large_tree.png"

        )

        db.session.add(
            completed_tree
        )

        forest.water_count = 0

        forest.current_stage = "Seed"

    db.session.commit()

    return redirect(
        f"/forest/{team.id}"
    )

@app.route(
'/team_forest/<int:team_id>'
)
def team_forest(team_id):

    team = Team.query.get_or_404(
        team_id
    )

    completed_trees = CompletedTree.query.filter_by(
        team_id=team.id
    ).all()

    return render_template(

        'team_forest.html',

        team=team,

        trees=completed_trees
    )


# ==========================
# Leaderboard
# ==========================

@app.route("/leaderboard")
def leaderboard():

    forests = Forest.query.order_by(
        Forest.tree_count.desc()
    ).all()

    return render_template(
        "leaderboard.html",
        forests=forests,
        Team=Team
    )

# ==========================
# Run Application
# ==========================

if __name__ == "__main__":

    app.run(
        debug=True
    )
