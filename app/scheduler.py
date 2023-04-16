# import asyncio

# from apscheduler.schedulers.asyncio import AsyncIOScheduler

# from app import logs
# from app.core.config import settings
# from app.tasks import handle_callback_task, handle_pending_callback_task

# if __name__ == "__main__":
#     logs.init()
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     scheduler = AsyncIOScheduler()

#     scheduler.add_job(
#         handle_callback_task,
#         "interval",
#         seconds=settings.callback_task_interval_seconds,
#     )
#     scheduler.add_job(
#         handle_pending_callback_task,
#         "interval",
#         seconds=settings.callback_pending_task_interval_seconds,
#     )
#     scheduler.start()
#     loop.run_forever()
