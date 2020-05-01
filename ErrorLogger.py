import os

class ErrorLogger:
    def __init__(self, timestamp):
        self.Filepath = f"./ErrorLogs/Log-{timestamp}.txt"
        self.Initialise(self.Filepath)
        self.ErrorList = []

    def Initialise(self, filepath):
        path = os.path.dirname(filepath)
        os.makedirs(path, exist_ok=True)
        with open(filepath, 'w+') as f:
            pass

    def CheckSolutionExists(self, sol_array, period, agent_id):
        if len(sol_array) == 0:
            self.ErrorList.append(f"No solution found for agent {agent_id} in period {period}.")
            print(f"No solution found for agent {agent_id} in period {period}.")
            return False
        return True

    def SaveLog(self):
        if len(self.ErrorList) > 0:
            with open(self.Filepath, 'w') as f:
                for item in self.ErrorList:
                    f.write(f"{item}\n")

