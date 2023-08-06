import re
from typing import Optional


DEFAULT_CRON_EXPRESSION = "0 0 * * MON-FRI"


class CronExpression:
    minutes: str
    hours: str
    day_of_month: str
    month: str
    day_of_week: str
    year: Optional[str]

    def __init__(self, raw_cron: str):
        cron_fields = raw_cron.split(" ")
        num_cron_fields = len(cron_fields)
        if num_cron_fields < 5 or num_cron_fields > 6:
            raise RuntimeError(
                f"Cron expression has {num_cron_fields} fields, but expected 5-6"
            )

        self.minutes = cron_fields[0]
        self.hours = cron_fields[1]
        self.day_of_month = cron_fields[2]
        self.month = cron_fields[3]
        self.day_of_week = cron_fields[4]
        self.year = cron_fields[5] if num_cron_fields > 5 else "*"

    def __str__(self):
        return f"{self.minutes} {self.hours} {self.day_of_month} {self.month} {self.day_of_week}"


class EventBridgeCronExpressionAdapter:
    cron_expression: CronExpression

    def __init__(self, raw_cron: str):
        self.cron_expression = CronExpression(raw_cron)
        self.fix_days(self.cron_expression)

    def __str__(self):
        # Event Bridge cron expressions require an extra field for year, which we just set to *.
        return f"{str(self.cron_expression)} *"

    @staticmethod
    def fix_days(cron_expression: CronExpression):
        """
        Event Bridge has the following limitation:
        > You can't specify the Day-of-month and Day-of-week fields in the same cron expression.
        > If you specify a value or a * (asterisk) in one of the fields, you must use a ? (question mark) in the other.

        https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-rule-schedule.html#eb-cron-expressions
        """
        if cron_expression.day_of_month == "?" or cron_expression.day_of_week == "?":
            return

        # First try to change either * to ?
        if cron_expression.day_of_month == "*":
            cron_expression.day_of_month = "?"
            return

        if cron_expression.day_of_week == "*":
            cron_expression.day_of_week = "?"
            return

        # Neither field is *, so have to just favor one of the fields.
        # Arbitrarily favoring day_of_week.
        cron_expression.day_of_month = "?"


class EventBridgeCronExpressionParser:
    def parse(self, schedule_expression: str) -> CronExpression:
        raw_cron = re.search("cron\\((.+)\\)", schedule_expression).group(1)
        return CronExpression(raw_cron)
