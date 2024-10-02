import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import calendar

# 샘플 데이터 생성 함수
def generate_sample_data():
    months = list(range(1, 13))
    departments = ['영업', '마케팅', 'IT', '인사', '재무']
    data = []
    
    for month in months:
        for dept in departments:
            completed_hours = round(np.random.uniform(10, 50), 1)
            target_hours = 40
            data.append({
                '월': month,
                '부서': dept,
                '이수시간': completed_hours,
                '목표시간': target_hours
            })
    
    return pd.DataFrame(data)

# 메인 함수
def main():
    st.set_page_config(page_title="월별 학습시간 이수현황 대시보드", layout="wide")
    st.title("월별 학습시간 이수현황 대시보드")

    # 샘플 데이터 생성
    df = generate_sample_data()

    # 사이드바: 부서 선택
    selected_departments = st.sidebar.multiselect(
        "부서 선택",
        options=df['부서'].unique(),
        default=df['부서'].unique()
    )

    # 데이터 필터링
    filtered_df = df[df['부서'].isin(selected_departments)]

    # 월별 총 이수시간 계산
    monthly_total = filtered_df.groupby('월')['이수시간'].sum().reset_index()
    monthly_total['월'] = monthly_total['월'].apply(lambda x: calendar.month_abbr[x])

    # 그래프 1: 월별 총 이수시간
    fig1 = px.bar(monthly_total, x='월', y='이수시간', title='월별 총 이수시간')
    st.plotly_chart(fig1, use_container_width=True)

    # 그래프 2: 부서별 월간 이수시간
    fig2 = px.line(filtered_df, x='월', y='이수시간', color='부서', title='부서별 월간 이수시간')
    st.plotly_chart(fig2, use_container_width=True)

    # 그래프 3: 부서별 목표 대비 이수율
    completion_rate = filtered_df.groupby('부서').agg({
        '이수시간': 'sum',
        '목표시간': 'sum'
    }).reset_index()
    completion_rate['이수율'] = (completion_rate['이수시간'] / completion_rate['목표시간']) * 100

    fig3 = px.bar(completion_rate, x='부서', y='이수율', title='부서별 목표 대비 이수율 (%)')
    fig3.update_traces(text=completion_rate['이수율'].round(1), textposition='outside')
    st.plotly_chart(fig3, use_container_width=True)

    # 데이터 테이블 표시
    st.subheader("상세 데이터")
    st.dataframe(filtered_df)

if __name__ == "__main__":
    main()
