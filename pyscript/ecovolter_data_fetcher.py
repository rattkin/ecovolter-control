# https://asnplus.github.io/revc-charger-local-api-documentation/


import hmac
import hashlib
import time
import json
import asyncio
import aiohttp

def safe_round(value, ndigits=0):
    try:
        return round(float(value), ndigits)
    except (TypeError, ValueError):
        return 0.0

@service
async def fetch_ecovolter_data():

    # 1. Configuration
    key = ""

    base_url = f"http://{key}.local/api/v1/charger/"

    if not key:
        log.error("EcoVolter key is not set in ecovolter_data_fetcher.py")
        return


    async with aiohttp.ClientSession() as session:
        # --- Section 1: Fetch Charger Settings (from /charger/settings) ---
        settings_url = f"{base_url}settings"
        ts_settings = str(int(time.time()))
        sign_data_settings = f"{settings_url}\n{ts_settings}\n"
        signature_settings = hmac.new(
            key.encode(), sign_data_settings.encode(), hashlib.sha256
        ).hexdigest()

        headers_settings = {
            "Authorization": f"HmacSHA256 {signature_settings}",
            "X-Timestamp": ts_settings,
            "Accept": "application/json",
        }

        log.info(f"Generated signature for settings GET request: {signature_settings}")

        try:
            async with session.get(
                settings_url, headers=headers_settings
            ) as response_settings:
                response_settings.raise_for_status()
                charger_data_settings = await response_settings.json()

            log.info(
                f"Successfully received settings data: {json.dumps(charger_data_settings, indent=2)}"
            )

            state.set(
                "sensor.ecovolter_target_current",
                charger_data_settings.get("targetCurrent", 0),
                {
                    "friendly_name": "Cílový proud",
                    "unit_of_measurement": "A",
                    "unique_id": f"{key}_target_current",
                },
            )
            state.set(
                "sensor.ecovolter_boost_time",
                charger_data_settings.get("boostTime", 0),
                {
                    "friendly_name": "Režim Boost",
                    "unit_of_measurement": "s",
                    "unique_id": f"{key}_boost_time",
                },
            )
            state.set(
                "sensor.ecovolter_kwh_price",
                charger_data_settings.get("kwhPrice", 0),
                {
                    "friendly_name": "Cena za kWh",
                    "unique_id": f"{key}_kwh_price",
                },
            )
            state.set(
                "sensor.ecovolter_boost_current",
                charger_data_settings.get("boostCurrent", 0),
                {
                    "friendly_name": "Boost proud",
                    "unit_of_measurement": "A",
                    "unique_id": f"{key}_boost_current",
                },
            )
            state.set(
                "sensor.ecovolter_max_current",
                charger_data_settings.get("maxCurrent", 0),
                {
                    "friendly_name": "Maximální proud",
                    "unit_of_measurement": "A",
                    "unique_id": f"{key}_max_current",
                },
            )
            state.set(
                "sensor.ecovolter_is_charging_enabled",
                charger_data_settings.get("isChargingEnable", False),
                {
                    "friendly_name": "Nabíjení povoleno",
                    "unique_id": f"{key}_is_charging_enabled",
                },
            )
            state.set(
                "sensor.ecovolter_is_three_phase_mode_enabled",
                charger_data_settings.get("isThreePhaseModeEnable", False),
                {
                    "friendly_name": "Třífázový režim povolen",
                    "unique_id": f"{key}_is_three_phase_mode_enabled",
                },
            )
            state.set(
                "sensor.ecovolter_is_boost_mode_enabled",
                charger_data_settings.get("isBoostModeEnable", False),
                {
                    "friendly_name": "Režim Boost povolen",
                    "unique_id": f"{key}_is_boost_mode_enabled",
                },
            )
            state.set(
                "sensor.ecovolter_is_local_panel_enabled",
                charger_data_settings.get("isLocalPanelEnable", False),
                {
                    "friendly_name": "Místní panel povolen",
                    "unique_id": f"{key}_is_local_panel_enabled",
                },
            )

        except aiohttp.ClientError as e:
            log.error(f"HTTP GET request to settings API failed: {e}")
        except json.JSONDecodeError:
            log.error(
                f"Failed to parse JSON response from settings API. Response text: {await response_settings.text()}"
            )
        except Exception as e:
            log.error(f"An unexpected error occurred while fetching settings: {e}")

        # --- Section 2: Fetch Charger Status (from /charger/status) ---
        status_url = f"{base_url}status"
        ts_status = str(int(time.time()))
        sign_data_status = f"{status_url}\n{ts_status}\n"
        signature_status = hmac.new(
            key.encode(), sign_data_status.encode(), hashlib.sha256
        ).hexdigest()

        headers_status = {
            "Authorization": f"HmacSHA256 {signature_status}",
            "X-Timestamp": ts_status,
            "Accept": "application/json",
        }

        log.info(f"Generated signature for status GET request: {signature_status}")

        try:
            async with session.get(
                status_url, headers=headers_status
            ) as response_status:
                response_status.raise_for_status()
                charger_data_status = await response_status.json()

            # log.error(
            #     f"Successfully received status data: {json.dumps(charger_data_status, indent=2)}"
            # )

            charge_state = (
                "Nabíjení" if charger_data_status.get("isCharging") else "Nenabíjí se"
            )
            vehicle_state = (
                "Připojeno"
                if charger_data_status.get("isVehicleConnected")
                else "Odpojeno"
            )

            state.set(
                "sensor.ecovolter_charge_state",
                charge_state,
                {
                    "friendly_name": "Stav nabíjení",
                    "unique_id": f"{key}_charge_state",
                },
            )

            state.set(
                "sensor.ecovolter_vehicle_state",
                vehicle_state,
                {
                    "friendly_name": "Stav vozidla",
                    "unique_id": f"{key}_vehicle_state",
                },
            )

            state.set(
                "sensor.ecovolter_charged_energy",
                safe_round(charger_data_status.get("chargedEnergy", 0), 2),
                {
                    "friendly_name": "Nabitá energie",
                    "unit_of_measurement": "kWh",
                    "unique_id": f"{key}_charged_energy",
                },
            )
            state.set(
                "sensor.ecovolter_charging_cost",
                safe_round(charger_data_status.get("chargingCost", 0), 2),
                {
                    "friendly_name": "Cena nabíjení",
                    "unique_id": f"{key}_charging_cost",
                },
            )
            state.set(
                "sensor.ecovolter_charging_time",
                charger_data_status.get("chargingTime", 0),
                {
                    "friendly_name": "Doba nabíjení",
                    "unit_of_measurement": "s",
                    "unique_id": f"{key}_charging_time",
                },
            )
            state.set(
                "sensor.ecovolter_remaining_boost_time",
                charger_data_status.get("remainingBoostTime", 0),
                {
                    "friendly_name": "Zbývající čas Boost",
                    "unit_of_measurement": "s",
                    "unique_id": f"{key}_remaining_boost_time",
                },
            )
            state.set(
                "sensor.ecovolter_actual_power",
                safe_round(charger_data_status.get("actualPower", 0), 0),
                {
                    "friendly_name": "Aktuální výkon",
                    "unit_of_measurement": "kW",
                    "unique_id": f"{key}_actual_power",
                },
            )
            state.set(
                "sensor.ecovolter_current_l1",
                safe_round(charger_data_status.get("currentL1", 0), 0),
                {
                    "friendly_name": "Proud L1",
                    "unit_of_measurement": "A",
                    "unique_id": f"{key}_current_l1",
                },
            )
            state.set(
                "sensor.ecovolter_current_l2",
                safe_round(charger_data_status.get("currentL2", 0), 0),
                {
                    "friendly_name": "Proud L2",
                    "unit_of_measurement": "A",
                    "unique_id": f"{key}_current_l2",
                },
            )
            state.set(
                "sensor.ecovolter_current_l3",
                safe_round(charger_data_status.get("currentL3", 0), 0),
                {
                    "friendly_name": "Proud L3",
                    "unit_of_measurement": "A",
                    "unique_id": f"{key}_current_l3",
                },
            )
            state.set(
                "sensor.ecovolter_voltage_l1",
                safe_round(charger_data_status.get("voltageL1", 0), 0),
                {
                    "friendly_name": "Napětí L1",
                    "unit_of_measurement": "V",
                    "unique_id": f"{key}_voltage_l1",
                },
            )
            state.set(
                "sensor.ecovolter_voltage_l2",
                safe_round(charger_data_status.get("voltageL2", 0), 0),
                {
                    "friendly_name": "Napětí L2",
                    "unit_of_measurement": "V",
                    "unique_id": f"{key}_voltage_l2",
                },
            )
            state.set(
                "sensor.ecovolter_voltage_l3",
                safe_round(charger_data_status.get("voltageL3", 0), 0),
                {
                    "friendly_name": "Napětí L3",
                    "unit_of_measurement": "V",
                    "unique_id": f"{key}_voltage_l3",
                },
            )
            state.set(
                "sensor.ecovolter_is_charging",
                charger_data_status.get("isCharging", False),
                {
                    "friendly_name": "Probíhá nabíjení",
                    "unique_id": f"{key}_is_charging",
                },
            )
            state.set(
                "sensor.ecovolter_is_boost_mode_available",
                charger_data_status.get("isBoostModeAvailable", False),
                {
                    "friendly_name": "Režim Boost k dispozici",
                    "unique_id": f"{key}_is_boost_mode_available",
                },
            )
            state.set(
                "sensor.ecovolter_is_boost_mode_active",
                charger_data_status.get("isBoostModeActive", False),
                {
                    "friendly_name": "Režim Boost aktivní",
                    "unique_id": f"{key}_is_boost_mode_active",
                },
            )
            state.set(
                "sensor.ecovolter_is_three_phase_mode_available",
                charger_data_status.get("isThreePhaseModeAvailable", False),
                {
                    "friendly_name": "Třífázový režim k dispozici",
                    "unique_id": f"{key}_is_three_phase_mode_available",
                },
            )
            state.set(
                "sensor.ecovolter_is_three_phase_mode_active",
                charger_data_status.get("isThreePhaseModeActive", False),
                {
                    "friendly_name": "Třífázový režim aktivní",
                    "unique_id": f"{key}_is_three_phase_mode_active",
                },
            )
            state.set(
                "sensor.ecovolter_is_vehicle_connected",
                charger_data_status.get("isVehicleConnected", False),
                {
                    "friendly_name": "Vozidlo připojeno",
                    "unique_id": f"{key}_is_vehicle_connected",
                },
            )
            state.set(
                "sensor.ecovolter_is_charging_schedule_active",
                charger_data_status.get("isChargingScheduleActive", False),
                {
                    "friendly_name": "Plán nabíjení aktivní",
                    "unique_id": f"{key}_is_charging_schedule_active",
                },
            )
            state.set(
                "sensor.ecovolter_temperature_current_limit",
                charger_data_status.get("temperatureCurrentLimit", 0),
                {
                    "friendly_name": "Teplotní proudový limit",
                    "unit_of_measurement": "A",
                    "unique_id": f"{key}_temperature_current_limit",
                },
            )
            state.set(
                "sensor.ecovolter_adapter_max_current",
                charger_data_status.get("adapterMaxCurrent", 0),
                {
                    "friendly_name": "Maximální proud adaptéru",
                    "unit_of_measurement": "A",
                    "unique_id": f"{key}_adapter_max_current",
                },
            )
            temperatures = charger_data_status.get("temperatures", {})
            state.set(
                "sensor.ecovolter_adapter_temperature",
                safe_round(temperatures.get("adapter", [0])[0], 2),
                {
                    "friendly_name": "Teplota adaptéru",
                    "unit_of_measurement": "°C",
                    "unique_id": f"{key}_adapter_temperature",
                },
            )
            state.set(
                "sensor.ecovolter_relay_temperature",
                safe_round(temperatures.get("relay", [0])[0], 2),
                {
                    "friendly_name": "Teplota relé",
                    "unit_of_measurement": "°C",
                    "unique_id": f"{key}_relay_temperature",
                },
            )
            state.set(
                "sensor.ecovolter_internal_temperature",
                safe_round(temperatures.get("internal", 0), 2),
                {
                    "friendly_name": "Vnitřní teplota",
                    "unit_of_measurement": "°C",
                    "unique_id": f"{key}_internal_temperature",
                },
            )

        except aiohttp.ClientError as e:
            log.error(f"HTTP GET request to status API failed: {e}")
        except json.JSONDecodeError:
            log.error(
                f"Failed to parse JSON response from status API. Response text: {await response_status.text()}"
            )
        except Exception as e:
            log.error(f"An unexpected error occurred while fetching status: {e}")

