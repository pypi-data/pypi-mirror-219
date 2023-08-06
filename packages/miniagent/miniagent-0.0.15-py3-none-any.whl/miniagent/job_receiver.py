from datetime import datetime, timedelta
from . import scheduler
from .executer import ExecuterCaller

class ScheduledJob:

    def __init__(self, caller: ExecuterCaller, jobs: list) -> None:

        self.caller = caller
        for job in jobs:
            self._run_job(job)

    def _run_job(self, job: dict) -> int:

        executer = job.pop('executer')

        from . import app_name
        if job.get('agents'):
            agents = job.pop('agents')
            if app_name not in agents:
                return 0

        scheduler.add_job(
            #func=self.caller.execute_command,
            func=self._call_execute_command,
            args=[job['id'], {'executer':executer}],
            **job
        )        
        return 1
    
    def _call_execute_command(self, id: str, message: dict):

        from . import app, zipkin
        with app.app_context():

            if zipkin:
                zipkin.create_span('scheduled_job.'+ id)
                zipkin.update_tags(param=message)

            rtn, comment = self.caller.execute_command(message)

            if zipkin:
                zipkin.update_tags(
                    param  = message,
                    result = comment,
                )         