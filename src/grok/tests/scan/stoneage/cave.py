import grok

class Cave(grok.Model):
    pass

class Index(grok.View):
    pass

index = grok.PageTemplate("""\
<html>
<body>
<h1>A comfy cave</h1>
</body>
</html>
""")
