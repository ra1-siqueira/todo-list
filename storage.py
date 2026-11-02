# Biblioteca padrao
import csv
import os

# Modulos do projeto
from task import Task

class TaskStorage:
    TODO     : str       = 'todo.csv'
    TMP      : str       = 'tmp.temp'
    HISTORY  : str       = 'command_history'
    INFO     : str       = 'info.txt'
    HEADER   : list[str] = ['name', 'done', 'date', 'pin', 'daily']
    
    def __init__(self) -> None:
        self._init_storage()
        
    def _init_storage(self) -> None:
        try:
            with open(TaskStorage.TODO, 'x', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=TaskStorage.HEADER)
                writer.writeheader()
        except FileExistsError:
            pass
                
    def save(self, task: Task) -> None:
        with open(TaskStorage.TODO, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=TaskStorage.HEADER)
            writer.writerow({
                'name' : task.name,
                'done' : task.is_done,
                'date' : task.date,
                'pin'  : task.is_pinned,
                'daily': task.is_daily
            })
            
    def list_tasks(self) -> list[Task]:
        t_list = []
        with open(TaskStorage.TODO, newline='') as f:
            reader = csv.DictReader(f)             
            for t in reader:
                task = Task(
                    t['name' ],
                    t['done' ] == 'True',
                    t['date' ],
                    t['pin'  ] == 'True',
                    t['daily'] == 'True'
                )
                t_list.append(task)
        return t_list
        
    def update_all(self, tasks: list[Task]) -> None:
        with open(TaskStorage.TMP, 'w', newline='') as dst:
            writer = csv.DictWriter(dst, fieldnames=TaskStorage.HEADER)
            writer.writeheader()
            for t in tasks:
                writer.writerow({
                    'name' : t.name,
                    'done' : t.is_done,
                    'date' : t.date,
                    'pin'  : t.is_pinned,
                    'daily': t.is_daily
                })
        os.replace(TaskStorage.TMP, TaskStorage.TODO)
    
    def get_info(self) -> str:
        with open(TaskStorage.INFO, encoding='utf-8') as f:
            return f.read()
    
    def update_history(self, command: str) -> None:
        with open(TaskStorage.HISTORY, 'a', encoding='utf-8') as f:
            f.write(command + '\n')
            
    def get_history(self) -> list[str]:
        try:
            with open(TaskStorage.HISTORY, encoding='utf-8') as f:        
                return f.readlines()
        except FileNotFoundError:
            return []
            
    def clear_history(self) -> None:
        with open(TaskStorage.HISTORY, 'w', encoding='utf-8') as f:
            pass
