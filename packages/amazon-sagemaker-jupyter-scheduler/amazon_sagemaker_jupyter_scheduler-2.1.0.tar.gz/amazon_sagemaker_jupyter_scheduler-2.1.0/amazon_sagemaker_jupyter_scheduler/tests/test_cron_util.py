from amazon_sagemaker_jupyter_scheduler.cron_util import (
    EventBridgeCronExpressionAdapter,
    EventBridgeCronExpressionParser,
    CronExpression,
)


def test_cron_expression_5_parts__happy_path():
    # Given
    raw_cron = "30 20 * 6 MON-FRI"

    # When
    cron_expression = CronExpression(raw_cron)

    # Then
    assert cron_expression.minutes == "30"
    assert cron_expression.hours == "20"
    assert cron_expression.day_of_month == "*"
    assert cron_expression.month == "6"
    assert cron_expression.day_of_week == "MON-FRI"


def test_cron_expression_6_parts__happy_path():
    # Given
    raw_cron = "30 20 * 6 MON-FRI 2025"

    # When
    cron_expression = CronExpression(raw_cron)

    # Then
    assert cron_expression.minutes == "30"
    assert cron_expression.hours == "20"
    assert cron_expression.day_of_month == "*"
    assert cron_expression.month == "6"
    assert cron_expression.day_of_week == "MON-FRI"
    assert cron_expression.year == "2025"


def test_event_bridge_cron_parser__happy_path():
    # Given
    schedule_expression = "cron(30 20 * 6 MON-FRI 2025)"

    # When
    cron_expression = EventBridgeCronExpressionParser().parse(schedule_expression)

    # Then
    assert cron_expression.minutes == "30"
    assert cron_expression.hours == "20"
    assert cron_expression.day_of_month == "*"
    assert cron_expression.month == "6"
    assert cron_expression.day_of_week == "MON-FRI"
    assert cron_expression.year == "2025"


def test_event_bridge_cron_adapter__conflicting_parts__overrides_day_of_month():
    adapter = EventBridgeCronExpressionAdapter("30 20 1-28 6 MON-FRI")
    assert str(adapter.cron_expression) == "30 20 ? 6 MON-FRI"
