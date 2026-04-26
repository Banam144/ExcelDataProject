import pandas as pd
import matplotlib.pyplot as plt

# =====================================================================
# Task 2, part a) Read, transpose and clean IAG stock data
# =====================================================================

# Đọc file và sử dụng dòng chứa năm làm header
df_stock = pd.read_excel("ratios_stock.xlsx", skiprows=7, index_col=0)

# Xoay bảng (Transpose) và đặt lại chỉ mục cho cột Year
df_stock_t = df_stock.T.reset_index()
df_stock_t.rename(columns={'index': 'Year'}, inplace=True)
df_stock_t.columns = df_stock_t.columns.str.strip()

# Trích xuất số năm (ví dụ: JUN '24 -> 2024) để đồng bộ hóa dữ liệu
df_stock_t['Year'] = df_stock_t['Year'].apply(lambda x: "20" + str(x).split("'")[1] if "'" in str(x) else None)

# Lọc các cột ROE, DE và đổi tên theo yêu cầu
df_stock_final = df_stock_t[['Year', 'Net Income Return on SH Equity (%)', 'Total Debt/Equity (%)']].copy()
df_stock_final.columns = ['Year', 'ROE_stock', 'DE_stock']

# Chuyển đổi dữ liệu sang dạng số và sắp xếp theo thời gian
df_stock_final.dropna(subset=['Year'], inplace=True)
df_stock_final[['ROE_stock', 'DE_stock']] = df_stock_final[['ROE_stock', 'DE_stock']].apply(pd.to_numeric, errors='coerce')
df_stock_final = df_stock_final.sort_values('Year').reset_index(drop=True)


# =====================================================================
# Task 2, part b) Process competitor data and merge datasets
# =====================================================================

# Đọc và xử lý dữ liệu đối thủ (tương tự phần a)
df_comp = pd.read_excel("ratios_comp.xlsx", skiprows=7, index_col=0)
df_comp_t = df_comp.T.reset_index()
df_comp_t.rename(columns={'index': 'Year'}, inplace=True)
df_comp_t.columns = df_comp_t.columns.str.strip()

# Đồng bộ hóa năm cho đối thủ (ví dụ: DEC '24 -> 2024)
df_comp_t['Year'] = df_comp_t['Year'].apply(lambda x: "20" + str(x).split("'")[1] if "'" in str(x) else None)

# Lọc và đổi tên cột cho đối thủ
df_comp_final = df_comp_t[['Year', 'Net Income Return on SH Equity (%)', 'Total Debt/Equity (%)']].copy()
df_comp_final.columns = ['Year', 'ROE_comp', 'DE_comp']

# Chuyển đổi dữ liệu sang dạng số
df_comp_final.dropna(subset=['Year'], inplace=True)
df_comp_final[['ROE_comp', 'DE_comp']] = df_comp_final[['ROE_comp', 'DE_comp']].apply(pd.to_numeric, errors='coerce')

# Thực hiện gộp hai bộ dữ liệu dựa trên cột Year
df_merged = pd.merge(df_stock_final, df_comp_final, on='Year', how='inner')


# =====================================================================
# Task 2, part c) Visualization and statistical analysis
# =====================================================================

# i) Vẽ biểu đồ đường so sánh chỉ số ROE của hai công ty
plt.figure(figsize=(10, 6))
plt.plot(df_merged['Year'], df_merged['ROE_stock'], label='IAG ROE', marker='o', color='blue')
plt.plot(df_merged['Year'], df_merged['ROE_comp'], label='Competitor ROE', marker='s', color='orange')

plt.title('ROE Comparison: IAG vs Competitor (2011-2025)')
plt.xlabel('Year')
plt.ylabel('ROE (%)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# ii) Tính toán giá trị trung bình (mean) và độ lệch chuẩn (standard deviation)
summary_stats = df_merged[['ROE_stock', 'DE_stock', 'ROE_comp', 'DE_comp']].agg(['mean', 'std'])
print(summary_stats)