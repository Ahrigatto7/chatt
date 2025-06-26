import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="DB 편집기", layout="wide")
st.title("✍️ 지식 DB 편집기")
st.markdown("웹 화면에서 직접 토픽을 추가하거나 수정합니다.")

CSV_PATH = 'Topic DB 216b50e66dba805abdb2ebd9cbd601da.csv'

# 데이터 로딩 함수 (캐시 사용으로 성능 최적화)
@st.cache_data
def load_data(filepath):
    expected_columns = ['Name', 'Description', 'Related Keywords', 'Related Examples']
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        df = pd.read_csv(filepath)
        if not all(col in df.columns for col in expected_columns):
            st.error(f"CSV 파일에 필요한 열({', '.join(expected_columns)})이 없습니다.")
            return pd.DataFrame(columns=expected_columns)
        return df.fillna('')
    else:
        st.info("기존 DB 파일이 없어 새로 생성합니다. '새 토픽 추가'로 데이터를 입력해주세요.")
        df = pd.DataFrame(columns=expected_columns)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        return df

# --- NEW: 추가/수정 폼을 함수로 분리 (코드 중복 제거) ---
def topic_form(form_key, defaults=None):
    """토픽 추가/수정을 위한 입력 폼을 생성하는 함수"""
    if defaults is None:
        defaults = {'Name': '', 'Description': '', 'Related Keywords': '', 'Related Examples': ''}
    
    with st.form(key=form_key):
        name = st.text_input("토픽 이름 (Name)", value=defaults.get('Name', ''))
        desc = st.text_area("설명 (Description)", value=defaults.get('Description', ''), height=200)
        keywords = st.text_input("관련 키워드 (Related Keywords)", value=defaults.get('Related Keywords', ''))
        examples = st.text_area("관련 사례 (Related Examples)", value=defaults.get('Related Examples', ''), height=150)
        
        submitted = st.form_submit_button("저장하기")
        
        if submitted:
            return {
                "Name": name, "Description": desc, 
                "Related Keywords": keywords, "Related Examples": examples
            }
    return None

# --- 메인 로직 ---
df = load_data(CSV_PATH)

# session_state에 데이터가 있으면 '새 토픽 추가' 모드로 시작
default_mode_index = 0
if 'new_topic_data' in st.session_state and st.session_state.new_topic_data:
    default_mode_index = 0

mode = st.radio("편집 모드를 선택하세요.", ("새 토픽 추가", "기존 토픽 수정"), horizontal=True, index=default_mode_index)
st.markdown("---")

if mode == "기존 토픽 수정":
    st.subheader("기존 토픽 수정")
    topic_list = [""] + df['Name'].tolist()
    selected_topic_name = st.selectbox("수정할 토픽을 선택하세요.", options=topic_list)

    if selected_topic_name:
        topic_data_to_edit = df[df['Name'] == selected_topic_name].iloc[0].to_dict()
        edited_data = topic_form(form_key="edit_form", defaults=topic_data_to_edit)
        
        if edited_data:
            idx = df.index[df['Name'] == selected_topic_name][0]
            df.loc[idx] = list(edited_data.values())
            try:
                df.to_csv(CSV_PATH, index=False, encoding='utf-8-sig')
                st.success(f"'{edited_data['Name']}' 토픽이 성공적으로 수정되었습니다!")
                st.cache_data.clear()
                st.rerun()
            except Exception as e:
                st.error(f"파일 저장 중 오류 발생: {e}")

else: # 새 토픽 추가
    st.subheader("새 토픽 추가")
    
    # 세션 상태에서 데이터 가져오기 (있는 경우)
    defaults = st.session_state.get('new_topic_data', None)
    
    new_data = topic_form(form_key="add_form", defaults=defaults)
    
    if new_data:
        if new_data['Name'] and not df['Name'].str.contains(new_data['Name']).any():
            new_row = pd.DataFrame([new_data])
            df = pd.concat([df, new_row], ignore_index=True)
            try:
                df.to_csv(CSV_PATH, index=False, encoding='utf-8-sig')
                st.success(f"'{new_data['Name']}' 토픽이 성공적으로 추가되었습니다!")
                # 작업 완료 후 세션 상태 정리
                if 'new_topic_data' in st.session_state:
                    del st.session_state.new_topic_data
                st.cache_data.clear()
                st.rerun()
            except Exception as e:
                st.error(f"파일 저장 중 오류가 발생했습니다: {e}")
        elif not new_data['Name']:
            st.warning("토픽 이름은 반드시 입력해야 합니다.")
        else:
            st.error(f"'{new_data['Name']}'은(는) 이미 존재하는 토픽 이름입니다.")