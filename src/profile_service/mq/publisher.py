from __future__ import annotations

# TODO: Использовать common-mq
# from common_mq import MessagePublisher
# from profile_service.dtos.events import ProfileUpdatedV1, ThemeUpdatedV1, AccountDeletedV1

# class ProfileEventPublisher:
#     """Публикация событий профиля"""
#     
#     def __init__(self, publisher: MessagePublisher):
#         self.publisher = publisher
#     
#     async def publish_profile_updated(self, event: ProfileUpdatedV1):
#         """Опубликовать событие обновления профиля"""
#         await self.publisher.publish(
#             exchange="profile",
#             routing_key="profile.updated.v1",
#             message=event
#         )

