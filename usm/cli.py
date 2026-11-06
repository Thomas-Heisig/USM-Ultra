import argparse, json
from .core import Lab

def main():
    parser=argparse.ArgumentParser(description="USM-Ultra virtual lab")
    parser.add_argument("command",choices=["demo","status","web"])
    parser.add_argument("--host",default="127.0.0.1")
    parser.add_argument("--port",type=int,default=8000)
    args=parser.parse_args()
    lab=Lab()
    if args.command=="demo":
        lab.cpus["cpu0"].access(256,2,True,0xBEEF)
        print(vars(lab.cpus["cpu0"].access(256,2)))
    elif args.command=="status":
        print(json.dumps(lab.status(),indent=2))
    else:
        try:
            import uvicorn
            from .web import app
        except ImportError as exc:
            raise SystemExit("Install pip install -e '.[web]'") from exc
        uvicorn.run(app,host=args.host,port=args.port)

if __name__=="__main__":
    main()
