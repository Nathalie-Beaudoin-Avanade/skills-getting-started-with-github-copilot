"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")


def normalize_email(email: str) -> str:
    """Normalize student email to prevent case/whitespace duplicates."""
    return email.strip().lower()

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball team for all skill levels",
        "schedule": "Tuesdays and Saturdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Learn tennis skills and play friendly matches",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["jackson@mergington.edu", "isabella@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore painting, drawing, and sculpture techniques",
        "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["grace@mergington.edu"]
    },
    "Drama Club": {
        "description": "Perform in theatrical productions and improve acting skills",
        "schedule": "Tuesdays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific discoveries",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["ryan@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 14,
        "participants": ["noah@mergington.edu", "ava@mergington.edu"]
    },
    "Volleyball Club": {
        "description": "Practice teamwork, serving, and match-play volleyball skills",
        "schedule": "Tuesdays and Thursdays, 5:00 PM - 6:30 PM",
        "max_participants": 18,
        "participants": ["liam@mergington.edu", "zoe@mergington.edu"]
    },
    "Track and Field": {
        "description": "Train in sprinting, distance running, and field events",
        "schedule": "Mondays and Wednesdays, 5:00 PM - 6:30 PM",
        "max_participants": 22,
        "participants": ["ethan@mergington.edu", "nora@mergington.edu"]
    },
    "Choir Ensemble": {
        "description": "Develop vocal technique and perform choral music",
        "schedule": "Wednesdays and Fridays, 4:30 PM - 6:00 PM",
        "max_participants": 24,
        "participants": ["chloe@mergington.edu", "henry@mergington.edu"]
    },
    "Photography Club": {
        "description": "Learn composition, lighting, and storytelling through photography",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["lily@mergington.edu"]
    },
    "Math Olympiad": {
        "description": "Solve advanced math problems and prepare for competitions",
        "schedule": "Tuesdays, 4:30 PM - 6:00 PM",
        "max_participants": 16,
        "participants": ["aaron@mergington.edu", "ella@mergington.edu"]
    },
    "Robotics Club": {
        "description": "Design, build, and program robots for challenges",
        "schedule": "Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": ["owen@mergington.edu", "scarlett@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]
    normalized_email = normalize_email(email)

    if not normalized_email:
        raise HTTPException(status_code=400, detail="Email is required")

    # Add student
    # Validate student is not already signed up
    if normalized_email in {normalize_email(p) for p in activity["participants"]}:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")
    activity["participants"].append(normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def unregister_participant(activity_name: str, email: str):
    """Unregister a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    normalized_email = normalize_email(email)

    if not normalized_email:
        raise HTTPException(status_code=400, detail="Email is required")

    matching_email = next(
        (participant for participant in activity["participants"] if normalize_email(participant) == normalized_email),
        None,
    )

    if matching_email is None:
        raise HTTPException(status_code=404, detail="Participant not found in this activity")

    activity["participants"].remove(matching_email)
    return {"message": f"Unregistered {matching_email} from {activity_name}"}
