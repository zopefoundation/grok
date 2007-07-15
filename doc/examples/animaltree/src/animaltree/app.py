import grok

class AnimalTree(grok.Application, grok.Container):
    def __init__(self):
        super(AnimalTree, self).__init__()
        self['start'] = Node(u'mammoth')

class Node(grok.Container):
    def __init__(self, text):
        super(Node, self).__init__()
        self.text = text
        
    def learn(self, new_animal, new_question, new_answer):
        if new_answer == 'yes':
            old_answer = 'no'
        else:
            old_answer = 'yes'
        self[new_answer] = Node(new_animal.strip())
        self[old_answer] = Node(self.text)
        self.text = new_question.strip()
        
    def isLeaf(self):
        '''return whether there are subnodes'''
        return self.has_key('yes')

    def question(self):
        if self.isLeaf():
            return self.text # the text is the question
        else: # otherwise the text is the name of the animal
            if self.text[0].lower() in 'aeiou':
                article = 'an'
            else:
                article = 'a'
            return 'Is it %s %s?' % (article, self.text)
        
class Index(grok.View):
    grok.context(AnimalTree)

class Guess(grok.View):
    grok.context(Node)
    
    def yes_url(self):
        if self.context.isLeaf():
            return self.url('yes/guess')
        else:
            return self.url('correct')
        
    def no_url(self):
        if self.context.isLeaf():
            return self.url('no/guess')
        else:
            return self.url('learn')

class Correct(grok.View):
    grok.context(Node)

class Learn(grok.View):
    grok.context(Node)

    def update(self, new_animal=None, new_question=None):
        if new_animal:
            if self.request.has_key('bt_yes'):
                new_answer = 'no'
            else:
                new_answer = 'yes'
            self.context.learn(new_animal, new_question, new_answer)
            self.redirect(self.application_url())
    