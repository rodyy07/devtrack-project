from abc import ABC, abstractmethod
from datetime import datetime

#--------------------BASE CLASS--------------------
class BaseEntity(ABC):
    @abstractmethod

    def validate(self):
        pass
    def to_dict(self):
        return {
            key:value
            for key,value in self.__dict__.items()

        }

#--------------------REPORTER CLASS--------------------
class Reporter(BaseEntity):
    def __init__(self,id,name,email,team):
        self.id = id
        self.name = name
        self.email = email
        self.team = team

    def validate(self):
        if not self.name:
            raise ValueError("Name is required")

        if "@" not in self.email:
            raise ValueError("Invalid email")


#--------------------ISSUE CLASS--------------------
class Issue(BaseEntity):

    STATUS_CHOICES = ["open", "in_progress", "resolved", "closed"]
    PRIORITY_CHOICES = ["low", "medium", "high", "critical"]

    def __init__(self, id, title, description, status, priority, reporter_id):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.reporter_id = reporter_id
        self.created_at = str(datetime.now())

    def validate(self):
        if not self.title:
            raise ValueError("Title cannot be empty")

        if self.status not in self.STATUS_CHOICES:
            raise ValueError("Invalid status")

        if self.priority not in self.PRIORITY_CHOICES:
            raise ValueError("Invalid priority")

    def describe(self):
        return f"{self.title} [{self.priority}]"

#--------------------Subclasses--------------------
class CriticalIssue(Issue):
    def describe(self):
        return f"[URGENT]{self.title} - needs immediate attention"

class LowPriorityIssue(Issue):
    def describe(self):
        return f"[LOW PRIORITY]{self.title} - can be addressed later"