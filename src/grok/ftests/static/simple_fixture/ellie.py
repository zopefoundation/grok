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

class MammothSkin(grok.Layer):
    pass

grok.register_skin(MammothSkin)

class CaveDrawings(grok.View):

    def render(self):
        return "stick figures"

class TarPit(grok.View):
    grok.layer(MammothSkin)

    def render(self):
        return "inky darkness all around"
    
