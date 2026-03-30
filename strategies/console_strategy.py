from core.interfaces import IOutputStrategy

class ConsoleOutput(IOutputStrategy):
    def send(self, data: list):
        print("\n=== NYC LEADING CAUSES OF DEATH ===")
        for record in data:
            cause = record.get('Leading Cause')
            race = record.get('Race Ethnicity')
            deaths = record.get('Deaths')
            year = record.get('Year')
            print(f"[{year}] {cause} | Race: {race} | Deaths: {deaths}")