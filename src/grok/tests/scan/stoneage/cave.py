import grok

class Cave(grok.Model):
    pass

index = grok.PageTemplate("""\
<html>
<body>
<h1>A comfy cave</h1>
</body>
</html>
""")
