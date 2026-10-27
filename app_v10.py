import random
import re
import html
import streamlit as st

st.set_page_config(page_title="찐친 고민상담소", page_icon="🫧", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
.stApp { background: linear-gradient(180deg, #f2f7f2 0%, #faf8f4 100%); }
.block-container { max-width: 760px; padding-top: 2rem; padding-bottom: 3rem; }
.hero { background:#e2eee3; border:1px solid #d4e3d5; border-radius:26px; padding:28px 24px; margin-bottom:22px; }
.hero h1 { font-size:32px; color:#294a38; margin:0 0 10px; font-weight:800; }
.hero p { color:#506957; font-size:15px; line-height:1.85; margin:0; }
.section-title { color:#294a38; font-size:22px; font-weight:800; margin:22px 0 6px; }
.section-desc { color:#78877d; font-size:14px; margin-bottom:16px; }
.stButton > button { width:100%; min-height:58px; border-radius:16px; border:1px solid #dfe8e0; background:#fff; color:#304538; font-weight:700; font-size:15px; white-space:pre-wrap; transition:.15s; }
.stButton > button:hover { border-color:#8caf96; color:#294a38; background:#edf5ee; }
.stTextArea textarea { border-radius:16px; border:1px solid #dce6dd; background:#fff; font-size:15px; }
.chat-card { background:#fff; border:1px solid #e0e9e1; border-radius:22px; padding:22px; line-height:1.95; color:#35483b; margin:10px 0 16px; white-space:pre-wrap; }
.chat-label { color:#67846e; font-size:13px; font-weight:800; margin-bottom:8px; }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

CATEGORIES = {
    "🏫 학교생활": {
        "desc": "출결, 공부, 선생님, 학교 스트레스",
        "topics": [
            "학교 가는 것 자체가 너무 힘들어",
            "출결이나 졸업 때문에 불안해",
            "성적이나 공부 때문에 스트레스야",
            "선생님이랑 사이가 안 좋아",
            "학교에서 겉도는 기분이 들어",
            "진로 때문에 학교생활이 막막해",
        ],
    },
    "🫂 인간관계": {
        "desc": "친구, 가족, 주변 사람들 문제",
        "topics": [
            "친구랑 멀어진 것 같아",
            "나만 먼저 연락하는 것 같아",
            "사람들 눈치를 너무 많이 봐",
            "뒷담화나 따돌림 때문에 힘들어",
            "가족이랑 자꾸 부딪혀",
            "사람한테 정이 떨어졌어",
        ],
    },
    "💗 연애": {
        "desc": "짝사랑, 연락, 연애, 이별",
        "topics": [
            "짝사랑 중인데 너무 힘들어",
            "상대방 마음을 모르겠어",
            "연애 중인데 자꾸 불안해",
            "연락 문제로 스트레스받아",
            "헤어진 사람을 못 잊겠어",
            "내가 더 좋아하는 것 같아",
        ],
    },
    "🌱 미래": {
        "desc": "진로, 대학, 돈, 자존감, 앞으로의 삶",
        "topics": [
            "내가 뭘 하고 싶은지 모르겠어",
            "취업이나 대학 때문에 불안해",
            "돈 문제 때문에 막막해",
            "남들은 잘 사는 것 같은데 나만 뒤처져",
            "내가 잘하는 게 없는 것 같아",
            "앞으로 어떻게 살아야 할지 모르겠어",
        ],
    },
}

# 답변 구성: 공감 + 현실적인 한마디 + 할 수 있는 행동
ADVICE = {
    "학교 가는 것 자체가 너무 힘들어": [
        "야, 매일 가야 하는 곳이 스트레스면 아침부터 기운 쫙 빠지지. 남들은 별일 없이 다니는 것 같아도 너한테는 그게 쉬운 일이 아닐 수 있음.\n\n근데 일단 뭐가 제일 힘든지부터 나눠 보자. 사람이 힘든 건지, 학교 분위기가 싫은 건지, 몸이랑 마음이 지친 건지. 원인도 모르고 무조건 버티기만 하면 더 지쳐. 내일 하루를 덜 힘들게 만들 방법부터 찾자.",
        "학교가 그냥 귀찮은 정도가 아니라 가는 것 자체가 버거운 거면 좀 진지하게 봐야 돼. 네가 의지가 약해서라고 몰아붙일 일은 아님.\n\n일단 담임이나 믿을 만한 어른 한 명한테 지금 상태를 구체적으로 말해 봐. 혼자 꾹 참고 있다가 한꺼번에 터지는 게 제일 손해야. 해결책은 같이 찾아도 됨."
    ],
    "출결이나 졸업 때문에 불안해": [
        "야 그건 불안할 만하지. 졸업 걸려 있으면 별생각 다 들고, 혼자 최악의 상황까지 상상하게 되잖아.\n\n근데 아직 확인 안 된 일을 머릿속에서 확정 짓지는 말자. 지금 학교에서 정확히 어떤 절차가 필요한지, 뭘 제출해야 하는지 담당 선생님한테 확인하는 게 먼저야. 불안해한다고 해결되는 건 아니지만, 확인하고 움직이면 바꿀 수 있는 건 생김. 지금은 자책 말고 할 일부터 잡자.",
        "솔직히 마음 졸일 만한 상황이긴 함. 근데 혼자 '나 이제 끝났다' 하고 결론 내리면 해결할 기회까지 놓치잖아.\n\n출결 현황, 남은 절차, 필요한 서류를 하나씩 확인해. 가능하면 보호자나 선생님이랑 같이 확인하고. 네 인생 전체가 지금 이 문제 하나로 판정 나는 건 아니니까, 겁먹더라도 할 수 있는 행동은 하자."
    ],
    "성적이나 공부 때문에 스트레스야": [
        "성적 안 나오면 점수만 속상한 게 아니라 내가 멍청한가 싶고 자존감까지 털리지. 근데 점수 하나로 네 머리 전체를 평가하는 건 너무 단순한 계산임.\n\n대신 어디서 막히는지 보자. 시간이 부족한 건지, 공부법이 안 맞는 건지, 이미 지쳐서 집중이 안 되는 건지. 원인도 모르고 무작정 더 하겠다고 덤비면 효율 개박살 나. 한 과목, 한 단원부터 정리하자.",
    ],
    "선생님이랑 사이가 안 좋아": [
        "매일 봐야 하는 사람이랑 사이 안 좋으면 피할 수도 없어서 더 짜증 나지. 네 입장에선 억울한 부분도 있을 거고.\n\n근데 바로 감정적으로 부딪히면 네가 손해 볼 수도 있으니까, 무슨 일이 있었는지 날짜랑 상황을 차분히 정리해 둬. 네가 잘못한 부분이 있으면 인정하면 되고, 부당한 부분이 있으면 다른 믿을 만한 선생님한테 도움을 요청해. 선생님이라고 무조건 옳은 건 아니지만 대응은 똑똑하게 하자.",
    ],
    "학교에서 겉도는 기분이 들어": [
        "사람들 사이에 있는데도 혼자인 기분 들면 은근히 사람 미치게 함. 다들 자기들끼리 잘 지내는 것 같고 나만 붕 뜬 느낌 들잖아.\n\n근데 그 반에서 잘 안 맞는다고 네가 어디서도 못 어울리는 사람인 건 아님. 모두한테 인기 얻으려고 애쓰지 말고, 일단 한 명이라도 편하게 말 섞을 사람을 찾아봐. 억지로 무리에 끼려고 네 성격까지 뜯어고칠 필요 없어.",
    ],
    "진로 때문에 학교생활이 막막해": [
        "진로 아직 모르겠다고 인생 망한 거 아님 ㅋㅋ 아직 안 해 본 일이 얼마나 많은데 벌써 평생 직업을 확정하냐.\n\n지금은 '내 천직이 뭐지?' 같은 거창한 질문 말고, 해 보고 싶은 거랑 진짜 하기 싫은 거부터 적어 봐. 작은 경험도 해 보고. 진로는 한 번 고르면 평생 못 바꾸는 계약서가 아니야. 일단 다음 한 걸음만 정하자.",
    ],
    "친구랑 멀어진 것 같아": [
        "예전 같지 않다는 느낌 들면 혼자 별생각 다 하게 되지. 내가 뭘 잘못했나, 이제 나랑 놀기 싫은가 싶고.\n\n근데 상대가 바쁜 건지 진짜 관계가 변한 건지 아직 모를 수도 있어. 한 번은 먼저 가볍게 말을 걸어 보고 반응을 봐. 그래도 계속 너 혼자만 애쓰는 느낌이면 조금 거리를 두는 것도 괜찮아. 관계 유지한다고 네 자존심까지 매번 접을 필요는 없음.",
    ],
    "나만 먼저 연락하는 것 같아": [
        "아 그거 은근 개서운함 ㅋㅋ 연락은 맨날 내가 먼저 하고, 안 하면 조용하고. 그러면 '나만 친하다고 생각하나?' 싶지.\n\n한동안 네가 먼저 연락 안 해 보고 네 생활을 해 봐. 상대 엿 먹이려고 밀당하라는 게 아니라, 관계가 진짜 한쪽 힘으로만 굴러가는지 보라는 거임. 연락 안 온다고 네 가치가 떨어지는 건 아니야. 네 하루를 걔 답장 대기 화면으로 만들진 말자.",
        "솔직히 네가 계속 먼저 연락하는 게 당연한 일이 되면 상대는 그 노력 자체를 못 느낄 수도 있어. 그렇다고 일부러 게임하듯 시험할 필요는 없고.\n\n한 번 네가 연락할 에너지를 너한테 써 봐. 상대도 관계를 이어 가고 싶으면 자기 방식으로 표현하겠지. 계속 너만 애쓰면 그 관계에 어느 정도 힘을 쓸지 다시 정해도 돼."
    ],
    "사람들 눈치를 너무 많이 봐": [
        "누가 표정만 살짝 바꿔도 '내가 뭐 잘못했나?' 하고 집 와서까지 복기하는 거면 진짜 피곤하겠다. 머릿속에서 혼자 재판 열고 있는 거잖아.\n\n근데 모든 사람 기분을 네가 책임질 순 없어. 누가 무표정했다고 네 잘못이라는 증거는 없잖아. '이건 사실이야, 아니면 내 추측이야?' 하고 한 번 끊어 봐. 처음엔 어렵지만 남의 반응보다 네 기준을 조금씩 키우는 게 중요함.",
    ],
    "뒷담화나 따돌림 때문에 힘들어": [
        "그건 네가 예민해서 그런 게 아님. 누가 일부러 배제하거나 상처 주면 당연히 힘들지. 그런 상황에서 '내가 더 잘하면 되나?' 하면서 네 탓만 하지 마.\n\n혼자 해결하려고 버티지 말고, 있었던 일을 기록해 두고 믿을 만한 어른이나 선생님한테 알려. 상대에게 인정받는 게 목표가 아니라 네가 안전하게 지내는 게 먼저야. 네가 전부 감당해야 하는 문제 아님.",
    ],
    "가족이랑 자꾸 부딪혀": [
        "가족은 가까우니까 더 세게 부딪힐 때가 있음. 밖에서는 참다가 집에서 터지기도 하고, 말 한마디가 오래 남기도 하고.\n\n둘 다 화난 상태에서 결판 내려 하면 보통 더 꼬임. 조금 진정된 다음에 '맨날 왜 그래'보다 '그렇게 말하면 내가 이런 기분이 들어'라고 얘기해 봐. 대화해도 안 통하거나 위협받는 상황이면 다른 믿을 만한 어른한테 도움 요청해도 돼. 가족이라고 무조건 참아야 하는 건 아님.",
    ],
    "사람한테 정이 떨어졌어": [
        "계속 실망하면 그냥 사람 자체가 피곤해지지. 기대했다가 뒤통수 맞는 기분 들면 '다 필요 없다' 싶을 수도 있고.\n\n지금 억지로 누구를 믿으려고 애쓰지 않아도 돼. 다만 몇 명한테 상처받았다고 세상 사람 전부 똑같다고 결론 내리진 말자. 당분간 거리 두고 네 컨디션부터 챙겨. 사람한테 정 떨어질 정도면 일단 좀 쉬어야 할 수도 있음.",
    ],
    "짝사랑 중인데 너무 힘들어": [
        "좋아하는 마음은 내 마음인데 내 맘대로 껐다 켰다 못 하니까 개빡치지 ㅋㅋ 연락 한 번에 기분 천국 갔다가 답 없으면 지옥 가고.\n\n근데 걔 반응에 네 하루 전체를 맡기진 마. 좋아하는 건 괜찮은데 네 생활까지 다 갖다 바칠 필요는 없잖아. 고백할지 말지는 네가 거절당해도 감당할 수 있을지, 지금 관계가 어떤지 보고 정하자. 좋아한다고 네 마음을 막 굴려도 되는 건 아님.",
    ],
    "상대방 마음을 모르겠어": [
        "애매하게 굴면 혼자 추리소설 쓰게 됨 ㅋㅋ 답장 속도 분석하고 말투 해석하고. 근데 그렇게 머리 굴려도 정답이 안 나오면 너만 지침.\n\n한 번의 행동 말고 전체적인 모습을 봐. 꾸준히 시간을 내는지, 네 얘기를 존중하는지, 말이랑 행동이 맞는지. 그래도 모르겠으면 가볍게 물어봐도 돼. 계속 헷갈리게 만드는 관계가 너한테 편한지도 같이 생각해 보고.",
    ],
    "연애 중인데 자꾸 불안해": [
        "좋아하니까 잃을까 봐 무서운 거겠지. 그 마음 자체가 이상한 건 아님. 근데 불안할 때마다 상대 반응을 확인해야 겨우 진정되는 상태면 너도 너무 힘들 거야.\n\n실제로 무슨 일이 있었는지랑 네가 걱정하는 걸 구분해 보자. 그리고 상대에게 차분하게 네 마음을 말해 봐. 연애는 한 명이 계속 안심시키고 다른 한 명이 계속 참는 게임이 아니야. 둘 다 편해질 방법을 찾아야지.",
    ],
    "연락 문제로 스트레스받아": [
        "연락 때문에 싸우는 거 은근 흔한데 당사자는 안 흔함. 답장 기다리는 사람은 하루 종일 신경 쓰이거든.\n\n서로 연락을 얼마나 중요하게 생각하는지 얘기해 봐. 네가 원하는 걸 전부 포기할 필요도 없고, 상대가 매초 답해야 하는 것도 아님. 둘이 맞출 생각이 있는지가 중요해. 얘기했는데도 네 마음을 계속 우습게 보면 그건 연락 속도만의 문제가 아닐 수도 있어.",
    ],
    "헤어진 사람을 못 잊겠어": [
        "헤어졌다고 마음까지 바로 로그아웃되는 건 아니잖아. 같이했던 일상까지 한꺼번에 사라지니까 생각나는 게 당연함. 아직 못 잊었다고 찌질한 거 아님.\n\n근데 일부러 상대 소식 찾아보고 옛날 대화 계속 읽으면 상처가 계속 새로고침될 수 있어. 힘들면 잠깐 숨김이나 거리 두기 해도 돼. 빨리 잊는 게 목표가 아니라 네 일상이 조금씩 돌아오는 게 목표야.",
    ],
    "내가 더 좋아하는 것 같아": [
        "마음 크기를 자로 잴 순 없는데 나만 애쓰는 느낌이면 서운하지. 먼저 연락하고, 약속 잡고, 이해하고, 기다리고. 이게 계속 너 몫이면 지칠 수밖에.\n\n네가 먼저 표현하는 게 잘못은 아냐. 다만 상대도 관계를 위해 뭔가 하고 있는지 봐. 계속 네가 맞추기만 해야 유지되는 관계라면 네가 원하는 걸 말해 봐. 좋아하는 사람이 있다고 네 자존심까지 반납할 필요는 없어.",
    ],
    "내가 뭘 하고 싶은지 모르겠어": [
        "하고 싶은 일 확실한 사람만 있는 줄 알지? 사실 해 보지도 않은 게 많은데 어떻게 바로 알겠냐 ㅋㅋ\n\n평생의 꿈 찾겠다고 압박 주지 말고, 일단 관심 가는 것 하나를 실제로 해 봐. 싫은 것도 알아내면 수확임. 지금은 인생 정답 맞히기보다 선택지를 하나씩 시험해 보는 시기라고 생각하자.",
    ],
    "취업이나 대학 때문에 불안해": [
        "결과가 걸린 일이니까 불안한 게 당연하지. 주변 사람들은 다 잘 풀리는 것 같은데 나만 불확실하면 더 조급하고.\n\n근데 결과 나오기 전까지 혼자 최악의 결말을 백 번 돌려 봐도 결과가 바뀌진 않잖아. 일정, 서류, 추가 지원처럼 지금 할 수 있는 걸 확인하고 나머지는 잠깐 내려놓자. 한 번의 결과가 네 가능성 전체를 판정하는 건 아님.",
    ],
    "돈 문제 때문에 막막해": [
        "돈 문제는 '긍정적으로 생각해!' 한다고 해결되는 게 아니라서 더 답답하지. 당장 필요한 게 있는데 부족하면 진짜 막막함.\n\n일단 이번 달에 꼭 필요한 돈이랑 미룰 수 있는 지출을 나눠 보자. 필요한 금액과 기한이 보이면 방법을 찾기가 조금 쉬워져. 혼자 감당하기 어려운 상황이면 믿을 만한 어른한테 도움을 요청해도 돼. 돈이 부족한 게 네 사람값이 부족하다는 뜻은 아님.",
    ],
    "남들은 잘 사는 것 같은데 나만 뒤처져": [
        "SNS 보면 남들은 다 잘나가고 나만 제자리인 것 같지. 근데 남의 하이라이트랑 네 비하인드 장면을 비교하면 당연히 네가 손해임.\n\n사람마다 출발점도 상황도 달라. 남들 속도 따라가느라 네가 뭘 원하는지 잊지 마. 지금 성과가 별로 없어도 인생 망한 거 아니고, 네 속도가 느리다고 잘못된 길인 것도 아님.",
    ],
    "내가 잘하는 게 없는 것 같아": [
        "지금 잘하는 게 안 보인다고 진짜 아무것도 없는 건 아니야. 익숙한 건 별거 아니라고 치부하고, 남이 잘하는 것만 크게 보이기도 하거든.\n\n잘하는 것만 찾지 말고 오래 붙잡고 있는 일, 남들보다 덜 지치는 일, 조금이라도 궁금한 걸 봐. 능력은 처음부터 만렙으로 생기는 게 아님. 지금의 너를 최종 버전이라고 생각하지 마.",
    ],
    "앞으로 어떻게 살아야 할지 모르겠어": [
        "미래 생각하면 막막하지. 아직 일어나지도 않은 일을 오늘 다 해결하려고 하면 누구라도 머리 터짐.\n\n지금 당장 10년 계획 없어도 돼. 이번 주에 할 수 있는 일 하나만 정하자. 정보를 찾아보든, 누군가한테 물어보든, 하루 쉬든. 인생 전체의 답을 오늘 밤까지 제출할 필요 없어. 그건 숙제도 아니잖아 ㅋㅋ",
    ],
}

def safety_response():
    return (
        "야, 이 얘기는 가볍게 넘기고 싶지 않아. 여기까지 말할 정도면 진짜 많이 힘들었을 수 있겠다.\n\n"
        "지금은 혼자서 버티는 걸 목표로 하지 말자. 믿을 만한 가족이나 선생님한테 지금 상태를 그대로 알려 줘. "
        "당장 스스로를 다치게 할 것 같거나 안전을 지키기 어렵다면 혼자 있지 말고 가까운 어른에게 바로 도움을 요청해. "
        "한국에서는 자살예방상담전화 109로 이야기할 수 있고, 급박한 위험이면 112 또는 119에 연락할 수 있어.\n\n"
        "지금 모든 문제를 해결할 필요는 없어. 우선 네가 안전한 게 먼저야."
    )

def answer_custom(user_text):
    text = user_text.strip()
    lower = text.lower()

    danger_patterns = [
        r"죽고\s*싶", r"자살", r"극단적", r"목숨을\s*끊",
        r"살기\s*싫", r"사라지고\s*싶", r"자해", r"죽어버리",
    ]
    if any(re.search(pattern, lower) for pattern in danger_patterns):
        return safety_response()

    patterns = [
        (["외롭", "혼자", "쓸쓸"], [
            "야, 외로움이 꼭 주변에 사람이 없을 때만 오는 건 아니잖아. 사람들 사이에 있어도 혼자인 느낌 들 수 있음.\n\n네가 유난인 게 아니라 지금 마음 둘 곳이 필요한 걸 수도 있어. 억지로 괜찮은 척하지 말고 편한 사람 한 명한테라도 연락해 봐. 오늘 하루에 인생 친구를 만들 필요는 없고, 작은 연결 하나면 됨.",
            "혼자 버티는 시간이 길어지면 별일 아닌 것도 크게 느껴질 수 있어. 일단 네가 외롭다는 사실을 인정하자. 그걸로 네가 약한 사람 되는 거 아님.\n\n오늘은 편한 사람한테 먼저 연락하거나 네가 좋아하는 걸 하면서 숨 좀 돌려. 사람 만나기조차 버거우면 쉬어도 되고. 억지로 텐션 올릴 필요 없음."
        ]),
        (["불안", "걱정", "초조", "무서"], [
            "야, 머릿속에서 최악의 상황 무한 재생하면 진짜 아무것도 못 하지. 아직 안 일어난 일인데 몸은 이미 겪은 것처럼 지치는 거임.\n\n지금 실제로 일어난 일과 네가 걱정하는 걸 나눠 보자. 당장 할 수 있는 건 하나만 처리하고, 나머지는 잠깐 보류해. 모든 걸 한 번에 해결해야 하는 거 아니야.",
            "불안하다고 네가 약한 건 아님. 중요한 일이 있으면 누구든 흔들릴 수 있지.\n\n근데 걱정만 계속한다고 답이 생기는 건 아니니까, 확인할 수 있는 사실부터 보자. 혼자 생각할수록 더 꼬이면 잠깐 자리 옮기거나 믿을 만한 사람한테 말해 봐. 머릿속에서 혼자 재판 열지 말자."
        ]),
        (["우울", "무기력", "지쳐", "힘들", "피곤"], [
            "야, 많이 지쳤나 보다. 그럴 때는 뭘 하기도 싫고 원래 좋아하던 것도 재미없을 수 있어. 거기다 '왜 난 이것도 못 하지' 하면서 너까지 조지지는 말자.\n\n오늘은 밥 먹고 물 마시고 조금 쉬는 것부터 해도 돼. 이런 상태가 오래 가거나 일상생활이 어려울 정도면 혼자 참지 말고 믿을 만한 어른이나 전문가한테 도움 요청하자. 그건 오버하는 게 아님.",
            "솔직히 계속 버티기만 하면 사람이 방전됨. 배터리 1퍼인데 고성능 게임 돌리려는 거랑 비슷하잖아.\n\n오늘 할 일을 줄일 수 있으면 줄여. 그리고 뭐가 제일 힘든지 딱 하나만 골라 보자. 모든 걸 한 번에 해결할 필요 없어. 지금은 네 컨디션부터 챙겨야 돼."
        ]),
        (["돈", "월급", "알바", "생활비"], [
            "돈 문제는 '긍정적으로 생각해!' 한다고 해결되는 게 아니라서 더 답답하지. 현실적으로 필요한 돈이 있는데 부족하면 막막할 만함.\n\n이번 달 꼭 필요한 지출이랑 미룰 수 있는 지출부터 나눠 보자. 금액과 기한이 보이면 해결 방법도 찾기 쉬워져. 혼자 감당하기 어려우면 믿을 만한 어른한테 도움을 요청해도 돼."
        ]),
        (["부모", "엄마", "아빠", "가족"], [
            "가족 문제는 남한테 말하기도 애매하고 집에 가면 또 마주쳐야 해서 더 빡세지.\n\n네가 무조건 참아야 하는 건 아냐. 대화가 가능하면 감정 좀 가라앉았을 때 네 입장을 말해 보고, 계속 안 통하면 다른 믿을 만한 어른한테 도움을 구해. 가족이라고 네 감정이 없는 건 아니잖아."
        ]),
        (["친구", "손절", "배신", "인간관계", "뒷담"], [
            "사람 때문에 상처받으면 그 일만 힘든 게 아니라 다른 사람까지 믿기 어려워지지.\n\n일단 지금 당장 손절이냐 화해냐 결론 내릴 필요는 없어. 네가 원하는 게 사과인지, 거리 두기인지, 솔직한 대화인지부터 생각해 봐. 관계도 중요하지만 네 마음도 중요함."
        ]),
        (["연애", "남친", "여친", "짝사랑", "전애인", "헤어"], [
            "마음이라는 게 진짜 내 맘대로 안 되지 ㅋㅋ 머리로는 알겠는데 감정은 따로 움직일 때가 있음.\n\n근데 상대 마음을 추측하느라 너 혼자 다 닳고 있는 건 아닌지 보자. 네가 원하는 관계가 뭔지도 중요해. 좋아하는 사람이 있다고 네가 계속 불안하고 상처받아야 하는 건 아님."
        ]),
        (["졸업", "대학", "취업", "진로", "미래", "시험", "성적", "공부"], [
            "앞날이 걸린 문제는 불안할 수밖에 없지. 주변 사람들은 다 결정하는 것 같은데 나만 모르겠으면 조급하고.\n\n근데 지금 모른다는 게 앞으로도 모른다는 뜻은 아냐. 확인할 수 있는 정보랑 지금 할 수 있는 행동부터 나눠 보자. 큰 문제를 작은 단계로 쪼개면 덜 막막해져."
        ]),
    ]
    for keywords, responses in patterns:
        if any(word in lower for word in keywords):
            return random.choice(responses)

    return random.choice([
        "야, 일단 네가 그렇게 느낀 데에는 이유가 있겠지. 무조건 네 탓으로 돌릴 필요는 없어.\n\n근데 지금 당장 결론부터 내리려고 하면 더 꼬일 수 있음. 실제로 무슨 일이 있었는지랑 네가 제일 속상했던 부분부터 나눠 보자. 해결책보다 네 마음을 먼저 정리해야 할 때도 있거든.",
        "읽어 보니까 마음이 복잡하겠다. 이런 건 남한테 설명하는 것부터 쉽지 않을 때가 있잖아.\n\n혼자서 모든 책임을 떠안지는 말자. 네가 바꿀 수 있는 것과 당장 바꾸기 어려운 걸 나눠 보자. 네가 모든 걸 혼자 해결해야 하는 것도 아니고.",
        "솔직히 모든 고민에 딱 떨어지는 정답이 있는 건 아님. 그래도 혼자 머릿속에서 계속 굴리는 것보단 말로 꺼내 보는 게 나을 수 있어.\n\n너 자신부터 몰아붙이지 말자. 상황이 힘든 거랑 네가 부족한 사람인 건 다른 얘기니까. 지금 할 수 있는 작은 것부터 잡아 보자.",
        "야, 무조건 괜찮다고만 하진 않을게. 상황이 좆같을 수도 있고 네가 잘못한 부분이 있을 수도 있음. 근데 그걸 알아보는 거랑 너 자신을 통째로 깎아내리는 건 다른 문제야.\n\n지금은 무슨 일이 있었는지 차분히 나눠 보고, 네가 할 수 있는 다음 행동 하나부터 정해 보자."
    ])

def go_home():
    st.session_state.page = "home"
    st.session_state.category = ""
    st.session_state.topic = ""

for key, default in {
    "page": "home",
    "category": "",
    "topic": "",
    "custom_text": "",
    "custom_answer": "",
    "topic_answer": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

st.markdown("""
<div class="hero">
  <h1>💬 찐친 고민상담소</h1>
  <p>야, 무슨 일 있어?<br>
  여기선 괜찮은 척 안 해도 됨.<br>
  하고 싶은 얘기부터 편하게 풀어놔 봐.</p>
</div>
""", unsafe_allow_html=True)

if st.session_state.page == "home":
    st.markdown('<div class="section-title">뭐 때문에 속 터지는데?</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">제일 가까운 고민을 골라 봐. 애매하면 기타 눌러도 됨.</div>', unsafe_allow_html=True)

    for category, info in CATEGORIES.items():
        if st.button(f"{category}\n{info['desc']}", key=f"category_{category}", use_container_width=True):
            st.session_state.category = category
            st.session_state.page = "topics"
            st.rerun()

    if st.button("💬 기타 고민\n분류고 뭐고 그냥 내 얘기 하고 싶음", key="other", use_container_width=True):
        st.session_state.page = "custom"
        st.rerun()

    st.markdown('<p style="text-align:center;color:#91a095;font-size:12px;margin-top:28px;">너무 혼자 끙끙대지 말고 일단 말해 봐 🌿</p>', unsafe_allow_html=True)

elif st.session_state.page == "topics":
    category = st.session_state.category
    if st.button("← 처음으로", key="topics_back"):
        go_home()
        st.rerun()

    st.markdown(f'<div class="section-title">{category}</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">이 중에 네 상황이랑 비슷한 거 있어?</div>', unsafe_allow_html=True)

    for i, topic in enumerate(CATEGORIES[category]["topics"]):
        if st.button(topic, key=f"topic_{i}", use_container_width=True):
            st.session_state.topic = topic
            st.session_state.topic_answer = random.choice(ADVICE.get(topic, ["야, 그럴 만한 이유가 있었겠지. 네 마음부터 천천히 보자."]))
            st.session_state.page = "advice"
            st.rerun()

elif st.session_state.page == "advice":
    if st.button("← 고민 목록으로", key="advice_back"):
        st.session_state.page = "topics"
        st.rerun()

    st.markdown('<div class="section-title">야, 네 얘기 들어보자</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chat-card"><div class="chat-label">💭 네가 고른 고민</div><b>{html.escape(st.session_state.topic)}</b></div>', unsafe_allow_html=True)
    st.markdown('<div class="chat-card"><div class="chat-label">🫂 친구가 하는 말</div></div>', unsafe_allow_html=True)
    st.write(st.session_state.topic_answer)

    if st.button("💬 내 상황을 더 얘기할래", key="topic_more", use_container_width=True):
        st.session_state.custom_text = st.session_state.topic + "에 대해 고민 중이야. "
        st.session_state.page = "custom"
        st.rerun()

    if st.button("다른 고민도 얘기하기", key="advice_home", use_container_width=True):
        go_home()
        st.rerun()

elif st.session_state.page == "custom":
    if st.button("← 처음으로", key="custom_back"):
        go_home()
        st.rerun()

    st.markdown('<div class="section-title">무슨 일인데?</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">말 정리 안 해도 됨. 걍 생각나는 대로 적어 봐.</div>', unsafe_allow_html=True)

    with st.form("custom_form"):
        user_text = st.text_area(
            "네 고민",
            value=st.session_state.custom_text,
            placeholder="예: 요즘 친구들이랑 있어도 나만 겉도는 것 같음...",
            height=180,
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("내 얘기 들어줘 💚", use_container_width=True)

    if submitted:
        if not user_text.strip():
            st.warning("야 ㅋㅋ 한 글자라도 적어 줘야 같이 고민하지!")
        else:
            st.session_state.custom_text = user_text
            st.session_state.custom_answer = answer_custom(user_text)
            st.session_state.page = "custom_answer"
            st.rerun()

elif st.session_state.page == "custom_answer":
    if st.button("← 고민 다시 수정하기", key="edit_custom"):
        st.session_state.page = "custom"
        st.rerun()

    st.markdown('<div class="section-title">읽어 봤어</div>', unsafe_allow_html=True)
    st.markdown("**네가 적은 고민**")
    st.info(st.session_state.custom_text)
    st.markdown('<div class="chat-card"><div class="chat-label">🫂 친구가 하는 말</div></div>', unsafe_allow_html=True)
    st.write(st.session_state.custom_answer)

    if st.button("다른 고민도 얘기하기", key="custom_again", use_container_width=True):
        st.session_state.custom_text = ""
        st.session_state.custom_answer = ""
        go_home()
        st.rerun()

st.markdown("---")
st.caption("찐친 고민상담소는 고민을 정리하는 데 도움을 주는 공간이야. 위험하거나 감당하기 어려운 상황에서는 믿을 만한 어른이나 전문가에게도 도움을 요청해 줘.")
