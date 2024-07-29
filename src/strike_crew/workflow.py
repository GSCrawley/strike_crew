# workflow.py

from crewai import Crew, Task
from strike_crew.models import EmergingThreat
from typing import List

class ThreatIntelWorkflow:
    def __init__(self, crew: Crew):
        self.crew = crew

    def run(self, initial_query: str) -> List[EmergingThreat]:
        # Create a task for the Crew Manager
        manager_task = Task(
            description=f"Coordinate the threat intelligence gathering process for the query: {initial_query}",
            agent=self.crew.manager
        )

        # The Crew Manager will coordinate the execution of tasks
        crew_result = self.crew.kickoff(manager_task)
        
        return self._process_results(crew_result)

    def run_continuous(self, interval: int = 3600):
        import time
        while True:
            results = self.run("Latest cybersecurity threats")
            print(f"Found {len(results)} emerging threats")
            for threat in results:
                print(f"Emerging Threat: {threat}")
            time.sleep(interval)

    def _process_results(self, crew_result) -> List[EmergingThreat]:
        results = []
        if isinstance(crew_result, list):
            for item in crew_result:
                if isinstance(item, dict):
                    threat = EmergingThreat(
                        ioc=item.get('ioc', {}),
                        ttps=item.get('ttps', {}),
                        threat_actors=item.get('threat_actors', []),
                        cve_ids=item.get('cve_ids', [])
                    )
                    results.append(threat)
        elif isinstance(crew_result, dict):
            threat = EmergingThreat(
                ioc=crew_result.get('ioc', {}),
                ttps=crew_result.get('ttps', {}),
                threat_actors=crew_result.get('threat_actors', []),
                cve_ids=crew_result.get('cve_ids', [])
            )
            results.append(threat)
        return results