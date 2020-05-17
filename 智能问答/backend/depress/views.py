from django.shortcuts import render
from .forms import LoginForm, SignupForm, ChangeDetailForm
from .models import User, Test, Problem, Answers, History, Record, LabelRecord
from django.http import HttpResponse, HttpResponseRedirect, Http404
import datetime
import hashlib
import binascii
import sys

# Create your views here.


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = encode(form.cleaned_data['password'], email)
            try:
                user = User.objects.get(email=email)
                if user.password == password:
                    response = HttpResponseRedirect('/depress/xlpg')
                    request.session['name'] = user.name
                    request.session['email'] = user.email
                    request.session.set_expiry(0)
                    return response
                raise Http404()
            except:
                form = LoginForm()
                return render(request, 'depress/home.html', {
                    'form': form,
                    'err_msg': [['邮箱或密码错误']],
                    'mode': 1
                })
        else:
            form = LoginForm()
            error = form.errors
            err_msg = []
            for e in error:
                err_msg.append(error[e])
            return render(request, 'depress/home.html', {
                'form': form,
                'mode': 1,
                'err_msg': err_msg
            })
    else:
        raise Http404()


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            verify = form.cleaned_data['verify']
            right_verify = request.session.get('verify', '')
            if verify == right_verify:
                email = form.cleaned_data['email']
                name = form.cleaned_data['name']
                password = encode(form.cleaned_data['password1'], email)
                sex = form.cleaned_data.get('sex', '')
                address = form.cleaned_data.get('address', '')
                tel = form.cleaned_data.get('tel', '')
                user = User(email=email, name=name, password=password, sex=sex, address=address, tel=tel)
                user.save()
                form = LoginForm()
                return render(request, 'depress/home.html', {
                    'form': form,
                    'mode': 1,
                    'suc_msg': '注册成功'
                })
            else:
                return render(request, 'depress/home.html', {
                    'form': form,
                    'mode': 1,
                    'err_msg': ['验证码错误！']
                })
        else:
            error = form.errors
            err_msg = []
            for e in error:
                err_msg.append(error[e])
            return render(request, 'depress/home.html', {
                'mode': -1,
                'err_msg': err_msg
            })


def index(request):
    email = request.session.get('email', '')
    if email == '':
        form = LoginForm()
        return render(request, 'depress/home.html', {'form': form, 'mode': 1})
    else:
        response = HttpResponseRedirect('xlpg')
        return response


def znwd(request):
    return get_html(request, 'depress/znwd.html')


def aqtc(request):
    request.session.flush()
    return index(request)


def xgzl(request):
    email = request.session.get('email', '')
    if email == '':
        return index(request)
    else:
        if request.method == 'GET':
            form = ChangeDetailForm()
            user = User.objects.get(email=email)
            form['name'].initial = user.name
            form['email'].initial = user.email
            form['address'].initial = user.address
            form['tel'].initial = user.tel
            form['sex'].initial = user.sex
            return get_html(request, 'depress/xgzl.html', {'form': form})
        else:
            form = ChangeDetailForm(request.POST)
            suc_msg = ''
            err_msg = []
            if form.is_valid():
                name = form.cleaned_data['name']
                password = form.cleaned_data.get('password1', '')
                sex = form.cleaned_data.get('sex', '')
                address = form.cleaned_data.get('address', '')
                tel = form.cleaned_data.get('tel', '')
                user = User.objects.get(email=email)
                user.name = name
                user.sex = sex
                user.address = address
                user.tel = tel
                if password != '':
                    user.password = password
                user.save()
                suc_msg = '修改成功！'
            else:
                error = form.errors
                for e in error:
                    err_msg.append(error[e])
            form = ChangeDetailForm()
            form['name'].initial = request.POST.get('name', '')
            form['email'].initial = email
            form['address'].initial = request.POST.get('address', '')
            form['tel'].initial = request.POST.get('tel', '')
            form['sex'].initial = request.POST.get('sex', '')
            return get_html(request, 'depress/xgzl.html', {
                'form': form,
                'err_msg': err_msg,
                'suc_msg': suc_msg
            })


def xlpg(request):
    email = request.session.get('email', '')
    if email == '':
        return index(request)
    elif request.method == 'GET':
        records = Record.objects.filter(email=email).order_by('time').reverse()
        my_tests = []
        for r in records:
            t = {
                'tid': r.tid,
                'time': r.time,
                'score': r.score,
                'comment': r.comment,
                'level': r.level,
                'same_num': r.same_num,
                'name': Test.objects.get(tid=r.tid).name
            }
            my_tests.append(t)

        context = {
            'my_tests': my_tests,
            'my_tests_length': len(my_tests)
        }
        # 获取推荐测试
        context = get_tests(email, context)
        return get_html(request, 'depress/xlpg.html', context)
    raise Http404()


def change_mode(request):
    mode = request.GET.get('mode')
    if mode == '1':
        form = LoginForm()
        mode = 1
        return render(request, 'depress/home.html', {'form': form, 'mode': mode})
    else:
        mode = -1
        return render(request, 'depress/home.html', {'mode': mode})


def test(request):
    tid = request.GET.get('tid', '')
    if tid == '':
        raise Http404()
    else:
        try:
            t = Test.objects.get(tid=int(tid))
            rule = []
            for r in t.rule.split(';'):
                r = r.split(':')
                rule.append({
                    'level': r[0],
                    'comment': r[1]
                })
            if request.method == 'GET':
                problems = []
                ps = Problem.objects.filter(tid=tid).order_by('nov')
                for p in ps:
                    choice = []
                    # answer = []
                    # explanation = []
                    for i in range(len(p.choice.split(';'))):
                        choice.append(p.choice.split(';')[i])
                        # answer.append(p.answer.split(';')[i])
                        # if p.explanation == '':
                        #     continue
                        # else:
                        #     explanation.append(p.explanation.split(';')[i])
                    problems.append({
                        'pid': p.pid,
                        'nov': p.nov,
                        'description': p.description,
                        'type': p.type,
                        'choice': choice
                    })
                t.name = t.name.replace('《', '').replace('》', '')
                context = {
                    'tid': tid,
                    'test': t,
                    'problems': problems,
                    'problem_num':len(problems),
                    'index': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
                }
                return get_html(request, 'depress/test.html', context)
            elif request.method == 'POST':
                email = request.session.get('email', '')
                te = Test.objects.get(tid=tid)
                te.num += 1
                te.save()
                if email == '':
                    form = LoginForm()
                    return render(request, 'depress/home.html', {
                        'form': form,
                        'mode': 1
                    })
                else:
                    all_score = 0
                    comment = ''
                    level = 0
                    last_level = -1
                    percent = 0.
                    for key in request.POST:
                        value = request.POST.getlist(key)
                        pid = int(key)
                        score = 0
                        p = Problem.objects.get(pid=pid)
                        answer = []
                        for i in range(len(p.choice.split(';'))):
                            if (isinstance(value, list) and str(i) in value) or (not isinstance(value, list) and i == int(value)):
                                score += int(p.answer.split(';')[i])
                                answer.append('1')
                            else:
                                answer.append('0')
                        answer = ';'.join(answer)
                        a = Answers.objects.filter(email=email, pid=pid, tid=tid)
                        if a:
                            a = a.first()
                            a.answer = answer
                            a.score = score
                            a.save()
                        else:
                            Answers(email=email, pid=pid, tid=tid, answer=answer, score=score, same_num=0).save()
                        all_score += score
                    for i, r in enumerate(rule):
                        if all_score <= int(r['level']):
                            level = int(r['level'])
                            comment = r['comment']
                            percent = float(i) / float(len(rule))
                            break
                        else:
                            last_level = int(r['level'])
                    same_num = Record.objects.filter(score__gt=last_level, score__lte=level, tid=tid).__len__()
                    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(level, comment, percent, all_score)
                    Record(email=email, tid=tid, time=time, score=all_score, comment=comment, level=percent, same_num=same_num).save()

                    scores = [
                        {
                            'time': r.time.strftime('%Y-%m-%d'),
                            'score': r.score
                        } for r in Record.objects.filter(tid=tid, email=email).order_by('time')
                    ]

                    context = {
                        'tid': tid,
                        'score': all_score,
                        'comment': comment,
                        'level': percent,
                        'same_num': same_num,
                        'test': t,
                        'scores': scores[0:10],
                        'test_name': te.name
                    }

                    # 获取推荐测试
                    context = get_tests(email, context)
                    # 添加标签
                    if t.lid:
                        lids = t.lid.split('&')
                        for lid in lids:
                            if lid == '*':
                                continue
                            else:
                                for l in lid.split(';'):
                                    add_label(email, int(l))
                    return get_html(request, 'depress/test_result.html', context)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise Http404()


def test_result(request):
    tid = request.GET.get('tid', '')
    time = request.GET.get('time', '')
    email = request.session.get('email', '')

    if tid == '' or time == '' or request.method == 'POST' or email == '':
        return index(request)
    else:
        time = time.replace('_', '-')
        time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
        record = None
        records = Record.objects.filter(tid=tid, email=email).order_by('time')
        scores = []
        for r in records:
            t = r.time
            scores.append({
                'time': t.strftime('%Y-%m-%d'),
                'score': r.score
            })
            if time.year == t.year and time.month == t.month and time.day == t.day and time.hour == t.hour and time.minute == t.minute:
                record = r
        if not record:
            raise Http404()
        same_num = Record.objects.filter(tid=tid, level__gt=record.level-0.1, level__lte=record.level+0.1).__len__() - 1

        context = {
            'tid': tid,
            'score': record.score,
            'comment': record.comment,
            'level': record.level,
            'same_num': same_num,
            'scores': scores[0:10],
            'test_name': Test.objects.get(tid=tid).name
        }
        context = get_tests(email, context)
        return get_html(request, 'depress/test_result.html', context)


def get_html(request, url='depress/home.html', context={}):
    name = request.session.get('name', '')
    email = request.session.get('email', '')

    if email == '' or url == '':
        form = LoginForm()
        return render(request, 'depress/home.html', {
            'form': form,
            'mode': 1
        })
    else:
        context['name'] = name
        context['email'] = email
        return render(request, url, context)


def add_label(email, lid):
    label = LabelRecord.objects.filter(email=email, lid=lid).first()
    if label:
        label.times = label.times + 1
        label.save()
    else:
        LabelRecord(email=email, lid=lid, times=1, weight=1).save()


def if_add_test(test_label, user_label):
    if test_label == '*':
        return 2
    else:
        for l in user_label:
            if str(l.lid) in test_label:
                return 1
    return 0


def get_tests(email, context):
    labels = LabelRecord.objects.filter(email=email)
    label_1 = labels.filter(lid__range=(100, 200))
    label_2 = labels.filter(lid__range=(200, 300))
    label_3 = labels.filter(lid__range=(300, 400))
    label_4 = labels.filter(lid__range=(400, 500))
    recommend_tests = []
    tests = Test.objects.filter()
    temp_tests = []
    for i, t in enumerate(tests):
        if i < 10:
            temp_tests.append({
                'tid': t.tid,
                'name': t.name,
                'num': t.num
            })
        label = t.lid.split('&')
        if len(label_3) != 0:
            if_add = if_add_test(label[2], label_3)
            if if_add == 1:
                recommend_tests.append(t)
                continue
            elif if_add == 0:
                continue
        if len(label_2) != 0:
            if_add = if_add_test(label[1], label_2)
            if if_add == 1:
                recommend_tests.append(t)
                continue
            elif if_add == 0:
                continue
        if len(label_4) != 0:
            if_add = if_add_test(label[3], label_4)
            if if_add == 1:
                recommend_tests.append(t)
                continue
            elif if_add == 0:
                continue
        if len(label_1) != 0:
            if if_add_test(label[0], label_1) != 0:
                recommend_tests.append(t)
                continue
    context['recommend_tests'] = recommend_tests
    context['tests'] = temp_tests
    context['recommend_tests_length'] = len(recommend_tests)
    return context


def encode(pw, salt):
    b = hashlib.pbkdf2_hmac("sha256", str.encode(pw), str.encode(salt), 1000)
    return binascii.hexlify(b).decode()
