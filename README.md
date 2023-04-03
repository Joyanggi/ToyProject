# ToyProject
* 프로젝트 설명

이번에 항해를 함께 하게 된 분들의 프로필을 올릴 수 있는 웹 사이트입니다. 회원 가입을 하면 메인 화면에 올라온 간단한 프로필들을 조회할 수 있고, 가입 후에 자신의 프로필을 올리면 다른 사람의 프로필에 방명록을 남길 수 있는 기능도 구현되어 있습니다. 추가로 프로필을 보고 싶은 사람의 이름으로 검색을 하는 기능도 구현하였습니다.

유튜브 링크
https://www.youtube.com/watch?v=Rij7n7SrLtM

와이어 프레임 링크
https://regular-toothbrush-ae8.notion.site/a3b7a43d3913451e8ec8b6e38514f831?v=8da1cdde95b04b548f7e9515ce223fb1

- 기술 스택

프론트엔드 : HTML, CSS, javascript

백엔드 : Python

DB : MongoDB

* 기능 설명
1. 회원가입/로그인
  * 회원가입
    1. 회원가입을 할 때, 아이디는 영문, 숫자로 5-11자로 만들어야 하고, 비밀번호는 영문, 숫자로 8자 이상으로 만들어야 합니다.
    2. 비밀번호 재입력을 통해 비밀번호 확인을 하고, 약관에 필수 약관에 대해서 동의를 체크해야 가입할 수 있도록 구현했습니다.(약관의 내용은 넣지 않았습니다.)
    3. 회원가입을 완료하면 서버에서 jwt 토큰을 제공하여 자동으로 로그인할 수 있도록 구현했습니다.
  - 로그인
    1. 메인화면에 있는 프로필을 클릭해서 상세 프로필로 들어가려면 로그인 페이지로 넘어가도록 구현했습니다.
    2. 로그인 후에 프로플을 클릭하면 상세 프로필 페이지로 들어가도록 구현했습니다.
    3. 로그인에 성공하면 jwt 토큰을 제공하여 로그인하도록 구현했습니다.
  - 로그아웃
    1. 로그아웃 버튼을 누르면 쿠키에 들어있는 토큰의 만료시간을 새로 지정하여 쿠키가 사라지도록 설정했습니다.
2. 프로필 등록/편집/삭제
  - 프로필 등록/편집
    1. 프로필을 등록할 때 사진을 넣지 않아도 기본 이미지로 설정되도록 구현했습니다.
    2. name, field, email을 넣지 않으면 등록이 불가능하도록 했고, email의 경우 email의 형식에 맞춰 적지 않아도 등록이 불가능하도록 구현했습니다.
    3. 편집도 등록과 비슷하게 작동하도록 구현했습니다.
  - 프로필 삭제
    1. 로그인한 계정에서 만든 프로필만 삭제할 수 있도록 구현했습니다.
3. 방명록 등록/삭제
  - 방명록 등록
    1. 로그인한 계정이 프로필을 만들지 않았을 경우, 방명록을 등록할 수 없도록 구현했습니다.
    2. 방명록을 등록할 때, 등록한 사람의 프로필 이미지, 이름과 방명록 내용이 나오도록 구현했습니다.
  - 방명록 삭제
    1. 로그인한 계정에서 만든 방명록만 삭제할 수 있도록 구현했습니다.
4. 검색
  - 이름으로 검색
    1. 메인화면에 있는 검색창에 이름을 적어서 검색 버튼을 누르면 검색한 내용을 포함한 이름을 가진 프로필을 나열하도록 구현했습니다.


