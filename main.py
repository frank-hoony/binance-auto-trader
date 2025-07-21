import asyncio
from telegram_reader.chat_list_viewer import ChatListViewer

async def main():
    viewer = ChatListViewer()
    await viewer.start()
    await viewer.interactive_selection()
    await viewer.stop()

if __name__ == "__main__":
    asyncio.run(main())

