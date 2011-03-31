from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.internet import reactor
import sys

from modules.middag.handler import MiddagHandler

class Bot(irc.IRCClient):
	def _get_nickname(self):
		return self.factory.nickname
	nickname = property(_get_nickname)
	handlers = {"!middag": MiddagHandler()}
	
	def signedOn(self):
		self.join(self.factory.channel)
		print "Signed on as %s." % (self.nickname,)
	
	def joined(self, channel):
		print "Joined %s." % (channel,)
	
	def privmsg(self, user, channel, msg):
		if not user:
			return
		for keyword in self.handlers.keys():
			if keyword in msg:
				for line in self.handlers[keyword].privmsg(user, channel, msg):
					self.msg(self.factory.channel, line.encode("utf-8"))


class BotFactory(protocol.ClientFactory):
    protocol = Bot
    def __init__(self, channel, nickname='habeebs'):
        self.channel = channel
        self.nickname = nickname
        
    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()
        
    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)

if __name__ == "__main__":
	try:
		nick = sys.argv[1]
		chan = sys.argv[2]
		server = sys.argv[3]
		port = sys.argv[4]
		reactor.connectTCP(server, int(port), BotFactory("#"+chan, nick))
		reactor.run()
	except:
		print "Usage:"
		print "python bot.py nick channel server port"
		print ""
		print "Omit # for channel"