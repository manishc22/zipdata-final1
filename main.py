from dotenv import load_dotenv
import os

from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from supabase import create_client, Client
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates/")

load_dotenv()
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


@app.get("/demoapp/reporting", response_class=HTMLResponse)
async def workspace(request: Request):
    title = 'Management Reporting'
    description = 'Integrated, single-window, view of all your Company Sales & Financial Performance'
    report = 'http://localhost:8501/?embed=true'
    return templates.TemplateResponse("app.html", {"request": request, "title": title, "description": description, "script": report})


@app.get("/demoapp/states")
async def reporting(request: Request):
    title = 'States / Regional Performance'
    description = 'Detailed Sales Performance data from different Regions / States'
    report = 'http://localhost:8501/States?embed=true'
    return templates.TemplateResponse("app.html", {"request": request, "title": title, "description": description, "script": report})


@app.get("/demoapp/home")
async def reporting(request: Request):
    title = 'Demo Data App - Home'
    description = 'Data App for a (dummy) Retail / E-Commerce Furniture Business'
    report = 'http://localhost:8501/Home?embed=true'
    return templates.TemplateResponse("app.html", {"request": request, "title": title, "description": description, "script": report})


@app.get("/demoapp/products")
async def reporting(request: Request):
    title = 'Product Analysis and Sales Performance'
    description = 'Detailed Sales data of different Products'
    report = 'http://localhost:8501/Products?embed=true'
    return templates.TemplateResponse("app.html", {"request": request, "title": title, "description": description, "script": report})


@app.get("/demoapp/stores")
async def reporting(request: Request):
    title = 'Store Sales Analysis and KPIs'
    description = 'Detailed Sales and KPIs of different Stores'
    report = 'http://localhost:8501/Stores?embed=true'
    return templates.TemplateResponse("app.html", {"request": request, "title": title, "description": description, "script": report})


@app.get("/demoapp/returns")
async def reporting(request: Request):
    title = 'Product Returns Data and Analysis'
    description = 'Detailed Cumulative and product-wise Analysis of Returns'
    report = 'http://localhost:8501/Returns?embed=true'
    return templates.TemplateResponse("app.html", {"request": request, "title": title, "description": description, "script": report})


@app.get("/", response_class=HTMLResponse)
async def dashboards(request: Request):
    return templates.TemplateResponse("website.html", {"request": request})


@app.get("/about-us", response_class=HTMLResponse)
async def dashboards(request: Request):
    return templates.TemplateResponse("about-us.html", {"request": request})


@app.get("/blog-main", response_class=HTMLResponse)
async def dashboards(request: Request):
    return templates.TemplateResponse("concept-blog.html", {"request": request})


@app.get("/demoapp/home", response_class=HTMLResponse)
async def dashboards(request: Request):
    return templates.TemplateResponse("app.html", {"request": request})


@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/external")
async def login():
    return RedirectResponse("https://www.linkedin.com/in/chaturvedimanish")


@app.post("/submit")
async def handleform(request: Request, name: str = Form(), company: str = Form(None), email: str = Form(), message: str = Form(None), phone: str = Form(None)):
    if name != '':
        supabase.table('website_contact').insert(
            {'name': name, 'email': email, 'phone': phone, 'company': company, 'message': message}).execute()
        confirmation = 'Thank you for contacting us. We will get back to you shortly.'
    else:

        confirmation = 'Sorry but the form could not be submitted as the name field was empty. You may try to go back and fill it again'
    return templates.TemplateResponse("submit.html", {"request": request, "confirmation": confirmation})
