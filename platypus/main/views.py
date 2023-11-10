from django.shortcuts import render, redirect
from .models import *
import time
import random
from django.http import HttpResponse, JsonResponse

from django.views.decorators.csrf import csrf_exempt
import json
import cv2
from pyzbar.pyzbar import decode
# Create your views here.
#참고용 프론트 페이지 렌더링
def backplate(request):
    return render(request,'main/backplate.html')

"""
def index(request):
    context={}
    try:#이미 가입된 회원인 경우
        useremail = request.session['useremail']
        user = USER_TABLE.objects.get(email=useremail)  
        try:      
            nickname = user.nickname
            learner_pk = user.learner_pk
            teacher_pk = user.teacher_pk
            ##
            learner = LEARNER_TABLE.objects.get(learner_pk=learner_pk)
            #
            lgen1 = learner.l_genre_1
            lgen1_list = lgen1.split('/')
            lgen1_name = lgen1_list[0]
            lgen1_sol = lgen1_list[1]#푼것의 수
            lgen1_cor = lgen1_list[2]#맞춘것의 수
            #
            lgen2 = learner.l_genre_2
            lgen2_list = lgen2.split('/')
            lgen2_name = lgen2_list[0]
            lgen2_sol = lgen2_list[1]
            lgen2_cor = lgen2_list[2]
            #
            lgen3 = learner.l_genre_3
            lgen3_list = lgen3.split('/')
            lgen3_name = lgen3_list[0]
            lgen3_sol = lgen3_list[1]
            lgen3_cor = lgen3_list[2]
            ##
            teacher = TEACHER_TABLE.objects.get(teacher_pk=teacher_pk)
            #
            tgen1 = teacher.t_genre_1
            tgen1_list = tgen1.split('/')
            tgen1_name = tgen1_list[0]
            tgen1_sco = tgen1_list[1]#총받은문제평가점수
            tgen1_num = tgen1_list[2]#총받은평가수
            #
            tgen2 = teacher.t_genre_2
            tgen2_list = tgen2.split('/')
            tgen2_name = tgen2_list[0]
            tgen2_sco = tgen2_list[1]
            tgen2_num = tgen2_list[2]
            #
            tgen3 = teacher.t_genre_3
            tgen3_list = tgen3.split('/')
            tgen3_name = tgen3_list[0]
            tgen3_sco = tgen3_list[1]
            tgen3_num = tgen3_list[2]
            #
            #context 삽입
            context['nickname'] = nickname
            context['lgen1_name'] = lgen1_name
            context['lgen2_name'] = lgen2_name
            context['lgen3_name'] = lgen3_name
            context['lgen1_sol'] = lgen1_sol
            context['lgen2_sol'] = lgen2_sol
            context['lgen3_sol'] = lgen3_sol
            context['lgen1_cor'] = lgen1_cor
            context['lgen2_cor'] = lgen2_cor
            context['lgen3_cor'] = lgen3_cor
            context['tgen1_name'] = tgen1_name
            context['tgen2_name'] = tgen2_name
            context['tgen3_name'] = tgen3_name
            context['tgen1_sco'] = tgen1_sco
            context['tgen2_sco'] = tgen2_sco
            context['tgen3_sco'] = tgen3_sco
            context['tgen1_num'] = tgen1_num
            context['tgen2_num'] = tgen2_num
            context['tgen3_num'] = tgen3_num
            context["message"]="SUCCESS"
        except:
            context["message"]="ERR"
        #이어서(TESTBANK만들었으면)
        return render(request, 'main/index.html', {'data':context})
    except:#가입 안된 회원의 경우
        return redirect('/404')
    
"""
"""
#로그인 기능 구현
def signin(request):
    if request.method == 'POST':
        useremail = request.POST['useremail']
        password = request.POST['password']
        if (useremail is not None) and (password is not None):
            try:
                user = USER_TABLE.objects.get(email=useremail, password=password)
                #세션에 넣어주면 됨
                request.session['useremail'] = user.email
                request.session['learner_pk'] = user.learner_pk
                request.session['teacher_pk'] = user.teacher_pk
            except:
                return redirect('/404')
            # 로그인 성공 후 리디렉션할 페이지 지정
            return redirect('/')  # 로그인 성공 시 이동할 URL
        else:
            # 로그인 실패 시 어떤 처리를 할지 여기에 작성
            return redirect('/500')
    else:
        request.session.flush()
        return render(request, 'main/signin.html')
"""
"""
def signup(request):
    if request.method == "POST":
        useremail = request.POST['useremail']
        password = request.POST['password']
        nickname = request.POST['nickname']
        if (useremail is not None) and (password is not None):
            try:#중복검사
                user = USER_TABLE.objects.get(email=useremail)
                return redirect('/DOUBLED!')
            except:
                #+유저생성,출제자,학습자데이터 생성
                gen_learner_pk = f'L{str(time.time())}'
                gen_teacher_pk = f'T{str(time.time())}'
                try:
                    new_user = USER_TABLE(
                        email=useremail,
                        password=password,
                        nickname=nickname,
                        learner_pk=gen_learner_pk,
                        teacher_pk=gen_teacher_pk,
                    )
                    new_learner = LEARNER_TABLE(
                        learner_pk=gen_learner_pk,
                        l_genre_1 = "없음/0/0",
                        l_genre_2 = "없음/0/0",
                        l_genre_3 = "없음/0/0",
                        l_test_banks = "/",
                    )
                    new_teacher = TEACHER_TABLE(
                        teacher_pk =gen_teacher_pk,
                        t_genre_1 = "없음/0/0",
                        t_genre_2 = "없음/0/0",
                        t_genre_3 = "없음/0/0",
                        t_test_banks = "/",
                    )
                    new_user.save()
                    new_learner.save()
                    new_teacher.save()
                    #세션에 넣어주면 됨
                    request.session['useremail'] = new_user.email
                    request.session['learner_pk'] = new_user.learner_pk
                    request.session['teacher_pk'] = new_user.teacher_pk
                    return redirect('/signin')#로그인하러가라
                except:
                    return redirect('/500')
        else:
            return redirect('/signup')
    else:
        return render(request, 'main/signup.html')
"""
#Slide  시작
def index(request):
    return render(request, 'main/index.html')

def scanner(request):
    return render(request, 'main/scanner.html')

def book_info(request):
    context={}
    #세션확인시작!
    return render(request,'main/book_info.html',{'data':context})
    try:
        useremail = request.session['useremail']
        user = USER_TABLE.objects.get(email=useremail)
    except:
        return redirect('/signin')
    book_pk = request.GET.get('pk')
    testbank_count = request.GET.get('bc')
    book = BOOK_TABLE.objects.get(book_pk=book_pk)
    book_name = book.book_name
    ISBN_code = book.ISBN_code
    genre_code = book.genre_code
    hash_note = book.hash_note
    queryset = TESTBANK_TABLE.objects.all()
    queryset = queryset.filter(book_pk=book_pk)
    testbank_pk_list = []
    testbank_name_list = []
    try:
        for query in queryset:
            testbank_pk_list.append(query.test_bank_pk)
            testbank_name_list.append(query.test_bank_name)
    except:
        pass
    context['testbank_pk_list'] = testbank_pk_list
    context['textbank_name_list'] = testbank_name_list
    context['book_pk'] = book_pk
    context['testbank_count'] = testbank_count
    context['book_name'] = book_name
    context['ISBN_code'] = ISBN_code
    context['genre_code'] = genre_code
    context['hash_note'] = hash_note
    
    return render(request,'main/book_info.html',{'data':context})

def justsolve_1(request):
    return render(request, 'main/justsolve_1.html')

def justsolve_2(request):
    return render(request, 'main/justsolve_2.html')

def justsolve_3(request):
    return render(request,'main/justsolve_3.html')

def testbank(request):#낸문제/푼문제(과거)모두 확인가능 + 문제검색
    context={}
    #세션확인시작!
    try:
        useremail = request.session['useremail']
        user = USER_TABLE.objects.get(email=useremail)
    except:
        return redirect('/signin')
    #세션확인끝!
    learner_pk = user.learner_pk
    teacher_pk = user.teacher_pk
    learner = LEARNER_TABLE.objects.get(learner_pk=learner_pk)
    teacher = TEACHER_TABLE.objects.get(teacher_pk=teacher_pk)
    l_test_banks = learner.l_test_banks
    l_test_banks_list = l_test_banks.split('/')
    t_test_banks = teacher.t_test_banks
    t_test_banks_list = t_test_banks.split('/')
    context['learner_pk'] = learner_pk
    context['teacher_pk'] = teacher_pk
    context['l_test_banks_list'] = l_test_banks_list
    context['t_test_banks_list'] = t_test_banks_list
    context['l_genre_1'] = learner.l_genre_1
    context['l_genre_2'] = learner.l_genre_2
    context['l_genre_3'] = learner.l_genre_3
    context['t_genre_1'] = teacher.t_genre_1
    context['t_genre_2'] = teacher.t_genre_2
    context['t_genre_3'] = teacher.t_genre_3
    context['l_genre_code1'] = context['l_genre_1'].split('/')[0]
    context['l_genre_code2'] = context['l_genre_2'].split('/')[0]
    context['l_genre_code3'] = context['l_genre_3'].split('/')[0]
    context['t_genre_code1'] = context['t_genre_1'].split('/')[0]
    context['t_genre_code2'] = context['t_genre_2'].split('/')[0]
    context['t_genre_code3'] = context['t_genre_3'].split('/')[0]
    return render(request, 'main/testbank.html',{'data':context})
    #... 공사중

def testbank_detail(request):#테뱅과 테뱅 리뷰를 보여줌
    context = {}
    #세션확인시작!
    try:
        useremail = request.session['useremail']
        user = USER_TABLE.objects.get(email=useremail)
    except:
        return redirect('/signin')
    #세션확인끝!
    testbank_pk = request.GET.get('pk')#testbank_detail/?pk=
    try:
        testbank = TESTBANK_TABLE.objects.get(test_bank_pk=testbank_pk)
        context['testbank_pk'] = testbank.test_bank_pk
        context['book_pk'] = testbank.book_pk
        context['test_bank_name'] = testbank.test_bank_name
        #
        test_keys_str = testbank.test_keys
        test_key_list = test_keys_str.split('/')
        context['test_key_list'] = test_key_list
    except:
        context['message'] = "ERR"
    return render(request,'main/testbank_detail.html',{'data':context})

def create_testbank(request):#테뱅을 만드는 페이지
    context = {}
    context['test_bank_pk'] = f'{str(time.time())}'
    return render(request,'main/create_testbank.html',{'data':context})
    try:
        useremail = request.session['useremail']
        user = USER_TABLE.objects.get(email=useremail)
    except:
        return redirect('/signin')
    #test_bank_pk = request.GET.get('pk')
    

def justsolve(request):#무지성으로 문제풀이하는 사이트
    context = {}
    #세션확인시작!
    try:
        useremail = request.session['useremail']
        user = USER_TABLE.objects.get(email=useremail)
    except:
        return redirect('/signin')
    #세션확인끝!
    email = user.email
    learner_pk = user.learner_pk
    #teacher_pk = user.teacher_pk
    test_bank_pk = request.GET.get('pk')
    testbank = TESTBANK_TABLE.objects.get(test_bank_pk=test_bank_pk)
    test_bank_name = testbank.test_bank_name
    test_keys_str = testbank.test_keys
    test_keys_list = test_keys_str.split('/')
    test_keys_list = list(filter(None, test_keys_list))
    context['email'] = email
    context['learner_pk'] = learner_pk#문제푼사람
    #context['teacher_pk'] = teacher_pk#문제낸사람
    context['test_bank_pk'] = test_bank_pk
    context['test_bank_name'] = test_bank_name
    context['test_keys_list'] = test_keys_list
    return render(request,'main/justsolve.html',{'data':context})
#html 렌더링 끝


#위는 잘 모르겠고, api로 요청하면 건네주는 방식으로 함
def api(request):
    return render(request,'main/api.html')

def api2(request):
    return render(request, 'main/api2.html')

@csrf_exempt
def api_make_testbank(request):#이걸 INDEX에서 하자.
    data={}
    if request.method == "POST":
        post_data = json.loads(request.body)
        test_bank_pk = f"T{str(time.time()).split('.')[1]}"
        book_pk = f"B{str(time.time()).split('.')[1]}"
        test_bank_name = post_data.get('test_bank_name')
        book_name = post_data.get('book_name')
        genre_code = post_data.get('genre_code')
        score = "0/0"
        test_keys = "/"
        review_keys = "/"
        new_testbank = TESTBANK_TABLE(
            test_bank_pk = test_bank_pk,
            book_pk = book_pk,
            test_bank_name = test_bank_name,
            genre_code = genre_code,
            score = score,
            test_keys = test_keys,
            review_keys = review_keys,
        )
        new_book = BOOK_TABLE(
            book_pk = book_pk,
            book_name = book_name,
            genre_code = genre_code,
        )
        new_testbank.save()
        new_book.save()
        data['test_bank_pk'] = test_bank_pk
        data['test_bank_name'] = test_bank_name
        data['message'] = "TESTBANK CREATED"
            #이후 api로 추가하면 됨.
        return JsonResponse({'data': data})
    else:
        return JsonResponse({'error': 'POST 요청이 아닙니다.'})

@csrf_exempt
#테이블의 이름과 pk를 가지고 모든 정보를 조회합니다.
def api_get_db(request):
    if request.method == 'POST':
        # POST 요청에서 데이터 추출
        post_data = json.loads(request.body)
        table_name = post_data.get('table')
        pk = post_data.get('primaryKey')
        data = {}
        if table_name == "USER_TABLE":
            user = USER_TABLE.objects.get(email=pk)
            data['email'] = user.email
            data['nickname'] = user.nickname
            data['learner_pk'] = user.learner_pk
            data['teacher_pk'] = user.teacher_pk
            data['note'] = user.note
        elif table_name == "LEARNER_TABLE":
            learner = LEARNER_TABLE.objects.get(learner_pk=pk)
            data['learner_pk'] = learner.learner_pk
            data['l_genre_1'] = learner.l_genre_1
            data['l_genre_2'] = learner.l_genre_2
            data['l_genre_3'] = learner.l_genre_3
            data['l_test_banks'] = learner.l_test_banks
        elif table_name == "TEACHER_TABLE":
            teacher = TEACHER_TABLE.objects.get(teacher_pk=pk)
            data['teacher_pk'] = teacher.teacher_pk
            data['t_genre_1'] = teacher.t_genre_1
            data['t_genre_2'] = teacher.t_genre_2
            data['t_genre_3'] = teacher.t_genre_3
            data['t_test_banks'] = teacher.t_test_banks
        elif table_name == "BOOK_TABLE":
            book = BOOK_TABLE.objects.get(book_pk=pk)
            data['book_pk'] = book.book_pk
            data['book_name'] = book.book_name
            data['ISBN_code'] = book.ISBN_code
            data['genre_code'] = book.genre_code
            data['hast_note'] = book.hash_note
        elif table_name == "TESTBANK_TABLE":
            testbank = TESTBANK_TABLE.objects.get(test_bank_pk=pk)
            data['test_bank_pk'] = testbank.test_bank_pk
            data['book_pk'] = testbank.book_pk
            data['test_bank_name'] = testbank.test_bank_name
            data['genre_code'] = testbank.genre_code
            data['score'] = testbank.score
            data['test_keys'] = testbank.test_keys
            data['review_keys'] = testbank.review_keys
        elif table_name == "TEST_TABLE":
            test = TEST_TABLE.objects.get(test_pk=pk)
            data['test_pk'] = test.test_pk
            data['type'] = test.type
            data['question'] = test.question
            data['ox_answer'] = test.ox_answer
            data['mt_answer'] = test.mt_answer
            data['sa_answer'] = test.sa_answer
        elif table_name == "REVIEW_TABLE":
            review = REVIEW_TABLE.objects.get(review_pk=pk)
            data['review_pk'] = review.review_pk
            data['reviewr_email'] = review.reviewr_email
            data['score'] = review.score
            data['note'] = review.note
        # 임시적으로 응답을 생성하는 예시
        response_data = {
            'table': table_name,
            'primaryKey': pk,
            'data': data
            # 원하는 데이터 형식으로 응답 데이터를 구성해야 합니다.
        }
        return JsonResponse(response_data)  # JSON 형식으로 응답
    else:
        return JsonResponse({'error': 'POST 요청이 아닙니다.'})

@csrf_exempt
def api_update_db(request):#생성이 아니라 수정이므로 pk가 없는 경우 오류반환
    if request.method == 'POST':
        # POST 요청에서 데이터 추출
        post_data = json.loads(request.body)
        table_name = post_data.get('table')
        pk = post_data.get('primaryKey')
        #ud = post_data.get('updateForm')#반드시 업데이트 안하는 데이터는 None임을 가정함
        data = {}
        if table_name == "USER_TABLE":
            user = USER_TABLE.objects.get(email=pk)
            #수정가능항목:없음
            return JsonResponse({'error': '수정가능한 내역이 없는 테이블'})
        elif table_name == "LEARNER_TABLE":
            learner = LEARNER_TABLE.objects.get(learner_pk=pk)
            #수정가능항목:1_genre_N,l_test_banks
            if post_data.get('l_genre_1') is not None:
                learner.l_genre_1 = post_data.get('l_genre_1')
            else:
                pass
            if post_data.get('l_genre_2') is not None:
                learner.l_genre_2 = post_data.get('l_genre_2')
            else:
                pass
            if post_data.get('l_genre_3') is not None:
                learner.l_genre_3 = post_data.get('l_genre_3')
            else:
                pass
            if post_data.get('l_test_banks') is not None:
                learner.l_test_banks = post_data.get('l_test_banks')
            else:
                pass
            learner.save()
        elif table_name == "TEACHER_TABLE":
            teacher = TEACHER_TABLE.objects.get(teacher_pk=pk)
            #수정가능항목:t_genre_N,t_test_banks
            if post_data.get('t_genre_1') is not None:
                teacher.t_genre_1 = post_data.get('t_genre_1')
            else:
                pass
            if post_data.get('t_genre_2') is not None:
                teacher.t_genre_2 = post_data.get('t_genre_2')
            else:
                pass
            if post_data.get('t_genre_3') is not None:
                teacher.t_genre_3 = post_data.get('t_genre_3')
            else:
                pass
            if post_data.get('t_test_banks') is not None:
                teacher.t_test_banks = post_data.get('t_test_banks')
            else:
                pass
            teacher.save()
        elif table_name == "BOOK_TABLE":
            book = BOOK_TABLE.objects.get(book_pk=pk)
            #수정가능항목:hash_note
            if post_data.get('hash_note') is not None:
                book.hash_note = post_data.get('hash_note')
            else:
                pass
            book.save()
        elif table_name == "TESTBANK_TABLE":#예를들어, testbank에 연결된 test들이 추가될때마다 사용될 수 있는것이다.
            testbank = TESTBANK_TABLE.objects.get(test_bank_pk=pk)
            #수정가능항목:score,test_keys,review_keys
            if post_data.get('score') is not None:
                testbank.score = post_data.get('score')
            else:
                pass
            if post_data.get('test_keys') is not None:
                testbank.test_keys = post_data.get('test_keys')
            else:
                pass
            if post_data.get('review_keys') is not None:
                testbank.review_keys = post_data.get('review_keys') 
            else:
                pass
            testbank.save()
        elif table_name == "TEST_TABLE":
            test = TEST_TABLE.objects.get(test_pk=pk)
            #수정가능항목:없음
            return JsonResponse({'error': '수정가능한 내역이 없는 테이블'})
        elif table_name == "REVIEW_TABLE":
            review = REVIEW_TABLE.objects.get(review_pk=pk)
            #수정가능항목:없음
            return JsonResponse({'error': '수정가능한 내역이 없는 테이블'})
        return JsonResponse({'error': 'NOT ERROR, DONE!'})
    else:
        return JsonResponse({'error': 'POST 요청이 아닙니다.'})

@csrf_exempt
def api_make_test(request):
    if request.method == 'POST':
        # POST 요청에서 데이터 추출
        post_data = json.loads(request.body)
        test_bank_pk = post_data.get('test_bank_pk')#물려놓을 tb
        test_pk = f"t{str(time.time()).split('.')[1]}"
        new_quiz = TEST_TABLE(
            test_pk = test_pk,
            type = post_data.get('type'),
            question = post_data.get('question'),
        )
        new_quiz.save()
        the_quiz = TEST_TABLE.objects.get(test_pk=test_pk)
        if post_data.get('ox_answer') is not None:
            the_quiz.ox_answer = post_data.get('ox_answer')
        else:
            pass
        if post_data.get('mt_answer') is not None:
            the_quiz.mt_answer = post_data.get('mt_answer')
        else:
            pass
        if post_data.get('sa_answer') is not None:
            the_quiz.sa_answer = post_data.get('sa_answer')
        else:
            pass
        the_quiz.save()
        #TB수정
        testbank = TESTBANK_TABLE.objects.get(test_bank_pk=test_bank_pk)
        testbank.test_keys = testbank.test_keys + f"{test_pk}/"
        testbank.save()
        return JsonResponse({'message': 'SUCCESSFULLY MADE!'})
    else:
        return JsonResponse({'error': 'POST 요청이 아닙니다.'})

@csrf_exempt
def api_end_test(request):
    if request.method == 'POST':
        # POST 요청에서 데이터 추출
        post_data = json.loads(request.body)
        test_bank_pk = post_data.get('test_bank_pk')
        learner_pk = post_data.get('learner_pk')
        test_length = post_data.get('test_length')
        score = post_data.get('score')
        testbank = TESTBANK_TABLE.objects.get(test_bank_pk=test_bank_pk)
        learner = LEARNER_TABLE.objects.get(learner_pk=learner_pk)
        genre_code = testbank.genre_code
        learner.l_test_banks = learner.l_test_banks + f'{test_bank_pk}/'
        if genre_code == learner.l_genre_1:
            lgen_1 = learner.l_genre_1
            lgen1_list = lgen_1.split('/')
            lgen1_list[1] = str(int(lgen1_list[1])+int(test_length))
            lgen1_list[2] = str(int(lgen1_list[2])+int(score))
            learner.l_genre_1 = '/'.join(lgen1_list)
        elif genre_code == learner.l_genre_2:
            lgen_2 = learner.l_genre_2
            lgen2_list = lgen_2.split('/')
            lgen2_list[1] = str(int(lgen2_list[1])+int(test_length))
            lgen2_list[2] = str(int(lgen2_list[2])+int(score))
            learner.l_genre_2 = '/'.join(lgen2_list)
        elif genre_code == learner.l_genre_3:
            lgen_3 = learner.l_genre_3
            lgen3_list = lgen_3.split('/')
            lgen3_list[1] = str(int(lgen3_list[1])+int(test_length))
            lgen3_list[2] = str(int(lgen3_list[2])+int(score))
            learner.l_genre_3 = '/'.join(lgen3_list)
        else:
            pass
        learner.save()
        return JsonResponse({'message':'점수반영완료!'})
    else:
        return JsonResponse({'error':'올바른 POST 요청 아님'})

@csrf_exempt
def api_search_testbank_by_genre(request):
    if request.method == 'POST':
        # POST 요청에서 데이터 추출
        post_data = json.loads(request.body)
        genre = post_data.get('genre')#검색할 genre
        queryset = TESTBANK_TABLE.objects.all()
        queryset = queryset.filter(genre_code=genre)
        book_list = []
        testbank_pk_list = []
        for query in queryset:
            book_list.append(query.book_pk)
            testbank_pk_list.append(query.test_bank_pk)
        return JsonResponse({'book_list': book_list, 'testbank_pk_list': testbank_pk_list})
    else:
        return JsonResponse({'error': 'POST 요청이 아닙니다.'})

@csrf_exempt
def api_search_testbank_by_ISBN(request):
    if request.method == 'POST':
        post_data = json.loads(request.body)
        ISBN = post_data.get('ISBN')#검색할 genre
        ISBN = str(ISBN)
        try:
            book = BOOK_TABLE.objects.get(ISBN_code=ISBN)
            book_pk = book.book_pk
            book_name = book.book_name
        except:#없는 경우
            return JsonResponse({'ERROR': '책을 찾을 수 없습니다','message':'ERR'})
        queryset = TESTBANK_TABLE.objects.all()
        queryset = queryset.filter(book_pk=book_pk)
        testbank_pk_list = []
        for query in queryset:
            testbank_pk_list.append(query.test_bank_pk)
        random_testbank_pk =  random.choice(testbank_pk_list)
        return JsonResponse({'message':'SUCCESS', 'book_pk': book_pk, 'book_name':book_name,'testbank_pk_list': testbank_pk_list, 'testbank_count': len(testbank_pk_list), 'random_testbank_pk': random_testbank_pk})
    else:
        return JsonResponse({'error': 'POST 요청이 아닙니다.'})
    
@csrf_exempt
def api_barcode_reader(request):
    if request.method == 'POST':  # 이미지 파일이 포함된 POST 요청 확인
        image_file = request.FILES['image']  # 이미지 파일 가져오기
        file_name = f"P{str(time.time()).split('.')[1]}.jpg"
        # 이미지를 저장할 경로 지정 (예: media/images/ 디렉토리 내에 저장)
        with open(f"media/{file_name}", 'wb') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)
        # 이미지가 성공적으로 저장되었음
        pass
    else:
        return JsonResponse({'message': '이미지를 받지 못했거나 잘못된 요청입니다.'}, status=400)
    # read the image in numpy array using cv2s
    img = cv2.imread(f'media/{file_name}')
    # Decode the barcode image
    detectedBarcodes = decode(img)
    # If not detected then print the message
    if not detectedBarcodes:
        return HttpResponse("바코드를 찾지 못했습니다! 똑바로 대주세요!")
    else:
        # Traverse through all the detected barcodes in image
        for barcode in detectedBarcodes:  
            # Locate the barcode position in image
            (x, y, w, h) = barcode.rect
            # Put the rectangle in image using 
            # cv2 to highlight the barcode
            cv2.rectangle(img, (x-10, y-10),
                          (x + w+10, y + h+10), 
                          (255, 0, 0), 2)
            #바로 삭제해벌임..
            if os.path.exists(f"media/{file_name}"):
                os.remove(f"media/{file_name}")
            else:
                pass
            if barcode.data!="":
            # Print the barcode data
                return HttpResponse(barcode.data)
            else:
                return HttpResponse("ERR")