# backend/models/topics_model.py

from backend.models.BaseModel import BaseModel


class QueuesModel(BaseModel):
    def __init__(
        self,
        queue_id=None,
        queue_arn=None,
        queue_name=None,
        queue_url=None,
        strategy_id=None,
        created_date=None,
        is_subscribed=None,
        is_deleted=None,
    ):
        super().__init__()
        self.queue_id = queue_id
        self.strategy_id = strategy_id
        self.queue_arn = queue_arn
        self.queue_name = queue_name
        self.queue_url = queue_url
        self.strategy_id = strategy_id
        self.created_date = created_date
        self.is_subscribed = is_subscribed
        self.is_deleted = is_deleted
