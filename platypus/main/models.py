from django.db import models
import os

class USER_TABLE(models.Model):
    email = models.CharField(max_length=128, primary_key=True)
    password = models.CharField(max_length=64)
    nickname = models.CharField(max_length=64,null=True,blank=True)
    learner_pk = models.CharField(max_length=32)
    teacher_pk = models.CharField(max_length=32)
    note = models.CharField(max_length=255, null=True, blank=True)

class LEARNER_TABLE(models.Model):
    learner_pk = models.CharField(max_length=32, primary_key=True)
    l_genre_1 = models.CharField(max_length=32, null=True, blank=True)#풀이장르는 3개까지 선택 가능, 장르코드(이름)/누적으로푼문제수/맟춘문제
    l_genre_2 = models.CharField(max_length=32, null=True, blank=True)
    l_genre_3 = models.CharField(max_length=32, null=True, blank=True)
    l_test_banks = models.CharField(max_length=255, null=True, blank=True)#테스트뱅크리스트.tbpk/tbpk2/..

class TEACHER_TABLE(models.Model):
    teacher_pk = models.CharField(max_length=32, primary_key=True)
    t_genre_1 = models.CharField(max_length=32, null=True, blank=True)#출제장르는 3개까지 선택 가능, 장르코드(이름)/출제한누적문제수/총받은누적평가점수
    t_genre_2 = models.CharField(max_length=32, null=True, blank=True)
    t_genre_3 = models.CharField(max_length=32, null=True, blank=True)
    t_test_banks = models.CharField(max_length=255, null=True, blank=True)

class BOOK_TABLE(models.Model):
    book_pk = models.CharField(max_length=8,primary_key=True)#이미지 파일 경로는 media/{book_pk}.png(일원화)
    book_name = models.CharField(max_length=64)
    ISBN_code = models.CharField(max_length=32,null=True,blank=True)
    genre_code = models.CharField(max_length=8,null=True,blank=True)#그냥 한국어 이름으로 함
    hash_note = models.CharField(max_length=255, null=True, blank=True)#해시태그가 들어감 #강원대 #전북대

class TESTBANK_TABLE(models.Model):
    test_bank_pk = models.CharField(max_length=8, primary_key=True)
    book_pk = models.CharField(max_length=8)
    test_bank_name = models.CharField(max_length=64) 
    genre_code = models.CharField(max_length=8,null=True,blank=True)#그냥 한국어 이름으로 함
    score = models.CharField(max_length=64)#'누적평가점수/해당TB'
    test_keys = models.CharField(max_length=255)#하위 문항 pks
    review_keys = models.CharField(max_length=255,null=True,blank=True)

class TEST_TABLE(models.Model):
    test_pk = models.CharField(max_length=8, primary_key=True)
    type = models.CharField(max_length=8)#'OX','MT','SA'
    question = models.CharField(max_length=255)#선다형_MT인 경우 함께 쓰도록 함. 
    ox_answer = models.CharField(max_length=8,null=True,blank=True)
    mt_answer = models.CharField(max_length=8,null=True,blank=True)
    sa_answer = models.CharField(max_length=64,null=True,blank=True)

class REVIEW_TABLE(models.Model):
    review_pk = models.CharField(max_length=8, primary_key=True)
    reviewr_email = models.CharField(max_length=128)#user pk
    score = models.CharField(max_length=8)#평가점수
    note = models.CharField(max_length=255,null=True,blank=True)
