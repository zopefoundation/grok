import grok

class Mammoth(grok.Model):
    pass

index = grok.PageTemplate("""\
<html>
<body>
<h1>ME GROK HUNT MAMMOTH!</h1>
</body>
</html>
""")
