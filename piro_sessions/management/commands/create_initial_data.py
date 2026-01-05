from django.core.management.base import BaseCommand
from piro_sessions.models import Session
from datetime import date

class Command(BaseCommand):
    help = '초기 세션 데이터를 생성합니다'

    def handle(self, *args, **kwargs):
        sessions_data = [
            {'title': '2025.12.23(화) 오전', 'date': date(2025, 12, 23)},
            {'title': '2025.12.23(화) 오후', 'date': date(2025, 12, 23)},
            {'title': '2025.12.25(목)', 'date': date(2025, 12, 25)},
            {'title': '2025.12.27(토) 오전', 'date': date(2025, 12, 27)},
            {'title': '2025.12.27(토) 오후', 'date': date(2025, 12, 27)},
            {'title': '2025.12.30(화) 오전', 'date': date(2025, 12, 30)},
            {'title': '2025.12.30(화) 오후', 'date': date(2025, 12, 30)},
            {'title': '2026.01.01(목) 오전', 'date': date(2026, 1, 1)},
            {'title': '2026.01.01(목) 오후', 'date': date(2026, 1, 1)},
            {'title': '2026.01.03(토) 오전', 'date': date(2026, 1, 3)},
            {'title': '2026.01.03(토) 오후', 'date': date(2026, 1, 3)},
            {'title': '2026.01.06(화)', 'date': date(2026, 1, 3)},
            {'title': '2026.01.08(목) 오전', 'date': date(2026, 1, 3)},
            {'title': '2026.01.08(목) 오후', 'date': date(2026, 1, 3)},
            {'title': '2026.01.10(토) 오전', 'date': date(2026, 1, 3)},
            {'title': '2026.01.10(토) 오후', 'date': date(2026, 1, 3)},
            {'title': '2026.01.13(화) 오전', 'date': date(2026, 1, 3)},
            {'title': '2026.01.13(화) 오후', 'date': date(2026, 1, 3)},
            {'title': '2026.01.15(목) 오전', 'date': date(2026, 1, 3)},
            {'title': '2026.01.15(목) 오후', 'date': date(2026, 1, 3)},
            {'title': '2026.01.17(토)', 'date': date(2026, 1, 3)},
            {'title': '2026.01.20(화)', 'date': date(2026, 1, 3)},
            {'title': '2026.01.22(목)', 'date': date(2026, 1, 3)},
            {'title': '2026.01.24(토)', 'date': date(2026, 1, 3)},
        ]

        for session_data in sessions_data:
            session, created = Session.objects.get_or_create(
                title=session_data['title'],
                defaults={'date': session_data['date']}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ 세션 생성: {session.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'- 이미 존재: {session.title}')
                )

        self.stdout.write(self.style.SUCCESS('\n초기 데이터 생성 완료!'))