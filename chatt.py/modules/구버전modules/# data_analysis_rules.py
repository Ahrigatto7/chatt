# data_analysis_rules.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# ✅ CSV 파일 경로를 여기에 입력
DATA_PATH = "your_data.csv"  # 예: "./data/my_dataset.csv"
TARGET_COLUMN = "target_column"  # 예: "Label",
"Category" 등

def main():
    # 1. 데이터 불러오기
    print("🔍 데이터 불러오는 중...")
    df = pd.read_csv(DATA_PATH)
    print(df.head())

    # 2. 기초 통계 확인
    print("\n📊 기초 통계:")
    print(df.describe())
    print(df.info())

    # 3. 결측치 제거
    df = df.dropna()
    print("\n✅ 결측치 제거 완료")

    # 4. 시각화 (페어플롯 & 상관 행렬)
    sns.pairplot(df)
    plt.show()

    plt.figure(figsize=(10,
8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
    plt.title("Correlation Matrix")
    plt.show()

    # 5. 연관 규칙 분석 (이진화된 데이터일 경우 사용)
    # print("\n📌 연관 규칙 분석:")
    # frequent_itemsets = apriori(df, min_support=0.2, use_colnames=True)
    # rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    # print(rules[
    ['antecedents', 'consequents', 'support', 'confidence', 'lift'
    ]
])

    # 6. 결정 트리로 규칙 추출
    print("\n🌲 결정 트리 규칙 학습 중...")

    # 문자열 인코딩
    label_encoders = {}
    for col in df.select_dtypes(include='object'):
        le = LabelEncoder()
        df[col
] = le.fit_transform(df[col
])
        label_encoders[col
] = le

    if TARGET_COLUMN not in df.columns:
        print(f"❌ 오류: '{TARGET_COLUMN}' 컬럼이 데이터에 없습니다.")
        return

    X = df.drop(TARGET_COLUMN, axis=1)
    y = df[TARGET_COLUMN
]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = DecisionTreeClassifier(max_depth=3)
    model.fit(X_train, y_train)

    plt.figure(figsize=(16,
8))
    plot_tree(model, feature_names=X.columns, class_names=True, filled=True)
    plt.title("Decision Tree Rules")
    plt.show()

    print("✅ 분석 완료!")

if __name__ == "__main__":
    main()
