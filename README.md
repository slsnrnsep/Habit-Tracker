# 프로젝트 이름: Habit Tracker

당신의 습관을 기록해보세요! 평소 "다음에 해야지"라고만 생각하고 미뤄두었던 좋은 습관들을 기록해 관리해 드립니다.
뿐만 아니라 다른 사용자들의 좋은 습관들도 참고하여 기록해 둘 수 있습니다. 건강한 삶의 습관, Habit Tracker로 시작하세요!

- 웹사이트 링크: http://hoae.shop/login
- 데모영상: https://www.youtube.com/watch?v=5EtZ74O4tSA&t=2s&ab_channel=jinkyukim

---

👨‍💻 1. 제작 기간 & 팀원 소개

- 2021년 09월 13일 ~ 2021년 09월 17일
- 4인 1조 팀 프로젝트
  - 정영호
  - 김진규
  - 백승엽
  - 김다원

---

##🎨 2. 프로젝트 초안

![login_page](https://user-images.githubusercontent.com/90589276/133870486-c5495c5a-025c-45af-807f-71cac3c713e4.png)
![sign_up_page](https://user-images.githubusercontent.com/90589276/133870485-458592c1-9450-4591-8cf3-af3b4566bd4f.png)
![profile_page](https://user-images.githubusercontent.com/90589276/133870484-857c54d5-d119-46db-98d1-5176e6f5e69c.png)
![habit_page](https://user-images.githubusercontent.com/90589276/133870483-830bc514-a75a-426d-8248-1f8c6e1c96bc.png)
---

🔨 3. 사용 기술

- Back-end

- Front-end
  - Bulma
  - Bootstrap
  - Swiper (슬라이드)
  - Wave (동적인 배경화면)



  - Server: AWS EC2 (Ubuntu 18.04 LTS)

- Framework: Flask (Python)
- Database: MongoDB
- View : HTML5, CSS3, Javascript
- Design Tool (Figma)
- Tool : Git, Notion

---

💻 5. 기능

1. 로그인 + 회원가입
   - JWT를 이용하여 로그인과 회원가입 구현
   - 아이디 중복확인 가능
   - 아이디, 비밀번호 특정 룰 있음
2. 메인 페이지
   - 유저 당 1개의 슬라이드
3. 마이 페이지
   - CRUD?
     - mongoDB의 id로 특정 유저의 프로필 수정 가능
     - 프로필 업로드
     - 닉네임 수정
     - 자기소개 수정
4. 습관 페이지
   - 습관 당 1개의 슬라이드
   - CRUD?
     - mongoDB의 id로 특정 유저의 습관들만 보여줌

---

 ❗️ 프로젝트 중 힘들었지만 배운점이 있다면?

- 페이지가 여러개여서 다같이 서버 연결시키는 점이 어려웠다.
	-백앤드 부분을 위해 처음 api를 잘잡는게 중요
	- wire frame을 구체적이게 짜면 짤 수록 좋음 (기능부분포함해서까지)
- 여러명이 파일을 수정하고 각자 컴퓨터에 돌리다보니 기능들이 꼬였다.
	- 깃허브가 도움이 됨
