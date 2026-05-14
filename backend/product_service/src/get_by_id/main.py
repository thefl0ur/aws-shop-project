from shared.create_handler import create_handler
from get_by_id.routes import router

handler = create_handler(router)
