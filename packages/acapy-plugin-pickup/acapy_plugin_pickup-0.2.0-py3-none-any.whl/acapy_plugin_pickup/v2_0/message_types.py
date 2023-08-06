"""Define message types."""

from aries_cloudagent.protocols.didcomm_prefix import DIDCommPrefix

PROTOCOL = "https://didcomm.org/messagepickup"
VERSION = "2.0"
BASE = f"{PROTOCOL}/{VERSION}"

DELIVERY_REQUEST = f"{BASE}/delivery-request"
DELIVERY = f"{BASE}/delivery"
STATUS_REQUEST = f"{BASE}/status-request"
STATUS = f"{BASE}/status"
LIVE_DELIVERY_CHANGE = f"{BASE}/live-delivery-change"
MESSAGES_RECEIVED = f"{BASE}/messages-received"

MESSAGE_TYPES = DIDCommPrefix.qualify_all(
    {
        DELIVERY_REQUEST: "acapy_plugin_pickup.v2_0.delivery.DeliveryRequest",
        DELIVERY: "acapy_plugin_pickup.v2_0.delivery.Delivery",
        STATUS_REQUEST: "acapy_plugin_pickup.v2_0.status.StatusRequest",
        STATUS: "acapy_plugin_pickup.v2_0.status.Status",
        LIVE_DELIVERY_CHANGE: "acapy_plugin_pickup.v2_0.live_mode.LiveDeliveryChange",
        MESSAGES_RECEIVED: "acapy_plugin_pickup.v2_0.delivery.MessagesReceived",
    }
)
