# Biblioteca padrao
from datetime   import date

# Modulos do projeto
from storage    import TaskStorage
from task       import Task

class TaskManager:
    def __init__(self) -> None:
        self.storage : TaskStorage = TaskStorage()
        self.tasks   : list[Task]  = self.storage.list_tasks()
        
    def create(self, name: str) -> None:
        task = Task(name)
        self.tasks.append(task)
        self.storage.save(task)
        
    def get_tasks(self) -> list[Task]:
        return self.tasks.copy()
    
    def _find(self, name: str) -> Task | None:
        for t in self.tasks:
            if t.name == name:
                return t
        return None
    
    def toggle_done(self, name: str) -> None:
        task = self._find(name)
        if task:
            task.toggle_done()
            self.storage.update_all(self.tasks)
        
    def toggle_pin(self, name: str, case: str) -> None:
        task = self._find(name)
        if task:
            if task.is_pinned and case == 'unpin':
                task.unpin()
            elif task.is_pinned == False and case == 'pin':
                task.pin()
            self.storage.update_all(self.tasks)
                    
    def toggle_daily(self, name: str) -> None:
        task = self._find(name)
        if task:
            task.toggle_daily()
            self.storage.update_all(self.tasks)
            
    def reorder_after_pin(self, recently_pinned: str) -> None:
        pinned_tasks     = []
        not_pinned_tasks = []       
        for t in self.tasks:
            if t.name == recently_pinned and t.is_pinned:
                pinned_tasks.append(t)
            elif t.name == recently_pinned:
                not_pinned_tasks.append(t)             
        for t in self.tasks:
            if t.is_pinned and t.name != recently_pinned:
                pinned_tasks.append(t)
            elif t.name != recently_pinned:
                not_pinned_tasks.append(t)              
        self.tasks = pinned_tasks + not_pinned_tasks
        self.storage.update_all(self.tasks)

    # nao deleta uma tarefa fixada
    def delete(self, name: str) -> None:
        self.tasks = [
            t for t in self.tasks
            if t.name != name or t.is_pinned
        ]
        self.storage.update_all(self.tasks)
        
    def force_delete(self, name: str) -> None:
        self.tasks = [
            t for t in self.tasks
            if t.name != name
        ]
        self.storage.update_all(self.tasks)
    
    # preserva as tarefas fixadas
    def delete_all(self) -> None:
        self.tasks = [
            t for t in self.tasks
            if t.is_pinned
        ]
        self.storage.update_all(self.tasks)
        
    def force_delete_all(self) -> None:
        self.tasks = []
        self.storage.update_all(self.tasks)
        
    def mark_all_as_pending(self) -> None:
        for t in self.tasks:
            if t.is_done:
                t.toggle_done()
        self.storage.update_all(self.tasks)
        
    def update_daily_tasks(self) -> None:
        current_day = date.today()
        if not self.tasks:
            return
        for t in self.tasks:
            if t.is_daily and t.is_done and t.date != current_day:
                t.toggle_done()
        self.storage.update_all(self.tasks)
