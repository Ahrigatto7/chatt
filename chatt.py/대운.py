# === 통합: 세력 분석 + 대운-세운 응기 + 입묘/묘고 + 적포구조 분석 ===

# 1. 기본 매핑

element_mapping = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火',
    '戊': '土', '己': '土', '庚': '金', '辛': '金',
    '壬': '水', '癸': '水', '子': '水', '丑': '土',
    '寅': '木', '卯': '木', '辰': '土', '巳': '火',
    '午': '火', '未': '土', '申': '金', '酉': '金',
    '戌': '土', '亥': '水'
}

burial_mapping = {
    '木': '未',
    '火': '戌',
    '金': '丑',
    '水': '辰'
}

heavenly_stem_relations = {
    ('甲', '己'): '합',
    ('乙', '庚'): '합',
    ('丙', '辛'): '합',
    ('丁', '壬'): '합',
    ('戊', '癸'): '합'
}

earthly_branch_relations = {
    ('子', '丑'): '합',
    ('寅', '亥'): '합',
    ('卯', '戌'): '합',
    ('辰', '酉'): '합',
    ('巳', '申'): '합',
    ('午', '未'): '합',
    ('子', '午'): '충',
    ('丑', '未'): '충',
    ('寅', '申'): '충',
    ('卯', '酉'): '충',
    ('辰', '戌'): '충',
    ('巳', '亥'): '충',
    ('寅', '巳'): '형',
    ('卯', '子'): '형',
    ('丑', '戌'): '형',
    ('午', '卯'): '파',
    ('酉', '子'): '파',
    ('辰', '未'): '입묘',
    ('戌', '丑'): '입묘'
}

branch_conflict = {
    '子': '午', '丑': '未', '寅': '申',
    '卯': '酉', '辰': '戌', '巳': '亥',
    '午': '子', '未': '丑', '申': '寅',
    '酉': '卯', '戌': '辰', '亥': '巳'
}

# 2. 기능 함수

def calculate_power(ganzhi_list):
    elements_count = {'木': 0, '火': 0, '土': 0, '金': 0, '水': 0}
    for g in ganzhi_list:
        elem = element_mapping.get(g)
        if elem:
            elements_count[elem] += 1
    return elements_count

def analyze_power(elements_count):
    strongest = max(elements_count, key=elements_count.get)
    weakest = min(elements_count, key=elements_count.get)
    return strongest, weakest

def check_relation(g1, g2, relation_table):
    return relation_table.get((g1, g2)) or relation_table.get((g2, g1)) or '없음'

def analyze_eunggi(original_heavenly, original_earthly, daewoon, sewun):
    results = {}
    for oh in original_heavenly:
        result = check_relation(daewoon[0], oh, heavenly_stem_relations)
        results[f'대운천간-{oh}'] = result
    for sh in sewun[0]:
        result = check_relation(daewoon[0], sh, heavenly_stem_relations)
        results[f'대운천간-세운천간{sh}'] = result
    for oe in original_earthly:
        result = check_relation(daewoon[1], oe, earthly_branch_relations)
        results[f'대운지지-{oe}'] = result
    for se in sewun[1]:
        result = check_relation(daewoon[1], se, earthly_branch_relations)
        results[f'대운지지-세운지지{se}'] = result
    return results

def is_buried(gan, ji):
    element = element_mapping.get(gan)
    burial_place = burial_mapping.get(element)
    return ji == burial_place

def is_burial_open(ji, transit_ji):
    return branch_conflict.get(ji) == transit_ji

def analyze_burial(gan_list, ji_list, daewoon, sewun):
    results = []
    for gan, ji in zip(gan_list, ji_list):
        if is_buried(gan, ji):
            result = f"{gan}{ji}: 입묘성립"
            open_by_daewoon = is_burial_open(ji, daewoon[1])
            open_by_sewun = is_burial_open(ji, sewun[1])
            if open_by_daewoon:
                result += " (대운에 의해 庫 열림)"
            elif open_by_sewun:
                result += " (세운에 의해 庫 열림)"
            else:
                result += " (庫 유지)"
            results.append(result)
    return results

def judge_structure(original, with運):
    original_mokhwa = original['木'] + original['火']
    original_geumsu = original['金'] + original['水']
    운_mokhwa = with運['木'] + with運['火']
    운_geumsu = with運['金'] + with運['水']
    if original_mokhwa > original_geumsu and 운_mokhwa > 운_geumsu:
        return '적포구조 유지'
    elif original_mokhwa > original_geumsu and 운_mokhwa < 운_geumsu:
        return '반적포구조 전환'
    else:
        return '적포구조 아님 (다른 구조)'

# 3. 실행 예시

if __name__ == "__main__":
    # 원국
    원국_천간 = ['甲', '丙', '庚', '壬']
    원국_지지 = ['寅', '午', '酉', '辰']
    
    # 대운
    대운 = ('丙', '戌')
    
    # 세운
    세운 = (['壬'], ['子'])
    
    # 세력 분석
    original_power = calculate_power(원국_천간 + 원국_지지)
    운_power = calculate_power([대운[0], 대운[1]] + 세운[0] + 세운[1])
    total_power = {elem: original_power[elem] + 운_power[elem] for elem in original_power}
    
    strongest, weakest = analyze_power(total_power)
    structure_result = judge_structure(original_power, total_power)
    
    # 응기 분석
    eunggi_result = analyze_eunggi(원국_천간, 원국_지지, 대운, sewun=세운)
    
    # 입묘 분석
    burial_result = analyze_burial(원국_천간, 원국_지지, 대운, sewun=세운)
    
    # 결과 출력
    print("\n=== 세력 분석 결과 ===")
    print("오행 분포:", total_power)
    print(f"가장 강한 오행: {strongest}")
    print(f"가장 약한 오행: {weakest}")
    print(f"적포구조 판정: {structure_result}")
    
    print("\n=== 대운-원국-세운 응기 분석 ===")
    for k, v in eunggi_result.items():
        print(f"{k}: {v}")
    
    print("\n=== 입묘/묘고 분석 ===")
    for r in burial_result:
        print(r)
