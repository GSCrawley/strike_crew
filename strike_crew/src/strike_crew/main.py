#!/usr/bin/env python
import sys
from strike_crew.crew import StrikeCrewCrew
import config 



osint_agent = Agent(
    role=
)
def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    crew = StrikeCrewCrew(
    agents=[osint_agent],
    tasks=[osint_task],
    verbose=2
)
    return crew.kickoff()