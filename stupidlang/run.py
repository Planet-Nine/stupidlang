from .parser import parse
from .evaluator import eval_ptree, Program

def backtolang(exp):
    """
    Takes a expression list and converts it back into a
    stupidlang expression.

    Parameters
    ----------

    exp : list
        A list representing a parsed stupidlang expression

    Returns
    -------
    str
        A string with the corrsponding stupidlang code
    Examples
    --------
    >>> from stupidlang.run import backtolang
    >>> backtolang(None)
    'nil'
    >>> backtolang(True)
    '#t'
    >>> backtolang(10)
    '10'
    """
    boolmap={True:'#t', False:'#f'}
    if  isinstance(exp, list):
        return '(' + ' '.join(map(backtolang, exp)) + ')'
    elif isinstance(exp, bool):
        return boolmap[exp]
    elif exp is None:
        return 'nil'
    else:
        return str(exp)

def repl(env, prompt='SL> '):
    """
    A REPL for the stupidlang language

    Parameters
    ----------

    env : Environment
        a concrete implementation instance of the Environment interface
    prompt : str, optional
        a string for the prompt, default SL>

    """
    try:
        import readline
    except:
        pass
    while True:
        try:
            val = eval_ptree(parse(input(prompt)), env)
        except (KeyboardInterrupt, EOFError):
            break
        if val is not None:
            print(backtolang(val))

def run_program_asif_repl(program, env):
    """
    Runs code with output as-if we were in a repl

    Parameters
    ----------

    program: str
        a multi-line string representing the stupidlang program
    env : Environment
        a concrete implementation instance of the Environment interface

    Returns
    -------

    str:
        The output of the program as if it were being run in a REPL
	
    Examples
    --------
    >>> from stupidlang.run import *
    >>> from stupidlang.evaluator import *
    >>> from stupidlang.env_dictimpl import *
    >>> globenv = global_env(Env)
    >>> program = '''
    ... (def rad 5)
    ... rad
    ... (def radiusfunc (func (radius) (* pi (* radius radius))))
    ... (radiusfunc rad)
    ... (def myvar 0)
    ... (if (== myvar 1) (store rad 6) (store rad 7))
    ... (radiusfunc rad)
    ... (== 1 1)
    ... '''
    >>> run_program_asif_repl(program,globenv)
    nil
    nil
    5
    nil
    78.53981633974483
    nil
    nil
    153.93804002589985
    #t
    nil

    """
    prog=Program(program, env)
    for result in prog.run():
        print(backtolang(result))

def run_program(program, env):
    """
    Runs code without output until the last line where output is provided.

    Parameters
    ----------

    program: str
        a multi-line string representing the stupidlang program
    env : Environment
        a concrete implementation instance of the Environment interface

    Returns
    -------

    str:
        The last output of the program as if it were being run in a REPL

    Examples
    --------
    >>> from stupidlang.run import *
    >>> from stupidlang.evaluator import *
    >>> from stupidlang.env_dictimpl import *
    >>> globenv = global_env(Env)
    >>> program = '''
    ... (def rad 5)
    ... rad
    ... (def radiusfunc (func (radius) (* pi (* radius radius))))
    ... (radiusfunc rad)
    ... (def myvar 0)
    ... (if (== myvar 1) (store rad 6) (store rad 7))
    ... (radiusfunc rad)'''
    >>> run_program(program,globenv)
    '153.93804002589985'

    """

    prog=Program(program, env)
    endit = None
    for result in prog.run():
        endit = result
    return backtolang(endit)
