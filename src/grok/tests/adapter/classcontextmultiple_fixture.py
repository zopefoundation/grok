import grok


class Cave(grok.Model):
    pass


class Club(grok.Model):
    pass


class Anything:
    grok.context(Cave)
    grok.context(Club)
