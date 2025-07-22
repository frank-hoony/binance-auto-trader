import asyncio
import logging
from pyrogram import Client
from pyrogram.enums import ChatType
from config.config import TELEGRAM_CONFIG

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatListViewer:
    def __init__(self):
        self.app = Client(
            TELEGRAM_CONFIG['session_name'],
            api_id=TELEGRAM_CONFIG['api_id'],
            api_hash=TELEGRAM_CONFIG['api_hash']
        )
        
    async def start(self):
        await self.app.start()
        me = await self.app.get_me()
        print(f"✅ 로그인: {me.first_name} (@{me.username})")
        
    async def stop(self):
        await self.app.stop()
        
    async def show_my_chats(self, limit=100):
        """내가 참여중인 모든 채팅방 목록을 보여주기"""
        print(f"\n{'='*80}")
        print(f"📱 내가 참여중인 채팅방 목록 (최근 {limit}개)")
        print(f"{'='*80}")
        
        channels = []
        groups = []
        private_chats = []
        
        count = 0
        async for dialog in self.app.get_dialogs(limit=limit):
            count += 1
            chat = dialog.chat
            
            # 채팅 타입에 따른 아이콘
            if chat.type == ChatType.CHANNEL:
                icon = "📺"
                chat_type = "채널"
            elif chat.type == ChatType.SUPERGROUP:
                icon = "👥"
                chat_type = "슈퍼그룹"
            elif chat.type == ChatType.GROUP:
                icon = "👥"
                chat_type = "그룹"
            else:
                icon = "👤"
                chat_type = "개인"
            
            # 채팅방 이름
            title = chat.title or f"{chat.first_name or ''} {chat.last_name or ''}".strip()
            
            # username이 있으면 @username, 없으면 ID 표시
            identifier = f"@{chat.username}" if chat.username else f"ID: {chat.id}"
            
            # 멤버 수 (있을 경우)
            members = getattr(chat, 'members_count', 0) or 0
            member_info = f" ({members:,}명)" if members > 0 else ""
            
            # 읽지 않은 메시지
            unread = f" [📬{dialog.unread_messages_count}]" if dialog.unread_messages_count > 0 else ""
            
            print(f"{count:3d}. {icon} {title}")
            print(f"     └─ {chat_type} | {identifier}{member_info}{unread}")
            
            # 설정 파일용으로 분류
            chat_info = {
                'title': title,
                'id': chat.id,
                'username': chat.username,
                'type': chat_type,
                'members': members
            }
            
            if chat.type == ChatType.CHANNEL:
                channels.append(chat_info)
            elif chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                groups.append(chat_info)
            else:
                private_chats.append(chat_info)
        
        # 요약 정보
        print(f"\n{'='*50}")
        print(f"📊 요약: 총 {count}개")
        print(f"   📺 채널: {len(channels)}개")
        print(f"   👥 그룹: {len(groups)}개") 
        print(f"   👤 개인: {len(private_chats)}개")
        
        return channels, groups, private_chats
    
    def generate_config_code(self, selected_chats):
        """선택된 채팅방들의 config.py 코드 생성"""
        config_lines = ["\n# 모니터링할 채널/그룹 목록"]
        config_lines.append("MONITORED_CHANNELS = [")
        
        for chat in selected_chats:
            if chat['username']:
                # username이 있으면 @username 사용
                config_lines.append(f"    '@{chat['username']}',  # {chat['title']} ({chat['type']})")
            else:
                # username이 없으면 ID 사용
                config_lines.append(f"    {chat['id']},  # {chat['title']} ({chat['type']})")
        
        config_lines.append("]")
        
        return "\n".join(config_lines)
    
    async def interactive_selection(self):
        """대화형으로 채팅방 선택"""
        channels, groups, private_chats = await self.show_my_chats()
        
        # 모든 채팅방을 하나의 리스트로 합치기
        all_chats = channels + groups
        
        if not all_chats:
            print("❌ 채널이나 그룹이 없습니다.")
            return
        
        print(f"\n{'='*50}")
        print("🎯 모니터링할 채팅방 선택")
        print("="*50)
        
        # 채팅방 목록을 번호와 함께 표시
        for i, chat in enumerate(all_chats, 1):
            identifier = f"@{chat['username']}" if chat['username'] else f"ID:{chat['id']}"
            print(f"{i:2d}. {chat['title']} ({identifier}) - {chat['type']}")
        
        print("\n📝 사용법:")
        print("  • 단일 선택: 3")
        print("  • 여러 선택: 1,3,5,7")
        print("  • 범위 선택: 1-5")
        print("  • 혼합 선택: 1,3,7-10")
        print("  • 전체 선택: all")
        
        while True:
            selection = input("\n선택할 번호를 입력하세요: ").strip()
            
            if not selection:
                continue
                
            try:
                selected_chats = []
                
                if selection.lower() == 'all':
                    selected_chats = all_chats
                else:
                    # 선택된 번호들 파싱
                    selected_indices = set()
                    
                    for part in selection.split(','):
                        part = part.strip()
                        if '-' in part:
                            # 범위 선택 (예: 1-5)
                            start, end = map(int, part.split('-'))
                            selected_indices.update(range(start, end + 1))
                        else:
                            # 단일 선택 (예: 3)
                            selected_indices.add(int(part))
                    
                    # 유효한 인덱스만 선택
                    for idx in selected_indices:
                        if 1 <= idx <= len(all_chats):
                            selected_chats.append(all_chats[idx - 1])
                
                if selected_chats:
                    print(f"\n✅ {len(selected_chats)}개 채팅방 선택됨:")
                    for chat in selected_chats:
                        identifier = f"@{chat['username']}" if chat['username'] else f"ID:{chat['id']}"
                        print(f"   • {chat['title']} ({identifier})")
                    
                    # config.py 코드 생성
                    config_code = self.generate_config_code(selected_chats)
                    
                    print(f"\n{'='*60}")
                    print("📄 config.py에 추가할 코드:")
                    print("="*60)
                    print(config_code)
                    
                    # 파일로 저장
                    with open('config/monitored_channels.py', 'w', encoding='utf-8') as f:
                        f.write(config_code)

                    
                    print(f"\n💾 'monitored_channels.txt' 파일로 저장되었습니다!")
                    print("   이 내용을 config.py 파일에 복사해서 붙여넣으세요.")
                    
                    break
                else:
                    print("❌ 선택된 채팅방이 없습니다.")
                    
            except ValueError:
                print("❌ 잘못된 입력입니다. 다시 입력해주세요.")
            except Exception as e:
                print(f"❌ 오류: {e}")

async def main():
    viewer = ChatListViewer()
    
    try:
        await viewer.start()
        await viewer.interactive_selection()
        
    except KeyboardInterrupt:
        print("\n❌ 사용자에 의해 중단되었습니다.")
    except Exception as e:
        logger.error(f"오류 발생: {e}")
    finally:
        await viewer.stop()

if __name__ == "__main__":
    asyncio.run(main())
