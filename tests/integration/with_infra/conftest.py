import os
from dotenv import load_dotenv


current_dir = os.path.dirname(__file__)
env_test_path = os.path.abspath(os.path.join(current_dir, ".env.test"))

load_dotenv(dotenv_path=env_test_path, override=True)
