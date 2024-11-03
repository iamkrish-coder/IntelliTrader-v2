# backend/models/topics_model.py

from backend.models.BaseModel import BaseModel


class TopicsModel(BaseModel):
    def __init__(
        self,
        topic_id=None,
        topic_arn=None,
        topic_name=None,
        strategy_id=None,
        created_date=None,
        modified_date=None,
        is_active=None,
        is_published=None,
        is_subscribed=None,
        is_deleted=None,
    ):
        super().__init__()
        self.topic_id = topic_id
        self.topic_arn = topic_arn
        self.topic_name = topic_name
        self.strategy_id = strategy_id
        self.created_date = created_date
        self.modified_date = modified_date
        self.is_active = is_active
        self.is_published = is_published
        self.is_subscribed = is_subscribed
        self.is_deleted = is_deleted
