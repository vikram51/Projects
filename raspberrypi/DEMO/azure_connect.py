import asyncio

from queue import Queue
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device.aio import ProvisioningDeviceClient
from azure.iot.device import MethodResponse
import random
import pnp_helper

DEVICE_ID_SCOPE = "0ne00976B17"
DEVICE_ID = "mwciuczxs7"
DEVICE_KEY = "vEzNNhL4aLB+N/sWsBAmzHy4a67u9YTnZAHXwf1V1CI="    #Primary Key

model_id = "dtmi:pigatecontrol:PiGate_lp;1"
sensorName1 = "gate_open_count"

device_client = None

async def send_telemetry_from_car_counter(device_client, telemetry_msg, component_name=None):
    msg = pnp_helper.create_telemetry(telemetry_msg, component_name)
    await device_client.send_message(msg)
    print("Sent message")
    print(msg)
    await asyncio.sleep(1)


async def provision_device(provisioning_host, id_scope, registration_id, symmetric_key, model_id):
    provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host=provisioning_host,
        registration_id=registration_id,
        id_scope=id_scope,
        symmetric_key=symmetric_key,
    )

    provisioning_device_client.provisioning_payload = {"modelId": model_id}
    return await provisioning_device_client.register()

async def send_telemetry(device_client, veh_count):
    print("Sending telemetry from various components")

    veh_count_msg = {"ParkingCounter": veh_count}
    print("sending count {}".format(veh_count_msg))
    await send_telemetry_from_car_counter(
        device_client, veh_count_msg
    )

async def azureConnect():
    global device_client

    provisioning_host = (
        "global.azure-devices-provisioning.net"
    )
    id_scope = DEVICE_ID_SCOPE
    registration_id = DEVICE_ID
    symmetric_key = DEVICE_KEY

    registration_result = await provision_device(
        provisioning_host, id_scope, registration_id, symmetric_key, model_id
    )

    if registration_result.status == "assigned":
        print("Device was assigned")
        print(registration_result.registration_state.assigned_hub)
        print(registration_result.registration_state.device_id)
        device_client = IoTHubDeviceClient.create_from_symmetric_key(
            symmetric_key=symmetric_key,
            hostname=registration_result.registration_state.assigned_hub,
            device_id=registration_result.registration_state.device_id,
            product_info=model_id,
        )
    else:
        raise RuntimeError(
            "Could not provision device. Aborting Plug and Play device connection."
        )

    connect_task = asyncio.create_task(device_client.connect())
    #receiver_task = asyncio.create_task(receive_message(device_client))
    await connect_task
    #await receiver_task