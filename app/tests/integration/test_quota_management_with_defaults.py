from datetime import datetime, timedelta
from uuid import UUID, uuid4
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.application.service.QuotaManagementService import QuotaManagementService
from app.domain.service.Plan import Plan
from app.domain.service.Quota import Quota
from app.domain.service.QuotaDefaults import QuotaDefaults
from app.domain.authentication.UserPlan import UserPlan
from app.domain.ValueObjects import BillingCycle, UserPlanStatus


@pytest.fixture
def quota_defaults():
    return QuotaDefaults.default()


@pytest.fixture
def custom_quota_defaults():
    return QuotaDefaults.from_config(
        fallback_limit=100,
        anonymous_limit=5,
        reset_days=7
    )


@pytest.fixture
def mock_repositories():
    return {
        'quota_repository': AsyncMock(),
        'user_plan_repository': AsyncMock(),
        'plan_repository': AsyncMock(),
        'transaction_logger': AsyncMock(),
        'datetime_converter': MagicMock(),
        'uuid_generator': MagicMock(),
        'service_access_validator': AsyncMock(),
    }


class TestQuotaManagementServiceWithDefaults:

    @pytest.mark.asyncio
    async def test_create_default_quota_for_user_with_plan_limit(self, mock_repositories, quota_defaults):
        user_id = uuid4()
        plan_id = uuid4()
        current_time = datetime.now()

        user_plan = UserPlan(
            id=uuid4(),
            user_id=user_id,
            plan_id=plan_id,
            status=UserPlanStatus.ACTIVE,
            started_at=current_time,
            expires_at=None,
            auto_renew=False,
            payment_gateway=None,
            payment_gateway_subscription_id=None,
            created_at=current_time,
            updated_at=current_time
        )

        plan = Plan(
            id=plan_id,
            name="Pro",
            billing_cycle=BillingCycle.MONTHLY,
            features=[],
            rate_limits={},
            quota_limits={"api_calls": 1000},
            is_active=True,
            created_at=current_time,
            updated_at=current_time
        )

        mock_repositories['user_plan_repository'].find_active_by_user.return_value = user_plan
        mock_repositories['plan_repository'].find_by_id.return_value = plan
        mock_repositories['datetime_converter'].now_utc.return_value = current_time
        mock_repositories['datetime_converter'].add_timedelta.return_value = current_time + timedelta(days=1)
        mock_repositories['uuid_generator'].generate.return_value = uuid4()
        mock_repositories['quota_repository'].find_by_user_and_service.return_value = None

        saved_quota = Quota(
            id=uuid4(),
            user_id=user_id,
            service_name="test_service",
            quota_type="api_calls",
            current_usage=0,
            limit=1000,
            reset_at=current_time + timedelta(days=1),
            created_at=current_time,
            updated_at=current_time
        )
        mock_repositories['quota_repository'].save.return_value = saved_quota

        service = QuotaManagementService(**mock_repositories, quota_defaults=quota_defaults)

        result = await service.execute(user_id, "test_service", "api_calls", 1)

        assert result.limit == 1000
        mock_repositories['quota_repository'].save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_default_quota_for_user_with_no_plan_limit_uses_fallback(self, mock_repositories, quota_defaults):
        user_id = uuid4()
        plan_id = uuid4()
        current_time = datetime.now()

        user_plan = UserPlan(
            id=uuid4(),
            user_id=user_id,
            plan_id=plan_id,
            status=UserPlanStatus.ACTIVE,
            started_at=current_time,
            expires_at=None,
            auto_renew=False,
            payment_gateway=None,
            payment_gateway_subscription_id=None,
            created_at=current_time,
            updated_at=current_time
        )

        plan = Plan(
            id=plan_id,
            name="Free",
            billing_cycle=BillingCycle.MONTHLY,
            features=[],
            rate_limits={},
            quota_limits={},
            is_active=True,
            created_at=current_time,
            updated_at=current_time
        )

        mock_repositories['user_plan_repository'].find_active_by_user.return_value = user_plan
        mock_repositories['plan_repository'].find_by_id.return_value = plan
        mock_repositories['datetime_converter'].now_utc.return_value = current_time
        mock_repositories['datetime_converter'].add_timedelta.return_value = current_time + timedelta(days=1)
        mock_repositories['uuid_generator'].generate.return_value = uuid4()
        mock_repositories['quota_repository'].find_by_user_and_service.return_value = None

        saved_quota = Quota(
            id=uuid4(),
            user_id=user_id,
            service_name="test_service",
            quota_type="api_calls",
            current_usage=0,
            limit=50,
            reset_at=current_time + timedelta(days=1),
            created_at=current_time,
            updated_at=current_time
        )
        mock_repositories['quota_repository'].save.return_value = saved_quota

        service = QuotaManagementService(**mock_repositories, quota_defaults=quota_defaults)

        result = await service.execute(user_id, "test_service", "api_calls", 1)

        assert result.limit == 50

    @pytest.mark.asyncio
    async def test_create_default_quota_for_anonymous_user(self, mock_repositories, quota_defaults):
        user_id = uuid4()
        current_time = datetime.now()

        mock_repositories['user_plan_repository'].find_active_by_user.return_value = None
        mock_repositories['datetime_converter'].now_utc.return_value = current_time
        mock_repositories['datetime_converter'].add_timedelta.return_value = current_time + timedelta(days=1)
        mock_repositories['uuid_generator'].generate.return_value = uuid4()
        mock_repositories['quota_repository'].find_by_user_and_service.return_value = None

        saved_quota = Quota(
            id=uuid4(),
            user_id=user_id,
            service_name="test_service",
            quota_type="api_calls",
            current_usage=0,
            limit=1,
            reset_at=current_time + timedelta(days=1),
            created_at=current_time,
            updated_at=current_time
        )
        mock_repositories['quota_repository'].save.return_value = saved_quota

        service = QuotaManagementService(**mock_repositories, quota_defaults=quota_defaults)

        result = await service.execute(user_id, "test_service", "api_calls", 1)

        assert result.limit == 1

    @pytest.mark.asyncio
    async def test_custom_quota_defaults_applied(self, mock_repositories, custom_quota_defaults):
        user_id = uuid4()
        current_time = datetime.now()

        mock_repositories['user_plan_repository'].find_active_by_user.return_value = None
        mock_repositories['datetime_converter'].now_utc.return_value = current_time
        mock_repositories['datetime_converter'].add_timedelta.return_value = current_time + timedelta(days=7)
        mock_repositories['uuid_generator'].generate.return_value = uuid4()
        mock_repositories['quota_repository'].find_by_user_and_service.return_value = None

        saved_quota = Quota(
            id=uuid4(),
            user_id=user_id,
            service_name="test_service",
            quota_type="api_calls",
            current_usage=0,
            limit=5,
            reset_at=current_time + timedelta(days=7),
            created_at=current_time,
            updated_at=current_time
        )
        mock_repositories['quota_repository'].save.return_value = saved_quota

        service = QuotaManagementService(**mock_repositories, quota_defaults=custom_quota_defaults)

        result = await service.execute(user_id, "test_service", "api_calls", 1)

        assert result.limit == 5

    @pytest.mark.asyncio
    async def test_reset_period_from_quota_defaults(self, mock_repositories, custom_quota_defaults):
        user_id = uuid4()
        current_time = datetime.now()

        mock_repositories['user_plan_repository'].find_active_by_user.return_value = None
        mock_repositories['datetime_converter'].now_utc.return_value = current_time

        expected_reset_time = current_time + timedelta(days=7)
        mock_repositories['datetime_converter'].add_timedelta.return_value = expected_reset_time
        mock_repositories['uuid_generator'].generate.return_value = uuid4()
        mock_repositories['quota_repository'].find_by_user_and_service.return_value = None

        saved_quota = Quota(
            id=uuid4(),
            user_id=user_id,
            service_name="test_service",
            quota_type="api_calls",
            current_usage=0,
            limit=5,
            reset_at=expected_reset_time,
            created_at=current_time,
            updated_at=current_time
        )
        mock_repositories['quota_repository'].save.return_value = saved_quota

        service = QuotaManagementService(**mock_repositories, quota_defaults=custom_quota_defaults)

        await service.execute(user_id, "test_service", "api_calls", 1)

        mock_repositories['datetime_converter'].add_timedelta.assert_called_with(
            current_time,
            timedelta(days=7)
        )
