import grok


class Cave(grok.Model):
    pass


class Club(grok.Model):
    pass


grok.context(Cave)
grok.context(Club)
