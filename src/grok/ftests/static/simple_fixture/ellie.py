import grok

class Mammoth(grok.Model):
    pass

class Index(grok.View):
    pass

index = grok.PageTemplate("""\
<html>
<body>
<a tal:attributes="href static/file.txt">Some text in a file</a>
</body>
</html>""")

class MammothLayer(grok.ILayer):
    pass

class MammothSkin(grok.Skin):
    grok.layer(MammothLayer)


class CaveDrawings(grok.View):

    def render(self):
        return "stick figures"

class TarPit(grok.View):
    grok.layer(MammothLayer)

    def render(self):
        return "inky darkness all around"
    
