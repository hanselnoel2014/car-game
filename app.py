import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

CAR_CONFIGS = {
    "sports":  {"color": "#e74c3c", "accent": "#c0392b", "width": 36, "height": 62,  "type": "sports"},
    "muscle":  {"color": "#3498db", "accent": "#2980b9", "width": 42, "height": 66,  "type": "muscle"},
    "suv":     {"color": "#2ecc71", "accent": "#27ae60", "width": 46, "height": 70,  "type": "suv"},
    "classic": {"color": "#f39c12", "accent": "#d35400", "width": 44, "height": 68,  "type": "classic"},
    "pickup":  {"color": "#9b59b6", "accent": "#8e44ad", "width": 46, "height": 72,  "type": "pickup"},
    "supercar":{"color": "#1abc9c", "accent": "#16a085", "width": 34, "height": 58,  "type": "supercar"},
}

HARD_CONFIG = {
    "speed": 7, "enemy_speed": 9, "spawn_rate": 45,
    "obstacle_rate": 90, "label": "Hard"
}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/select", response_class=HTMLResponse)
async def select_car(request: Request):
    cars = [
        {"id": "sports",   "name": "Sports Car",    "description": "Fast & nimble",       **CAR_CONFIGS["sports"]},
        {"id": "muscle",   "name": "Muscle Car",     "description": "Raw American power",  **CAR_CONFIGS["muscle"]},
        {"id": "suv",      "name": "SUV",            "description": "Tough & tall",        **CAR_CONFIGS["suv"]},
        {"id": "classic",  "name": "Classic Cruiser","description": "Old-school style",    **CAR_CONFIGS["classic"]},
        {"id": "pickup",   "name": "Pickup Truck",   "description": "Rugged hauler",       **CAR_CONFIGS["pickup"]},
        {"id": "supercar", "name": "Supercar",       "description": "Street-legal rocket", **CAR_CONFIGS["supercar"]},
    ]
    return templates.TemplateResponse("select.html", {"request": request, "cars": cars})


@app.get("/game", response_class=HTMLResponse)
async def game(request: Request, car: str = "sports"):
    car_cfg = CAR_CONFIGS.get(car, CAR_CONFIGS["sports"])
    return templates.TemplateResponse(
        "game.html",
        {
            "request":   request,
            "car":       car,
            "car_cfg":   car_cfg,
            "level_cfg": HARD_CONFIG,
        },
    )


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

