from datetime import timedelta

import pytest

from app.domain.service.QuotaDefaults import QuotaDefaults


class TestQuotaDefaults:
    def test_default_creation(self):
        quota_defaults = QuotaDefaults.default()

        assert quota_defaults.fallback_limit == 50
        assert quota_defaults.anonymous_limit == 1
        assert quota_defaults.reset_period == timedelta(days=1)

    def test_from_config_creation(self):
        quota_defaults = QuotaDefaults.from_config(
            fallback_limit=100,
            anonymous_limit=5,
            reset_days=7
        )

        assert quota_defaults.fallback_limit == 100
        assert quota_defaults.anonymous_limit == 5
        assert quota_defaults.reset_period == timedelta(days=7)

    def test_get_limit_for_plan_with_plan_limit(self):
        quota_defaults = QuotaDefaults.default()

        result = quota_defaults.get_limit_for_plan(1000)

        assert result == 1000

    def test_get_limit_for_plan_with_none(self):
        quota_defaults = QuotaDefaults.default()

        result = quota_defaults.get_limit_for_plan(None)

        assert result == 50

    def test_get_limit_for_plan_with_zero(self):
        quota_defaults = QuotaDefaults.default()

        result = quota_defaults.get_limit_for_plan(0)

        assert result == 0

    def test_get_anonymous_limit(self):
        quota_defaults = QuotaDefaults.default()

        result = quota_defaults.get_anonymous_limit()

        assert result == 1

    def test_get_anonymous_limit_custom(self):
        quota_defaults = QuotaDefaults.from_config(
            fallback_limit=50,
            anonymous_limit=10,
            reset_days=1
        )

        result = quota_defaults.get_anonymous_limit()

        assert result == 10

    def test_get_reset_period(self):
        quota_defaults = QuotaDefaults.default()

        result = quota_defaults.get_reset_period()

        assert result == timedelta(days=1)

    def test_get_reset_period_custom(self):
        quota_defaults = QuotaDefaults.from_config(
            fallback_limit=50,
            anonymous_limit=1,
            reset_days=30
        )

        result = quota_defaults.get_reset_period()

        assert result == timedelta(days=30)

    def test_multiple_instances_independent(self):
        default_1 = QuotaDefaults.default()
        default_2 = QuotaDefaults.from_config(
            fallback_limit=200,
            anonymous_limit=20,
            reset_days=14
        )

        assert default_1.fallback_limit == 50
        assert default_2.fallback_limit == 200
        assert default_1.anonymous_limit == 1
        assert default_2.anonymous_limit == 20
