from fastapi import FastAPI
from api.user.routes import router as user_router
from api.product.routes import router as product_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(user_router)
app.include_router(product_router)


# CORS 설정
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)