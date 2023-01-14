from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
session = WolframLanguageSession()

session.evaluate(wlexpr('Range[5]'))
#session.evaluate(wlexpr('Print[Solve[x^2-4==0, x]]'))
