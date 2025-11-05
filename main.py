import asyncio
import json
import secrets
import websockets
from nostr.key import PrivateKey
from nostr.event import Event
from pyln.client import LightningRpc

def generate_nwc_uri(relay_url, private_key):
    pubkey = private_key.public_key.hex()
    secret = private_key.hex()
    uri = f"nostr+walletconnect://{pubkey}?relay={relay_url}&secret={secret}"
    return uri

class NWC:
    def __init__(self, lnd_rpc_path, relay_url, macaroon_path=None, cert_path=None):
        self.lnd = LightningRpc(lnd_rpc_path, macaroon=macaroon_path, cert=cert_path)
        self.relay_url = relay_url
        self.private_key = PrivateKey()
        self.wallet_pubkey = self.private_key.public_key.hex()
        self.ws = None
        self.subscription_id = "nwc-sub"

    def _pay_invoice(self, params):
        bolt11 = params.get('invoice')
        result = self.lnd.pay(bolt11)
        return {'result': {'preimage': result['payment_preimage']}}

    def _get_balance(self, params):
        funds = self.lnd.listfunds()
        balance = sum(channel['channel_sat'] for channel in funds['channels'] if channel['state'] == 'CHANNELD_NORMAL')
        return {'result': {'balance': balance}}

    def _make_invoice(self, params):
        amount = params.get('amount')
        description = params.get('description', '')
        invoice = self.lnd.invoice(amount, description)
        return {'result': {'invoice': invoice['bolt11']}}

    def _lookup_invoice(self, params):
        payment_hash = params.get('payment_hash')
        invoice = self.lnd.listinvoices(payment_hash=payment_hash)
        if invoice:
            return {'result': invoice[0]}
        return {'error': {'message': 'Invoice not found'}}

    def _list_transactions(self, params):
        payments = self.lnd.listpays()
        return {'result': {'transactions': payments['pays']}}

    def _get_info(self, params):
        info = self.lnd.getinfo()
        return {'result': {'alias': info['alias'], 'color': info['color'], 'pubkey': info['id'], 'network': info['network'], 'blockheight': info['blockheight'], 'fees': {'method': 'fixed', 'rate': 0}}}

    async def handle_request(self, event):
        content = json.loads(event.content)
        method = content.get('method')
        params = content.get('params', {})

        handlers = {
            'pay_invoice': self._pay_invoice,
            'get_balance': self._get_balance,
            'make_invoice': self._make_invoice,
            'lookup_invoice': self._lookup_invoice,
            'list_transactions': self._list_transactions,
            'get_info': self._get_info,
        }

        try:
            if method in handlers:
                response = handlers[method](params)
            else:
                response = {'error': {'message': 'Method not supported'}}
        except Exception as e:
            response = {'error': {'message': str(e)}}

        response_event = Event(
            kind=23195,
            content=json.dumps(response),
            tags=[['e', event.id], ['p', event.pubkey]]
        )
        response_event.sign(self.private_key.hex())
        self.publish_event(response_event)

    async def publish_event(self, event):
        if self.ws:
            await self.ws.send(event.to_message())

    async def _process_message(self, message):
        msg = json.loads(message)
        event_data = msg[2]
        event = Event(
            event_data["content"],
            event_data["pubkey"],
            event_data["created_at"],
            event_data["kind"],
            event_data["tags"],
            event_data["sig"]
        )
        if msg[0] == "EVENT" and msg[1] == self.subscription_id and event.verify() and event.kind == 23194:
            await self.handle_request(event)

    async def listen(self):
        async with websockets.connect(self.relay_url) as ws:
            self.ws = ws
            subscription = {
                "kinds": [23194],
                "#p": [self.wallet_pubkey]
            }
            req = ["REQ", self.subscription_id, subscription]
            await ws.send(json.dumps(req))
            async for message in ws:
                try:
                    await self._process_message(message)
                except:
                    pass

if __name__ == '__main__':
    lnd_rpc_path = '/path/to/lightning-rpc'
    macaroon_path = '/path/to/admin.macaroon'  # Opcional si está en default
    cert_path = '/path/to/tls.cert'  # Opcional si no usa TLS
    relay_url = 'wss://relay.nostr.band'
    nwc = NWC(lnd_rpc_path, relay_url, macaroon_path, cert_path)
    uri = generate_nwc_uri(relay_url, nwc.private_key)
    print(f"NWC URI: {uri}")
    print("Comparte este URI con la wallet externa para conectar.")
    asyncio.run(nwc.listen())