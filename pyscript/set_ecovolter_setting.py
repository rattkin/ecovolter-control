import hmac
import hashlib
import time
import json
import asyncio
import aiohttp
import base64

@service
async def set_ecovolter_setting(
    target_current: int,
    boost_time: int,
    kwh_price: float,
    boost_current: int,
    max_current: int,
    is_charging_enabled: bool,
    is_three_phase_mode_enabled: bool,
    is_boost_mode_enabled: bool,
    is_local_panel_enabled: bool,
):
    # 1. Configuration
    key = ""

    base_url = f"http://{key}.local/api/v1/charger/"
    settings_url = f"{base_url}settings"

    if not key:
        log.error("EcoVolter key is not set in set_ecovolter_setting.py")
        return
    
    ts = str(int(time.time()))

    data = {
     
        "timestamp": int(ts) * 1000,
        "targetCurrent": target_current,
        "boostTime": boost_time,
        "kwhPrice": kwh_price,
        "boostCurrent": boost_current,
        "maxCurrent": max_current,
        "isChargingEnable": is_charging_enabled,
        "isThreePhaseModeEnable": is_three_phase_mode_enabled,
        "isBoostModeEnable": is_boost_mode_enabled,
        "isLocalPanelEnable": is_local_panel_enabled,
    }
    json_payload = json.dumps(data, separators=(',', ':'))

    sign_data = f"{settings_url}\n{ts}\n{json_payload}"
    signature = hmac.new(key.encode(), sign_data.encode(), hashlib.sha256).hexdigest()

    headers = {"Authorization": f"HmacSHA256 {signature}", "X-Timestamp": ts}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.patch(
                settings_url, headers=headers, data=json_payload.encode("utf-8")
            ) as response:
                # log.error(response)
                # Instead of raising an exception, we check the status code
                # and log the error body if the request was not successful.
                if response.status >= 400:
                    error_body = await response.text()
                    log.error(
                        f"HTTP PATCH request failed with status: {response.status}"
                    )
                    log.error(f"Server error response body: {error_body}")
                    return  # Exit the service to prevent further issues

                log.info(
                    f"Successfully patched EcoVolter settings. Response status: {response.status}"
                )
                # You may want to call fetch_ecovolter_data() here to update HA states immediately
                await pyscript.fetch_ecovolter_data()
    except aiohttp.ClientError as e:
        log.error(
            f"HTTP PATCH request to EcoVolter settings API failed due to a network error: {e}"
        )
    except Exception as e:
        log.error(f"An unexpected error occurred while patching settings: {e}")
