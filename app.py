from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from LLM_QA_CLI import preprocess, get_answer
from dotenv import load_dotenv
import markdown

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/ask", response_class=HTMLResponse)
async def ask(request: Request, question: str = Form(...)):
    processed = preprocess(question)
    answer = get_answer(processed)
    html_answer = markdown.markdown(answer)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "question": question,
            "processed": processed,
            "html_answer": html_answer,
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
