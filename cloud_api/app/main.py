import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import database
from app.config import Settings
from app.routes import actuatable_property, actuation, actuator, condition_rule, \
    context_aware_rule, event_rule, event_rule_type, feature_of_interest, gateway, group, \
    location, observable_property, observation, response_procedure, procedure_type, sensor, thing

app = FastAPI()
app.include_router(actuatable_property.router)
app.include_router(actuation.router)
app.include_router(actuator.router)
app.include_router(condition_rule.router)
app.include_router(context_aware_rule.router)
app.include_router(event_rule.router)
app.include_router(event_rule_type.router)
app.include_router(feature_of_interest.router)
app.include_router(gateway.router)
app.include_router(group.router)
app.include_router(location.router)
app.include_router(observable_property.router)
app.include_router(observation.router)
app.include_router(response_procedure.router)
app.include_router(procedure_type.router)
app.include_router(sensor.router)
app.include_router(thing.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=Settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    database.create_db_and_tables()


@app.get("/")
def read_health():
    return {"status": "UP"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
