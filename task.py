from datetime import date

class Task:
    def __init__(
        self,
        name      : str,
        done      : bool        = False,
        task_date : date | None = None,
        pin       : bool        = False,
        daily     : bool        = False
    ) -> None:
        self.name      : str  = name
        self.is_done   : bool = done
        if task_date is None:
            task_date = date.today()
        self.date      : date = task_date
        self.is_pinned : bool = pin
        self.is_daily  : bool = daily
        
    def toggle_done(self) -> None:
        self.is_done   = not self.is_done
        self.task_date = date.today()
        
    def pin(self) -> None:
        self.is_pinned = True
        
    def unpin(self) -> None:
        self.is_pinned = False
        
    def toggle_daily(self) -> None:
        self.is_daily  = not self.is_daily
        self.task_date = date.today()
