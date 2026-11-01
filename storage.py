# Biblioteca padrao
import csv
import os

# Modulos do projeto
from task import Task

class TaskStorage:
    FILENAME : str       = 'todo.csv'
    TMP      : str       = 'todo.temp'
    HEADER   : list[str] = ['name', 'done', 'date', 'pin', 'daily']
    
    def __init__(self) -> None:
        self._init_storage()
        
    def _init_storage(self) -> None:
        try:
            with open(TaskStorage.FILENAME, 'x', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=TaskStorage.HEADER)
                writer.writeheader()
        except FileExistsError:
            pass
                
    def save(self, task: Task) -> None:
        with open(TaskStorage.FILENAME, 'a', newline='') as f:
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
        with open(TaskStorage.FILENAME, newline='') as f:
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
        os.replace(TaskStorage.TMP, TaskStorage.FILENAME)
