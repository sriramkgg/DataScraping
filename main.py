from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import io
import base64
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

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
            root_1 = (-b - D ** 0.5) / (2 * a)
            root_2 = (-b + D ** 0.5) / (2 * a)
            roots = 'The roots of the equation are ' + str([int(root_1), int(root_2)]) + '.'
            caveat = 'The roots listed here are floored. The plot shows actual values.'

            lb = 2*root_1 - root_2
            ub = 2*root_2 - root_1

            x = np.linspace(lb, ub, num=300, endpoint=True)
            y = a * (x ** 2) + b * x + c

            fig = plt.figure()
            plt.scatter(x, y)
            plt.scatter(np.array([root_1, root_2]), np.array([0, 0]))
        elif D == 0:
            root_1 = -b / (2 * a)
            roots = 'The root of the equation is ' + str([int(root_1)]) + '.'
            caveat = 'The root listed here is floored. The plot shows actual value.'

            lb = root_1 - 150
            ub = root_1 + 150

            x = np.linspace(lb, ub, num=300, endpoint=True)
            y = a * (x ** 2) + b * x + c

            fig = plt.figure()
            plt.scatter(x, y)
            plt.scatter(np.array([root_1]), np.array([0]))
        else:
            opt_val = -b / (2 * a)
            roots = 'The equation does not have any real root.'
            caveat = ''

            lb = opt_val - 150
            ub = opt_val + 150

            x = np.linspace(lb, ub, num=300, endpoint=True)
            y = a * (x ** 2) + b * x + c

            fig = plt.figure()
            plt.scatter(x, y)

    else:
        return templates.TemplateResponse('index.html',
                                          {'request': request,
                                           'roots': 'Not a valid quadratic equation. ' \
                                                    'Please use a non zero value for the coefficient a.'})

    equation = 'The equation is ' + str(a) + 'x^2 + ' + str(b) + 'x + ' + str(c) + '= 0'

    pngImage = io.BytesIO()
    fig.savefig(pngImage)
    pngImageB64String = base64.b64encode(pngImage.getvalue()).decode('ascii')
    return templates.TemplateResponse('index.html',
                                      {'request': request,
                                       'equation': equation,
                                       'caveat': caveat,
                                       'roots': roots,
                                       'picture': pngImageB64String})
