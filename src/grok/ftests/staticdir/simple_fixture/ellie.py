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
