# 33-2nd-BranchTime-backend
김민정, 임한구

# 33기 2차 프로젝트 BranchTime팀

<img width="544" alt="로고" src="https://user-images.githubusercontent.com/103249222/174513495-04076b0d-316c-4570-9df1-f7ea24589382.png">


<br/>

## 🌼 프로젝트 소개 🌼


* 글쓰기에 최적화 된 블로그 플랫폼 사이트를 선정했습니다.
* 짧은 기간동안 개발에 집중할 수 있도록 디자인과 기획 일부를 [브런치](https://brunch.co.kr)를 참조하여 학습목적으로 만들었습니다.
* 실무 수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
* 이 프로젝트에서 사용하고 있는 로고와 배너는 해당 프로젝트 팀원 소유이므로 해당 프로젝트 외부인이 사용할 수 없습니다.

<br/>

## 🌼 개발 인원 및 기간 🌼
**개발기간** : 2022/06/07~2022/06/17

<br/>

**개발인원 및 파트** : 
#### Frontend
- 박슬기 🐷 : Nav, 글 쓰기 페이지
- 김형겸 🍋 : 메인 페이지, 검색, 로그인
- 박주영 🌟 : 글 목록 페이지, 글 상세 페이지, 
- 신윤지 🐜 : 마이 페이지, 북 애니메이션

#### Backend
- 임한구 🎅🏻 : 소셜로그인, 마이페이지, 포스팅 리스트, 포스팅 디테일
- 김민정 🌟 : 포스팅 작성, 댓글 작성 및 리스트, 이메일 제안하기, 작가 리스트 

<br/>

## 🌼 기술 🌼
**Front-End** : React.js 
<br/>
**Back-End** : Python, Django web framework, MySQL, pyjwt, AWS
<br/>
**Common** : Git-Hub, slack, trello

<br/>

## 🌼 페이지별 구현 사항 🌼

### Users APP
#### 1. KakaoLoginView
 - 카카오 소셜로그인 API를 활용한 로그인 기능
 - 프론트엔드에서 인증후 code반환하면 그 code를 활용하여 access_token을 받아 사용자 정보(email, name, thumbnail)받아 Database에 저장.
 - 사용자 정보를 DB에 저장시 socialaccount DB에 api에서 제공하는 PK값과 해당하는 회사명("kakao")를 동시에 저장 (transantion활용)
#### 2. UserDetailView
 - 로그인하여 마이페이지 접속시 GET요청에 의해 반환
 - 로그인 데코레이터 활용하여 사용자 DB접근하여 사용자 정보 반환
#### 3. ProfileUpdate 
 - 마이페이지 수정  
 - AWS(S3) 활용 프로필사진 변경
 - 사용자 이름, 사용자 소개 수정

### contents APP
#### 1. CommentUploadView
 - 

#### 2. PostUploadView
 - 

#### 3. PostView
 - 

#### 4. ContentImageUploadView
 - 

#### 5. CommentView
 - 

#### 6. PostListView
 - 

#### 7. PostSubListView
 - 

#### 8. PostAllListView




### authors APP
#### 1. ProposalView
 - 
#### 2. AuthorListView
 - 
#### 3. AuthorDetailView
 - 




<br/>

## 🌼 프로젝트 진행 과정 🌼
||Trello|Daily Standup Meeting|
|------|---|---|
|협업 방식|칸반보드를 활용한 회의록 작성 및 진행상황 공유|매일 아침 30분동안 진행사항과 오늘 할 작업 내용 공유|
|IMG|<img width="1408" alt="트렐로" src="https://user-images.githubusercontent.com/103249222/174526348-44380889-6b7d-407a-90af-98c7c0480b00.png">|![트렐로디테일](https://user-images.githubusercontent.com/103249222/174526409-d2501faa-6ad2-49ca-9966-af12a7d66e65.png)|





