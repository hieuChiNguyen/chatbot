from dotenv import load_dotenv


def load_env(env_file: str="local"):
    if env_file == "local":
        load_dotenv(".env.local", override=True)
    elif env_file == "production":
        load_dotenv(".env.production", override=True)
    else:
        raise ValueError(f"Unknown ENV: {env_file}")
