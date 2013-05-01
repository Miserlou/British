import unicorn_lexer
import random
tokens = []
token = None

global_env = {}

class Token(object):
    def __init__(self, val):
        self.val = val

    # def __repr__(self):
    #     return "<%s %s>"%(self.__class__.__name__, self.val)

class StatementToken(Token):
    def __init__(self, val):
        self.val = val

class ExprToken(Token):
        pass

class ShowToken(StatementToken):
    lbp = None
    def std(self):
        next()
        self.second = expression(0)
        next(NewLineToken)
        return self
    def eval(self):
        print self.second.eval()

class PromptToken(Token):
    lbp = 10
    def nud(self):
        return self
    def eval(self):
        self.val = raw_input()
        return self.val

class RandomToken(Token):
    lbp = 10
    def nud(self):
        next(UsingToken)
        self.first = expression(0)
        next(ToToken)
        self.second = expression(0)
        # next(NewLineToken)
        return self
    def eval(self):
        self.val = random.randint(self.first.eval(), self.second.eval())
        return self.val

class UsingToken(Token):
    lbp = 0
    def led(self):
        pass
    def nud(self):
        pass

class ToToken(Token):
    lbp = 0
    def led(self):
        pass
    def nud(self):
        pass

class IsToken(StatementToken):
    def std(self):
        next()
        self.first = expression(0)
        next(QuestionToken)
        next(ThenToken)
        next(NewLineToken)
        self.second = statement()
        # print "second", self.second
        next(OrToken)
        self.third = expression(0)
        # print "third", self.third
        next(QuestionToken)
        next(ThenToken)
        next(NewLineToken)
        self.fourth = statement()
        # print "fourth", self.fourth
        next(OtherwiseToken)
        next()
        self.fifth = statement()
        # print "fifth", self.fifth
        return self
    def eval(self): 
        if self.first.eval() is True:
            return self.second.eval()
        elif self.third.eval() is True:
            return self.fourth.eval()
        else:
            return self.fifth.eval()

class QuestionToken(Token):
    lbp = 0
    def led(self):
        pass
    def nud(self):
        pass

class ThenToken(Token):
    lbp = 0
    def led(self):
        pass
    def nud(self):
        pass

class OrToken(Token):
    lbp = 0
    def led(self):
        pass
    def nud(self):
        pass

class OtherwiseToken(Token):
    lbp = 0
    def led(self):
        pass
    def nud(self):
        pass

class EndToken(Token):
    lbp = 0
    def led(self):
        pass
    def nud(self):
        pass

class MoreToken(Token):
    lbp = 20
    def led(self, left):
        self.first = left
        self.second = expression(20)
        return self
    def eval(self):
        if self.first.eval() > self.second.eval():
            # print "true"
            return True
        else:
            # print "false"
            return False

class LessToken(Token):
    lbp = 20
    def led(self, left):
        self.first = left
        self.second = expression(20)
        return self
    def eval(self):
        if self.first.eval() < self.second.eval():
            # print "true"
            return True
        else:
            # print "false"
            return False           
class EqualToken(Token):
    lbp = 20
    def led(self, left):
        self.first = left
        self.second = expression(20)
        return self
    def eval(self):
        if self.first.eval() == self.second.eval():
            # print "true"
            return True
        else:
            # print "false"
            return False 

class MoreEqualToken(Token):
    lbp = 20
    def led(self, left):
        self.first = left
        self.second = expression(20)
        return self
    def eval(self):
        if self.first.eval() >= self.second.eval():
            # print "true"
            return True
        else:
            # print "false"
            return False 

class LessEqualToken(Token):
    lbp = 20
    def led(self, left):
        self.first = left
        self.second = expression(20)
        return self
    def eval(self):
        if self.first.eval() <= self.second.eval():
            # print "true"
            return True
        else:
            # print "false"
            return False 

class IdToken(Token):
    lbp = 10
    def nud (self):
        return self
    def eval(self):
        return global_env[self.val]

class StringToken(Token):
    def nud(self):
        return self
    def eval(self):
        return self.val

class ReservedToken(Token):
    pass

class AddToken(Token):
    lbp = 20
    def nud(self):
        return expression(100)
    def led(self, left):
        self.first = left
        self.second = expression(20)
        return self
    def eval(self):
        return self.first.eval() + self.second.eval()

class SubToken(Token):
    lbp = 20
    def nud(self):
        return -expression(100)
    def led(self, left):
        self.first = left
        self.second = expression(20)
        return self
    def eval(self):
        return self.first.eval() - self.second.eval()

class MulToken(Token):
    lbp = 30
    def led(self, left):
        self.first = left
        self.second = expression(30)
        return self
    def eval(self):
        return self.first.eval() * self.second.eval()

class DivToken(Token):
    lbp = 30
    def led(self, left):
        self.first = left
        self.second = expression(30)
        return self 
    def eval(self):
        return self.first.eval() / self.second.eval()

class IntToken(Token):
    def __init__(self, val):
        self.val = int(val)
    def nud(self):
        return self
    def eval(self):
        return self.val

#not finished
class ConcatToken(Token):
    lbp = 20
    def led(self):
        self.second = expression(20)
        return self
    def eval(self):
        print self.second.eval()


class AssignToken(Token):
    lbp = 100
    def led (self, left):
        self.first = left
        # self.second = statement()
        # print "this is second", self.second
        self.second = expression(10)
        return self
    def eval(self):
        global_env[self.first.val] = self.second.eval()

class FinalToken(object):
    lbp = 0
    def led(self):
        pass
    def nud(self):
        pass

class NewLineToken(Token):
    lbp = 0
    def led(self):
        pass
    def nud(self):
        pass


RESERVED = ReservedToken

token_exprs = [
    (r'([ \t\r]+)',            None),
    (r'(#[^\n]*)',               None),
    (r'([0-9]+)',                IntToken),
    (r'"(.*)"',                  StringToken),
    (r"'(.*)'",                  StringToken),
    (r'(<-)',                    AssignToken),
    (r'(\?)',                    QuestionToken),
    (r'(\n)',                    NewLineToken),
    (r'(\()',                    RESERVED),
    (r'(\))',                    RESERVED),
    (r'(;)',                     RESERVED),
    (r'(:)',                     RESERVED),
    (r'(\.)',                    RESERVED),
    (r'(\,)',                    ConcatToken),
    (r'(\!)',                    RESERVED),
    (r'(\+)',                    AddToken),
    (r'(-)',                     SubToken),
    (r'(\*)',                    MulToken),
    (r'(\/)',                    DivToken),
    (r'(<=)',                    LessEqualToken),
    (r'(>=)',                    MoreEqualToken),
    (r'(=)',                     EqualToken),
    (r'(<)',                     LessToken),
    (r'(>)',                     MoreToken),
    (r'(!=)',                    RESERVED),
    (r'(=/=)',                   RESERVED),
    (r'(and)',                   RESERVED),
    (r'(or)',                    OrToken),
    (r'(not)',                   RESERVED),
    (r'(is)',                    IsToken),
    (r'(then:)',                 ThenToken),
    # (r'(loop)',                  LoopToken),
    (r'(list)',                  RESERVED),
    # (r'(with)',                  WithToken),
    # (r'(starting)',              StartingToken),
    (r'(otherwise:)',            OtherwiseToken),
    (r'(show)',                  ShowToken),
    # (r'(stop)',                  StopToken),
    (r'(end)',                   EndToken),
    (r'(to)',                    ToToken),
    (r'(using)',                 UsingToken),
    (r'(randomize)',             RandomToken),
    (r'(prompt)',                PromptToken),
    (r'([A-Za-z][A-Za-z0-9_]*)', IdToken),    
    (r'\'',                    None),
]

def unicorn_tokenize(characters):
    global tokens, token
    tokens = unicorn_lexer.lex(characters, token_exprs)
    token = tokens.pop(0)
    print tokens

def next(expected_token_type = None):
    global token

    if tokens:
        if expected_token_type is not None:
            if type(token) != expected_token_type:
                raise Exception("OMG THIS SUCKS")
        next_t = tokens.pop(0)
        token = next_t
        return token
    else:
        return FinalToken()

def expression(rbp=0):
    global token
    t = token
    token = next()
    left = t.nud()
    if token.lbp is not None:
        while rbp < token.lbp:
            t = token
            token = next()
            left = t.led(left)
    else:
        statement()
    return left


def statement():
    global token
    if isinstance(token, StatementToken):
        return token.std()
    else:
        expr = expression(0)
        next(NewLineToken)
        if type(expr) not in [AssignToken, MoreToken, LessToken, MoreEqualToken, LessEqualToken, EqualToken]:
            raise Exception("OMG THIS SUCKS EVEN MORE")
        else:
            return expr

class StatementList(StatementToken):
    def __init__(self, statements):
        self.statements = statements

    def std(self):
        pass

    def eval(self):
        for stmt in self.statements:
            stmt.eval()

def stmtlist():
    whatever = [] 
    while type(token) != FinalToken:
        s = statement();
        whatever.append(s)
    stmt_list = StatementList(whatever)
    return stmt_list
    
        
def parse():
    return stmtlist()
   
