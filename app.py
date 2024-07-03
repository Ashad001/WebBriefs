from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
from webpage_summarizer import WebpageSummarizerAI

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Webpage Summarizer API. To use this service, prepend the API URL to the website URL you want to summarize. For example, visit /summarize/?url=https://example.com."
    }

@app.get("/summarize/", response_class=PlainTextResponse)
def summarize_url(request: Request):
    url = request.query_params.get("url")
    print("url--> ", url)
    summarizer = WebpageSummarizerAI(web_site=url.strip())
    print("--> Error")
    result = summarizer.run()
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
