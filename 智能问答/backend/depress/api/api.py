from ..models import History, Test, Problem, User
from django.http import HttpResponse
import json


def get_history(request):
    email = request.GET.get('email', '')
    history = History.objects.filter(email=email).order_by('time')
    msgs = []
    for h in history:
        msg = {}
        msg['text'] = h.text
        msg['time'] = h.time.strftime('%Y-%m-%d %H:%M:%S')
        msg['send'] = h.send
        msgs.append(msg)
    reply = {
        'msgs': msgs
    }
    return HttpResponse(json.dumps(reply))


def add_test(request):
    test_id = 2
    test_name = ''
    test_intro = ''
    test_num = 0
    test_price = 0
    test_label = '*&*&306&*'
    id = 1
    filename = 'F:\大创\抑郁症智能公益平台\\0项目\数据\\tests\\test1产后.txt'
    test_rule = ''
    problem_tid = 1
    problem_pid = 0
    problem_nov = 0
    problem_type = 0
    problem_description = ''
    problem_choice = ''
    problem_answer = ''
    problem_explanation = ''
    f = open(filename, 'r', encoding='utf-8')
    data = f.read()
    for i, test in enumerate(data.split('%')):
        if test == '':
            continue
        for j, item in enumerate(test.split('#')):
            if j == 0:
                test_id = 1000 + id
                test_name = item
            elif j == 1:
                test_intro = item
            elif j == 2:
                test_rule = item
                print(test_id, test_name, test_intro, test_rule)
                Test(tid=test_id, name=test_name, intro=test_intro, rule=test_rule, num=test_num, price=test_price, lid=test_label).save()
            elif j >= 3 and item != '':
                ps = item.split('*')
                problem_nov = j - 2
                problem_pid = int(str(test_id) + str(1000 + problem_nov))
                problem_description = ps[0].replace('\n', '').split('.')[1]
                problem_type = ps[1]
                choices = ps[2:]
                problem_choice = []
                problem_answer = []
                for c in choices:
                    c = c.split(';')
                    problem_choice.append(c[0])
                    problem_answer.append(c[1])
                problem_choice = ';'.join(problem_choice)
                problem_answer = ';'.join(problem_answer)
                # if len(ps) == 5:
                #     problem_explanation = ps[4]
                # else:
                problem_explanation = ''
                print(problem_pid, problem_description, problem_type, problem_choice, problem_answer, problem_explanation)
                Problem(tid=test_id, pid=problem_pid, nov=problem_nov, description=problem_description, choice=problem_choice, answer=problem_answer, explanation=problem_explanation).save()


def send_verify(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        if email == '':
            return HttpResponse('')
        else:
            try:
                User.objects.get(email=email)
                res = {
                    'code': 400
                }
                return HttpResponse(json.dumps(res))
            except:
                import random
                verify = str(random.randint(1000, 9999))
                msg = '感谢您使用抑郁症智能公益平台，您的验证码为：' + verify
                send_email(email, msg)
                request.session['verify'] = verify
                res = {
                    'code': 200
                }
                return HttpResponse(json.dumps(res))


def send_email(to, msg):

    from django.core.mail import send_mail
    from django.conf import settings

    send_mail('请查收验证码[抑郁症智能公益平台]', msg, settings.EMAIL_HOST_USER, [to], fail_silently=False)
