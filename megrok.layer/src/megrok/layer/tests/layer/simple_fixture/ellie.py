import grok
import megrok.layer

class Mammoth(grok.Model):
    pass

class Index(grok.View):
    grok.context(Mammoth)

index = grok.PageTemplate("""\
<html>
<body>
<a tal:attributes="href static/file.txt">Some text in a file</a>
</body>
</html>""")

class MammothLayer(megrok.layer.IMinimalLayer):
    pass

class MammothSkin(megrok.layer.Skin):
    megrok.layer.layer(MammothLayer)


class CaveDrawings(grok.View):
    grok.context(Mammoth)

    def render(self):
        return "stick figures"

class TarPit(grok.View):
    grok.context(Mammoth)
    megrok.layer.layer(MammothLayer)

    def render(self):
        return "inky darkness all around"
    
