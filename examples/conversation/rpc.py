from pyon.net.transport import NameTrio
from pyon.net import messaging
from pyon.net.conversation import RPCServer, RPCClient, RPCConversation

node, ioloop_process = messaging.make_node()

def server_app(bank_name):
    server  = BankService(node, name = NameTrio('london', bank_name), service = 'buy_bonds')
    server.listen()
    try:
        while True:
            server.get_one_msg()
    except:
        server.terminate()

def client_app(bank_name, msg = 'Ihu from buy_bonds'):
    client = BankClient(node, NameTrio('rumi'),
                        server_name = NameTrio('london', bank_name))
    client.buy_bonds(msg)


class BankClient(RPCClient):

    def __init__(self, node, base_name, server_name):
        self.role = 'bank_client'
        self.protocol = 'buy_bonds'
        self.rpc_conv = RPCConversation(self.protocol, 'bank_service', 'bank_client')
        RPCClient.__init__(self, node, base_name, server_name, self.rpc_conv)

    def buy_bonds(self, msg):
        return RPCClient.request(self, msg, {'op':'buy_bonds'})



class BankService(RPCServer):
    def __init__(self, node, name, service):
        self.role = 'bank_server'
        self.protocol = 'buy_bonds'
        self.service = 'buy_bonds'
        self.rpc_conv = RPCConversation(self.protocol, 'bank_service', 'bank_client')
        RPCServer.__init__(self, node, name, self.service, self.rpc_conv)

    def process_msg(self, msg, header):
        if header.setdefault('op', '') == self._service:
            msg =  'Correct call. The message is:%s' %(msg)
            print msg
        else:
            msg = 'I do not support this call:%s' % (header['op'])
            print msg
        return msg
