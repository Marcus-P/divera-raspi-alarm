import asyncio,sys
from .settings import load_settings
from .divera import send_news
async def main():
 component=sys.argv[1] if len(sys.argv)>1 else "System"
 c=load_settings()
 if not c.routing.technical_recipient_ids:return
 await send_news(f"TECHNISCHE STÖRUNG · {component}",f"Die automatische Systemüberwachung hat eine Störung bei {component} erkannt und eine Wiederherstellung gestartet.",c.routing.technical_recipient_ids)
if __name__=="__main__":asyncio.run(main())
