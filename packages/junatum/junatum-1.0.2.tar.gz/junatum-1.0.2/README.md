# Junatum 프로젝트

![Github Workflow](https://github.com/Junatum/junatum/actions/workflows/main.yml/badge.svg)

Junatum 프로젝트는 공통으로 사용되는 모듈을 패키지화 하는 프로젝트입니다.


# 주요 시스템 구성 요소

* Python 3.10
* Python 3.11


# 개발

## 패키징 하는 방법

1. setup.py 에서 version 을 변경합니다.
2. `make build` 를 실행한다.

## 테스트 방법

1. `pyenv`를 준비한다.
   ```
   pyenv virtualenv 3.10.0 py310
   pyenv virtualenv 3.11.0 py311

   pyenv local py310 py311
   ```
2. `tox` 를 실행한다.

## 브랜치 전략

* Trunk-based Development ([링크](https://www.flagship.io/glossary/trunk-based-development/)) 를 기반으로 합니다.

## 커밋

* 항상 커밋 메시지 첫 항목에는 해당 티켓 번호를 명시합니다. ex) MINT-2018 홈 레이아웃을 개선함
* 만약 작업 중인 버전이나 테스트 중인 커밋은 티켓 번호 뒤에 WIP라고 명시합니다. ex) MINT-2019 WIP 모듈 하나 테스트
* 가급적 커밋 메시지는 요약된 한글 버전으로 작성합니다.
* 아래 템플릿을 .gitmessage.txt로 저장하고, git에 적용해서 사용하기를 강력 권장합니다.
  ```
  지라티켓-번호 70자 이내 제목

  본문(주로 왜 변경하였는지 기술)
  ```
  ```
  git config --local commit.template .gitmessage.txt
  ```

## 파이썬 스타일 가이드 ([PEP8](https://www.python.org/dev/peps/pep-0008/))

* `PEP8`을 항상 따르도록 함. 아래 프로그램을 사용하여 확인합니다.
  ```
  flake8 .
  ```

## 유닛 테스트

**새로 들어가는 기능이나 코드에는 항상 유닛 테스트 추가를 기본 원칙으로 합니다.**

## 트러블 슈팅

* `WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError("Can't connect to HTTPS URL because the SSL module is not available.")': /simple/pytz/`와 같은 에러가 발생할 경우, `pip install -r requirements.txt --no-cache-dir`를 사용하여 해결함.


# 라이센스

[LICENSE](LICENSE) 참조


# 저자

* Junatum <admin@junatum.com>

© 2015-2023 Junatum. All rights reserved.
