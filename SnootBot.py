# imports for the irc protocol
import irc.bot
import irc.strings

# import for my twitter interface
import twit


class SnootBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0])

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(":", 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(self.connection.get_nickname()):
            self.do_command(e, a[1].strip())
        return

    def do_command(self, e, cmd):
        nick = e.source.nick
        c = self.connection
        if cmd == 'die':
            self.die()
        elif 'post ' in cmd:
            tweet = cmd[5:]
            twit.post_tweet(tweet, nick)
            c.privmsg(self.channel, 'New tweet from <{}>: "{}"'.format(nick, tweet))
        elif cmd == 'latest':
            latest = twit.get_latest_tweet()
            c.privmsg(self.channel, latest)
        elif cmd == 'help':
            help_string = 'Available commands are: "post": post a status update; \
                          "latest": get the latest tweet from the bot; "help": send this message'
            c.privmsg(nick, help_string)


def main():
    server = 'irc.snoonet.org'
    port = 6667
    channel = '#random'
    nickname = 'SnootBot'
    bot = SnootBot(channel, nickname, server, port)
    bot.start()


if __name__ == '__main__':
    main()
