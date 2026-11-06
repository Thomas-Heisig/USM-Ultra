"""Small interactive USM BASIC console for early virtual-first development.

IMPORTANT: This is a HOST-SIDE Python interpreter, NOT 6502 machine code.
It is a temporary UI fallback while a licensed native 6502 BASIC is ported.
No eval/exec; only explicitly supported arithmetic and commands.
"""
import ast
import operator
import re
from dataclasses import dataclass, field

_BINOPS = {ast.Add:operator.add, ast.Sub:operator.sub, ast.Mult:operator.mul,
           ast.FloorDiv:operator.floordiv, ast.Div:operator.floordiv, ast.Mod:operator.mod}
_CMPS = {ast.Eq:operator.eq, ast.NotEq:operator.ne, ast.Lt:operator.lt,
         ast.LtE:operator.le, ast.Gt:operator.gt, ast.GtE:operator.ge}

@dataclass
class BasicConsole:
    program: dict[int,str] = field(default_factory=dict)
    variables: dict[str,int] = field(default_factory=dict)
    output: list[str] = field(default_factory=list)
    awaiting: str | None = None

    def expression(self, source):
        source = re.sub(r"(?<![<>!=])=(?!=)", "==", source.strip().upper())
        tree = ast.parse(source, mode="eval")
        def walk(n, depth=0):
            if depth > 24: raise ValueError("expression too deep")
            if isinstance(n, ast.Constant) and type(n.value) is int:
                return n.value
            if isinstance(n, ast.Name) and re.fullmatch(r"[A-Z][A-Z0-9]*",n.id):
                return self.variables.get(n.id,0)
            if isinstance(n, ast.UnaryOp) and isinstance(n.op,(ast.USub,ast.UAdd)):
                v=walk(n.operand,depth+1)
                return -v if isinstance(n.op,ast.USub) else v
            if isinstance(n,ast.BinOp) and type(n.op) in _BINOPS:
                a,b=walk(n.left,depth+1),walk(n.right,depth+1)
                if b==0 and isinstance(n.op,(ast.FloorDiv,ast.Div,ast.Mod)):
                    raise ValueError("division by zero")
                return _BINOPS[type(n.op)](a,b)
            if isinstance(n,ast.Compare) and len(n.ops)==1 and type(n.ops[0]) in _CMPS:
                return int(_CMPS[type(n.ops[0])](walk(n.left,depth+1),walk(n.comparators[0],depth+1)))
            raise ValueError("unsupported BASIC expression")
        result=walk(tree.body)
        if not -2147483648 <= result <= 2147483647:
            raise ValueError("integer overflow")
        return result

    def statement(self, statement):
        s=statement.strip()
        upper=s.upper()
        if upper.startswith("REM") and (len(s)==3 or s[3].isspace()): return None
        if upper.startswith("PRINT "):
            args=s[6:].strip()
            if args.startswith('"') and args.endswith('"') and len(args)>=2:
                self.output.append(args[1:-1])
            else: self.output.append(str(self.expression(args)))
            return None
        if upper.startswith("LET "): s=s[4:].strip()
        m=re.fullmatch(r"([A-Za-z][A-Za-z0-9]*)\s*=\s*(.+)",s)
        if m:
            self.variables[m.group(1).upper()]=self.expression(m.group(2))
            return None
        m=re.fullmatch(r"GOTO\s+(\d+)",upper)
        if m: return ("goto",int(m.group(1)))
        m=re.fullmatch(r"IF\s+(.+?)\s+THEN\s+(\d+)",upper)
        if m: return ("goto",int(m.group(2))) if self.expression(m.group(1)) else None
        if upper in ("END","STOP"): return ("stop",None)
        if upper=="": return None
        raise ValueError("unsupported statement: "+s[:60])

    def run(self, max_steps=10000):
        if not 1<=max_steps<=100000: raise ValueError("invalid step budget")
        lines=sorted(self.program)
        pc=0
        steps=0
        self.variables.clear()
        while pc<len(lines):
            if steps>=max_steps: raise ValueError("BASIC execution limit reached")
            action=self.statement(self.program[lines[pc]])
            steps+=1
            if action and action[0]=="stop": break
            if action and action[0]=="goto":
                if action[1] not in self.program: raise ValueError("undefined BASIC line")
                pc=lines.index(action[1])
            else: pc+=1
        return {"steps":steps,"output":self.output[-200:],"variables":dict(self.variables)}

    def submit(self, text):
        text=text.strip()
        if len(text)>512: raise ValueError("BASIC line too long")
        m=re.fullmatch(r"(\d{1,5})(?:\s+(.*))?",text)
        if m:
            line=int(m.group(1))
            if line>63999: raise ValueError("line number out of range")
            if m.group(2): self.program[line]=m.group(2)
            else: self.program.pop(line,None)
        elif text.upper()=="RUN": return self.run()
        elif text.upper()=="LIST":
            return {"listing":[f"{n} {self.program[n]}" for n in sorted(self.program)],"output":self.output[-200:]}
        elif text.upper()=="NEW":
            self.program.clear()
            self.variables.clear()
            self.output.clear()
        else:
            self.statement(text)
        return {"lines":len(self.program),"output":self.output[-200:],"variables":dict(self.variables)}
