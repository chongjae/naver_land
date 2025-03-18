import logging
from typing import Any

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_USERNAME
from .naver_land import NaverLandApi
from .const import DOMAIN, TITLE, AREA, TYPE

_LOGGER = logging.getLogger(__name__)

TRADE_TYPES = {
    "A1": "매매",
    "B1": "전세",
    "B2": "월세",
    "B3": "단기임대"
}

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(AREA): cv.string,
        vol.Required(TYPE): vol.In(list(TRADE_TYPES.keys()))
    }
)


async def async_validate_login(hass, apt_id: str, area: str, trade_type: str) -> dict[str, Any]:
    client = NaverLandApi(apt_id, area, trade_type)

    errors = {}
    try:
        apt_name = await client.get_apt_name()
        if apt_name is None:
            _LOGGER.exception("아파트 정보 취득 실패")
            errors["base"] = "invalid_apt_id"
    except Exception as ex:
        _LOGGER.exception("아파트 정보 취득 실패 : %s", ex)
        errors["base"] = "invalid_apt_id"
    return errors


class NaverLandConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(
            self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """초기 단계 처리"""

        if user_input is None:
            description_placeholders = {
                "A1_desc": TRADE_TYPES["A1"],
                "B1_desc": TRADE_TYPES["B1"],
                "B2_desc": TRADE_TYPES["B2"],
                "B3_desc": TRADE_TYPES["B3"],
            }

            return self.async_show_form(
                step_id="user",
                data_schema=STEP_USER_DATA_SCHEMA,
                description_placeholders=description_placeholders
            )

        apt_id = user_input[CONF_USERNAME]
        area = user_input[AREA]
        trade_type = user_input[TYPE]

        if errors := await async_validate_login(self.hass, apt_id, area, trade_type):
            return self.async_show_form(
                step_id="user",
                data_schema=STEP_USER_DATA_SCHEMA,
                errors=errors,
            )
        await self.async_set_unique_id(f"{DOMAIN}_{apt_id}")
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title=f"{TITLE} ({apt_id})", data=user_input)
