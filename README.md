# D-WORK-BACK : D-WORK 프로젝트의 AWS에서 구동되는 백엔드 프로그램입니다.

Flask와 MongoDB를 활용한 간단한 회원/메모/북마크 관리 예제입니다.  
**⚠️ 본 코드는 학습 및 공유 목적이며, 실제 서비스 환경에서는 보안을 반드시 강화해야 합니다.**

로컬에서 실행시켜도 localhost의 5000 포트로 접근하면 사용할 수 있을 겁니다.

---

## 사용한 라이브러리, 기술

pymongo, flask, MongoDB

## 🚀 주요 기능

- 회원가입 & 로그인
- 메모 작성 및 조회
- 공고(Postings) 전체 조회
- 공고 북마크 추가, 조회, 삭제

---

## 💻 사전 준비

### ✅ Python 설치

- Python 3.8 이상 권장
- [Python 다운로드](https://www.python.org/downloads/)

### ✅ 가상환경 설정

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 패키지 설치

```bash
pip install -r requirements.txt
```

이미 필요한 패키지들은 required.txt 파일로 같이 올려두었으니 이렇게 다운로드만 받으면 됩니다.

## 🗂️ MongoDB 설정

### ✅ MongoDB Atlas (클라우드)

MongoDB Atlas 가입 및 클러스터 생성

DB 유저 생성 (DB_USER, DB_PASS)

네트워크 접근 → IP 화이트리스트 등록

연결 URI 확인 (예: mongodb+srv://...)

### ✅ 로컬 MongoDB (옵션)

로컬 MongoDB 설치 후 mongod 실행

기본 포트: 27017

### 🔑 .env 파일 생성

```bash
touch .env
```

.env 예시 내용: 로컬 기준입니다.

```ini
DB_USER=your_username // 설정한 MONGODB 아이디
DB_PASS=your_password // 설정한 MONGODB 패스워드
DB_HOST=localhost
```

## 추가 설명

어지간하면 python global에 모든 라이브러리 설치하지 말고, venv 관련해서 알아보신 뒤에 venv 환경에 설치하고 사용하세요 ( 파이썬 공식 권장 )

VSCode에서 venv 환경이 안 잡히는 경우가 있으면 그냥 터미널에서 실행시키세요.

## 보안 관련 문제들

백엔드 메인 프로젝트가 아니었기 때문에 JWT, 인증 관련 보안을 아무런 조치도 취하지 않았습니다.

.env 파일 절대 업로드 금지 (.gitignore에 추가)

비밀번호는 현재 평문 저장, 실제 서비스에서는 반드시 bcrypt 등으로 해싱

MongoDB Atlas → IP 화이트리스트와 강력한 비밀번호 설정

CORS → 운영 환경에서 특정 도메인만 허용하도록 제한 -> 지금은 전체 허용입니다.

에러 메시지 → 사용자에게 간단한 메시지 제공, 내부 로그로 상세 내용 관리

DB 사용자 권한 최소화 (읽기/쓰기 분리 등)
