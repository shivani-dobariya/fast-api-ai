# JWT Configurations
JWT_SECRET_KEY = 'lX[&H?/TFEL/;FpjO)|lfs*^u[,q"y=Z1k&mg56M>NSGWjR._X:hAj7l&L.mk4@'
JWT_ALGORITHUM = 'HS256'
AUTH_TOKEN_EXP_MIN = 1
AUTH_TOKEN_EXP_DAY = 7
REFRESH_AUTH_TOKEN_EXP_DAY = 7
REFRESH_AUTH_TOKEN_EXP_MIN = 0


from openai import OpenAI

open_ai = OpenAI(api_key='OPENAI_KEY')
default_chat_completion_model = 'gpt-4-0125-preview'

#  CORS Configuration
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]
