from gevent import spawn
from gevent import queue as gqueue
from pyon.net.transport import NameTrio
from pyon.net import channel
from pyon.net import messaging
from pyon.net import conversation
from pyon.net.conversation import Conversation, Principal,PrincipalName

node, ioloop_process = messaging.make_node()

def bank_app(name):
    #principal initialisation
    participant = Principal(node, PrincipalName(namespace = 'rumi-PC',
                                                name = 'rumi'))
    # conversation bootstrapping
    c = participant.start_conversation(protocol = 'buy_bond',
                                    role = 'bank_client')

    c.invite('bank_server', PrincipalName(namespace = 'stephen-PC',
                                     name = service_provider_name,
                                     merge_with_first_send = True))

    #interactions
    c.send('bank_server', 'buy_bonds', 'I will send you a request shortly. Please wait for me.')
    msg, header = c.recv('bank_server')
    print 'Msg received: %s' % (msg)

    c.close()
    participant.terminate()

def bank_client(name):
    #principal initialisation
    participant = Principal(node, PrincipalName(namespace = 'stephen-PC',
                                                     name = service_provider_name))
    participant.start_listening()
    c = participant.accept_invitation(merge_with_first_send = True)

    #interactions
    msg, header = c.recv('bank_client')
    if (header['op'] == 'buy_bonds'):
        c.send('bank_client', 'The market is closed today. Sorry!!!')
    participant.terminate()