from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory='templates')


@app.get('/solve')
async def online_solve(a: float = 0,
                       b: float = 0,
                       c: float = 0):
    if a != 0:
        D = b**2 - 4*a*c
        if D > 0:
            return {'roots': [int((-b - D ** 0.5) / (2 * a)), int((-b + D ** 0.5) / (2 * a))]}
        elif D == 0:
            return {'roots': [int(-b / (2 * a))]}
        else:
            return {'roots': []}
    else:
        return {'roots': 'Not a quadratic equation'}


@app.get('/main')
async def root(request: Request):
    return templates.TemplateResponse('index.html',
                                      {'request': request})


@app.post('/main')
async def solve_equation(request: Request,
                         a: float = Form(...),
                         b: float = Form(...),
                         c: float = Form(...)):
    if a != 0:
        D = b**2 - 4*a*c
        if D > 0:
            return_dict = {'request': request,
                           'roots': 'The roots of the equation are ' + str([int((-b - D ** 0.5) / (2 * a)), int((-b + D ** 0.5) / (2 * a))])}
        elif D == 0:
            return_dict = {'request': request,
                           'roots': 'The roots of the equation are ' + str([int(-b / (2 * a))])}
        else:
            return_dict = {'request': request,
                           'roots': 'The roots of the equation are []'}
    else:
        return_dict = {'request': request,
                       'roots': 'Not a valid quadratic equation. Please use a non zero value for the coefficient a'}
    return templates.TemplateResponse('index.html',
                                      return_dict)

