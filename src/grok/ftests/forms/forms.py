"""
  >>> from grokcore.layout import ILayout
  >>> from zope.component import getMultiAdapter
  >>> from zope.publisher.browser import TestRequest

  >>> cow = Cow()
  >>> request = TestRequest()

  >>> mylayout = getMultiAdapter((request, cow), ILayout)

  FormPage:
  >>> myform = getMultiAdapter((cow, request), name='myformpage')
  >>> print myform()
  <html>
   <body>
     <div class="layout"><form action="http://127.0.0.1" method="post"
        class="edit-form" enctype="multipart/form-data">
  <BLANKLINE>
  <BLANKLINE>
  <BLANKLINE>
  <BLANKLINE>
  <BLANKLINE>
    <table class="form-fields">
      <tbody>
  <BLANKLINE>
          <tr>
            <td class="label">
  <BLANKLINE>
              <label for="form.color">
                <span class="required">*</span><span>Color</span>
              </label>
            </td>
            <td class="field">
              <div class="widget"><input class="textType" id="form.color" name="form.color" size="20" type="text" value=""  /></div>
  <BLANKLINE>
            </td>
          </tr>
  <BLANKLINE>
      </tbody>
    </table>
  <BLANKLINE>
    <div id="actionsView">
  <BLANKLINE>
    </div>
  </form>
  </div>
   </body>
  </html>




  Display form:
  >>> myview = getMultiAdapter((cow, request), name='myview')
  >>> print myview()
  <html>
   <body>
     <div class="layout">...
          <tr class="even">
            <td class="fieldname">
              Color
            </td>
            <td>
              globally dark
            </td>
          </tr>...
     </div>
   </body>
  </html>

  >>> myview
  <grok.ftests.forms.forms.MyView object at ...>
  >>> myview.layout
  <grok.ftests.forms.forms.Master object at ...>
  >>> print myview.content()
   <table class="listing">
    <thead>
      <tr>
        <th class="label-column">&nbsp;</th>
        <th>&nbsp;</th>
      </tr>
    </thead>
    <tbody>
  <BLANKLINE>
        <tr class="even">
          <td class="fieldname">
            Color
          </td>
          <td>
            globally dark
          </td>
        </tr>
  <BLANKLINE>
    </tbody>
    <tfoot>
      <tr class="controls">
        <td colspan="2" class="align-right">
        </td>
      </tr>
    </tfoot>
  </table>
  <BLANKLINE>

  Edit form:
  >>> myeditview = getMultiAdapter((cow, request), name='myeditview')
  >>> print myeditview()
  <html>
   <body>
     <div class="layout"><form action="http://127.0.0.1" method="post"
        class="edit-form" enctype="multipart/form-data">
  <BLANKLINE>
  <BLANKLINE>
  <BLANKLINE>
  <BLANKLINE>
  <BLANKLINE>
    <table class="form-fields">
      <tbody>
  <BLANKLINE>
          <tr>
            <td class="label">
  <BLANKLINE>
              <label for="form.color">
                <span class="required">*</span><span>Color</span>
              </label>
            </td>
            <td class="field">
              <div class="widget"><input class="textType" id="form.color" name="form.color" size="20" type="text" value="globally dark"  /></div>
  <BLANKLINE>
            </td>
          </tr>
  <BLANKLINE>
      </tbody>
    </table>
  <BLANKLINE>
    <div id="actionsView">
      <span class="actionButtons">
        <input type="submit" id="form.actions.apply" name="form.actions.apply" value="Apply" class="button" />
      </span>
    </div>
  </form>
  </div>
   </body>
  </html>
  <BLANKLINE>

  >>> myeditview
  <grok.ftests.forms.forms.MyEditView object at ...>
  >>> myeditview.layout
  <grok.ftests.forms.forms.Master object at ...>
  >>> print myeditview.content()
  <form action="http://127.0.0.1" method="post"
        class="edit-form" enctype="multipart/form-data">
     ...<span>Color</span>...
     ... value="globally dark" ...
     ... value="Apply" ...
  </form>


"""
import grokcore.component as grok

from grokcore.view import templatedir
from grok import Layout, DisplayFormPage, EditFormPage, FormPage
from zope import interface, schema


templatedir('templates')


class ICowProperties(interface.Interface):
    color = schema.TextLine(title=u"Color")


class Cow(grok.Context):
    grok.implements(ICowProperties)
    color = u"globally dark"


class Master(Layout):
    grok.name('master')
    grok.context(Cow)


class MyView(DisplayFormPage):
    grok.context(Cow)


class MyEditView(EditFormPage):
    grok.context(Cow)

class MyFormPage(FormPage):
    grok.context(Cow)
