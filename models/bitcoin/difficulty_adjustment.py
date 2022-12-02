from models.base_model import BaseModel, db
from peewee import IntegerField, DecimalField

class BitcoinDifficultyAdjustment(BaseModel):
    progress_percent = DecimalField()
    difficulty_change = DecimalField()
    estimated_retarget_date = IntegerField()
    remaining_blocks = IntegerField()
    remaining_time = IntegerField()
    previous_retarget = DecimalField()
    next_retarget_height = IntegerField()
    time_average = IntegerField()
    time_offset = IntegerField

    class Meta:
        table_name = "bitcoin_difficulty_adjustment"
        database = db

    def to_string(self):
        return f"Progress: {self.progress_percent}% | Difficulty Change: {self.difficulty_change} | Estimated retarget date: {self.estimated_retarget_date}"
