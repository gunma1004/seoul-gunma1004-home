import os
import urllib.parse
import hashlib  # <--- 이 줄을 추가해 주세요!

# 1. 사이트 기본 설정
SITE_ORIGIN = "https://seoul-gunma1004-home.netlify.app"
SITE_NAME = "건마1004"
DEFAULT_PHONE = "0507-1280-3199"

PARTNER_SHOPS = [
    {"name": "퀸즈홈테라피", "phone": "0507-1280-3296", "category": "리프레시 홈타이", "price": "타이 60분 80,000원", "img": "01"},
    {"name": "한국미인테라피", "phone": "0507-1280-3140", "category": "스페셜 테라피", "price": "아로마 90분 110,000원", "img": "02"},
    {"name": "오늘밤테라피", "phone": "0507-1280-3199", "category": "아로마 마사지", "price": "힐링 90분 120,000원", "img": "03"},
    {"name": "주주테라피", "phone": "0507-1280-3197", "category": "스웨디시 케어", "price": "스페셜 120분 150,000원", "img": "04"},
    {"name": "기쁨테라피", "phone": "0507-1280-3183", "category": "감성 리프레시", "price": "아로마 60분 90,000원", "img": "05"},
    {"name": "미인클럽테라피", "phone": "0507-1280-3180", "category": "VIP 스페셜", "price": "힐링 60분 100,000원", "img": "06"}
]

# 2. 서울, 경기, 인천 전체 시·구·동 데이터
REGION_DATA = {
    "seoul": {
        "name": "서울특별시", "short": "서울",
        "districts": {
            "강남구": ["개포동", "대치동", "도곡동", "일원동", "수서동", "자곡동", "삼성동", "청담동", "압구정동", "신사동", "논현동", "역삼동", "세곡동"],
            "강동구": ["강일동", "상일동", "명일동", "고덕동", "암사동", "천호동", "성내동", "둔촌동", "길동"],
            "강북구": ["미아동", "번동", "수유동", "우이동"],
            "강서구": ["염창동", "등촌동", "화곡동", "가양동", "마곡동", "방화동", "공항동"],
            "관악구": ["봉천동", "신림동", "남현동"],
            "광진구": ["중곡동", "능동", "구의동", "광장동", "자양동", "화양동", "군자동"],
            "구로구": ["신도림동", "구로동", "가리봉동", "고척동", "개봉동", "오류동", "수궁동", "항동"],
            "금천구": ["가산동", "독산동", "시흥동"],
            "노원구": ["월계동", "공릉동", "하계동", "중계동", "상계동"],
            "도봉구": ["쌍문동", "방학동", "창동", "도봉동"],
            "동대문구": ["용신동", "제기동", "전농동", "답십리동", "장안동", "청량리동", "회기동", "휘경동", "이문동"],
            "동작구": ["노량진동", "상도동", "흑석동", "사당동", "대방동", "신대방동"],
            "마포구": ["공덕동", "아현동", "도화동", "용강동", "대흥동", "서강동", "서교동", "합정동", "망원동", "연남동", "성산동", "상암동"],
            "서대문구": ["충현동", "천연동", "북아현동", "신촌동", "연희동", "홍제동", "홍은동", "남가좌동", "북가좌동"],
            "서초구": ["서초동", "반포동", "방배동", "양재동", "잠원동", "내곡동"],
            "성동구": ["왕십리동", "마장동", "사근동", "행당동", "응봉동", "금호동", "옥수동", "성수동", "송정동", "용답동"],
            "성북구": ["성북동", "삼선동", "동선동", "돈암동", "안암동", "보문동", "정릉동", "길음동", "종암동", "월곡동", "장위동", "석관동"],
            "송파구": ["잠실동", "문정동", "가락동", "방이동", "석촌동", "오금동", "위례동", "신천동", "풍납동", "거여동", "마천동"],
            "양천구": ["목동", "신월동", "신정동"],
            "영등포구": ["영등포동", "여의동", "당산동", "도림동", "문래동", "양평동", "신길동", "대림동"],
            "용산구": ["후암동", "용산동", "남영동", "청파동", "원효로동", "효창동", "용문동", "한강로동", "이촌동", "이태원동", "한남동", "서빙고동", "보광동"],
            "은평구": ["녹번동", "불광동", "갈현동", "구산동", "대조동", "응암동", "역촌동", "신사동", "증산동", "수색동", "진관동"],
            "종로구": ["청운동", "사직동", "삼청동", "부암동", "평창동", "무악동", "교남동", "가회동", "종로동", "이화동", "혜화동", "창신동", "숭인동"],
            "중구": ["소공동", "회현동", "명동", "필동", "장충동", "광희동", "을지로동", "신당동", "다산동", "약수동", "청구동", "동화동", "황학동", "중림동"],
            "중랑구": ["면목동", "상봉동", "중화동", "묵동", "망우동", "신내동"]
        }
    },
    "gyeonggi": {
        "name": "경기도", "short": "경기",
        "districts": {
            "수원시 장안구": ["파장동", "율천동", "정자동", "영화동", "송죽동", "조원동", "연무동"],
            "수원시 권선구": ["세류동", "평동", "서둔동", "구운동", "금곡동", "호매실동", "권선동", "곡선동"],
            "수원시 팔달구": ["행궁동", "매교동", "매산동", "고등동", "화서동", "지동", "우만동", "인계동"],
            "수원시 영통구": ["매탄동", "원천동", "영통동", "망포동", "광교동"],
            "성남시 수정구": ["신흥동", "태평동", "수진동", "단대동", "산성동", "복정동", "위례동"],
            "성남시 중원구": ["성남동", "중앙동", "금광동", "은행동", "상대원동", "하대원동", "도촌동"],
            "성남시 분당구": ["분당동", "수내동", "정자동", "서현동", "이매동", "야탑동", "판교동", "백현동", "운중동"],
            "고양시 덕양구": ["주교동", "원신동", "흥도동", "성사동", "화정동", "행주동", "능곡동", "창릉동", "삼송동"],
            "고양시 일산동구": ["식사동", "중산동", "정발산동", "풍산동", "백석동", "마두동", "장항동", "고봉동"],
            "고양시 일산서구": ["일산동", "주엽동", "탄현동", "대화동", "송포동", "덕이동", "가좌동"],
            "용인시 처인구": ["중앙동", "역북동", "삼가동", "유림동", "동부동", "포곡읍", "모현읍"],
            "용인시 기흥구": ["신갈동", "영덕동", "구갈동", "상갈동", "보라동", "기흥동", "서농동", "구성동", "동백동"],
            "용인시 수지구": ["풍덕천동", "신봉동", "죽전동", "동천동", "상현동", "성복동"],
            "부천시 원미구": ["심곡동", "원미동", "중동", "상동", "도당동", "춘의동", "약대동", "역곡동"],
            "부천시 소사구": ["소사본동", "범박동", "괴안동", "송내동", "옥길동"],
            "부천시 오정구": ["성곡동", "원종동", "고강동", "오정동", "신흥동"],
            "안양시 만안구": ["안양동", "석수동", "박달동"],
            "안양시 동안구": ["비산동", "부흥동", "달안동", "관양동", "평촌동", "호계동", "범계동"],
            "안산시 상록구": ["일동", "이동", "사동", "본오동", "부곡동", "월피동", "성포동", "반월동"],
            "안산시 단원구": ["와동", "고잔동", "호수동", "원곡동", "백운동", "초지동", "선부동", "대부동"],
            "화성시": ["남양읍", "향남읍", "봉담읍", "동탄동", "진안동", "병점동", "반월동", "새솔동"],
            "평택시": ["신평동", "원평동", "통복동", "비전동", "세교동", "고덕동", "팽성읍", "안중읍", "포승읍"],
            "시흥시": ["대야동", "신천동", "은행동", "매화동", "목감동", "군자동", "정왕동", "배곧동", "능곡동"],
            "파주시": ["금촌동", "운정동", "교하동", "문산읍", "조리읍", "법원읍", "파주읍"],
            "의정부시": ["의정부동", "호원동", "장암동", "신곡동", "송산동", "자금동", "가능동", "흥선동"],
            "김포시": ["김포본동", "장기동", "사우동", "풍무동", "구래동", "마산동", "운양동", "고촌읍"],
            "광명시": ["광명동", "철산동", "하안동", "소하동", "일직동", "학온동"],
            "광주시": ["경안동", "송정동", "광남동", "오포동", "초월읍", "곤지암읍"],
            "군포시": ["군포동", "산본동", "금정동", "재궁동", "오금동", "수리동", "대야동"],
            "하남시": ["천현동", "신장동", "덕풍동", "풍산동", "미사동", "감일동", "위례동"],
            "오산시": ["중앙동", "대원동", "남촌동", "신장동", "세마동", "초평동"],
            "양주시": ["양주동", "회천동", "옥정동", "덕정동", "백석읍"],
            "이천시": ["창전동", "증포동", "중리동", "관고동", "부발읍"],
            "구리시": ["갈매동", "동구동", "인창동", "교문동", "수택동"],
            "안성시": ["안성동", "공도읍", "보개면", "대덕면"],
            "포천시": ["포천동", "선단동", "소흘읍", "일동면"],
            "의왕시": ["고천동", "부곡동", "오전동", "내손동", "청계동"],
            "여주시": ["여흥동", "중앙동", "오학동", "가남읍"],
            "동두천시": ["생연동", "중앙동", "불현동", "송내동"],
            "양평군": ["양평읍", "양서면", "용문면", "서종면"],
            "과천시": ["중앙동", "갈현동", "별양동", "부림동"],
            "가평군": ["가평읍", "청평면", "설악면"],
            "연천군": ["연천읍", "전곡읍"]
        }
    },
    "incheon": {
        "name": "인천광역시", "short": "인천",
        "districts": {
            "중구": ["신포동", "연안동", "신흥동", "동인천동", "개항동", "영종동", "운서동"],
            "동구": ["만석동", "화수동", "송현동", "송림동"],
            "미추홀구": ["숭의동", "용현동", "학익동", "도화동", "주안동", "관교동", "문학동"],
            "연수구": ["옥련동", "선학동", "연수동", "청학동", "동춘동", "송도동"],
            "남동구": ["구월동", "간석동", "만수동", "서창동", "논현동", "논현고잔동"],
            "부평구": ["부평동", "산곡동", "청천동", "갈산동", "삼산동", "부개동", "일신동", "십정동"],
            "계양구": ["효성동", "계산동", "작전동", "작전서운동", "계양동"],
            "서구": ["검암경서동", "연희동", "청라동", "가정동", "석남동", "가좌동", "검단동", "원당동", "당하동", "아라동"],
            "강화군": ["강화읍", "길상면", "화도면"],
            "옹진군": ["백령면", "영흥면", "연평면"]
        }
    }
}

def render_cards_html(area_label, dong_name=""):
    # 동 이름 기반 고유 시드값 생성
    seed = int(hashlib.md5(f"{area_label}_{dong_name}".encode('utf-8')).hexdigest(), 16)
    
    # 1. 노출 순서 셔플 (동마다 첫 번째 업체가 바뀜)
    shuffled_shops = PARTNER_SHOPS[:]
    start_idx = seed % len(shuffled_shops)
    ordered_shops = shuffled_shops[start_idx:] + shuffled_shops[:start_idx]

    # 2. 지역명 결합 수식어 패턴
    prefixes = [
        f"{dong_name}점 ",
        f"{dong_name} ",
        f"{dong_name} 1호 ",
        "프라이빗 ",
        "리프레시 "
    ]

    cards_html = ""
    for idx, s in enumerate(ordered_shops):
        # 업체명에 동적 수식어 결합 (예: 신월동점 퀸즈홈테라피, 신월 퀸즈홈테라피)
        prefix = prefixes[(seed + idx) % len(prefixes)] if dong_name else ""
        display_name = f"{prefix}{s['name']}".strip()
        
        cards_html += f"""
        <article class="shop-card">
          <a class="card-media" href="tel:{s['phone']}" aria-label="{display_name} 전화 문의">
            <span class="media-fallback">{s['category']}</span>
            <picture class="card-picture">
              <source media="(max-width: 680px)" srcset="/assets/cards/therapist-card-{s['img']}-240.webp">
              <img class="card-photo" src="/assets/cards/therapist-card-{s['img']}-512.webp" alt="{display_name} 대표 이미지" width="512" height="320" loading="lazy">
            </picture>
          </a>
          <div class="card-body">
            <span class="category-tag">{s['category']}</span>
            <h3><a class="card-title-link" href="tel:{s['phone']}">{display_name}</a></h3>
            <p class="address">{area_label} 일대 방문 상담</p>
            <div class="card-bottom">
              <div><span class="price-label">예약 기준</span><strong class="price">{s['price']}</strong></div>
              <div class="card-actions">
                <a class="detail-link" href="sms:{s['phone']}">문자</a>
                <a class="phone-link" href="tel:{s['phone']}">
                  <span>전화문의</span>
                </a>
              </div>
            </div>
          </div>
        </article>"""
    return cards_html

def generate_page(title_area, page_path, breadcrumbs, related_links):
    full_url = f"{SITE_ORIGIN}{page_path}"
    page_title = f"{title_area} 출장 리프레시 마사지 · 출장 스페셜 테라피 | {SITE_NAME}"
    meta_desc = f"{title_area} 출장 리프레쉬 마사지 코스, 시간, 가격과 예약 준비를 확인하세요. 제휴업체 모던 민지룸 마사지의 아로마마사지 관리 범위와 상담 정보를 함께 안내합니다."
    
    # 빵부스러기 JSON-LD
    bc_elements = []
    for idx, bc in enumerate(breadcrumbs, 1):
        bc_elements.append(f'{{"@type":"ListItem","position":{idx},"name":"{bc["name"]}","item":"{SITE_ORIGIN}{bc["path"]}"}}')
    bc_json = ",".join(bc_elements)

    # 상단 빠른 지역 칩
    nav_chips = ""
    for link in related_links[:9]:
        is_active = ' is-active' if link.get("active") else ''
        nav_chips += f'<a class="area-chip{is_active}" href="{link["path"]}">{link["name"]}</a>'

    cards = render_cards_html(title_area)

    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{page_title}</title>
  <meta name="description" content="{meta_desc}">
  <meta name="keywords" content="{title_area} 출장마사지, {title_area} 리프레시마사지, {title_area} 스페셜테라피, {SITE_NAME}">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
  <meta name="theme-color" content="#171b3c">
  <link rel="canonical" href="{full_url}">

  <meta property="og:title" content="{page_title}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:url" content="{full_url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{SITE_NAME}">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "CollectionPage",
        "name": "{page_title}",
        "description": "{meta_desc}",
        "url": "{full_url}",
        "inLanguage": "ko-KR",
        "isPartOf": {{ "@type": "WebSite", "name": "{SITE_NAME}", "url": "{SITE_ORIGIN}/" }},
        "about": {{ "@type": "Service", "name": "{title_area} 출장 리프레시 테라피", "areaServed": "{title_area}" }}
      }},
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [{bc_json}]
      }}
    ]
  }}
  </script>
  <link rel="stylesheet" href="/assets/style.css">
  <style>
    /* 인라인 fallback 스타일 */
    :root {{ --ink: #1a232d; --ink-soft: #606d7b; --primary: #376ca4; --primary-dark: #2b4664; --primary-pale: #edf2f8; --line: #d6dee6; --radius-lg: 16px; --radius-md: 24px; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; color: var(--ink); font-family: Pretendard, -apple-system, sans-serif; background: #f9fafb; line-height: 1.5; }}
    a {{ color: inherit; text-decoration: none; }}
    .app-header {{ position: sticky; top: 0; z-index: 20; background: rgba(255,255,255,.94); backdrop-filter: blur(12px); border-bottom: 1px solid var(--line); }}
    .header-inner, .page-shell {{ width: min(1180px, calc(100% - 32px)); margin: 0 auto; }}
    .brand-row {{ display: flex; align-items: center; justify-content: space-between; height: 68px; }}
    .brand {{ font-size: 1.25rem; font-weight: 850; display: inline-flex; align-items: center; gap: 8px; }}
    main {{ padding: 24px 0 48px; }}
    .intro {{ padding: clamp(24px, 4vw, 42px); border-radius: var(--radius-lg); background: #17111f; color: #fff; text-align: center; border-top: 5px solid var(--primary); }}
    h1 {{ font-size: clamp(1.8rem, 3.6vw, 2.7rem); margin: 10px 0; word-break: keep-all; }}
    .intro-copy {{ color: #f7edf2; margin-top: 8px; font-size: 1.05rem; }}
    .nearby-row {{ display: flex; gap: 8px; overflow-x: auto; padding: 18px 0; justify-content: center; }}
    .area-chip {{ padding: 8px 14px; border: 1px solid var(--line); border-radius: 999px; background: #fff; font-size: .88rem; font-weight: 750; flex: 0 0 auto; }}
    .area-chip.is-active {{ background: var(--primary-pale); border-color: var(--primary); color: var(--primary-dark); }}
    .card-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr)); gap: 18px; margin-top: 20px; }}
    .shop-card {{ border: 1px solid var(--line); border-radius: var(--radius-md); background: #fff; overflow: hidden; display: flex; flex-direction: column; }}
    .card-media {{ aspect-ratio: 16/10; position: relative; background: #eee; }}
    .card-photo {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .card-body {{ padding: 18px; text-align: center; display: flex; flex-direction: column; flex: 1; }}
    .category-tag {{ align-self: center; padding: 4px 8px; border-radius: 6px; background: #faeff9; color: #c865bc; font-size: .75rem; font-weight: 850; margin-bottom: 8px; }}
    .shop-card h3 {{ margin: 0 0 6px; font-size: 1.15rem; }}
    .address {{ color: var(--ink-soft); font-size: .86rem; margin: 0 0 12px; }}
    .card-bottom {{ margin-top: auto; padding-top: 12px; border-top: 1px solid #f0f0f5; display: flex; justify-content: space-between; align-items: center; }}
    .price {{ font-weight: 900; font-size: .96rem; color: var(--primary-dark); }}
    .phone-link {{ padding: 8px 14px; border-radius: 12px; background: var(--ink); color: #fff; font-size: .84rem; font-weight: 800; }}
    .detail-link {{ padding: 8px 12px; border-radius: 12px; border: 1px solid var(--line); font-size: .84rem; margin-right: 6px; }}
    .region-guide {{ margin-top: 36px; padding: 28px; background: #fff; border: 1px solid var(--line); border-radius: var(--radius-md); text-align: center; }}
    .price-table {{ width: 100%; border-collapse: collapse; margin-top: 14px; }}
    .price-table th, .price-table td {{ padding: 12px; border-bottom: 1px solid #f0f0f5; text-align: center; }}
    .site-footer {{ margin-top: 40px; padding: 36px 0; background: #fff; border-top: 1px solid var(--line); text-align: center; color: var(--ink-soft); font-size: .88rem; }}
  </style>
</head>
<body>
  <header class="app-header">
    <div class="header-inner">
      <div class="brand-row">
        <a class="brand" href="/" aria-label="{SITE_NAME} 홈">❤️ {SITE_NAME} ❤️</a>
        <div style="font-size: .88rem; font-weight: 700; color: var(--ink-soft);">수도권 출장 리프레시 모아보기</div>
      </div>
    </div>
  </header>

  <main class="page-shell">
    <section class="intro">
      <p style="color: #e6bb72; font-weight: 800; letter-spacing: .08em;">REFRESH THERAPY</p>
      <h1>{title_area} 출장 리프레시 마사지<br>출장 스페셜 테라피</h1>
      <p class="intro-copy">{title_area} 전 지역 1:1 맞춤 방문 안마와 프라이빗 힐링 코스를 예약하세요.</p>
    </section>

    <nav class="nearby-row" aria-label="지역 바로가기">
      {nav_chips}
    </nav>

    <section>
      <div style="text-align: center; margin: 24px 0 12px;">
        <h2 style="margin: 0; font-size: 1.45rem;">{title_area} 제휴 테라피 추천</h2>
        <p style="margin: 6px 0 0; color: var(--ink-soft); font-size: .9rem;">신속한 조율과 투명한 정찰제 요금으로 안내해 드립니다.</p>
      </div>

      <div class="card-grid">
        {cards}
      </div>
    </section>

    <section class="region-guide">
      <h2 style="margin: 0; font-size: 1.4rem;">{title_area} 출장 이용 요금표</h2>
      <table class="price-table">
        <thead><tr><th>코스</th><th>60분</th><th>90분</th><th>120분</th></tr></thead>
        <tbody>
          <tr><td>타이 리프레시</td><td>80,000원</td><td>100,000원</td><td>120,000원</td></tr>
          <tr><td>아로마 테라피</td><td>90,000원</td><td>110,000원</td><td>130,000원</td></tr>
          <tr><td>스페셜 힐링케어</td><td>100,000원</td><td>120,000원</td><td>140,000원</td></tr>
          <tr><td>VIP 시그니처</td><td>120,000원</td><td>150,000원</td><td>180,000원</td></tr>
        </tbody>
      </table>
      <p style="margin-top: 12px; font-size: .8rem; color: #8a8da3;">※ 상세 주소 및 심야 시간대 등에 따른 최종 조건은 상담 시 확인하세요.</p>
    </section>
  </main>

  <footer class="site-footer">
    <div class="header-inner">
      <p style="font-weight: 850; font-size: 1.1rem; color: var(--primary-dark); margin: 0 0 8px;">{SITE_NAME}</p>
      <p style="margin: 0 0 12px;">서울·경기·인천 출장 리프레시 마사지 및 홈케어 안내 플랫폼</p>
      <p style="font-size: .78rem; color: #8a8da3;">제공된 정보는 이용 편의를 돕기 위한 기준 안내이며, 실제 내용은 사전 상담에서 확인하시기 바랍니다.<br>© 2026 {SITE_NAME}. All rights reserved.</p>
    </div>
  </footer>
</body>
</html>
"""

def main():
    sitemap_urls = [SITE_ORIGIN + "/"]
    
    # 1. 홈 페이지 생성 (dist/index.html)
    os.makedirs("dist", exist_ok=True)
    home_links = [
        {"name": "서울 전체", "path": "/seoul/"},
        {"name": "경기 전체", "path": "/gyeonggi/"},
        {"name": "인천 전체", "path": "/incheon/"}
    ]
    home_bc = [{"name": "홈", "path": "/"}]
    with open("dist/index.html", "w", encoding="utf-8") as f:
        f.write(generate_page("수도권", "/", home_bc, home_links))
    print("✓ 홈(index.html) 생성 완료")

    # 2. 시·도 / 시·구·군 / 동 페이지 일괄 생성
    for city_key, city_info in REGION_DATA.items():
        city_path = f"/{city_key}/"
        sitemap_urls.append(SITE_ORIGIN + city_path)
        city_dir = os.path.join("dist", city_key)
        os.makedirs(city_dir, exist_ok=True)
        
        # 시/도 페이지
        dist_links = [{"name": d, "path": f"/{city_key}/{d}/"} for d in list(city_info["districts"].keys())[:10]]
        city_bc = [{"name": "홈", "path": "/"}, {"name": city_info["short"], "path": city_path}]
        with open(os.path.join(city_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(generate_page(city_info["name"], city_path, city_bc, dist_links))

        # 시/구/군 & 동 페이지
        for district_name, dongs in city_info["districts"].items():
            dist_path = f"/{city_key}/{district_name}/"
            sitemap_urls.append(SITE_ORIGIN + urllib.parse.quote(dist_path))
            dist_dir = os.path.join(city_dir, district_name)
            os.makedirs(dist_dir, exist_ok=True)

            dong_links = [{"name": d, "path": f"/{city_key}/{district_name}/{d}/"} for d in dongs]
            dist_bc = city_bc + [{"name": district_name, "path": dist_path}]

            # 구 페이지 생성
            with open(os.path.join(dist_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(generate_page(f"{city_info['short']} {district_name}", dist_path, dist_bc, dong_links))

            # 동 페이지 생성
            for dong_name in dongs:
                dong_path = f"/{city_key}/{district_name}/{dong_name}/"
                sitemap_urls.append(SITE_ORIGIN + urllib.parse.quote(dong_path))
                dong_dir = os.path.join(dist_dir, dong_name)
                os.makedirs(dong_dir, exist_ok=True)

                dong_bc = dist_bc + [{"name": dong_name, "path": dong_path}]
                sibling_dongs = [{"name": d, "path": f"/{city_key}/{district_name}/{d}/", "active": (d == dong_name)} for d in dongs]

                with open(os.path.join(dong_dir, "index.html"), "w", encoding="utf-8") as f:
                    f.write(generate_page(f"{city_info['short']} {district_name} {dong_name}", dong_path, dong_bc, sibling_dongs))

    # 3. sitemap.xml 생성
    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in sitemap_urls:
        sitemap_content += f"  <url><loc>{url}</loc><priority>0.8</priority></url>\n"
    sitemap_content += "</urlset>"
    with open("dist/sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    print(f"✓ sitemap.xml 생성 완료 (총 {len(sitemap_urls)}개 URL)")

    # 4. _redirects & robots.txt 생성
    with open("dist/_redirects", "w", encoding="utf-8") as f:
        f.write("/*    /index.html   200\n")
    with open("dist/robots.txt", "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE_ORIGIN}/sitemap.xml\n")
    print("✓ _redirects 및 robots.txt 생성 완료")

if __name__ == "__main__":
    main()