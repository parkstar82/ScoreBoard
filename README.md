# ScoreBoard / 스코어보드

A simple scoreboard application with timer functionality, built using Python and Tkinter.
Python과 Tkinter를 사용하여 만든 간단한 스코어보드 및 타이머 기능이 있는 애플리케이션입니다.

## Features / 기능

- Display red and blue team scores / 빨간 팀과 파란 팀의 점수 표시
- Increase and decrease team scores using keyboard shortcuts / 키보드 단축키를 사용하여 팀 점수 증가 및 감소
- Set custom timer duration / 사용자 정의 타이머 시간 설정
- Start, pause, and reset timer functionality / 타이머 시작, 일시 정지 및 초기화 기능
- Warning indicators for each team / 각 팀별 경고 표시
- Dual screen mode feature to distinguish between referee screen and scoreboard screen/ 심판 화면과 전광판 화면을 구분하기 위해 듀얼 스크린 모드 기능

## Installation / 설치

1. Clone the repository:

```bash
git clone https://github.com/parkstar82/ScoreBoard.git
```

2. Change the directory:
```bash
cd scoreboard
```
3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage / 사용법
1. Run the ScoreBoard application:
For one screen
```bash
python scoreboard.py
```

For dual screen
```bash
python scoreboard_dual.py
```

2. Use the following keyboard shortcuts:
- `1`: Increase red team score / 빨간 팀 점수 증가
- `2`: Decrease red team score / 빨간 팀 점수 감소
- `4`: Win red team / 빨간 팀 승리
- `-`: Increase blue team score / 파란 팀 점수 증가
- `=`: Decrease blue team score / 파란 팀 점수 감소
- `9`: Win blue team / 파란 팀 승리
- `Spacebar`: Start or pause the timer / 타이머 시작 또는 일시 정지
- `Enter`: Toggle fullscreen mode / 전체 화면 모드 전환
- `Esc` : Deactivate fullscreen mode / 전체 화면 비활성화

3. To exit the application, close the window or press Ctrl+C in the terminal.
애플리케이션을 종료하려면 창을 닫거나 터미널에서 Ctrl+C를 누릅니다.

## License / 라이선스
This project is licensed under the MIT License.
이 프로젝트는 MIT 라이선스에 따라 라이선스가 부여됩니다.